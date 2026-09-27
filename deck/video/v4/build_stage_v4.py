#!/usr/bin/env python3
"""Stitch the STAGE Meet video, V4: ../v3/captures/stage_v3.webm (capture_ui.py --beats stage, re-recorded on the rebuilt screen) -> meet_stage_demo.mp4,
with Pik's spoken follow-up (vo/stage_followup.wav) placed at the second the ask block became visible, and STAGE_CUES.md for Carl and Steven.
No music (it is a screen share), no captions. Run: python3 deck/video/v4/build_stage_v4.py"""
import json, pathlib, subprocess, shlex
D = pathlib.Path(__file__).resolve().parent
C, V = D.parent / "v3" / "captures", D.parent / "v3" / "vo"
OUT = D / "meet_stage_demo.mp4"
TL = json.loads((C / "stage_v3_timeline.json").read_text())
SS, END = TL["settle"], TL["end"]
ASK = TL["marks"]["ask"]
W, H, FPS = 1920, 1080, 30


def run(cmd):
    print(" ".join(shlex.quote(str(c)) for c in cmd)[:300]); subprocess.run([str(c) for c in cmd], check=True)


run(["ffmpeg", "-y", "-loglevel", "error", "-ss", SS, "-t", END + 1, "-i", C / "stage_v3.webm", "-i", V / "stage_followup.wav",
     "-filter_complex",
     f"[0:v]fps={FPS},scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,"
     f"tpad=stop_mode=clone:stop_duration={END},trim=duration={END},setpts=PTS-STARTPTS,format=yuv420p[v];"
     f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(ASK*1000)}|{int(ASK*1000)},apad,atrim=duration={END}[a]",
     "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-r", FPS,
     "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", OUT])
d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(OUT)], capture_output=True, text=True).stdout.strip()
m, L = TL["marks"], TL["lines"]
rows = [
 (0.0, "screen", "(press play)", "The Pik screen at rest: the graph of 200 people and 11 channel hubs, what Pik reads and never reads, the ground strip. Idle, \"At rest\"."),
 (3.0, "Steven", L["L1"], "Nothing yet. Say it at speaking pace, about 9 s."),
 (m["tiles"], "screen", "", "Status Heard; the line typed in; three tiles A–Z (Rin: nothing on file; Yui 29; Kei 29: \"2 of 7 words you asked for have a receipt. Not a score\"); the graph dims and lights the receipts behind each number."),
 (20.0, "Carl", L["L2"], "Nothing yet, about 6 s."),
 (m["chips"], "screen", "", "Two constraint chips in your words. Yui's tile dims: \"on the Pricing team\"."),
 (32.0, "Carl", L["L3"], "Nothing yet, about 3 s."),
 (m["ask"], "Pik (audio in the video)", TL["follow_up"], "The ask bar appears and the same sentence plays from the tab share. Let it finish, do not talk over it."),
 (43.0, "Steven", L["L4"], "Nothing yet, about 5 s."),
 (m["receipts"], "screen", "", "Yui comes forward. Her own words (verbatim, Will Can Must sheet) and under them Okada's note (paraphrase, grey), both with sources."),
 (56.0, "Steven", L["L5"], "Nothing yet, about 13 s."),
 (m["conclusion"], "screen", "", "The conclusion card: what this meeting concluded, Yui and Kei, next steps, \"ask them before deciding\"."),
 (m["filed"], "screen", "", "\"Filed · 1 question to Yui · Yui and Kei can see this page\". Read count unchanged: nothing new was read."),
 (END, "end", "", "Final frame held until here; the video ends."),
]
(D / "STAGE_CUES.md").write_text(
"# Stage cues: the Meet demo video on the new Pik screen (`meet_stage_demo.mp4`)\n\n"
"**Share this video as a tab with audio; press play at the moment you say \"Pik, are you there?\" or just start it and begin beat 1 at 3 s.**\n\n"
f"Video: `deck/video/v4/meet_stage_demo.mp4`, {float(d):.1f} s, 1920x1080, 30 fps, H.264 + AAC. The only sound in it is Pik's follow-up "
f"question at {m['ask']:.1f} s. Everything else is said live by Carl and Steven; the screen reacts on the marks below. "
"Second marks are measured from the recording (when each block actually became visible), not the plan. Same holds as V2 (speakers at 3, 20, 32, 43, 56 s).\n\n"
"| t | who | says | what appears |\n|---|---|---|---|\n" +
"".join(f"| {t:5.1f} s | {who} | {say} | {what} |\n" for t, who, say, what in rows) +
"\n## What the speakers must know\n\n"
"- Holds are generous on purpose: finish the line, then wait for the screen. If you finish early, keep looking at the screen, not the camera.\n"
"- Beat 2 dims **Yui** (\"on the Pricing team\"). That is the real behaviour; Steven's \"I keep coming back to Yui\" in beat 4 brings her forward again.\n"
f"- Beat 3: the spoken follow-up is exactly the on-screen text: \"{TL['follow_up']}\" (engine.ask on the vague line; it changed since V2). Nobody answers it; Steven moves to beat 4 at 43 s.\n"
"- Beat 5 is the longest line (13 s). The conclusion prints only at the mark, so do not rush it; the Filed line follows about 3 s later.\n"
"- The numbers on the tiles are coverage (\"2 of 7 words you asked for have a receipt\"), not a score; if a judge asks, that is the answer.\n"
"- Rebuild: `deck/video/pw/bin/python deck/video/v3/capture_ui.py --beats stage` (starts or reuses the worktree server), then `python3 deck/video/v4/build_stage_v4.py`. "
"The follow-up wav comes from `narrate_v3.py --only stage_followup`; if engine.ask's follow-up text changes, update scripts/stage_v3.json and re-render it.\n")
print("wrote", OUT, d, "s; cues ->", D / "STAGE_CUES.md")
