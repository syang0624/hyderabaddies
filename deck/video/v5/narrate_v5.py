#!/usr/bin/env python3
"""V5 narration: the lines re-cut to the tightened front (same Vertex Live path as ../v3/narrate_v3.py), Charon at 1.15, calm (Carl).

Charon (narrator) at --rate 1.30, Puck (the manager) at --manager-rate 1.20, per Steven's V2 feedback ("too slow and boring").
Only the ids that no longer fit their shorter beats live here; build_v5.py falls back to ../v3/vo for the rest. Output: deck/video/v5/vo/<id>.wav
(48 kHz mono). Setup and credentials: see ../v2/narrate_vertex.py (ADC in ~/.config/carl-life-os/gcloud-tmuc/, project recruit-hackathon-2026-e).
Run:  GOOGLE_APPLICATION_CREDENTIALS=~/.config/carl-life-os/gcloud-tmuc/application_default_credentials.json \
      prototype/.venv/bin/python deck/video/v5/narrate_v5.py [--only 02] [--rate 1.35] [--takes 2 --keep-shorter]
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
LINES = [  # V5, Carl's pacing: Charon at 1.15, calm; every line cut to fit its beat (cut words, not tempo)
    ("01_blur",      "Charon", STYLE, "The line between roles is blurring."),
    ("02a_asked",    "Charon", STYLE, "We asked people at Recruit Holdings."),
    ("02b_team",     "Charon", STYLE, "Team formation."),
    ("02c_decided",  "Charon", STYLE, "Every answer: who does what next, decided from memory."),
    ("04_meetpik",   "Charon", STYLE, "Meet Pik. It knows who's done what, and answers where you ask."),
    ("04b_meetyui",  "Charon", STYLE, "Pik knows how Yui is doing: it lives where she works."),
    ("05_mining",    "Charon", STYLE, "It reads what she already wrote, where the company allows."),
    ("06_receipts",  "Charon", STYLE, "Every line keeps its source."),
    ("08_slack",     "Charon", STYLE, "Or ask in Slack. One press to loop her in."),
    ("09_ticket",    "Charon", STYLE, "On a ticket, it fills in the owner, and shows why."),
    ("11_end",       "Charon", STYLE, "Because the future of your work depends on who you Pik."),
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
    ap.add_argument("--rate", type=float, default=1.15, help="atempo for Charon lines")
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
