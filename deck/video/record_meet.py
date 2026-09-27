#!/usr/bin/env python3
"""Record the Meet beat from the running prototype (localhost:8787) without a microphone.
Replays the scripted call's events into prototype/state/live.jsonl on a fixed clock while Playwright records the page.
Output: captures/meet_replay.webm (1920x1080). This is the stand-in until Carl and Steven's real take lands.
Usage: PW=/path/to/venv/python  $PW record_meet.py
"""
import asyncio, json, time, pathlib, shutil, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[2]
LIVE = ROOT / "prototype" / "state" / "live.jsonl"
OUT = pathlib.Path(__file__).parent / "captures"
CRIT = "Someone who will push back on the job-based culture instead of absorbing it, and who can hold their own in English in meetings."
EVENTS = [  # (seconds after page settle, event)
 (1.0, {"kind":"status","text":"Listening"}),
 (2.0, {"kind":"heard","text":"For the Northwind slot I need someone who will push back on the job-based culture instead of just absorbing it, and they have to hold their own in English in meetings."}),
 (3.2, {"kind":"show_candidates","criterion":CRIT,"ranking":["yui","kei","rin"]}),
 (7.5, {"kind":"heard","text":"Actually, we also need someone good for this. Just someone good."}),
 (8.3, {"kind":"follow_up","text":"Do they need to lead meetings in English, or mostly write?"}),
 (11.5,{"kind":"heard","text":"Okay, let's set up calls with Yui and Kei this week, and ask Yui whether that location note is actually true."}),
 (13.0,{"kind":"conclude","summary":"The team decided to set up calls with Yui Sato and Kei Tanaka this week. They will check with Yui whether her manager's note about being flexible on location is actually true.",
        "candidate_ids":["yui","kei"],"next_steps":["Set up calls with Yui and Kei this week","Ask Yui whether the location note is true"],
        "open_questions":["Is the location note in Okada's write-up actually Yui's view?"]}),
]
def emit(e):
    with LIVE.open("a") as f: f.write(json.dumps({"t": time.time(), **e}) + "\n")
async def main():
    LIVE.write_text("")  # clean log so the page starts idle
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width":1920,"height":1080}, device_scale_factor=1,
                                  record_video_dir=str(OUT), record_video_size={"width":1920,"height":1080})
        pg = await ctx.new_page()
        await pg.goto("http://localhost:8787/?present=1&before=1")
        await pg.wait_for_timeout(1500)
        t0 = time.time()
        for at, e in EVENTS:
            await asyncio.sleep(max(0, t0 + at - time.time())); emit(e)
        await pg.wait_for_timeout(5000)
        path = await pg.video.path()
        await ctx.close(); await b.close()
        dst = OUT / "meet_replay.webm"; shutil.move(path, dst); print("wrote", dst)
asyncio.run(main())
