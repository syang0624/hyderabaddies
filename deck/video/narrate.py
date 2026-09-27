#!/usr/bin/env python3
"""Narration for the Pik 90s video. Gemini 3.8 Flash TTS (GEMINI_API_KEY from ~/.config/carl-life-os/.env).
Re-run to regenerate every line deterministically-enough; prints each line's duration so the cut can be re-timed.
Usage: set -a; source ~/.config/carl-life-os/.env; set +a; python3 narrate.py [--only 03]
"""
import os, sys, json, base64, urllib.request, subprocess, pathlib
OUT = pathlib.Path(__file__).parent / "vo"; OUT.mkdir(exist_ok=True)
STYLE = "Read this as a calm, brisk documentary narrator. Warm, plain, unhurried but never slow. No dramatic pauses."
MANAGER = "Read this as a hiring manager on a video call, natural and conversational, thinking out loud."
LINES = [
 # id, voice, style (kept for reference; Gemini TTS reads any prefix aloud, so it is NOT sent), text
 ("01_blur",   "Charon", STYLE, "The line between jobs is blurring."),
 ("02_asks",   "Charon", STYLE, "So who do you call when you need someone to organize the hackathon, run a one-on-one evaluation, or lead a job board for construction?"),
 ("03_meet",   "Charon", STYLE, "Meet Pik. Company intelligence that works wherever you already are."),
 ("04_mining", "Charon", STYLE, "Pik reads what Yui already wrote and shipped, in the places your company allows."),
 ("04b_receipts","Charon", STYLE, "Every line keeps its source. What can't be sourced is dropped, and it says so."),
 ("05_zoom",   "Charon", STYLE, "Two hundred people. Always current."),
 ("06_manager","Puck",   MANAGER, "For the Northwind slot I need someone who will push back on the job-based culture instead of just absorbing it, and they have to hold their own in English in meetings."),
 ("06b_manager2","Puck", MANAGER, "Okay, let's set up calls with Yui and Kei this week, and ask Yui whether that location note is actually true."),
 ("07_slack",  "Charon", STYLE, "Or ask in Slack. One press to loop her in."),
 ("08_cand",   "Charon", STYLE, "Yui sees the same page. She answers before anyone decides."),
 ("09_beyond", "Charon", STYLE, "The next intern. The next mentor. The next one-on-one. Anyone the wrong pick is expensive for."),
 ("10_end",    "Charon", STYLE, "Because the future of your work depends on who you Pik."),
]
key = os.environ["GEMINI_API_KEY"]
only = sys.argv[sys.argv.index("--only")+1] if "--only" in sys.argv else None
for lid, voice, style, text in LINES:
    if only and not lid.startswith(only): continue
    body = {"contents":[{"parts":[{"text": text}]}],
            "generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":voice}}}}}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash-tts:generateContent?key={key}",
                                 data=json.dumps(body).encode(), headers={"Content-Type":"application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=120))
    pcm = base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
    mime = r["candidates"][0]["content"]["parts"][0]["inlineData"]["mimeType"]
    raw = OUT / (f"{lid}.raw.wav" if "wav" in mime else f"{lid}.pcm"); raw.write_bytes(pcm)
    wav = OUT / f"{lid}.wav"
    inp = ["-i",str(raw)] if "wav" in mime else ["-f","s16le","-ar","24000","-ac","1","-i",str(raw)]
    # trim leading/trailing silence so the cut can place lines exactly
    subprocess.run(["ffmpeg","-y","-loglevel","error",*inp,"-af",
                    "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,apad=pad_dur=0.12",
                    "-ar","48000","-ac","1",str(wav)], check=True)
    raw.unlink()
    d = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(wav)],capture_output=True,text=True).stdout.strip()
    print(f"{lid:14s} {float(d):5.2f}s  {len(text.split()):3d} words  {text[:60]}")
