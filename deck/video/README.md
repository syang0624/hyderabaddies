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

## Handoff: continuing this from another machine (Steven)

Everything is in git except the 86 MB of b-roll. Nothing needs scp.

1. `git pull` on `main`. You get `pik_90s_v1.mp4`, `renders/` (the Figma exports), `captures/` (the two Playwright recordings), `vo/` (narration wavs), and the scripts.
2. B-roll, only if you rebuild the blur and asks beats:
   ```bash
   mkdir -p deck/video/broll && cd deck/video/broll && for id in 6574285 3246669 8202010 8636292 7692854; do curl -L -o pexels_$id.mp4 https://www.pexels.com/download/video/$id/; done
   ```
3. Rebuild the cut: `python3 deck/video/build.py` (needs ffmpeg and Geist Medium in `~/Library/Fonts`).
4. Figma. The animated beats live in Carl's file `Pik - Recruit Holdings Hack` (key `1md8EyJXD30RKXXYb1pAoo`), frames `V1-00` … `V1-10`. To edit them from Claude:
   - Carl shares the file with you as **editor** (the MCP refuses writes on view-only).
   - Connect the Figma MCP: in Claude Code, `claude mcp add --transport http --scope user figma https://mcp.figma.com/mcp`, then `/mcp` in an interactive session and authorise; or add the Figma connector in claude.ai settings.
   - Ask Claude to load the `figma-use` and `figma-use-motion` skills, then edit keyframes on the `V1-*` frames and `export_video` the frame (top-level frame id, 1920 wide, 30 fps, high). Drop the mp4 into `renders/` under the same name and rebuild.
5. Narration needs `GEMINI_API_KEY` in the environment (Carl keeps his in `~/.config/carl-life-os/.env`; use your own key). Skip it if you are not changing lines; the wavs are committed.
6. Prototype captures need the page running: `cd prototype && make run-heuristic`, then `pw/bin/python deck/video/record_meet.py` and `record_candidate.py` (Playwright venv per the table above).
