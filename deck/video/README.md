# The 90-second video, and how to rebuild it

Output: `pik_90s_v1.mp4` (1920x1080, 30 fps, H.264 + AAC, 88 s). Built Sat Sep 26 2026, ~20:10 PDT.

## Pieces

| Piece | Where it comes from | Regenerate with |
|---|---|---|
| Animated beats (disclosure, blur, asks, Meet Pik, mining, receipts, zoom-out, Slack card, beyond, end card) | Figma Motion keyframes in the Pik file, frames named `V1-00` … `V1-10` at y=17000 and y=18400 on Page 1 | Edit in Figma, then `export_video` on the frame (Figma MCP) and drop the mp4 into `renders/` with the same name |
| Meet beat (stand-in) | `record_meet.py`: replays the scripted call's events into `prototype/state/live.jsonl` while Playwright records `localhost:8787/?present=1&before=1` | `$PW record_meet.py` (needs `make run-heuristic` running) |
| Candidate beat | `record_candidate.py`: Playwright opens `?as=yui&present=1`, opens a receipt, types Yui's note, presses Add note | `$PW record_candidate.py` |
| Narration | `narrate.py`: Gemini 3.8 Flash TTS, voice Charon (narrator) and Puck (the manager stand-in). Plain text only; the model reads any style prefix aloud | `set -a; source ~/.config/carl-life-os/.env; set +a; python3 narrate.py [--only 04]` |
| B-roll | Pexels, free licence, downloaded with `https://www.pexels.com/download/video/<id>/`: 6574285 (Shibuya), 3246669 (office), 8202010 and 8636292 (portraits), 7692854 (meeting, unused) | re-download into `broll/` (git-ignored) |
| Captions | rendered by PIL in `build.py` (this ffmpeg has no drawtext), Geist Medium from `~/Library/Fonts` | automatic |
| The cut | `build.py`: the `SEGMENTS` table is the edit; each row is one beat with its trim, b-roll under (multiply blend), narration offsets and captions | `python3 build.py` (~10 s) |

`$PW` is a venv with Playwright: `uv venv pw && uv pip install --python pw/bin/python playwright && pw/bin/python -m playwright install chromium`.

## What is a stand-in

- The Meet beat (43 s to 62 s) is a replay through the real page, not a real take. The manager's two lines are TTS (Puck). Replace `captures/meet_replay.webm` with the Cap recording of Carl and Steven, delete the two `06_*` narration entries in `SEGMENTS`, and rebuild.
- The Slack beat uses the Figma card, not Steven's Slack recording. If his clip lands, add a row with `src=captures/slack.webm`.

## Timing

See `TIMING.md` (written by every build).
