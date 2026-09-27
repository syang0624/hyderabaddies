#!/usr/bin/env python3
"""Stitch the Pik 90-second video, V3: V2's animated beats + the two real takes + the new Pik screen (Meet, CRUD, mirror) + V3 narration + a ducked music bed.

Inputs: ../v2/renders/<id>.mp4 (render.py, unchanged from V2), captures/*.webm + *_timeline.json (capture_ui.py), vo/*.wav (narrate_v3.py),
music/bed.wav (music_bed.py). Output: pik_90s_v3.mp4 (1920x1080, 30 fps, H.264 + AAC). Writes TIMING.md.
The SEGMENTS table is the edit: one row per beat; dur is the seconds kept; `speed` plays an animated beat faster (frames dropped, no
content lost); vo offsets are relative to the segment start (negative = a J-cut from the previous beat); caps are (text, start, end)
relative to the segment. A missing render becomes a bone slate that says the beat id, so timing can be checked before every beat lands.
Audio: narration mixed and loudnorm'd to -16 LUFS as in V2; the bed is multiplied by an envelope built from the narration offsets
(-26 dB under speech, -18 dB in gaps, 150 ms down / 500 ms up ramps, 2 s fade in, 3 s fade out on the end card), then summed and limited.
Run: python3 deck/video/v3/build_v3.py   (ffmpeg + PIL + Geist in ~/Library/Fonts; the envelope needs numpy: MUSIC_PY=<python with numpy>, else pure python)
"""
import subprocess, pathlib, glob, shlex, sys, json, os, wave, struct, math
D = pathlib.Path(__file__).resolve().parent
R2 = D.parent / "v2" / "renders"
C, V, M = D / "captures", D / "vo", D / "music"
OUT = D / "pik_90s_v3.mp4"
FONT = next(iter(glob.glob(str(pathlib.Path.home()/"Library/Fonts/Geist-Medium.ttf")) + glob.glob(str(pathlib.Path.home()/"Library/Fonts/Geist-*.ttf"))), None)
MONO = next(iter(glob.glob(str(pathlib.Path.home()/"Library/Fonts/GeistMono-Regular.ttf"))), FONT)
W, H, FPS = 1920, 1080, 30
BONE, INK = (0xEF, 0xEA, 0xE2), (0x2B, 0x25, 0x21)
DUCK_SPEECH, DUCK_GAP = -26.0, -18.0   # bed level relative to the narration (dB)
MUSIC_FADE_IN, MUSIC_FADE_OUT = 2.0, 3.0


def tl(name, default):
    p = C / f"{name}_timeline.json"
    return json.loads(p.read_text()) if p.exists() else default


MEET = tl("meet_v3", {"beat_ss": 2.0, "beat_len": 21.4, "vo": {"07_manager": -1.4, "07_english": 6.7, "07_manager2_alt": 15.5}, "marks": {}})
CRUD = tl("crud", {"beat_ss": 2.2, "marks": {}})
MIRROR = tl("mirror", {"beat_ss": 4.0, "marks": {}})
M2 = next((k for k in MEET["vo"] if k.startswith("07_manager2")), "07_manager2_alt")
mk = MEET.get("marks", {})
meet_len = float(MEET["beat_len"])
c_tiles = mk.get("tiles", 4.5); c_own = mk.get("own_words", 6.3); c_ask = mk.get("ask", 8.6); c_concl = mk.get("conclusion", meet_len - 1.8)

SEGMENTS = [
 dict(name="00_disclosure", src=R2/"00_disclosure.mp4", dur=2.1, light=True),
 dict(name="01_blur",       src=R2/"01_blur.mp4",       dur=4.4, light=True, vo=[("01_blur", 0.1)]),
 dict(name="02_asked",      src=R2/"02_asked.mp4",      dur=7.4, light=True, vo=[("02_asked", 0.1)],
      caps=[("Team formation. Internal mobility. Decided from memory.", 0.8, 5.6)]),
 dict(name="03_asks",       src=R2/"03_asks.mp4",       dur=4.5, speed=1.15, light=True, vo=[("03_asks", 0.1)],
      caps=[("Same question, every week.", 2.9, 4.5)]),
 dict(name="04_meetpik",    src=R2/"04_meetpik.mp4",    dur=3.7, light=True, vo=[("04_meetpik", 0.1)]),
 dict(name="05_mining",     src=R2/"05_mining.mp4",     dur=8.9, speed=1.3, light=True, vo=[("05_mining", 0.4)],
      caps=[("It reads what she already did.", 0.6, 4.0), ("Every line keeps its source. DMs never.", 4.3, 8.7)]),
 dict(name="06_receipts",   src=R2/"06_receipts.mp4",   dur=4.4, light=True, vo=[("06_receipts", 0.15)],
      caps=[("Any size. Always current.", 2.3, 4.4)]),
 dict(name="07_meet",       src=C/"meet_v3.webm", ss=MEET["beat_ss"], dur=meet_len, light=False,
      vo=[(k, float(v)) for k, v in MEET["vo"].items()],
      caps=[("Heard the criterion. Receipts for their words. No rank.", c_tiles + 0.4, c_ask - 0.2),
            ("Her own words, then what her manager wrote. Both attached, word for word.", c_ask + 0.2, c_concl - 0.3),
            ("What the meeting concluded. Receipts attached.", c_concl + 0.2, meet_len)]),
 dict(name="08_slack",      src=R2/"08_slack_real_pik.mp4", dur=7.6, light=False, vo=[("08_slack", 0.4)],  # real take in Carl's Dia with Pik on it (V2)
      caps=[("Ask where you already are. One press to loop her in.", 0.8, 7.4)]),
 dict(name="08b_crud",      src=C/"crud.webm", ss=CRUD["beat_ss"], dur=5.4, light=False, vo=[("08_crud", 0.2)],
      caps=[("HR adds a person by talking to Pik. Allowlisted channels only. DMs never.", 0.4, 5.4)]),
 dict(name="08c_mirror",    src=C/"mirror.webm", ss=MIRROR["beat_ss"], dur=3.0, light=False,
      caps=[("Yui sees the same page. She answers first.", 0.2, 3.0)]),
 dict(name="09_ticket",     src=R2/"09_notion_real_pik.mp4", dur=9.0, light=False, vo=[("09_ticket", 0.4)],  # real Notion take with Pik on it (V2)
      caps=[("A new ticket. Pik fills in the owner, and the why.", 1.0, 8.8)]),
 dict(name="10_verticals",  src=R2/"10_verticals.mp4",  dur=5.4, speed=1.1, light=True, vo=[("10_verticals_alt", 0.1)],
      caps=[("Anywhere the wrong person on the job is expensive.", 2.6, 5.4)]),
 dict(name="11_end",        src=(D/"renders"/"11_end.mp4") if (D/"renders"/"11_end.mp4").exists() else R2/"11_end.mp4",  # v3: + the music credit line (html/11_end.html, render.py)
      dur=3.6, light=True, vo=[("11_end", 0.25)]),
]


def run(cmd):
    print(" ".join(shlex.quote(str(c)) for c in cmd)[:300]); subprocess.run([str(c) for c in cmd], check=True)


def caption_png(text, light, path):
    """One caption as a transparent PNG (PIL; this ffmpeg has no drawtext). Bottom-centre pill, Geist Medium 38."""
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(FONT, 38)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    x0, y0, x1, y1 = tmp.textbbox((0, 0), text, font=font)
    tw, th = x1 - x0, y1 - y0
    px, py = 30, 18
    im = Image.new("RGBA", (tw + 2*px, th + 2*py), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if light:  # espresso pill on bone/light UIs
        d.rounded_rectangle((0, 0, im.width-1, im.height-1), radius=14, fill=INK + (235,)); fg = (255, 255, 255, 255)
    else:      # bone pill on the dark product UI
        d.rounded_rectangle((0, 0, im.width-1, im.height-1), radius=14, fill=BONE + (240,)); fg = INK + (255,)
    d.text((px - x0, py - y0), text, font=font, fill=fg)
    im.save(path); return im.height


def slate_png(name, path):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (W, H), BONE); d = ImageDraw.Draw(im)
    f1, f2 = ImageFont.truetype(MONO, 64), ImageFont.truetype(MONO, 28)
    d.text((W/2, H/2 - 30), name, font=f1, fill=INK, anchor="mm")
    d.text((W/2, H/2 + 50), "slate: this beat's render has not landed yet", font=f2, fill=(0x8A, 0x81, 0x7A), anchor="mm")
    im.save(path)


def build_segment(seg, idx):
    out = D/"_seg"/f"{idx:02d}_{seg['name']}.mp4"; out.parent.mkdir(exist_ok=True)
    ss, dur, speed = seg.get("ss", 0), seg["dur"], seg.get("speed", 1.0)
    src = seg["src"]; slate = not pathlib.Path(src).exists()
    if slate:
        png = out.parent / f"slate_{seg['name']}.png"; slate_png(seg["name"], png)
        inputs = ["-loop", "1", "-t", dur, "-i", png]
    else:
        inputs = ["-ss", ss, "-t", dur * speed + 1.0, "-i", src]
    # scale/pad to the frame, optional speed-up, hold the last frame if the clip is shorter than dur
    fc = [f"[0:v]" + (f"setpts=PTS/{speed}," if speed != 1.0 else "") +
          f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,"
          f"tpad=stop_mode=clone:stop_duration={dur},format=rgb24[v0]"]
    cur = "[v0]"
    for j, (text, a, b) in enumerate(seg.get("caps", [])):
        png = out.parent / f"cap_{idx:02d}_{j}.png"; caption_png(text, seg.get("light", True), png)
        inputs += ["-i", png]
        fc.append(f"{cur}[{1+j}:v]overlay=(W-w)/2:H-118-h:enable='between(t,{a},{b})'[c{j}]"); cur = f"[c{j}]"
    fc.append(f"{cur}trim=duration={dur},setpts=PTS-STARTPTS,format=yuv420p[vout]")
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-an",
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-r", FPS, out])
    return out, slate


def wav_dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


def envelope_wav(speech, total, path, sr=48000):
    """The duck envelope as a stereo wav: DUCK_GAP dB, DUCK_SPEECH dB while any narration plays (ramps 150 ms down before a line,
    500 ms up after), times the music fade in/out. Multiplied into the bed by ffmpeg's amultiply."""
    n = int(total * sr) + 1
    g_gap, g_sp = 10 ** (DUCK_GAP / 20), 10 ** (DUCK_SPEECH / 20)
    try:
        import numpy as np
        t = np.arange(n) / sr
        env = np.full(n, g_gap)
        down, up = 0.15, 0.5
        for a, b in speech:
            i0, i1 = int(max(0, a - down) * sr), int(min(total, b + up) * sr)
            seg_t = t[i0:i1]
            g = np.where(seg_t < a, g_gap + (g_sp - g_gap) * np.clip((seg_t - (a - down)) / down, 0, 1),
                         np.where(seg_t <= b, g_sp, g_sp + (g_gap - g_sp) * np.clip((seg_t - b) / up, 0, 1)))
            env[i0:i1] = np.minimum(env[i0:i1], g)
        fade = np.minimum(np.clip(t / MUSIC_FADE_IN, 0, 1), np.clip((total - t) / MUSIC_FADE_OUT, 0, 1))
        env = env * fade
        data = (np.clip(env, 0, 1) * 32767).astype("<i2")
        stereo = np.repeat(data[:, None], 2, axis=1).tobytes()
    except ImportError:  # pure python fallback (slower, same numbers)
        vals = bytearray()
        down, up = 0.15, 0.5
        for i in range(n):
            tt = i / sr; g = g_gap
            for a, b in speech:
                if a - down <= tt < a: g = min(g, g_gap + (g_sp - g_gap) * (tt - (a - down)) / down)
                elif a <= tt <= b: g = g_sp
                elif b < tt <= b + up: g = min(g, g_sp + (g_gap - g_sp) * (tt - b) / up)
            g *= min(1.0, max(0.0, tt / MUSIC_FADE_IN), max(0.0, (total - tt) / MUSIC_FADE_OUT))
            s = int(max(0.0, min(1.0, g)) * 32767); vals += struct.pack("<hh", s, s)
        stereo = bytes(vals)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(stereo)


def main():
    if not FONT: sys.exit("Geist font not found in ~/Library/Fonts")
    segs, t, vo_events, slates = [], 0.0, [], []
    for i, seg in enumerate(SEGMENTS):
        p, slate = build_segment(seg, i); segs.append(p)
        if slate: slates.append(seg["name"])
        for name, off in seg.get("vo", []):
            wav = V/f"{name}.wav"
            if not wav.exists(): sys.exit(f"missing narration {wav}")
            vo_events.append((wav, max(0.0, t + off)))
        seg["start"] = t; t += seg["dur"]
    print(f"total video {t:.1f}s; slates: {slates or 'none'}")
    if t > 90.0 + 1e-6: sys.exit(f"total {t:.2f}s exceeds 90.0; shorten a row")
    lst = D/"_seg"/"list.txt"; lst.write_text("".join(f"file '{p}'\n" for p in segs))
    silent = D/"_seg"/"video_only.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent])
    # 1) narration: mix + loudnorm to -16 LUFS (as V2)
    inputs, fc, labels = [], [], []
    for i, (wav, at) in enumerate(vo_events):
        inputs += ["-i", wav]
        fc.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=mono,adelay={int(at*1000)}|{int(at*1000)}[a{i}]"); labels.append(f"[a{i}]")
    fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=duration={t:.3f},aformat=sample_rates=48000:channel_layouts=stereo[aout]")
    voice = D/"_seg"/"voice.wav"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "[aout]", "-c:a", "pcm_s16le", voice])
    # 2) the bed under a narration-keyed envelope
    bed = M/"bed.wav"
    if bed.exists():
        speech = sorted((at, at + wav_dur(wav)) for wav, at in vo_events)
        env = D/"_seg"/"envelope.wav"; envelope_wav(speech, t, env)
        music = D/"_seg"/"music.wav"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", bed, "-i", env, "-filter_complex",
             f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=duration={t:.3f},apad,atrim=duration={t:.3f}[b];"
             f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=duration={t:.3f}[e];[b][e]amultiply[m]", "-map", "[m]", "-c:a", "pcm_s16le", music])
        mix = f"[1:a][2:a]amix=inputs=2:normalize=0,alimiter=limit=0.89:level=false,atrim=duration={t:.3f}[final]"
        audio_in = ["-i", voice, "-i", music]
    else:
        print("no music/bed.wav: narration only (run music_bed.py)")
        mix = f"[1:a]atrim=duration={t:.3f}[final]"; audio_in = ["-i", voice]
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, *audio_in, "-filter_complex", mix,
         "-map", "0:v", "-map", "[final]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT])
    (D/"TIMING.md").write_text("| start | beat | dur | source | narration (offset) | captions |\n|---|---|---|---|---|---|\n" + "".join(
        f"| {s['start']:5.1f}s | {s['name']} | {s['dur']:.1f}s | {'SLATE' if s['name'] in slates else pathlib.Path(s['src']).name}{' x' + str(s['speed']) if s.get('speed') else ''} | "
        f"{', '.join(f'{n} @{o:+.1f}' for n,o in s.get('vo',[])) or '(silent)'} | {' / '.join(c[0] for c in s.get('caps',[])) or ''} |\n" for s in SEGMENTS)
        + f"\nTotal {t:.1f}s. Built by build_v3.py. Slates: {', '.join(slates) or 'none'}. Music: {'bed.wav, ' + str(DUCK_SPEECH) + ' dB under speech, ' + str(DUCK_GAP) + ' dB in gaps' if bed.exists() else 'none'}.\n"
        + f"Meet capture: captures/meet_v3.webm ss {MEET['beat_ss']} (page seconds when each block was visible: {json.dumps(mk)}).\n"
        + "Music: Kosmose Vaikus by Kevin MacLeod, incompetech.com, CC BY 4.0.\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
