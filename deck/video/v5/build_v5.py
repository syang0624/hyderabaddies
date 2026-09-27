#!/usr/bin/env python3
"""Stitch the Pik 90-second video, V5: the tightened front (animated beats sped up), the REAL Meet take recorded by Carl and Steven
inside a Google Meet (its own audio kept, music ducked under it, no narration over it), then the real Slack and Notion takes,
the verticals and the end card. One brand (the screen's tokens), V4's inputs by path.

Inputs: ../v2/renders/*.mp4 (animated beats + the two real takes with Pik on them), ../v3/renders/11_end.mp4, vo/*.wav (V5 re-cut
lines, see narrate_v5.py) with ../v3/vo as the fallback, ../v3/music/bed.wav, captures/meet_real.mov|.mp4 (the take; a 40 s
page-coloured slate stands in until it lands). Output: pik_90s_v5.mp4 (1920x1080, 30 fps, H.264 + AAC). Writes TIMING.md.

Run:  python3 deck/video/v5/build_v5.py                                  # slate in the Meet slot until the take exists
      python3 deck/video/v5/build_v5.py --take deck/video/v5/captures/meet_real.mov --in 2.5 --out 44.0 --marks 13.5,33.0
        --take   the recording (any size or aspect; scaled and padded to 1920x1080, audio kept); its duration is re-measured
        --in     first hello, seconds into the file (default 0)        --out   two seconds after the conclusion card (default: the end)
        --marks  caption 2 and 3 starts, seconds after --in: when Rin and Yui appear, and when the conclusion card prints
Fit rule: the total must be <= 90.0 s. If the take runs long, the front is trimmed in this order, each to a floor:
mining 7.0 -> 6.0, asked 6.0 -> 4.5, blur 3.5 -> 3.0, asks 4.0 -> 3.5, receipts 3.5 -> 3.0, verticals 4.0 -> 3.6; then it errors.
Animated beats are sped (frames dropped) to their new length; their captions are written in the render's own seconds and scaled.
Audio: narration mixed and loudnorm'd to -16 LUFS; the take's audio loudnorm'd on its own and placed at its start; the bed is
multiplied by an envelope keyed to every voice span (-26 dB under voice, -18 dB in gaps), then summed and limited.
"""
import subprocess, pathlib, glob, shlex, sys, json, wave, struct, argparse
D = pathlib.Path(__file__).resolve().parent
R2, R3 = D.parent / "v2" / "renders", D.parent / "v3" / "renders"
V5, V3 = D / "vo", D.parent / "v3" / "vo"
M, C = D.parent / "v3" / "music", D / "captures"
OUT = D / "pik_90s_v5.mp4"
FONT = next(iter(glob.glob(str(pathlib.Path.home()/"Library/Fonts/Geist-Medium.ttf")) + glob.glob(str(pathlib.Path.home()/"Library/Fonts/Geist-*.ttf"))), None)
MONO = next(iter(glob.glob(str(pathlib.Path.home()/"Library/Fonts/GeistMono-Regular.ttf"))), FONT)
W, H, FPS = 1920, 1080, 30
PAGE, INK, MUTE = (0xFA, 0xFA, 0xFA), (0x17, 0x17, 0x17), (0x88, 0x88, 0x88)  # the screen's tokens
DUCK_SPEECH, DUCK_GAP = -26.0, -18.0
MUSIC_FADE_IN, MUSIC_FADE_OUT = 2.0, 3.0
MAX_EXTRA_TEMPO = 1.15  # the most a narration line is sped beyond its wav to fit a trimmed beat
SLATE_TAKE = 40.0
TAKE_BUDGET = (38.0, 42.0)
FIT_ORDER = [("05_mining", 6.0), ("02_asked", 4.5), ("01_blur", 3.0), ("03_asks", 3.5), ("06_receipts", 3.0), ("10_verticals", 3.6)]


def find_take():
    for ext in ("mov", "mp4", "MOV", "MP4", "mkv", "webm"):
        p = C / f"meet_real.{ext}"
        if p.exists(): return p
    return None


def media_dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


def vo_path(name):
    for base in (V5, V3):
        if (base / f"{name}.wav").exists(): return base / f"{name}.wav"
    sys.exit(f"missing narration {name}.wav in {V5} or {V3}")


def segments(take, t_in, t_out, marks):
    """The edit. `src_len` = the render's own length (for the speed); caps of sped beats are in render seconds (scaled at build)."""
    take_dur = (t_out - t_in) if take else SLATE_TAKE
    m2, m3 = marks
    return [
     dict(name="00_disclosure", src=R2/"00_disclosure.mp4", dur=2.0),
     dict(name="01_blur",       src=R2/"01_blur.mp4",       dur=3.5, src_len=5.5, vo=[("01_blur", 0.1)]),
     dict(name="02_asked",      src=R2/"02_asked.mp4",      dur=6.0, src_len=8.4, vo=[("02_asked", 0.1)],
          caps_src=[("Team formation. Internal mobility. Decided from memory.", 0.9, 6.2)]),
     dict(name="03_asks",       src=R2/"03_asks.mp4",       dur=4.0, src_len=7.0, vo=[("03_asks", 0.1)],
          caps_src=[("Same question, every week.", 4.6, 7.0)]),
     dict(name="04_meetpik",    src=R2/"04_meetpik.mp4",    dur=3.2, src_len=4.2, vo=[("04_meetpik", 0.05)]),
     dict(name="05_mining",     src=R2/"05_mining.mp4",     dur=7.0, src_len=11.5, vo=[("05_mining", 0.3)],
          caps_src=[("It reads what she already did.", 0.8, 5.4), ("Every line keeps its source. DMs never.", 5.8, 11.3)]),
     dict(name="06_receipts",   src=R2/"06_receipts.mp4",   dur=3.5, src_len=4.5, vo=[("06_receipts", 0.1)],
          caps_src=[("Any size. Always current.", 2.4, 4.5)]),
     dict(name="07_meet",       src=take if take else C/"meet_real.mov", ss=t_in, dur=take_dur, take=bool(take),
          caps=[("Pik joined the call.", 0.5, 4.0),
                ("Two people with receipts for the ask. Word for word.", m2, m2 + 4.5),
                ("Filed. Both of them see the same page.", m3, max(m3 + 3.0, take_dur))]),
     dict(name="08_slack",      src=R2/"08_slack_real_pik.mp4", dur=7.6, vo=[("08_slack", 0.4)],
          caps=[("Ask where you already are. One press to loop her in.", 0.8, 7.4)]),
     dict(name="09_ticket",     src=R2/"09_notion_real_pik.mp4", dur=9.0, vo=[("09_ticket", 0.4)],
          caps=[("A new ticket. Pik fills in the owner, and the why.", 1.0, 8.8)]),
     dict(name="10_verticals",  src=R2/"10_verticals.mp4",  dur=4.0, src_len=7.0, vo=[("10_verticals", 0.1)],
          caps_src=[("Anywhere the wrong person on the job is expensive.", 3.4, 7.0)]),
     dict(name="11_end",        src=(R3/"11_end.mp4") if (R3/"11_end.mp4").exists() else R2/"11_end.mp4", dur=3.6, src_len=5.0, vo=[("11_end", 0.2)]),
    ]


def fit_to_90(segs):
    """Trim the front in FIT_ORDER until the total is <= 90.0 s. Loud about every cut; exits if it cannot."""
    total = sum(s["dur"] for s in segs)
    by = {s["name"]: s for s in segs}
    for name, floor in FIT_ORDER:
        if total <= 90.0 + 1e-6: break
        s = by[name]; cut = min(s["dur"] - floor, total - 90.0)
        if cut > 0:
            s["dur"] = round(s["dur"] - cut, 2); total -= cut; s["trimmed"] = round(cut, 2)
            print(f"fit: {name} trimmed by {cut:.2f}s to {s['dur']:.2f}s (floor {floor})")
    if total > 90.0 + 1e-6: sys.exit(f"total {total:.2f}s still exceeds 90.0 after every allowed trim; shorten the take (--in/--out)")
    return total


def run(cmd):
    print(" ".join(shlex.quote(str(c)) for c in cmd)[:300]); subprocess.run([str(c) for c in cmd], check=True)


def caption_png(text, path):
    """One caption as a transparent PNG (PIL): an ink pill (#171717 at 92%) with white text, Geist Medium 38, every beat alike."""
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(FONT, 38)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    x0, y0, x1, y1 = tmp.textbbox((0, 0), text, font=font)
    tw, th = x1 - x0, y1 - y0
    px, py = 30, 18
    im = Image.new("RGBA", (tw + 2*px, th + 2*py), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width-1, im.height-1), radius=14, fill=INK + (235,))
    d.text((px - x0, py - y0), text, font=font, fill=(255, 255, 255, 255))
    im.save(path); return im.height


def slate_png(name, path, note):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (W, H), PAGE); d = ImageDraw.Draw(im)
    f1, f2 = ImageFont.truetype(MONO, 64), ImageFont.truetype(MONO, 28)
    d.text((W/2, H/2 - 30), name, font=f1, fill=INK, anchor="mm")
    d.text((W/2, H/2 + 50), note, font=f2, fill=MUTE, anchor="mm")
    im.save(path)


def build_segment(seg, idx):
    out = D/"_seg"/f"{idx:02d}_{seg['name']}.mp4"; out.parent.mkdir(exist_ok=True)
    ss, dur = seg.get("ss", 0), seg["dur"]
    speed = (seg["src_len"] / dur) if seg.get("src_len") else 1.0
    if speed < 1.0: speed = 1.0  # never slow a beat down; the last frame holds instead
    seg["speed"] = round(speed, 3)
    src = pathlib.Path(seg["src"]); slate = not src.exists()
    if slate:
        png = out.parent / f"slate_{seg['name']}.png"; slate_png(seg["name"], png, f"slate, {dur:.0f} s: the real take lands here (captures/meet_real.mov)")
        inputs = ["-loop", "1", "-t", dur, "-i", png]
    else:
        inputs = ["-ss", ss, "-t", dur * speed + 1.0, "-i", src]
    fc = [f"[0:v]" + (f"setpts=PTS/{speed:.4f}," if speed != 1.0 else "") +
          f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,"
          f"tpad=stop_mode=clone:stop_duration={dur},format=rgb24[v0]"]
    caps = list(seg.get("caps", [])) + [(t, a / speed, b / speed) for t, a, b in seg.get("caps_src", [])]
    seg["caps_final"] = [(t, round(a, 2), round(min(b, dur), 2)) for t, a, b in caps]
    cur = "[v0]"
    for j, (text, a, b) in enumerate(seg["caps_final"]):
        png = out.parent / f"cap_{idx:02d}_{j}.png"; caption_png(text, png)
        inputs += ["-i", png]
        fc.append(f"{cur}[{1+j}:v]overlay=(W-w)/2:H-118-h:enable='between(t,{a},{b})'[c{j}]"); cur = f"[c{j}]"
    fc.append(f"{cur}trim=duration={dur},setpts=PTS-STARTPTS,format=yuv420p[vout]")
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-an",
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-r", FPS, out])
    return out, slate


def take_audio(seg):
    """The take's own sound, cut to [in, in+dur], loudnorm'd to -16 LUFS on its own, as a 48 kHz stereo wav."""
    wav = D/"_seg"/"take_audio.wav"
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", seg["ss"], "-t", seg["dur"], "-i", seg["src"], "-vn",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo", "-c:a", "pcm_s16le", wav])
    return wav


def envelope_wav(speech, total, path, sr=48000):
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
        data = (np.clip(env * fade, 0, 1) * 32767).astype("<i2")
        stereo = np.repeat(data[:, None], 2, axis=1).tobytes()
    except ImportError:
        vals = bytearray(); down, up = 0.15, 0.5
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--take", default=None, help="the real Meet recording (mov/mp4); default: captures/meet_real.* if present, else a slate")
    ap.add_argument("--in", dest="t_in", type=float, default=0.0, help="first hello, seconds into the take")
    ap.add_argument("--out", dest="t_out", type=float, default=None, help="two seconds after the conclusion card; default: the end of the file")
    ap.add_argument("--marks", default="15.5,36.0", help="caption 2 and 3 starts, seconds after --in (Rin and Yui appear; the conclusion prints)")
    a = ap.parse_args()
    if not FONT: sys.exit("Geist font not found in ~/Library/Fonts")
    take = pathlib.Path(a.take) if a.take else find_take()
    if take and not take.exists(): sys.exit(f"take not found: {take}")
    t_out = a.t_out
    if take:
        full = media_dur(take)
        if t_out is None or t_out > full: t_out = full
        print(f"take {take.name}: {full:.2f}s in the file, using {a.t_in:.2f}s to {t_out:.2f}s = {t_out - a.t_in:.2f}s")
        if not (TAKE_BUDGET[0] - 0.01 <= t_out - a.t_in <= TAKE_BUDGET[1] + 0.01):
            print(f"NOTE: the take is outside the {TAKE_BUDGET[0]:.0f}-{TAKE_BUDGET[1]:.0f} s budget; the front is trimmed to keep 90.0")
    else:
        print(f"no take yet: a {SLATE_TAKE:.0f} s slate stands in the Meet slot (drop the file at {C/'meet_real.mov'} or pass --take)")
    marks = tuple(float(x) for x in a.marks.split(","))
    segs = segments(take, a.t_in, t_out, marks)
    total = fit_to_90(segs)
    built, t, vo_events, slates, overruns = [], 0.0, [], [], []
    for i, seg in enumerate(segs):
        p, slate = build_segment(seg, i); built.append(p)
        if slate: slates.append(seg["name"])
        for name, off in seg.get("vo", []):
            wav = vo_path(name); d = media_dur(wav)
            room = seg["dur"] - off - 0.05
            if d > room:  # a line longer than its beat: up to 15% extra tempo, then it is an overrun to fix by hand (cut words)
                f = min(MAX_EXTRA_TEMPO, d / max(room, 0.3))
                fast = D/"_seg"/f"vo_{name}_x{f:.2f}.wav"; (D/"_seg").mkdir(exist_ok=True)
                run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", f"atempo={f:.3f}", fast]); wav = fast; d = media_dur(wav)
                print(f"narration {name}: {f:.2f}x extra tempo to fit {seg['name']} ({d:.2f}s in {room:.2f}s)")
            if d > room + 0.05: overruns.append(f"{name} ({d:.2f}s at +{off}) overruns {seg['name']} ({seg['dur']}s) by {off + d - seg['dur']:.2f}s")
            vo_events.append((wav, t + off, d))
        if seg.get("take") and not slate:
            wav = take_audio(seg); vo_events.append((wav, t, seg["dur"]))
        seg["start"] = t; t += seg["dur"]
    print(f"total video {t:.1f}s; slates: {slates or 'none'}")
    for o in overruns: print("WARNING narration:", o)
    lst = D/"_seg"/"list.txt"; lst.write_text("".join(f"file '{p}'\n" for p in built))
    silent = D/"_seg"/"video_only.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent])
    # 1) voices: narration (mono TTS) + the take's audio, each placed at its absolute start; loudnorm on the sum
    inputs, fc, labels = [], [], []
    for i, (wav, at, _) in enumerate(vo_events):
        inputs += ["-i", wav]
        fc.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(at*1000)}|{int(at*1000)}[a{i}]"); labels.append(f"[a{i}]")
    fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=duration={t:.3f},aformat=sample_rates=48000:channel_layouts=stereo[aout]")
    voice = D/"_seg"/"voice.wav"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "[aout]", "-c:a", "pcm_s16le", voice])
    # 2) the bed under an envelope keyed to every voice span (narration and the take alike)
    bed = M/"bed.wav"
    if bed.exists():
        speech = sorted((at, at + d) for _, at, d in vo_events)
        env = D/"_seg"/"envelope.wav"; envelope_wav(speech, t, env)
        music = D/"_seg"/"music.wav"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", bed, "-i", env, "-filter_complex",
             f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=duration={t:.3f},apad,atrim=duration={t:.3f}[b];"
             f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=duration={t:.3f}[e];[b][e]amultiply[m]", "-map", "[m]", "-c:a", "pcm_s16le", music])
        mix = f"[1:a][2:a]amix=inputs=2:normalize=0,alimiter=limit=0.89:level=false,atrim=duration={t:.3f}[final]"
        audio_in = ["-i", voice, "-i", music]
    else:
        print("no music/bed.wav: voices only"); mix = f"[1:a]atrim=duration={t:.3f}[final]"; audio_in = ["-i", voice]
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, *audio_in, "-filter_complex", mix,
         "-map", "0:v", "-map", "[final]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT])
    (D/"TIMING.md").write_text("| start | beat | dur | source | narration (offset) | captions |\n|---|---|---|---|---|---|\n" + "".join(
        f"| {s['start']:5.1f}s | {s['name']} | {s['dur']:.1f}s{' (trimmed ' + str(s['trimmed']) + ')' if s.get('trimmed') else ''} | "
        f"{'SLATE' if s['name'] in slates else pathlib.Path(s['src']).name}{' x' + str(s['speed']) if s.get('speed', 1) != 1 else ''}{' (own audio)' if s.get('take') and s['name'] not in slates else ''} | "
        f"{', '.join(f'{n} @{o:+.1f}' for n,o in s.get('vo',[])) or '(silent)'} | {' / '.join(f'{c[0]} [{c[1]}-{c[2]}]' for c in s.get('caps_final',[])) or ''} |\n" for s in segs)
        + f"\nTotal {t:.1f}s. Built by build_v5.py. Slates: {', '.join(slates) or 'none'}. "
        + (f"Take: {take.name} {a.t_in:.2f}-{t_out:.2f}s, caption marks {marks}. " if take else "Take: not yet (slate). ")
        + f"Music: bed.wav, {DUCK_SPEECH} dB under voice, {DUCK_GAP} dB in gaps. Narration overruns: {'; '.join(overruns) or 'none'}.\n"
        + "Music: Kosmose Vaikus by Kevin MacLeod, incompetech.com, CC BY 4.0.\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
