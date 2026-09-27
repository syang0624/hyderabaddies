"""Simulated meeting for the live layer: TTS audio -> Gemini 3.8 Live -> tool calls, no microphone.

Speaks a scripted PM/HR call through macOS `say` into wav files (never through the speakers),
streams them to the same Live session live.py uses, and reports which blocks the model placed on
the shared screen after each line (question, people, constraint, ask, receipt, conclude) and how
long they took. Events go to state/live.jsonl, so the page reacts as in a real call. SPEAK is
forced to 0: nothing is ever played.

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

# (speaker voice, line, blocks we expect on the screen after it: a set of block kinds, or empty for "nothing")
# A line passes when every expected kind was placed, and "ask" / "conclude" fired only when expected.
SCRIPT = [
    ("Samantha", "Hey, how was the weekend? The coffee at this place is really good. Anyway, I have about ten minutes.", set()),
    ("Daniel", "Sure. So for the Northwind exchange slot. Honestly I need someone who will push back on the job-based culture over there instead of just absorbing it. And they have to hold their own in English in meetings.", {"question", "people"}),
    ("Samantha", "Got it. One constraint from my side: the posting starts April 2027, and we cannot lose anyone from pricing before the Q1 close.", {"constraint"}),
    ("Kyoko", "あと、英語で会議をリードできて、上司の意見にも異議を唱えられる人がいいです。", {"people"}),
    ("Samantha", "Actually, we also need someone good for this. Just someone good.", {"ask"}),
    ("Daniel", "I keep coming back to Yui. What did she actually write about this herself, and what did her manager write about her?", {"receipt"}),
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
    live.SPEAK = False  # never play audio in tests
    live.EVENTS.write_text("")
    live.DOC.clear()
    client = live.genai.Client(vertexai=True, project=live.PROJECT, location=live.LOCATION)
    # The SDK forwards this dict to websockets.connect; a 20 s pong timeout was dropping the socket on venue Wi-Fi.
    try:
        client._api_client._websocket_ssl_ctx.update({"ping_interval": 20, "ping_timeout": 90})
    except Exception:  # noqa: BLE001
        pass
    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"], system_instruction=live.system_prompt(), tools=live.TOOLS,
        input_audio_transcription={}, output_audio_transcription={},
        context_window_compression=types.ContextWindowCompressionConfig(sliding_window=types.SlidingWindow()),
        session_resumption=types.SessionResumptionConfig(handle=None),
    )
    fired: list[tuple[float, str, dict]] = []
    placed: list[tuple[float, set]] = []  # (t, block kinds placed) per tool call, graded per line
    said: list[str] = []
    heard_buf = [""]
    drops = 0
    audio = [(voice, text, expect, tts(voice, text)) for voice, text, expect in SCRIPT]  # render before connecting
    report = []
    # room tone, not digital zero: a real microphone always has a noise floor, and the server's voice
    # activity detection answered pure zeros with "<no speech detected>" and then dropped later lines
    import random, struct
    rnd = random.Random(7)
    silence = b"".join(struct.pack("<h", rnd.randint(-24, 24)) for _ in range(RATE // 10))
    idx = 0

    while idx < len(audio):
      config.session_resumption = types.SessionResumptionConfig(handle=RESUME["handle"])
      async with client.aio.live.connect(model=live.MODEL, config=config) as session:
        live.emit("status", text=f"simulated call via {live.MODEL}" + (f" (reconnect {drops})" if drops else ""))
        live.CURRENT["session"] = session
        live.CURRENT["on_placed"] = lambda k: placed.append((time.time(), set(k)))

        async def listen():
            while True:  # receive() returns after every turn_complete; keep reading until the socket closes
              async for msg in session.receive():
                  if msg.session_resumption_update and msg.session_resumption_update.resumable and msg.session_resumption_update.new_handle:
                      RESUME["handle"] = msg.session_resumption_update.new_handle
                  sc = msg.server_content
                  if sc and sc.input_transcription and sc.input_transcription.text:
                      heard_buf[0] += sc.input_transcription.text
                      if heard_buf[0].endswith((".", "?", "!", "。")) or len(heard_buf[0]) > 160:
                          txt = heard_buf[0].strip(); heard_buf[0] = ""
                          live.emit("heard", text=txt)
                          async def fallback(txt=txt, t_heard=time.time()):
                              kinds = await live.maybe_trigger(txt, t_heard)
                              if kinds:
                                  fired.append((time.time(), "transcript", {"kinds": sorted(kinds), "criterion": txt}))
                                  placed.append((time.time(), kinds))
                          asyncio.create_task(fallback())
                  if sc and sc.output_transcription and sc.output_transcription.text:
                      said.append(sc.output_transcription.text)
                  if msg.tool_call:
                      responses = []
                      for fc in msg.tool_call.function_calls:
                          fired.append((time.time(), fc.name, dict(fc.args or {})))
                          resp, kinds = await live.handle_tool_call(fc)
                          placed.append((time.time(), kinds))
                          responses.append(resp)
                      await session.send_tool_response(function_responses=responses)

        lt = asyncio.create_task(listen())
        try:
            while idx < len(audio):
                voice, text, expect, pcm = audio[idx]
                n0 = len(fired); p0 = len(placed)
                for i in range(0, len(pcm), RATE // 5):  # 100 ms chunks at real-time pace
                    await session.send_realtime_input(audio=types.Blob(data=pcm[i:i + RATE // 5], mime_type=f"audio/pcm;rate={RATE}"))
                    await asyncio.sleep(0.1)
                t_end = time.time()
                for _ in range(80):  # 8 s of silence so the model can act
                    await session.send_realtime_input(audio=types.Blob(data=silence, mime_type=f"audio/pcm;rate={RATE}"))
                    await asyncio.sleep(0.1)
                got = fired[n0:]
                kinds = set().union(*[k for _, k in placed[p0:]]) if placed[p0:] else set()
                ok = expect <= kinds and all((k in kinds) == (k in expect) for k in ("ask", "conclude"))
                lat = f"{got[0][0] - t_end:+.1f}s after the line ended" if got else "none"
                report.append((ok, voice, text[:60], sorted(kinds), sorted(expect), lat, [{"tool": n, **a} for _, n, a in got]))
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
        print(f"{'PASS' if ok else 'FAIL'}  {voice:9} {text!r}\n      placed={names} expected={expect} first={lat}")
        for a in args:
            print("      ", json.dumps(a, ensure_ascii=False)[:220])
    print(f"\n{passed}/{len(report)} lines behaved as expected. Socket drops: {drops}. Model spoke {len(said)} times: {' | '.join(s.strip() for s in said)[:200]!r}")
    print(f"screen at the end: {[b['type'] for b in live.DOC]}")
    return passed == len(report)


if __name__ == "__main__":
    sys.exit(0 if asyncio.run(main()) else 1)
