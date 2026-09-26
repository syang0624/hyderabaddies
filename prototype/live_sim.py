"""Simulated meeting for the live layer: TTS audio -> Gemini 3.8 Live -> tool calls, no microphone.

Speaks a scripted PM/HR call through macOS `say` into wav files (never through the speakers),
streams them to the same Live session live.py uses, and reports which tools fired after each
line and how long they took. Events go to state/live.jsonl, so the page reacts as in a real call.

Run:  .venv/bin/python live_sim.py            (needs macOS `say`; ~2 minutes)
"""
from __future__ import annotations

import asyncio
import json
import subprocess
import sys
import tempfile
import time
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import live  # noqa: E402
from google.genai import types  # noqa: E402

# (speaker voice, line, tools we expect to fire on it: set of names, or empty set for "nothing")
SCRIPT = [
    ("Samantha", "Hey, how was the weekend? The coffee at this place is really good. Anyway, I have about ten minutes.", set()),
    ("Daniel", "Sure. So for the Northwind exchange slot. Honestly I need someone who will push back on the job-based culture over there instead of just absorbing it. And they have to hold their own in English in meetings.", {"show_candidates"}),
    ("Samantha", "Got it. One constraint from my side: the posting starts April 2027, and we cannot lose anyone from pricing before the Q1 close.", {"note"}),
    ("Kyoko", "あと、英語で会議をリードできて、上司の意見にも異議を唱えられる人がいいです。", {"show_candidates"}),
    ("Daniel", "Okay. Looking at this, Yui's own words say she wants exactly that, and she has been running the Northwind sync in English. Let's set up calls with Yui and Kei this week, and ask Yui whether her manager's note about being flexible on location is actually true. That's it for today, thanks.", {"conclude"}),
]
RATE = 16000
RESUME = {"handle": None}  # latest session-resumption handle, reused on reconnect so context survives a drop


def tts(voice, text):
    out = Path(tempfile.mkdtemp()) / "line.wav"
    subprocess.run(["say", "-v", voice, "-o", str(out), "--data-format=LEI16@16000", text], check=True)
    with wave.open(str(out), "rb") as w:
        assert w.getframerate() == RATE and w.getnchannels() == 1, (w.getframerate(), w.getnchannels())
        return w.readframes(w.getnframes())


async def main():
    live.EVENTS.write_text("")
    client = live.genai.Client(vertexai=True, project=live.PROJECT, location=live.LOCATION)
    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"], system_instruction=live.system_prompt(), tools=live.TOOLS,
        input_audio_transcription={}, output_audio_transcription={},
        context_window_compression=types.ContextWindowCompressionConfig(sliding_window=types.SlidingWindow()),
        session_resumption=types.SessionResumptionConfig(handle=None),
    )
    fired: list[tuple[float, str, dict]] = []
    said: list[str] = []
    drops = 0
    audio = [(voice, text, expect, tts(voice, text)) for voice, text, expect in SCRIPT]  # render before connecting
    report = []
    silence = b"\x00\x00" * (RATE // 10)
    idx = 0

    while idx < len(audio):
      config.session_resumption = types.SessionResumptionConfig(handle=RESUME["handle"])
      async with client.aio.live.connect(model=live.MODEL, config=config) as session:
        live.emit("status", text=f"simulated call via {live.MODEL}" + (f" (reconnect {drops})" if drops else ""))

        async def listen():
            async for msg in session.receive():
                if msg.session_resumption_update and msg.session_resumption_update.resumable and msg.session_resumption_update.new_handle:
                    RESUME["handle"] = msg.session_resumption_update.new_handle
                sc = msg.server_content
                if sc and sc.output_transcription and sc.output_transcription.text:
                    said.append(sc.output_transcription.text)
                if msg.tool_call:
                    responses = []
                    for fc in msg.tool_call.function_calls:
                        args = dict(fc.args or {})
                        fired.append((time.time(), fc.name, args))
                        result = {"ok": True}
                        if fc.name == "show_candidates":
                            r = await asyncio.to_thread(live.engine.rank, args.get("criterion", ""))
                            result = {"shown": [{"id": x["candidate"], "name": x["name"]} for x in r["ranking"]]}
                            live.emit("show_candidates", criterion=args.get("criterion", ""), ranking=[x["candidate"] for x in r["ranking"]])
                        elif fc.name == "conclude":
                            live.emit("conclude", **args)
                        elif fc.name == "note":
                            live.emit("note", text=args.get("text", ""))
                        responses.append(types.FunctionResponse(id=fc.id, name=fc.name, response=result))
                    await session.send_tool_response(function_responses=responses)

        lt = asyncio.create_task(listen())
        try:
            while idx < len(audio):
                voice, text, expect, pcm = audio[idx]
                n0 = len(fired)
                for i in range(0, len(pcm), RATE // 5):  # 100 ms chunks at real-time pace
                    await session.send_realtime_input(audio=types.Blob(data=pcm[i:i + RATE // 5], mime_type=f"audio/pcm;rate={RATE}"))
                    await asyncio.sleep(0.1)
                t_end = time.time()
                for _ in range(80):  # 8 s of silence so the model can act
                    await session.send_realtime_input(audio=types.Blob(data=silence, mime_type=f"audio/pcm;rate={RATE}"))
                    await asyncio.sleep(0.1)
                got = fired[n0:]
                names = {n for _, n, _ in got}
                lat = f"{got[0][0] - t_end:+.1f}s after the line ended" if got else "none"
                report.append((names == expect, voice, text[:60], sorted(names), sorted(expect), lat, [a for _, _, a in got]))
                idx += 1
        except Exception as e:  # noqa: BLE001
            drops += 1
            live.emit("status", text=f"socket dropped during line {idx + 1} ({type(e).__name__}); reconnecting")
            if drops > 5:
                raise
        finally:
            lt.cancel()

    print("\n=== simulated call report ===")
    passed = 0
    for ok, voice, text, names, expect, lat, args in report:
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  {voice:9} {text!r}\n      fired={names} expected={expect} first={lat}")
        for a in args:
            print("      ", json.dumps(a, ensure_ascii=False)[:220])
    print(f"\n{passed}/{len(report)} lines behaved as expected. Socket drops: {drops}. Model spoke {len(said)} times: {' | '.join(s.strip() for s in said)[:200]!r}")
    return passed == len(report)


if __name__ == "__main__":
    sys.exit(0 if asyncio.run(main()) else 1)
