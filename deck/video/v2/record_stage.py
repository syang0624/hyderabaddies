#!/usr/bin/env python3
"""Record the STAGE Meet video: the Pik present-mode page only, with holds so Carl and Steven can say their lines live.

Replays the five-beat script (lines from prototype/live_sim.py) into prototype/state/live.jsonl on the cue clock below while
Playwright records localhost:8787/?present=1&before=1 (the "today" page, then the composed screen). No Meet chrome, no captions.
Pik's follow-up question comes from engine.ask() for the vague line, so the spoken line (vo/stage_followup.wav) matches the screen.
After each event the recorder waits for the block to actually be visible and logs that second mark, so STAGE_CUES.md is honest.
Writes captures/stage_replay.webm and captures/stage_timeline.json. Usage: deck/video/pw/bin/python deck/video/v2/record_stage.py
"""
import asyncio, json, time, pathlib, shutil, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "prototype"))
import engine  # noqa: E402  (read-only use: the follow-up text)
LIVE = ROOT / "prototype" / "state" / "live.jsonl"
D = pathlib.Path(__file__).resolve().parent
OUT = D / "captures"
END = 78.0

L1 = "Sure. So for the Northwind exchange slot. Honestly I need someone who will push back on the job-based culture over there instead of just absorbing it. And they have to hold their own in English in meetings."
L2 = "Got it. One constraint from my side: the posting starts April 2027, and we cannot lose anyone from pricing before the Q1 close."
L3 = "Actually, we also need someone good for this. Just someone good."
L4 = "I keep coming back to Yui. What did she actually write about this herself, and what did her manager write about her?"
L5 = "Okay. Looking at this, Yui's own words say she wants exactly that, and she has been running the Northwind sync in English. Let's set up calls with Yui and Kei this week, and ask Yui whether her manager's note about being flexible on location is actually true. That's it for today, thanks."
FOLLOW_UP = engine.ask(L3)["follow_up"]
CRIT = "push back on the job-based culture and hold their own in English"
Q1 = {"type": "question", "id": "q1", "text": "I need someone who will push back on the job-based culture over there instead of just absorbing it, and they have to hold their own in English in meetings."}
TILES = [
 {"id": "yui", "name": "Yui Sato", "role": "Product operations", "team": "Pricing",
  "why": "Yui wants to work with the US product team on pricing experiments and improve spoken English through immersion.", "source": "Will Can Must sheet", "source_id": "wcm-yui"},
 {"id": "kei", "name": "Kei Tanaka", "role": "Software engineer", "team": "Platform",
  "why": "Kei wants to understand why their partner ships faster and bring those practices back.", "source": "Will Can Must sheet", "source_id": "wcm-kei"},
 {"id": "rin", "name": "Rin Mori", "role": "Senior marketing analyst", "team": "Growth",
  "why": "Rin declared a desire to stay close to the Japan market for the next two years.", "source": "Will Can Must sheet", "source_id": "wcm-rin"},
]
P1 = {"type": "people", "id": "p1", "criterion": CRIT, "tiles": TILES}
C1 = {"type": "constraint", "id": "c1", "text": "starts April 2027", "affects": []}
C2 = {"type": "constraint", "id": "c2", "text": "cannot lose anyone from pricing before the Q1 close", "affects": [{"id": "yui", "name": "Yui Sato", "reason": "on the Pricing team", "field": "team"}]}
A1 = {"type": "ask", "id": "a1", "text": FOLLOW_UP}
R1 = {"type": "receipt", "id": "r1", "person": "yui", "name": "Yui Sato", "text": "I want to work with the US product team on pricing experiments. My spoken English in meetings is weak but my writing is strong, and I want to fix the speaking part by being immersed.", "source": "Will Can Must sheet, 2026-03-12", "source_id": "wcm-yui", "stamp": "verbatim", "kind": "own_words"}
R2 = {"type": "receipt", "id": "r2", "person": "yui", "name": "Yui Sato", "text": "Yui loves travel and is flexible on location. English is a concern for a US posting. Solid but not exceptional.", "source": "Okada's note, 2026-08-22", "source_id": "mn-yui", "stamp": "paraphrase", "kind": "manager"}
CONCLUDE = {"kind": "conclude", "summary": "Set up calls with Yui Sato and Kei Tanaka this week. Ask Yui whether Okada's note about being flexible on location is actually true.",
            "candidate_ids": ["yui", "kei"], "next_steps": ["Set up calls with Yui and Kei this week", "Ask Yui whether the location note is true"],
            "open_questions": ["Is the location note in Okada's write-up actually Yui's view?"]}

VIS = {  # what to wait for after an event, and the cue name it marks
 "tiles": ("#sblocks .blk:not(.wait) .stiles", "question + three tiles"),
 "chips": ("#sblocks .blk:not(.wait) .schip", "constraint chips, Yui's tile dims"),
 "ask": ("#sblocks .blk:not(.wait) .sask", "Pik's follow-up (spoken)"),
 "receipts": ("#sblocks .blk:not(.wait) .srecs", "Yui's own words + Okada's note"),
 "conclusion": ("#printer.on", "the conclusion prints"),
}
# (page second, event, mark name or None)
EVENTS = [
 (0.5,  {"kind": "status", "text": "Listening"}, None),
 (12.0, {"kind": "heard", "text": L1}, None),
 (12.5, {"kind": "compose", "doc": [Q1, P1]}, "tiles"),
 (12.6, {"kind": "show_candidates", "criterion": CRIT, "ranking": ["yui", "kei", "rin"]}, None),
 (26.0, {"kind": "heard", "text": L2}, None),
 (26.5, {"kind": "patch", "op": "add", "block": C1, "doc": [Q1, C1, P1]}, None),
 (26.9, {"kind": "patch", "op": "add", "block": C2, "doc": [Q1, C1, C2, P1]}, "chips"),
 (35.0, {"kind": "heard", "text": L3}, None),
 (35.5, {"kind": "compose", "doc": [Q1, C1, C2, P1, A1]}, "ask"),
 (35.55, {"kind": "follow_up", "text": FOLLOW_UP}, None),
 (48.0, {"kind": "heard", "text": L4}, None),
 (48.5, {"kind": "patch", "op": "add", "block": R1, "doc": [Q1, C1, C2, P1, A1, R1]}, None),
 (49.3, {"kind": "patch", "op": "add", "block": R2, "doc": [Q1, C1, C2, P1, A1, R1, R2]}, "receipts"),
 (69.0, {"kind": "heard", "text": L5}, None),
 (69.5, CONCLUDE, "conclusion"),
]

def emit(e):
    with LIVE.open("a") as f: f.write(json.dumps({"t": time.time(), **e}) + "\n")

async def main():
    print("follow-up:", FOLLOW_UP)
    LIVE.write_text("")
    OUT.mkdir(exist_ok=True)
    marks = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1,
                                  record_video_dir=str(OUT), record_video_size={"width": 1920, "height": 1080})
        pg = await ctx.new_page()
        t_ctx = time.time()
        await pg.goto("http://localhost:8787/?present=1&before=1")
        await pg.evaluate("document.body.style.zoom='1.5'")  # the 'today' page is small at 1080p; dropped when the stage mounts
        await pg.wait_for_timeout(1500)
        t0 = time.time(); settle = t0 - t_ctx
        for at, e, mark in EVENTS:
            await asyncio.sleep(max(0, t0 + at - time.time())); emit(e)
            if e["kind"] == "compose" and "tiles" == mark:
                await pg.wait_for_function("document.body.classList.contains('stage')", timeout=8000)
                await pg.evaluate("document.body.style.zoom=''")
            if mark:
                sel, label = VIS[mark]
                await pg.wait_for_selector(sel, state="visible", timeout=8000)
                marks[mark] = {"t": round(time.time() - t0, 2), "what": label}
                print(f"{marks[mark]['t']:6.2f} {label}")
        await asyncio.sleep(max(0, t0 + END + 0.5 - time.time()))
        path = await pg.video.path()
        await ctx.close(); await b.close()
        dst = OUT / "stage_replay.webm"; shutil.move(path, dst); print("wrote", dst)
    (OUT / "stage_timeline.json").write_text(json.dumps(dict(settle=round(settle, 3), end=END, follow_up=FOLLOW_UP, marks=marks,
        lines=dict(L1=L1, L2=L2, L3=L3, L4=L4, L5=L5), cues=[(t, e["kind"]) for t, e, _ in EVENTS]), indent=1))
    print("wrote", OUT / "stage_timeline.json")
asyncio.run(main())
