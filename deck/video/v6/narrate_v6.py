#!/usr/bin/env python3
"""V6 narration: an upbeat launch-video narrator (Gemini Live on Vertex, same path as ../v5/narrate_v5.py).

The name is written "Pick" in every TTS input so it is said like "pick", never "pike" (the screen keeps "Pik").
  --sample : render one line in the candidate voices (Puck, Fenrir, Zephyr, Sadachbia, Laomedeia), skip any the API rejects,
             keep the first four that work, write <scratch>/voices_sample.m4a (0.8 s silence between) and voices_sample.txt.
  default  : render every V6 line in --voice (default Puck) at --rate (atempo, <= 1.1), --takes N keeps the shortest valid take.
Run: GOOGLE_APPLICATION_CREDENTIALS=~/.config/carl-life-os/gcloud-tmuc/application_default_credentials.json \
     PYTHONDONTWRITEBYTECODE=1 <venv with google-genai>/bin/python narrate_v6.py [--sample] [--voice Puck] [--only 11]
"""
from __future__ import annotations
import asyncio, os, sys, wave, subprocess, pathlib, argparse
from google import genai
from google.genai import types

PROJECT = os.environ.get("GCP_PROJECT", "recruit-hackathon-2026-e")
LOCATION = os.environ.get("LIVE_LOCATION", "us-central1")
MODEL = os.environ.get("LIVE_MODEL", "gemini-3.8-live")
D = pathlib.Path(__file__).resolve().parent
OUT = D / "vo"
SCRATCH = D.parent.parent  # .../video-v6
STYLE = ("You are a text-to-speech engine and the narrator of a product launch video: bright, warm, energetic, confident; "
         "natural pace. Read the user's text aloud exactly, word for word. Never add, drop or change a word. Never comment. "
         "Output speech only.")
SAMPLE = "Meet Pick. It knows who's done what, and answers right where you ask."
CANDIDATES = ["Puck", "Fenrir", "Zephyr", "Sadachbia", "Laomedeia"]
LINES = [  # id, text (TTS spelling: "Pick")
    ("01_blur",      "The line between roles is blurring."),
    ("02a_asked",    "We asked people at Recruit Holdings."),
    ("02b_team",     "Team formation."),
    ("02c_decided",  "Every answer: who does what next, decided from memory."),
    ("04_meetpik",   "Meet Pick. It knows who's done what, and answers where you ask."),  # the words on the V2 Meet Pik card (the sample line adds "right")
    ("04b_meetyui",  "Pick knows how Yui is doing: it lives where she works."),
    ("05_mining",    "It reads what she already wrote, where the company allows."),
    ("06_receipts",  "Every line keeps its source."),
    ("08_slack",     "Or ask in Slack. One press to loop her in."),
    ("09_ticket",    "On a ticket, it fills in the owner, and shows why."),
    ("10_taskforce", "Tailor a task force to every task."),
    ("11_end",       "Because the future of your work depends on who you Pick."),
]


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


async def synth(client, voice, text) -> bytes:
    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"], system_instruction=STYLE,
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


def finish(pcm: bytes, out: pathlib.Path, rate: float, tag: str):
    raw = out.with_suffix(f".{tag}.raw.wav")
    with wave.open(str(raw), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
    tempo = f"atempo={rate}," if abs(rate - 1.0) > 1e-3 else ""
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af",
                    f"{tempo}silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.10",
                    "-ar", "48000", "-ac", "1", str(out)], check=True)
    raw.unlink()
    return probe(out)


async def one_line(client, sem, lid, text, voice, rate, takes):
    words = len(text.split()); floor = 0.17 * words
    best = None
    async with sem:
        for k in range(takes + 2):
            if best is not None and k >= takes:
                break
            try:
                pcm = await synth(client, voice, text)
            except Exception as e:  # noqa: BLE001
                print(f"[narrate] {lid}: take {k+1} failed: {e}", file=sys.stderr); continue
            if not pcm:
                print(f"[narrate] {lid}: take {k+1} empty", file=sys.stderr); continue
            cand = OUT / f"{lid}.take{k+1}.wav"
            d = finish(pcm, cand, rate, f"t{k+1}")
            if d < floor:
                print(f"[narrate] {lid}: take {k+1} {d:.2f}s < floor {floor:.1f}s, dropped", file=sys.stderr); cand.unlink(); continue
            if best is None or d < best[0]:
                if best: pathlib.Path(best[1]).unlink(missing_ok=True)
                best = (d, cand)
            else:
                cand.unlink()
    if best is None:
        return lid, None
    best[1].replace(OUT / f"{lid}.wav")
    print(f"{lid:14s} {best[0]:5.2f}s x{rate:.2f} {voice} {text}", flush=True)
    return lid, best[0]


async def sample(client):
    sd = OUT / "_sample"; sd.mkdir(parents=True, exist_ok=True)
    ok = []
    for v in CANDIDATES:
        if len(ok) >= 4:
            break
        try:
            pcm = await synth(client, v, SAMPLE)
        except Exception as e:  # noqa: BLE001
            print(f"[sample] {v}: rejected: {str(e)[:200]}", file=sys.stderr); continue
        if not pcm:
            print(f"[sample] {v}: empty audio", file=sys.stderr); continue
        p = sd / f"{v}.wav"; d = finish(pcm, p, 1.0, "s")
        if d < 0.17 * len(SAMPLE.split()):
            print(f"[sample] {v}: {d:.2f}s, truncated, skipped", file=sys.stderr); continue
        ok.append((v, p, d)); print(f"[sample] {v}: {d:.2f}s", flush=True)
    if not ok:
        sys.exit("[sample] no voice worked")
    sil = sd / "sil.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", "0.8", str(sil)], check=True)
    ins, fc = [], []
    seq = []
    for i, (v, p, d) in enumerate(ok):
        seq.append(p)
        if i < len(ok) - 1: seq.append(sil)
    for i, p in enumerate(seq):
        ins += ["-i", str(p)]; fc.append(f"[{i}:a]")
    out = SCRATCH / "voices_sample.m4a"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", "".join(fc) + f"concat=n={len(seq)}:v=0:a=1,loudnorm=I=-16:TP=-1.5[a]",
                    "-map", "[a]", "-ar", "48000", "-c:a", "aac", "-b:a", "160k", str(out)], check=True)
    t, lines = 0.0, []
    for i, (v, p, d) in enumerate(ok):
        lines.append(f"{i+1}. {v}  (starts at {t:.1f} s, {d:.2f} s long)"); t += d + 0.8
    rejected = [v for v in CANDIDATES if v not in [o[0] for o in ok]]
    (SCRATCH / "voices_sample.txt").write_text(
        f"voices_sample.m4a: one line in {len(ok)} Gemini Live prebuilt voices ({MODEL}, Vertex {PROJECT}/{LOCATION}), 0.8 s silence between, no tempo change.\n"
        f"Line (TTS spelling): \"{SAMPLE}\"\nSystem instruction: {STYLE}\n\nOrder:\n" + "\n".join(lines) +
        f"\n\nNot in the sample: {', '.join(rejected) or 'none'} (tried in order {', '.join(CANDIDATES)}; the first four that returned audio were kept).\n")
    print("wrote", out)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true"); ap.add_argument("--voice", default="Puck")
    ap.add_argument("--rate", type=float, default=1.0); ap.add_argument("--takes", type=int, default=2)
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    if a.rate > 1.1: sys.exit("atempo must be <= 1.1")
    OUT.mkdir(exist_ok=True)
    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    if a.sample:
        await sample(client); return
    sem = asyncio.Semaphore(4)
    res = await asyncio.gather(*(one_line(client, sem, lid, text, a.voice, a.rate, a.takes) for lid, text in LINES if not a.only or lid.startswith(a.only)))
    bad = [lid for lid, d in res if d is None]
    if bad: sys.exit(f"[narrate] failed: {bad}")


if __name__ == "__main__":
    asyncio.run(main())
