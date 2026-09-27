#!/usr/bin/env python3
"""Narration for the Pik video, through the shared Recruit GCP project (no API key).

Vertex in project recruit-hackathon-2026-e does not offer gemini-3.8-flash-tts (404 in us, us-central1,
global; checked Sat Sep 26 20:52 PDT), and Cloud Text-to-Speech is 403 for our accounts. What does work is
Gemini 3.8 Live on Vertex (the same model and location the Meet bot uses in prototype/live.py): send a text
turn, receive 24 kHz PCM. This script does that for every line in LINES and writes deck/video/v2/vo/<id>.wav
(48 kHz mono, silence trimmed, so a cut can place each line exactly) and prints each line's duration.

Setup (once):   cd prototype && make setup        (installs google-genai into prototype/.venv)
                gcloud auth application-default login   (any account in the Recruit hackathon group)
Run:            prototype/.venv/bin/python deck/video/v2/narrate_vertex.py [--only 03] [--rate 1.15]
Env:            GCP_PROJECT (default recruit-hackathon-2026-e), LIVE_LOCATION (us-central1), LIVE_MODEL (gemini-3.8-live)

Voices: Charon (narrator, calm and brisk), Puck (the manager stand-in). The pacing note in STYLE is the only
"instruction" the model gets; it reads the text itself verbatim. --rate applies an ffmpeg atempo on top
(1.0 = as spoken; Carl asked v2 to "speak a bit faster", so the default is 1.12).
"""
from __future__ import annotations
import asyncio, os, sys, wave, subprocess, pathlib, argparse
from google import genai
from google.genai import types

PROJECT = os.environ.get("GCP_PROJECT", "recruit-hackathon-2026-e")
LOCATION = os.environ.get("LIVE_LOCATION", "us-central1")
MODEL = os.environ.get("LIVE_MODEL", "gemini-3.8-live")
OUT = pathlib.Path(__file__).parent / "vo"
STYLE = ("You are a text-to-speech engine. Read the user's text aloud exactly, word for word, as a calm, brisk "
         "documentary narrator: warm, plain, quick, no dramatic pauses. Never add, drop or change a word. "
         "Never comment. Output speech only.")
MANAGER = ("You are a text-to-speech engine. Read the user's text aloud exactly, word for word, as a hiring "
           "manager on a video call, natural and conversational. Never add, drop or change a word. Output speech only.")

# id, voice, style, text. Replace these with the v2 lines; keep ids stable so build.py rows keep working.
LINES = [
    ("01_blur",   "Charon", STYLE, "The line between jobs is blurring."),
    ("03_meet",   "Charon", STYLE, "Meet Pik."),
]


async def synth(client, voice, style, text) -> bytes:
    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"], system_instruction=style,
        speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice))))
    pcm = bytearray()
    async with client.aio.live.connect(model=MODEL, config=config) as s:
        await s.send_client_content(turns=types.Content(role="user", parts=[types.Part(text=text)]), turn_complete=True)
        async for msg in s.receive():
            sc = msg.server_content
            if sc and sc.model_turn:
                for p in sc.model_turn.parts:
                    if p.inline_data:
                        pcm += p.inline_data.data
            if sc and sc.turn_complete:
                break
    return bytes(pcm)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="only ids starting with this")
    ap.add_argument("--rate", type=float, default=1.12, help="atempo factor, 1.0 = as spoken")
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    for lid, voice, style, text in LINES:
        if a.only and not lid.startswith(a.only):
            continue
        pcm = await synth(client, voice, style, text)
        if not pcm:
            sys.exit(f"[narrate] no audio for {lid}; the Live session returned nothing")
        raw = OUT / f"{lid}.raw.wav"
        with wave.open(str(raw), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
        wav = OUT / f"{lid}.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af",
                        f"atempo={a.rate},silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
                        "silenceremove=start_periods=1:start_threshold=-50dB,areverse,apad=pad_dur=0.12",
                        "-ar", "48000", "-ac", "1", str(wav)], check=True)
        raw.unlink()
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)],
                           capture_output=True, text=True).stdout.strip()
        print(f"{lid:14s} {float(d):5.2f}s  {len(text.split()):3d} words  {text[:70]}")


if __name__ == "__main__":
    asyncio.run(main())
