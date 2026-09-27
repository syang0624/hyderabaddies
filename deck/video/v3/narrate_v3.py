#!/usr/bin/env python3
"""V3 narration: the same Vertex Live path as ../v2/narrate_vertex.py, new lines, faster.

Charon (narrator) at --rate 1.30, Puck (the manager) at --manager-rate 1.20, per Steven's V2 feedback ("too slow and boring").
Every line is silence-trimmed at both ends so build_v3.py can start each beat on its first word. Output: deck/video/v3/vo/<id>.wav
(48 kHz mono). Setup and credentials: see ../v2/narrate_vertex.py (ADC in ~/.config/carl-life-os/gcloud-tmuc/, project recruit-hackathon-2026-e).
Run:  GOOGLE_APPLICATION_CREDENTIALS=~/.config/carl-life-os/gcloud-tmuc/application_default_credentials.json \
      prototype/.venv/bin/python deck/video/v3/narrate_v3.py [--only 07] [--rate 1.30] [--manager-rate 1.20]
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
PIK = ("You are a text-to-speech engine. Read the user's text aloud exactly, word for word, as a calm assistant asking one short "
       "question in a meeting: plain, unhurried, no drama. Never add, drop or change a word. Output speech only.")
MANAGER = ("You are a text-to-speech engine. Read the user's text aloud exactly, word for word, as a hiring "
           "manager on a video call, natural and conversational. Never add, drop or change a word. Output speech only.")

# id, voice, style, text. Ids are the build_v3.py rows. "_alt" ids are shorter variants kept so the cut can pick the one that fits.
LINES = [
    ("01_blur",      "Charon", STYLE, "In a post-LLM world, the line between what one person can do is blurring."),
    ("02_asked",     "Charon", STYLE, "We asked people at Recruit Holdings what their hardest problem in HR is. Every answer was the same shape: who does what next, decided from memory."),
    ("03_asks",      "Charon", STYLE, "Who should mentor the interns? Lead the pricing task force? Take the two-year exchange?"),  # the caption says "Same question, every week."
    ("04_meetpik",   "Charon", STYLE, "Meet Pik. It knows who's done what, and answers where you ask."),
    ("05_mining",    "Charon", STYLE, "Pik reads what Yui already wrote and shipped, where the company allows. Every line keeps its source."),
    ("06_receipts",  "Charon", STYLE, "Two hundred people, or twenty thousand. Always current."),
    ("07_manager",   "Puck",   MANAGER, "For the Northwind slot I need someone who will push back on the job-based culture instead of just absorbing it, and they have to hold their own in English in meetings."),
    ("07_english",   "Charon", STYLE, "The ask needs English in meetings. She wrote it herself: strong in writing, weaker speaking. Her manager wrote 'flexible on location'. Both attached, word for word."),
    ("07_manager2",  "Puck",   MANAGER, "Okay, let's set up calls with Yui and Kei this week, and ask Yui whether that location note is actually true."),
    ("07_manager2_alt", "Puck", MANAGER, "Okay, let's set up calls with Yui and Kei this week, and ask Yui about that location note."),
    ("08_slack",     "Charon", STYLE, "Or ask in Slack. One press to loop her in."),
    ("08_crud",      "Charon", STYLE, "New hire? Just tell Pik. Her page exists from day one."),
    ("09_ticket",    "Charon", STYLE, "On a ticket, it fills in the owner, and shows why."),
    ("10_verticals", "Charon", STYLE, "The same map answers hospitals, airlines, construction sites. Anywhere the wrong person on the job is expensive."),
    ("10_verticals_alt", "Charon", STYLE, "Hospitals. Airlines. Construction sites. Anywhere the wrong person on the job is expensive."),
    ("11_end",       "Charon", STYLE, "Because the future of your work depends on who you Pik."),
    # the stage video: Pik's spoken follow-up = engine.ask(L3)["follow_up"] on the current engine (changed since V2; recompute if the engine changes)
    ("stage_followup", "Charon", PIK, "What would this person actually do in the first month?"),
]
MANAGER_IDS = {lid for lid, voice, _, _ in LINES if voice == "Puck"}


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
    ap.add_argument("--rate", type=float, default=1.30, help="atempo for Charon lines")
    ap.add_argument("--manager-rate", type=float, default=1.20, help="atempo for Puck lines")
    ap.add_argument("--takes", type=int, default=1, help="synthesize N times and keep the shortest valid take (the Live model's pace varies per call)")
    ap.add_argument("--keep-shorter", action="store_true", help="only replace an existing wav when the new take is shorter")
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    failed = []

    def probe(p):
        return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                    capture_output=True, text=True).stdout.strip() or 0)

    for lid, voice, style, text in LINES:
        if a.only and not lid.startswith(a.only):
            continue
        rate = a.manager_rate if lid in MANAGER_IDS else a.rate
        words = len(text.split())
        floor = 0.17 * words  # a take shorter than this lost words (one V3 take came back at 0.67 s for 26 words)
        wav = OUT / f"{lid}.wav"
        best = (probe(wav), "kept") if (a.keep_shorter and wav.exists() and probe(wav) >= floor) else (None, None)
        tries = 0
        while tries < max(a.takes, 1) + 2:  # up to two extra tries cover a dropped or truncated take
            tries += 1
            try:
                pcm = await synth(client, voice, style, text)
            except Exception as e:  # noqa: BLE001
                print(f"[narrate] {lid}: take {tries} failed: {e}", file=sys.stderr); pcm = b""
            if not pcm:
                continue
            raw = OUT / f"{lid}.raw.wav"
            with wave.open(str(raw), "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
            cand = OUT / f"{lid}.take{tries}.wav"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af",
                            f"atempo={rate},silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                            "silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.10",
                            "-ar", "48000", "-ac", "1", str(cand)], check=True)
            raw.unlink()
            d = probe(cand)
            if d < floor:
                print(f"[narrate] {lid}: take {tries} is {d:.2f}s for {words} words (< {floor:.1f}s floor), dropped", file=sys.stderr)
                cand.unlink(); continue
            if best[0] is None or d < best[0] - 1e-3:
                if best[1] not in (None, "kept"):
                    pathlib.Path(best[1]).unlink(missing_ok=True)
                best = (d, str(cand))
            else:
                cand.unlink()
            if tries >= a.takes and best[0] is not None:
                break
        if best[0] is None:
            failed.append(lid); print(f"[narrate] NO VALID AUDIO for {lid}", file=sys.stderr); continue
        if best[1] != "kept":
            pathlib.Path(best[1]).replace(wav)
        print(f"{lid:18s} {best[0]:5.2f}s  x{rate:.2f}  {words:3d} words  {'(kept)' if best[1]=='kept' else ''} {text[:60]}", flush=True)
    if failed:
        sys.exit(f"[narrate] failed: {failed}")


if __name__ == "__main__":
    asyncio.run(main())
