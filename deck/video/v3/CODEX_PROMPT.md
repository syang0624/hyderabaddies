# Pik video V3: handoff for the next session (GPT-6 Astra / Codex, run by Steven)

Written Sun Sep 27 2026, ~00:00 PDT, by Claude in Carl's session. V3 is built and pushed; do not redo it. Run `date` first. Deadline Sun 11:00 PDT (repo + video ≤ 90 s + deck); Carl posts the submission.

## What exists (all under `deck/video/v3/`)

| Path | What |
|---|---|
| `pik_90s_v3.mp4` | The cut: 89.7 s, 1920x1080, 30 fps, H.264 + AAC, -16.9 LUFS, captions burned, music under the whole cut |
| `meet_stage_demo.mp4`, `STAGE_CUES.md` | The stage Meet video on the new Pik screen (78 s, only sound = Pik's follow-up at 36.1 s) and the cue sheet (speakers at 3, 20, 32, 43, 56 s; screen marks measured) |
| `STORYBOARD_v3.md`, `TIMING.md` | The beat table (what is animated / replayed / driven / real) and the build's own timing output |
| `build_v3.py` | The stitch. `SEGMENTS` is the edit; reads `captures/*_timeline.json` for the Meet/CRUD/mirror offsets; mixes voice (loudnorm -16) + `music/bed.wav` × a duck envelope (-26 dB under speech, -18 dB in gaps, 2 s in, 3 s out) |
| `build_stage_v3.py` | `captures/stage_v3.webm` + `vo/stage_followup.wav` → `meet_stage_demo.mp4` + `STAGE_CUES.md` |
| `capture_ui.py` | ONE script for every product-page beat: starts or reuses this checkout's `prototype/server.py` on `--port 8793` (8787 is Carl's live server, 8790 is his pi_mobile: never those), records headless (Playwright, 1920x1080) `meet`, `crud`, `stage`, `mirror` into `captures/` with `*_timeline.json` (when each block was actually visible). The Meet rows are `prototype/scripts/meet.json` re-timed to the measured narration (`meet_rows()`), written to `captures/meet_v3.json`, replayed by `prototype/live_script.py` (needs `prototype/.venv`; symlink the main checkout's if absent) |
| `scripts/stage_v3.json` | The stage replay rows (holds for the live lines); the ask text must equal `engine.ask(L3)["follow_up"]` (the script checks and warns) |
| `narrate_v3.py`, `vo/*.wav` | Narration on Vertex Live in `recruit-hackathon-2026-e` (Charon 1.30x, Puck 1.20x). `--takes N --keep-shorter` keeps the fastest complete take; ids = build rows; `_alt` = shorter variants; `07_manager2_alt` is the one in the cut |
| `music_bed.py`, `music/kosmose_vaikus.m4a`, `music/bed.wav`, `music/BED.md` | Carl's pick (Kosmose Vaikus by Kevin MacLeod, incompetech.com, CC BY 4.0), the calmest 96 s (242–338 s) normalised to -16 LUFS, the window/gain report |
| `html/11_end.html`, `render.py`, `renders/11_end.mp4` | The end card with the credit line; every other animated beat is reused from `../v2/renders/` by path |
| `captures/meet_v3.webm`, `crud.webm`, `mirror.webm`, `stage_v3.webm`, `*_timeline.json`, `meet_v3.json` | The recordings of the new Pik screen (this build's), and their measured marks |

## Re-stitch

```bash
python3 deck/video/v3/build_v3.py          # ~1.5 min; needs PIL (+ numpy for a fast envelope: a venv with numpy+pillow works); writes TIMING.md
python3 deck/video/v3/build_stage_v3.py
```
Check: `ffprobe pik_90s_v3.mp4` ≤ 90.0 s; `ffmpeg -i pik_90s_v3.mp4 -af ebur128 -f null -` ≈ -16 LUFS; extract stills and look. Never play audio through the speakers.

## Re-record the new-UI beats (this is the path when the redesign of `prototype/ui/index.html` lands)

```bash
deck/video/pw/bin/python deck/video/v3/capture_ui.py                    # all four beats, ~4 min
deck/video/pw/bin/python deck/video/v3/capture_ui.py --beats meet       # one beat
python3 deck/video/v3/build_v3.py && python3 deck/video/v3/build_stage_v3.py
```
Same event contract and URLs (`?present=1`, `&admin=1`, `?as=yui`, status/heard/compose/patch/conclude/filed/record): the script needs no change unless the redesign renames the selectors in `MEET_CHECKS` / `STAGE_CHECKS` (`#status`, `#tiles .tile`, `#conv .askbar`, `#conv .chip`, `#panel .cards .card(.grey)`, `#concl.on`, `#concl .filed.on`, `#ask`, `#confirm`, `.tile.draft`, `.stub input[id^=an-]`, `.note`). Then look at `captures/` stills before stitching: the graph must be static, the tiles readable at 1080p. A narration change: `narrate_v3.py --only <id> --takes 2 --keep-shorter`, then `capture_ui.py --beats meet` (the Meet rows re-time from the wavs), then the build. The UI on `main` at build time was `0f8d4da`; captures were made from it.

## Intentionally open (from STORYBOARD_v3.md; only Carl decides)

1. The beat-04 tagline. 2. Yui vs Adachi. 3. Steven's own voice for the manager lines, or Puck (and the shorter vs full closing line: `--m2 full`). 4. The Meet beat is 20.3 s, not 19.0 (two manager lines + the 26-word English narration do not fit 19 s); the "Actually, just someone good" line is only in the stage video. 5. Yui's note text in the mirror beat. Not finished: nothing else; the Slack and Notion beats are V2's real takes untouched.

## Rules

- Fictional company (Kaede Works) and people; interviewees are roles, never names; nothing from the VP meeting that is a number; the disclosure card is the first frame, always.
- No visible browser window, ever: headless Playwright on localhost only. Carl's Dia (and its Pik tab), his server on :8787 and his live listener are not to be touched; kill only PIDs you started.
- Never play audio (`say`, `afplay`): check by ffprobe/ebur128 and by looking at stills.
- The real takes (08 Slack, 09 Notion) keep their length; take seconds from animated beats or holds.
- Music credit stays: "Music: Kosmose Vaikus by Kevin MacLeod, incompetech.com, CC BY 4.0" (end card, STORYBOARD_v3.md, this file).
- Commit as Carl Kho <carl@somach.life>, plain-words messages, no attribution lines; `git fetch && git rebase origin/main` before every push; on a conflict in a file you did not author keep origin's version.
