#!/usr/bin/env python3
"""Record the V2 Meet beat from the running prototype (localhost:8787), no microphone.

Replays the scripted call as the live layer now emits it (compose / patch / conclude; see prototype/live.py after
commit 4b85916) into prototype/state/live.jsonl on a fixed clock while Playwright records ?present=1&before=1.
The clock is derived from the narration wavs in vo/ (07_manager, 07_meet, 07_manager2) so the page moves exactly
when the voice stops: the manager's first line starts LEAD seconds before the cut (a J-cut from the zoom-out).
Writes captures/meet_replay.webm and captures/meet_timeline.json (VO offsets and the beat length for build_v2.py).
Usage: deck/video/pw/bin/python deck/video/v2/record_meet.py
"""
import asyncio, json, time, pathlib, shutil, subprocess, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[3]
LIVE = ROOT / "prototype" / "state" / "live.jsonl"
D = pathlib.Path(__file__).resolve().parent
OUT, VO = D / "captures", D / "vo"
LEAD = 1.8  # seconds of the manager's first line already heard before the Meet cut (J-cut over the zoom-out)

def dur(name):
    w = VO / f"{name}.wav"
    for _ in range(240):  # narration may still be rendering
        if w.exists():
            return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(w)],
                                        capture_output=True, text=True).stdout.strip())
        time.sleep(1)
    sys.exit(f"[record_meet] {w} never appeared")

LINE1 = "For the Northwind slot I need someone who will push back on the job-based culture instead of just absorbing it, and they have to hold their own in English in meetings."
LINE2 = "Okay, let's set up calls with Yui and Kei this week, and ask Yui whether that location note is actually true."
CRIT = "push back on the job-based culture and hold their own in English"
Q1 = {"type": "question", "id": "q1", "text": LINE1}
TILES = [  # source ids the engine can resolve (the page drops any tile it cannot verify)
 {"id": "yui", "name": "Yui Sato", "role": "Product operations", "team": "Pricing",
  "why": "Yui wants to work with the US product team on pricing experiments and improve spoken English through immersion.", "source": "Will Can Must sheet", "source_id": "wcm-yui"},
 {"id": "kei", "name": "Kei Tanaka", "role": "Software engineer", "team": "Platform",
  "why": "Kei wants to understand why their partner ships faster and bring those practices back.", "source": "Will Can Must sheet", "source_id": "wcm-kei"},
 {"id": "rin", "name": "Rin Mori", "role": "Senior marketing analyst", "team": "Growth",
  "why": "Rin declared a desire to stay close to the Japan market for the next two years.", "source": "Will Can Must sheet", "source_id": "wcm-rin"},
]
P1 = {"type": "people", "id": "p1", "criterion": CRIT, "tiles": TILES}
R1 = {"type": "receipt", "id": "r1", "person": "yui", "name": "Yui Sato", "text": "I want to work with the US product team on pricing experiments. My spoken English in meetings is weak but my writing is strong, and I want to fix the speaking part by being immersed.", "source": "Will Can Must sheet, 2026-03-12", "source_id": "wcm-yui", "stamp": "verbatim", "kind": "own_words"}
R2 = {"type": "receipt", "id": "r2", "person": "yui", "name": "Yui Sato", "text": "Yui loves travel and is flexible on location. English is a concern for a US posting. Solid but not exceptional.", "source": "Okada's note, 2026-08-22", "source_id": "mn-yui", "stamp": "paraphrase", "kind": "manager"}
CONCLUDE = {"kind": "conclude", "summary": "Set up calls with Yui Sato and Kei Tanaka this week. Ask Yui whether Okada's note about being flexible on location is actually true.",
            "candidate_ids": ["yui", "kei"], "next_steps": ["Set up calls with Yui and Kei this week", "Ask Yui whether the location note is true"],
            "open_questions": ["Is the location note in Okada's write-up actually Yui's view?"]}

def timeline():
    m1, n, m2 = dur("07_manager"), dur("07_meet"), dur("07_manager2")
    a = m1 - LEAD + 0.25                # manager 1 ends (page clock)
    narr = a + 0.8                      # narrator over the re-sort
    b = narr + n + 0.3                 # manager 2 starts
    end = b + m2 + 1.5                  # beat length
    ev = [
        (0.3, {"kind": "status", "text": "Listening"}),
        (a, {"kind": "heard", "text": LINE1}),
        (a + 0.35, {"kind": "compose", "doc": [Q1, P1]}),
        (a + 0.45, {"kind": "show_candidates", "criterion": CRIT, "ranking": ["yui", "kei", "rin"]}),
        (a + 2.9, {"kind": "patch", "op": "add", "block": R1, "doc": [Q1, P1, R1]}),
        (a + 3.7, {"kind": "patch", "op": "add", "block": R2, "doc": [Q1, P1, R1, R2]}),
        (b + m2 - 0.4, {"kind": "heard", "text": LINE2}),
        (b + m2 + 0.3, CONCLUDE),
    ]
    vo = {"07_manager": -LEAD, "07_meet": narr, "07_manager2": b}
    return ev, vo, end, dict(m1=m1, n=n, m2=m2)

def emit(e):
    with LIVE.open("a") as f: f.write(json.dumps({"t": time.time(), **e}) + "\n")

async def main():
    ev, vo, end, d = timeline()
    print("durations", d, "beat", round(end, 2), "vo", vo)
    LIVE.write_text("")  # clean log so the page starts idle
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1,
                                  record_video_dir=str(OUT), record_video_size={"width": 1920, "height": 1080})
        pg = await ctx.new_page()
        await pg.goto("http://localhost:8787/?present=1&before=1")
        await pg.evaluate("document.body.style.zoom='1.5'")  # the 'today' page is small at 1080p; the stage resets this
        await pg.wait_for_timeout(1800)
        t0 = time.time()
        for at, e in ev:
            await asyncio.sleep(max(0, t0 + at - time.time()))
            emit(e); print(f"{time.time()-t0:5.2f} {e['kind']}")
            if e["kind"] == "compose":  # the stage replaces the page: drop the zoom the instant it mounts (its blocks are still hidden)
                await pg.wait_for_function("document.body.classList.contains('stage')", timeout=6000)
                await pg.evaluate("document.body.style.zoom=''")
        await asyncio.sleep(max(0, t0 + end + 2.0 - time.time()))
        path = await pg.video.path()
        await ctx.close(); await b.close()
        dst = OUT / "meet_replay.webm"; shutil.move(path, dst); print("wrote", dst)
    (OUT / "meet_timeline.json").write_text(json.dumps(dict(settle=1.8, beat=round(end, 2), vo=vo, durations=d,
                                                            events=[(round(t, 2), e["kind"]) for t, e in ev]), indent=1))
    print("wrote", OUT / "meet_timeline.json")
asyncio.run(main())
