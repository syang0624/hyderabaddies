"""Live meeting layer: microphone -> Gemini 3.8 Live (Vertex) -> tool calls -> the UI.

The model listens to an HR planning call. When the speakers describe who they need, it calls
show_candidates(criterion); the UI re-ranks on that criterion. When the call reaches a
conclusion, it calls conclude(...); the UI shows the post-call pop-up. Every event is appended
to state/live.jsonl, which server.py serves at /api/live. Nothing here scores anyone.

Run:  .venv/bin/python live.py            (Ctrl-C to stop)
Env:  GCP_PROJECT (default recruit-hackathon-2026-e), LIVE_LOCATION (us-central1),
      LIVE_MODEL (gemini-3.8-live), MIC (substring of the input device name, default: system default)
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
RATE = 16000
RESUME = {"handle": None}  # latest session-resumption handle, reused on reconnect so context survives a drop
CHUNK = 1600  # 100 ms
EVENTS = engine.STATE / "live.jsonl"

TOOLS = [types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="show_candidates", behavior="NON_BLOCKING",
        description=("Call this as soon as the speakers describe the kind of person they need for the slot "
                     "(skills, attitude, language, what they must be willing to do). Pass their words, lightly cleaned, "
                     "as one criterion sentence. Call it again whenever the criterion changes."),
        parameters=types.Schema(type="OBJECT", properties={
            "criterion": types.Schema(type="STRING", description="What matters for this slot, in the speakers' own words."),
        }, required=["criterion"]),
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
    types.FunctionDeclaration(
        name="note", behavior="NON_BLOCKING",
        description="Call this for any other fact the speakers state that should be on the record (a constraint, a date, a budget). One short sentence.",
        parameters=types.Schema(type="OBJECT", properties={"text": types.Schema(type="STRING")}, required=["text"]),
    ),
])]


def system_prompt():
    c = engine.load("company.json")
    people = "\n".join(f"- {p['id']}: {p['name']}, {p['role']}, {p['team']}, reports to {p['manager']}" for p in c["candidates"])
    return f"""You are Receipts, a silent listener on a call between an HR planner and a hiring manager at {c['name']}.
The decision: {c['decision']['title']}. Purpose: {c['decision']['purpose']}
Candidates under consideration (use these ids in tool calls):
{people}

Rules:
- You never speak unless a speaker addresses you by name ("Receipts"). If you must respond, use at most one short sentence.
- You never score, rank or recommend a person. Humans decide. You only call tools that put evidence on the shared screen.
- Call show_candidates the moment a speaker says what kind of person they need ("I need someone who...", "we're looking for...", "the person has to..."). Do it immediately, on that sentence, even if the description is incomplete. Call it again whenever the description changes or is refined, in any language.
- Call note for constraints, dates and budgets the speakers state.
- Call conclude when they agree on a next step or wrap up. Summarise only what they said.
- The speakers may talk in English or Japanese. Write tool arguments in English."""


NEED = re.compile(r"\b(need|needs|looking for|want|wants|ideal(?:ly)?|has to be|must be|should be)\b.{0,40}\b(someone|somebody|a person|people|engineer|manager|candidate)\b|\bsomeone who\b|\bthe person\b.{0,20}\b(has|must|needs|should)\b|欲しい|ほしい|必要|探して|人がいい|人が良い|人がほしい", re.I)
LAST_TOOL = {"t": 0.0}


async def maybe_trigger(text):
    """Fallback: if a heard sentence states a need and the model has not called show_candidates within 3 s of it, rank on it anyway."""
    if not NEED.search(text):
        return
    t_heard = time.time()
    await asyncio.sleep(3)
    if LAST_TOOL["t"] >= t_heard - 2:  # the model handled it
        return
    r = await asyncio.to_thread(engine.rank, text.strip())
    LAST_TOOL["t"] = time.time()
    emit("show_candidates", criterion=text.strip(), ranking=[x["candidate"] for x in r["ranking"]], via="transcript")


def emit(kind, **payload):
    row = {"t": time.time(), "kind": kind, **payload}
    with EVENTS.open("a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"[{time.strftime('%H:%M:%S')}] {kind}: {json.dumps(payload, ensure_ascii=False)[:200]}", flush=True)


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
    loop = asyncio.get_running_loop()
    q: asyncio.Queue = asyncio.Queue(maxsize=50)

    def on_audio(indata, frames, t, status):
        if status:
            print("mic:", status, file=sys.stderr)
        try:
            loop.call_soon_threadsafe(q.put_nowait, bytes(indata))
        except asyncio.QueueFull:
            pass

    dev = pick_mic()
    name = sd.query_devices(dev if dev is not None else sd.default.device[0])["name"]
    stream = sd.RawInputStream(samplerate=RATE, blocksize=CHUNK, dtype="int16", channels=1, device=dev, callback=on_audio)
    stream.start()
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
    if True:

        async def pump():
            while True:
                chunk = await q.get()
                await session.send_realtime_input(audio=types.Blob(data=chunk, mime_type=f"audio/pcm;rate={RATE}"))

        heard_box = {"text": "", "t": 0.0}

        async def flush_on_pause():
            while True:
                await asyncio.sleep(0.5)
                if heard_box["text"].strip() and time.time() - heard_box["t"] > 1.5:
                    txt = heard_box["text"].strip(); heard_box["text"] = ""
                    emit("heard", text=txt)
                    asyncio.create_task(maybe_trigger(txt))

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
                          emit("heard", text=txt)
                          asyncio.create_task(maybe_trigger(txt))
                  if sc and sc.output_transcription and sc.output_transcription.text:
                      emit("said", text=sc.output_transcription.text)
                  if msg.tool_call:
                      responses = []
                      for fc in msg.tool_call.function_calls:
                          args = dict(fc.args or {})
                          result = {"ok": True}
                          if fc.name == "show_candidates":
                              LAST_TOOL["t"] = time.time()
                              r = await asyncio.to_thread(engine.rank, args.get("criterion", ""))
                              result = {"shown": [{"id": x["candidate"], "name": x["name"], "evidence_items": len(x["receipts"])} for x in r["ranking"]]}
                              emit("show_candidates", criterion=args.get("criterion", ""), ranking=[x["candidate"] for x in r["ranking"]])
                          elif fc.name == "conclude":
                              emit("conclude", **args)
                          elif fc.name == "note":
                              emit("note", text=args.get("text", ""))
                          responses.append(types.FunctionResponse(id=fc.id, name=fc.name, response=result, scheduling="SILENT"))
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
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
