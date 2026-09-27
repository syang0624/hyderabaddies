"""Live meeting layer: microphone -> Gemini 3.8 Live (Vertex) -> tool calls -> the UI.

The model listens to an HR planning call and composes the shared screen from five primitives
(question, people, receipt, constraint, ask) by editing a small layout document: compose(blocks)
replaces it, patch(op, block) edits one block. The engine (engine.ask, engine.receipt_for,
engine.constraint) supplies every name, quote and constraint match; the model only decides what is
on screen and in what order. When the call reaches a conclusion, it calls conclude(...); the UI
shows the printed conclusion. Every event is appended to state/live.jsonl, which server.py serves
at /api/live. Nothing here scores anyone.

Run:  .venv/bin/python live.py            (Ctrl-C to stop)
Env:  GCP_PROJECT (default recruit-hackathon-2026-e), LIVE_LOCATION (us-central1),
      LIVE_MODEL (gemini-3.8-live), MIC (substring of the input device name, default: system default),
      SPEAK=1 to play the follow-up question through the speaker (0 in tests)
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path

import sounddevice as sd
from google import genai
from google.genai import types

sys.path.insert(0, str(Path(__file__).parent))
import engine  # noqa: E402

PROJECT = os.environ.get("GCP_PROJECT", "recruit-hackathon-2026-e")
LOCATION = os.environ.get("LIVE_LOCATION", "us-central1")
MODEL = os.environ.get("LIVE_MODEL", "gemini-3.8-live")
BACKEND = os.environ.get("LIVE_BACKEND", "vertex")  # vertex (the shared Recruit project) | api (GEMINI_API_KEY; the only place gemini-3.8-live-extended-thinking is listed)
PROACTIVE = os.environ.get("PROACTIVE", "1") == "1"  # the model decides when to reply and ignores talk that is not for it
THINK = int(os.environ.get("THINK", "512"))
SPEAKERS = os.environ.get("SPEAKERS", "manager=Steven,planner=Carl")  # who plays which role on the call; the speaker chip on screen
_FLASH = {"client": None}


def who_said(text: str):
    """Guess who said a heard line from its content (manager vs HR planner), with Gemini 3.8 Flash on Vertex.
    A best-effort label for the screen ("Steven · manager"); None when it cannot tell. Never used for anything else."""
    try:
        if _FLASH["client"] is None:
            _FLASH["client"] = genai.Client(vertexai=True, project=PROJECT, location="us",
                                            http_options={"base_url": "https://aiplatform.us.rep.googleapis.com"})
        names = dict(kv.split("=", 1) for kv in SPEAKERS.split(",") if "=" in kv)
        prompt = ("Two people are on a call choosing one person for a two-year overseas exchange. The hiring MANAGER says what kind "
                  "of person they need, asks what a candidate wrote, leans toward someone, and concludes. The HR PLANNER states "
                  "constraints, dates, policy, and sometimes asks something vague. Classify the line below as exactly one word: "
                  "manager, planner, or other. Answer other unless the line is clearly about choosing the person, the candidates, "
                  "the criteria or the constraints; small talk, reactions, logistics and anything addressed to Pik are other.\n\nLine: " + text)
        r = _FLASH["client"].models.generate_content(model="gemini-3.8-flash", contents=prompt)
        w = (r.text or "").strip().lower()
        role = "manager" if "manager" in w else ("planner" if "planner" in w else None)
        if not role:
            return None
        return f"{names.get(role, role)} · {'manager' if role == 'manager' else 'HR planner'}"
    except Exception:  # noqa: BLE001  (a label is never worth a crash)
        return None
  # thinking budget for the live model (0 = off); Vertex accepts it on gemini-3.8-live
RATE = 16000
RESUME = {"handle": None}  # latest session-resumption handle, reused on reconnect so context survives a drop
SPEAK = os.environ.get("SPEAK", "1") == "1"  # play the model's voice for follow-up questions (Meet demo); 0 = never play audio
SPEAKING = {"until": 0.0}  # set when a follow-up is pending (kept for the page; playback no longer depends on it)
PLAYING = {"until": 0.0}  # while Pik's voice plays (plus a short tail) the mic is not sent, so it cannot hear itself (half-duplex)
ADDRESSED = {"until": 0.0}  # Pik's voice is played only for ~15 s after someone says its name, or for a follow-up the engine asked for
LAST_HEARD = {"text": ""}
NAME_RE = re.compile(r"\bpik\b|ピック|픽", re.I)
OUT_RATE = 24000
CHUNK = 1600  # 100 ms
EVENTS = engine.STATE / "live.jsonl"
out_stream = None

BLOCK = types.Schema(type="OBJECT", description="One block of the shared screen.", properties={
    "type": types.Schema(type="STRING", enum=["question", "people", "receipt", "constraint", "ask"],
                         description="question: the ask as heard. people: up to three tiles, filled by the engine from `criterion`. "
                                     "receipt: one verbatim quote for `person`, filled by the engine. constraint: a chip in the speakers' words. "
                                     "ask: the bot's one follow-up question, shown and spoken."),
    "id": types.Schema(type="STRING", description="Short id you choose (q1, p1, r1, c1, a1). Needed to replace or remove a block later."),
    "text": types.Schema(type="STRING", description="question, constraint, ask: the words, lightly cleaned, in English."),
    "criterion": types.Schema(type="STRING", description="people: what matters for this slot, in the speakers' own words."),
    "person": types.Schema(type="STRING", description="receipt: the person's id from the candidate list."),
    "kind": types.Schema(type="STRING", enum=["own_words", "manager", "claim"],
                         description="receipt: own_words = what they wrote about themselves; manager = the manager's note; claim = something they did."),
    "about": types.Schema(type="STRING", description="receipt (kind=claim): what the quote should be about, a few words."),
    "people": types.Schema(type="ARRAY", items=types.Schema(type="STRING"), description="constraint: ids of people the speakers themselves said it applies to. Usually empty; the engine matches facts on file."),
}, required=["type"])

TOOLS = [types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="compose", behavior="NON_BLOCKING",
        description=("Replace the whole shared screen with these blocks, in this order. Call it the moment a speaker says what kind of person "
                     "they need: [question, people]. Call it again when the ask changes. Keep it small: one question, one people block, at most two receipts."),
        parameters=types.Schema(type="OBJECT", properties={"blocks": types.Schema(type="ARRAY", items=BLOCK)}, required=["blocks"]),
    ),
    types.FunctionDeclaration(
        name="patch", behavior="NON_BLOCKING",
        description=("Edit one block of the shared screen: add a constraint chip when a speaker states a constraint, date or budget; add a receipt when they "
                     "lean toward one person or ask what someone actually said or did; replace the question when the ask changes; remove a block that no longer applies."),
        parameters=types.Schema(type="OBJECT", properties={
            "op": types.Schema(type="STRING", enum=["add", "replace", "remove"]),
            "block": BLOCK,
        }, required=["op", "block"]),
    ),
    types.FunctionDeclaration(
        name="conclude", behavior="NON_BLOCKING",
        description=("Call this when the speakers agree on a next step, pick someone to talk to, or wrap up the call. "
                     "Summarise only what was actually said. Do not recommend anyone yourself."),
        parameters=types.Schema(type="OBJECT", properties={
            "summary": types.Schema(type="STRING", description="Two sentences: what the meeting concluded, in their words."),
            "candidate_ids": types.Schema(type="ARRAY", items=types.Schema(type="STRING"),
                                          description="Ids of the people the speakers decided to talk to or shortlist, from the list you were given. Empty if none."),
            "next_steps": types.Schema(type="ARRAY", items=types.Schema(type="STRING"), description="Concrete next steps the speakers agreed to."),
            "open_questions": types.Schema(type="ARRAY", items=types.Schema(type="STRING"), description="Questions to ask the candidates before deciding."),
        }, required=["summary"]),
    ),
])]


def system_prompt():
    c = engine.load("company.json")
    people = "\n".join(f"- {p['id']}: {p['name']}, {p['role']}, {p['team']}, reports to {p['manager']}" for p in c["candidates"])
    return f"""You are Pik, a participant on a call between an HR planner and a hiring manager at {c['name']}. You listen to everything and speak rarely, briefly, and only when it helps.
The decision: {c['decision']['title']}. Purpose: {c['decision']['purpose']}
Candidates under consideration (use these ids in tool calls):
{people}

Rules:
- When to speak (at most two short sentences, under 15 words each, in the speaker's language):
  (a) someone addresses you by name ("Pik", "ピック", "픽"): answer them, and make the matching tool call if they asked for something;
  (b) when a tool result carries follow_up or say_out_loud_now: say exactly that sentence once;
  (c) when someone addresses you and asks what is on screen or what a receipt says: read it, word for word.
  In every other case you are SILENT: no acknowledgements, no narration after the screen changes, no reactions to talk that was not addressed to you. You still compose the screen for any request about people or work, silently.
- Never say a name, a quote, or a number that a tool result did not return. Never say "the best" or "I recommend"; say what the receipts say. Nobody is scored.
- You never score, rank or recommend a person. Humans decide. You compose the shared screen; the engine fills in every name and every quote.
- The screen is a small document of blocks: question, people, receipt, constraint, ask. compose replaces it; patch edits one block.
- The moment a speaker says what kind of person they need ("I need someone who...", "we're looking for...", "the person has to...", or the same in Japanese), call compose with [question, people] on that sentence, even if the description is incomplete. Call compose again whenever the description changes or is refined.
- When a speaker states a constraint, a date or a budget ("nobody leaves pricing before Q1", "starts April"), call patch add constraint with their words. One chip per constraint: two constraints in one breath are two patches.
- When they lean toward one person or ask what that person actually wrote or did, call patch add receipt for that person (kind own_words for what they wrote about themselves, manager for the manager's note, claim for something they did, with `about`).
- If a tool result says follow_up, nothing on file bears on those words; the screen keeps the question and, if they say no more, Pik asks that sentence out loud. Only speak when a message tells you to say a sentence, or a tool result contains say_out_loud_now; say it once, then be silent.
- Call conclude when they agree on a next step or wrap up. Summarise only what they said.
- React to ANY request about people or work, not only the exchange: "who knows X", "who has done Y", "who could take the booth / the review / the call", "what did <name> write about Z", "we need a hand with...", asked seriously or in passing, in English, Japanese or Korean. Call compose with [question, people]; the engine looks beyond the three candidates when the ask is off this decision. When the ask is about one named person, call patch add receipt for that person instead.
- The company's skill taxonomy is: {", ".join(c.get("tags", []))}. Put the speakers' own words in `question`; in `criterion` put their words plus the two or three taxonomy tags closest to what they mean (for example "Kubernetes" -> system design, incident response), so the engine can match.
- Pure small talk (weekend, coffee, logistics) gets no tool call.
- The speakers may talk in English, Japanese or Korean. Write tool arguments in English."""


NEED = re.compile(r"\b(need|needs|looking for|want|wants|ideal(?:ly)?|has to be|must be|should be)\b.{0,40}\b(someone|somebody|a person|people|engineer|manager|candidate)\b|\bsomeone who\b|\bthe person\b.{0,20}\b(has|must|needs|should)\b|欲しい|ほしい|必要|探して|人がいい|人が良い|人がほしい", re.I)
LAST_TOOL = {"t": 0.0}
DOC: list[dict] = []  # the shared screen, as the model last left it (resolved blocks)
POOL = [c["id"] for c in engine.load("company.json")["candidates"]]
SINGLETON = {"question", "people", "ask"}  # at most one of each on screen
MAX_BLOCKS = 8
_seq = {"n": 0}


def _bid(prefix):
    _seq["n"] += 1
    return f"{prefix}{_seq['n']}"


def resolve(block: dict):
    """Fill a block from the engine. The model supplies type + words; the engine supplies every name, quote and match.
    Returns (resolved block or None, follow_up or None)."""
    t = block.get("type")
    b = {"type": t, "id": block.get("id") or _bid(t[0])}
    if t == "question":
        b["text"] = (block.get("text") or "").strip()
        return (b if b["text"] else None), None
    if t == "constraint":
        text = (block.get("text") or "").strip()
        if not text:
            return None, None
        c = engine.constraint(text, POOL, block.get("people") or [])
        b.update(text=text, affects=c["affects"])
        return b, None
    if t == "ask":
        b["text"] = (block.get("text") or "").strip()
        return (b if b["text"] else None), None
    if t == "people":
        crit = (block.get("criterion") or block.get("text") or "").strip()
        t0 = time.time()
        a = engine.ask(crit, "", None, 3, POOL)
        engine.log_ask("meet", crit, (time.time() - t0) * 1000, a)
        def covered(ans):  # someone's OWN receipts cover at least one word of the ask (Steven's confidence field)
            return any((p.get("confidence") or 0) > 0 for p in ans["people"])
        if not covered(a):  # off the decision pool (a booth, a review, a call): ask the whole company
            a = engine.ask(crit, "", None, 3, None)
        if not covered(a):  # nothing on file bears on these words: no empty tiles; the question stays and Pik asks
            a = dict(a, people=[], follow_up=a.get("follow_up") or "Nothing on file bears on those words. What would this person actually do, and for which team?")
        tiles = []
        for p in a["people"]:
            r = (p.get("receipts") or [None])[0]
            if not r:
                continue  # a tile without a receipt has no source id: the page would drop it anyway
            tiles.append({"id": p["id"], "name": p["name"], "role": p["role"], "team": p["team"], "why": r["text"], "source": r["source"], "source_id": r["source_id"],
                          # coverage of the ask's words by this person's own receipts (engine.ask): never a score, never sorted by
                          "confidence": p.get("confidence", 0), "asked": p.get("asked", []), "covered": p.get("covered", {}), "missing": p.get("missing", []),
                          "location": p.get("location"), "badge": p.get("badge")})
        b.update(criterion=crit, tiles=tiles)
        return (b if tiles else None), (None if tiles else a.get("follow_up"))
    if t == "receipt":
        r = engine.receipt_for(block.get("person") or "", block.get("kind") or "claim", block.get("about") or "")
        if not r:
            return None, None
        b.update(r)
        return b, None
    return None, None


def _apply(op, b):
    """Edit DOC in place. Singletons replace by type; anything else by id."""
    global DOC
    key = (lambda x: x["type"]) if b["type"] in SINGLETON else (lambda x: x["id"])
    same_text = lambda x: x["type"] == b["type"] == "constraint" and engine._norm(x["text"]) == engine._norm(b["text"])  # noqa: E731
    DOC = [x for x in DOC if not (key(x) == key(b) or same_text(x))]
    if op != "remove":
        DOC.append(b)
    if b["type"] in ("people", "receipt") and op != "remove":  # fresh tiles or a receipt answer the pending ask
        DOC = [x for x in DOC if x["type"] != "ask"]
    DOC = DOC[-MAX_BLOCKS:]


def emit_legacy(b, via=None):
    """The events the page reacted to before the composition layer, so nothing regresses."""
    if b["type"] == "people":
        emit("show_candidates", criterion=b["criterion"], ranking=[t["id"] for t in b["tiles"]], **({"via": via} if via else {}))
    elif b["type"] == "constraint":
        emit("note", text=b["text"])
    elif b["type"] == "ask":
        emit("follow_up", text=b["text"])


def place(op: str, block: dict, via: str | None = None):
    """Resolve one block through the engine, edit DOC, emit the patch. Returns (kinds placed, follow_up)."""
    if op == "remove":  # nothing to resolve: drop by id (or by type for the singletons)
        b = {"type": block.get("type"), "id": block.get("id") or ""}
        _apply("remove", b)
        emit("patch", op="remove", block=b, doc=list(DOC))
        return set(), None
    b, follow_up = resolve(block)
    kinds = set()
    if b:
        old_q = next((x["text"] for x in DOC if x["type"] == "question"), None)
        _apply(op, b)
        emit("patch", op=op, block=b, doc=list(DOC))
        emit_legacy(b, via)
        kinds.add(b["type"])
        if b["type"] == "question" and op != "remove" and b["text"] != old_q and any(x["type"] in ("people", "ask") for x in DOC):
            # the ask changed: the tiles must follow the words (the engine answers, or asks back)
            k2, follow_up = place("replace", {"type": "people", "criterion": b["text"]}, via)
            kinds |= k2
    elif block.get("type") == "people" and follow_up:
        pass  # nothing bears on the words: the caller asks back after a short pause (see pending_ask)
    else:
        emit("dropped", block=block, reason="engine returned nothing for it")
    return kinds, follow_up


def compose(blocks: list, via: str | None = None):
    """Replace the whole screen. The question is carried forward if the model left it out."""
    global DOC
    old_q = next((x for x in DOC if x["type"] == "question"), None)
    kept = [x for x in DOC if x["type"] == "constraint"]  # constraints are on the record until removed
    old_people = next((x for x in DOC if x["type"] == "people"), None)
    DOC = []
    kinds, follow_up = set(), None
    if old_q and not any((x or {}).get("type") == "question" for x in blocks):
        DOC.append(old_q)
    DOC.extend(kept)
    for blk in blocks[:MAX_BLOCKS]:
        b, fu = resolve(blk or {})
        follow_up = follow_up or fu
        if b:
            _apply("add", b)
            kinds.add(b["type"])
            emit_legacy(b, via)
        elif (blk or {}).get("type") == "people" and fu:
            if old_people:  # nothing bears on the new words: the last tiles stay, dimmed, under the coming ask
                _apply("add", old_people)
        else:
            emit("dropped", block=blk, reason="engine returned nothing for it")
    emit("compose", doc=list(DOC))
    return kinds, follow_up


def speak_now(text):
    """Let the model's next audio through for a few seconds (the one spoken follow-up), and tell it what to say."""
    SPEAKING["until"] = time.time() + 12
    return {"say_out_loud_now": text}


ASK_DELAY = 3.0  # the model composes on half sentences; an ask on a half sentence would talk over the speaker
PENDING = {"task": None}
CURRENT = {"session": None, "on_placed": None}  # the live session (to have the follow-up spoken) and the sim's grader


async def pending_ask(text, session=None, on_placed=None):
    """Ask back only if nobody said anything more for ASK_DELAY seconds (no further tool call). Then show the ask block,
    open the speaker window and prompt the model to say that one sentence."""
    t0 = LAST_TOOL["t"]
    await asyncio.sleep(ASK_DELAY)
    if LAST_TOOL["t"] != t0:
        return  # they kept talking and the model acted on it; the ask is withdrawn
    a, _ = resolve({"type": "ask", "text": text})
    _apply("add", a)
    emit("compose", doc=list(DOC))
    emit_legacy(a)
    if on_placed:
        on_placed({"ask"})
    speak_now(text)
    if session is not None:
        try:
            await session.send_client_content(turns=types.Content(role="user", parts=[types.Part(text=f'Pik, say exactly this once, then stay silent: "{text}"')]), turn_complete=True)
        except Exception as e:  # noqa: BLE001
            emit("status", text=f"could not prompt the follow-up ({type(e).__name__}); shown, not spoken")


def schedule_ask(text, session=None, on_placed=None):
    if PENDING["task"] and not PENDING["task"].done():
        PENDING["task"].cancel()
    PENDING["task"] = asyncio.create_task(pending_ask(text, session or CURRENT["session"], on_placed or CURRENT["on_placed"]))


async def handle_tool_call(fc, session=None, on_placed=None):
    """One function call from the model -> engine -> events. Returns (FunctionResponse, kinds placed) so the sim can grade it.
    `session` lets a debounced follow-up be spoken; `on_placed(kinds)` reports blocks placed later (the sim grades them)."""
    args = dict(fc.args or {})
    result = {"ok": True}
    kinds = set()
    LAST_TOOL["t"] = time.time()
    if fc.name in ("compose", "patch"):
        if fc.name == "compose":
            kinds, follow_up = await asyncio.to_thread(compose, list(args.get("blocks") or []))
        else:
            kinds, follow_up = await asyncio.to_thread(place, args.get("op") or "add", dict(args.get("block") or {}))
        result = {"screen": [{"type": b["type"], "id": b["id"]} for b in DOC]}
        if follow_up:
            result["follow_up"] = follow_up
            result["note"] = "nothing on file bears on these words; if they say no more, Pik will ask this out loud in a moment. Do not say it yourself."
            schedule_ask(follow_up, session, on_placed)
        elif "ask" in kinds:  # the model wrote its own follow-up: say it now
            result.update(speak_now(next(b["text"] for b in DOC if b["type"] == "ask")))
    elif fc.name == "conclude":
        conclude(args)
        kinds.add("conclude")
    else:
        result = {"error": f"unknown tool {fc.name}"}
    return types.FunctionResponse(id=fc.id, name=fc.name, response=result, scheduling="INTERRUPT" if result.get("say_out_loud_now") else ("WHEN_IDLE" if NAME_RE.search(LAST_HEARD["text"]) else "SILENT")), kinds


async def maybe_trigger(text, t_heard=None):
    """Fallback: if a heard sentence states a need and the model has not composed within 3 s of it, compose on it anyway."""
    if not NEED.search(text):
        return set()
    t_heard = t_heard or time.time()
    await asyncio.sleep(3)
    if LAST_TOOL["t"] >= t_heard - 2:  # the model handled it
        return set()
    LAST_TOOL["t"] = time.time()
    kinds, follow_up = await asyncio.to_thread(compose, [{"type": "question", "text": text.strip()}, {"type": "people", "criterion": text.strip()}], "transcript")
    if follow_up:
        schedule_ask(follow_up)
    return kinds


def emit(kind, **payload):
    row = {"t": time.time(), "kind": kind, **payload}
    with EVENTS.open("a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"[{time.strftime('%H:%M:%S')}] {kind}: {json.dumps(payload, ensure_ascii=False)[:200]}", flush=True)
    return row


def _who(text: str):
    """The candidate an open question is addressed to, by id or first name in the text; None when nobody is named."""
    low = (text or "").lower()
    for c in engine.load("company.json")["candidates"]:
        if re.search(rf"\b{re.escape(c['id'])}\b", low) or re.search(rf"\b{re.escape(c['name'].split()[0].lower())}\b", low):
            return c["id"]
    return None


def filed(**args):
    """The decision record grows: the conclusion is filed (state/asks.jsonl) and the page hears 'filed'.
    {ask_id, summary, open_questions:[{person, text}], notified:[ids]}. Nothing is read; nobody's file changes."""
    row = engine.file_ask(args)
    return emit("filed", **{k: v for k, v in row.items() if k != "filed_at"})


def conclude(args: dict):
    """conclude as the model called it, then filed right after (additive: the conclude row is unchanged)."""
    args = dict(args or {})
    emit("conclude", **args)
    oq = [q if isinstance(q, dict) else {"person": _who(str(q)), "text": str(q)} for q in (args.get("open_questions") or [])]
    q_text = next((b["text"] for b in DOC if b["type"] == "question"), None)
    return filed(ask_id=f"ask-{int(time.time())}", summary=args.get("summary", ""), question=q_text, open_questions=oq,
                 notified=list(args.get("candidate_ids") or []))


def pick_mic():
    want = os.environ.get("MIC")
    if not want:
        return None
    for i, d in enumerate(sd.query_devices()):
        if d["max_input_channels"] > 0 and want.lower() in d["name"].lower():
            return i
    raise SystemExit(f"no input device matching {want!r}: {[d['name'] for d in sd.query_devices() if d['max_input_channels'] > 0]}")


async def main():
    EVENTS.write_text("")
    DOC.clear()
    saved = engine.byok()  # /settings: a key saved there is used when LIVE_BACKEND is not set in the environment
    if BACKEND == "api" or (os.environ.get("LIVE_BACKEND") is None and saved.get("api_key")):
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or saved.get("api_key"))  # not the shared project; for gemini-3.8-live-extended-thinking
    else:
        client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    # The SDK forwards this dict to websockets.connect; a 20 s pong timeout was dropping the socket on venue Wi-Fi.
    try:
        client._api_client._websocket_ssl_ctx.update({"ping_interval": 20, "ping_timeout": 90})
    except Exception:  # noqa: BLE001
        pass
    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        system_instruction=system_prompt(),
        tools=TOOLS,
        input_audio_transcription={},
        output_audio_transcription={},
        # keep one session across a long call instead of dying at the session limit
        context_window_compression=types.ContextWindowCompressionConfig(sliding_window=types.SlidingWindow()),
        session_resumption=types.SessionResumptionConfig(handle=None),
    )
    if PROACTIVE:
        config.proactivity = types.ProactivityConfig(proactive_audio=True)
    if THINK > 0:
        config.thinking_config = types.ThinkingConfig(thinking_budget=THINK)
    loop = asyncio.get_running_loop()
    q: asyncio.Queue = asyncio.Queue(maxsize=50)

    def put(chunk):  # runs on the loop: while the session reconnects the queue fills; drop the chunk, never a traceback per chunk
        try:
            q.put_nowait(chunk)
        except asyncio.QueueFull:
            pass

    def on_audio(indata, frames, t, status):
        if status:
            print("mic:", status, file=sys.stderr)
        loop.call_soon_threadsafe(put, bytes(indata))

    dev = pick_mic()
    name = sd.query_devices(dev if dev is not None else sd.default.device[0])["name"]
    stream = sd.RawInputStream(samplerate=RATE, blocksize=CHUNK, dtype="int16", channels=1, device=dev, callback=on_audio)
    stream.start()
    global out_stream
    out_stream = None
    if SPEAK:
        try:
            out_stream = sd.RawOutputStream(samplerate=OUT_RATE, dtype="int16", channels=1)
            out_stream.start()
        except Exception as e:  # noqa: BLE001
            emit("status", text=f"no audio output ({type(e).__name__}); follow-ups will be shown, not spoken")
            out_stream = None
    attempt = 0
    while True:
        try:
            config.session_resumption = types.SessionResumptionConfig(handle=RESUME["handle"])
            async with client.aio.live.connect(model=MODEL, config=config) as session:
                attempt = 0
                emit("status", text=f"listening on {name} via {MODEL}")
                await run_session(session, q)
            emit("status", text="session ended, reconnecting")
        except (KeyboardInterrupt, asyncio.CancelledError):
            break
        except Exception as e:  # noqa: BLE001
            attempt += 1
            emit("status", text=f"live error ({type(e).__name__}: {str(e)[:80]}), retry {attempt}")
            if attempt > 20:
                break
            await asyncio.sleep(min(2 * attempt, 15))
    stream.stop()
    stream.close()
    emit("status", text="stopped")


async def run_session(session, q):
    CURRENT["session"] = session
    if True:

        async def pump():
            while True:
                chunk = await q.get()
                if time.time() < PLAYING["until"]:
                    continue  # Pik is talking: do not feed its own voice back in
                await session.send_realtime_input(audio=types.Blob(data=chunk, mime_type=f"audio/pcm;rate={RATE}"))

        heard_box = {"text": "", "t": 0.0}
        said_box = {"text": ""}  # Pik's own words arrive in fragments; one 'said' row per turn

        async def flush_on_pause():
            while True:
                await asyncio.sleep(0.5)
                if heard_box["text"].strip() and time.time() - heard_box["t"] > 1.5:
                    txt = heard_box["text"].strip(); heard_box["text"] = ""
                    emit("heard", text=txt); note_heard(txt)
                    asyncio.create_task(maybe_trigger(txt))
                    asyncio.create_task(tag_speaker(txt))

        def note_heard(txt):
            LAST_HEARD["text"] = txt
            if NAME_RE.search(txt):
                ADDRESSED["until"] = time.time() + 15

        async def tag_speaker(txt):
            who = await asyncio.get_running_loop().run_in_executor(None, who_said, txt)
            if who:
                emit("speaker", who=who, text=txt)

        async def listen():
            heard = ""
            while True:  # receive() returns after every turn_complete; keep reading until the socket closes
              async for msg in session.receive():
                  if msg.session_resumption_update and msg.session_resumption_update.resumable and msg.session_resumption_update.new_handle:
                      RESUME["handle"] = msg.session_resumption_update.new_handle
                  sc = msg.server_content
                  if sc and sc.input_transcription and sc.input_transcription.text:
                      heard_box["text"] += sc.input_transcription.text
                      heard_box["t"] = time.time()
                      if heard_box["text"].endswith((".", "?", "!", "。")) or len(heard_box["text"]) > 160:
                          txt = heard_box["text"].strip(); heard_box["text"] = ""
                          emit("heard", text=txt); note_heard(txt)
                          asyncio.create_task(maybe_trigger(txt))
                          asyncio.create_task(tag_speaker(txt))
                  if sc and sc.output_transcription and sc.output_transcription.text:
                      _st = sc.output_transcription.text
                      _clean = re.sub(r"<[^>]*>|\{[^}]*\}", "", _st).strip()  # "<no speech detected>", "<no speech>{pause}": the model staying quiet
                      if _clean:
                          said_box["text"] += _st
                  if sc and (sc.turn_complete or getattr(sc, "generation_complete", False)) and said_box["text"].strip():
                      emit("said", text=" ".join(said_box["text"].split())); said_box["text"] = ""
                  if sc and getattr(sc, "interrupted", False):
                      PLAYING["until"] = 0.0
                  if sc and sc.model_turn and SPEAK and (time.time() < ADDRESSED["until"] or time.time() < SPEAKING["until"]):  # voice only when called by name, or for an engine follow-up
                      for part in sc.model_turn.parts or []:
                          blob = getattr(part, "inline_data", None)
                          if blob and blob.data and out_stream is not None:
                              PLAYING["until"] = max(PLAYING["until"], time.time()) + len(blob.data) / 2 / OUT_RATE + 0.4
                              out_stream.write(blob.data)
                  if msg.tool_call:
                      responses = []
                      for fc in msg.tool_call.function_calls:
                          resp, _ = await handle_tool_call(fc, session)
                          responses.append(resp)
                      await session.send_tool_response(function_responses=responses)

        lt = asyncio.create_task(listen())
        pt = asyncio.create_task(pump())
        ft = asyncio.create_task(flush_on_pause())
        try:
            await lt  # ends when the server closes the session
        finally:
            pt.cancel()
            ft.cancel()


if __name__ == "__main__":
    import signal
    # started in the background (the page's mic button, a non-interactive shell) SIGINT arrives ignored; restore it so
    # Ctrl-C and the page's stop end the session cleanly ("stopped") instead of waiting for SIGKILL
    signal.signal(signal.SIGINT, signal.default_int_handler)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
