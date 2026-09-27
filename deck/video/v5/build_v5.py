#!/usr/bin/env python3
"""Stitch the Pik 90-second video, V5: Carl's cut around the real Meet take.

Front (calm, no speed-ups, narration at 1.15x): the blur, "We asked people at RECRUIT HOLDINGS" -> "Team formation." -> the three
quotes -> "Decided from memory.", Meet Pik, Meet Yui, her Slack and her email with the two surprise lines, the receipts pulse.
Middle: a 1 s bridge ("Pik joins the call." over the first frames of the recording), the real take (Carl and Steven in a Google
Meet, its own sound kept, dead air cut with 0.3 s cross-dissolves, cropped to the Meet under Dia's tab strip), then the
conclusion page held for 2 s. Tail: the real Slack take with a slow push-in to the composer and the card, the real Notion take
with a push-in to the row that fills, the end card (headline + credit). No caption pills anywhere; every word is in the beat's
own type. Music under everything, ducked under any voice.

Inputs: renders/ (V5 html beats, render.py), ../v2/renders (Meet Pik, the two real tail takes), vo/ (narrate_v5.py, 1.15x),
../v3/music/bed.wav, captures/meet_real.mp4 (1920x1240, 63 s). Output: pik_90s_v5.mp4 (1920x1080, 30 fps, H.264 + AAC).
Writes TIMING.md with every start, offset and the visual event each narration line lands on.
Run: python3 deck/video/v5/build_v5.py [--take PATH] [--windows "9.30-25.55,29.55-39.95,42.45-52.50,54.50-60.85"]
"""
import subprocess, pathlib, glob, shlex, sys, json, wave, struct, argparse
D = pathlib.Path(__file__).resolve().parent
R5, R2 = D / "renders", D.parent / "v2" / "renders"
V5, M, C = D / "vo", D.parent / "v3" / "music", D / "captures"
SEG = D / "_seg"
OUT = D / "pik_90s_v5.mp4"
FONT = next(iter(glob.glob(str(pathlib.Path.home()/"Library/Fonts/Geist-SemiBold.ttf")) + glob.glob(str(pathlib.Path.home()/"Library/Fonts/Geist-Medium.ttf"))), None)
MONO = next(iter(glob.glob(str(pathlib.Path.home()/"Library/Fonts/GeistMono-Regular.ttf"))), FONT)
W, H, FPS = 1920, 1080, 30
PAGE, INK, MUTE = (0xFA, 0xFA, 0xFA), (0x17, 0x17, 0x17), (0x88, 0x88, 0x88)
DUCK_SPEECH, DUCK_GAP = -26.0, -18.0
MUSIC_FADE_IN, MUSIC_FADE_OUT = 2.0, 3.0
XFADE = 0.3
# the recording: the macOS menu bar and Dia's tab strip are the top 136 px; the Meet fills the rest
TAKE_CROP = "crop=1920:1080:0:136"
PAGE_CROP = "crop=1350:754:34:274"   # the presented Pik page inside the recording (measured on frames)
# dead air cut from the take (tape seconds kept): hellos + Pik's first line + Steven's ask | Pik's second line + Carl's question |
# Pik reads Rin's receipt + Steven's "let's ask them" | Pik files it + "Thanks, Pik." About 0.7 s of air before each Pik line.
WINDOWS = [(9.30, 25.55), (29.55, 39.95), (42.45, 52.50), (54.50, 60.85)]
CONCL_FRAME = 60.2  # the conclusion card, printed and still


def run(cmd):
    print(" ".join(shlex.quote(str(c)) for c in cmd)[:260]); subprocess.run([str(c) for c in cmd], check=True)


def media_dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


def vo_path(name):
    p = V5 / f"{name}.wav"
    if not p.exists(): sys.exit(f"missing narration {p} (run narrate_v5.py)")
    return p


def find_take():
    for ext in ("mp4", "mov", "MOV", "MP4", "mkv"):
        p = C / f"meet_real.{ext}"
        if p.exists(): return p
    return None


def title_png(text, path, size=96, scrim=0.55):
    """A full-frame PNG: a scrim of ink over the scene and one large white line, centred (the bridge into the Meet)."""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGBA", (W, H), INK + (int(255 * scrim),))
    d = ImageDraw.Draw(im); font = ImageFont.truetype(FONT, size)
    d.text((W / 2, H / 2), text, font=font, fill=(255, 255, 255, 255), anchor="mm")
    im.save(path)


def slate_png(name, path, note):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (W, H), PAGE); d = ImageDraw.Draw(im)
    f1, f2 = ImageFont.truetype(MONO, 64), ImageFont.truetype(MONO, 28)
    d.text((W/2, H/2 - 30), name, font=f1, fill=INK, anchor="mm"); d.text((W/2, H/2 + 50), note, font=f2, fill=MUTE, anchor="mm")
    im.save(path)


def cut_take(take, windows):
    """The take, cropped to the Meet, dead air removed: the kept windows joined with 0.3 s video and audio cross-dissolves."""
    parts = []
    for i, (a, b) in enumerate(windows):
        p = SEG / f"take_part{i}.mov"
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", a, "-to", b, "-i", take, "-vf", f"{TAKE_CROP},fps={FPS},format=yuv420p",
             "-af", "aformat=sample_rates=48000:channel_layouts=stereo", "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-c:a", "pcm_s16le", p])
        parts.append((p, media_dur(p)))
    if len(parts) == 1:
        return parts[0][0], parts[0][1]
    inputs = []; fc = []; vcur, acur = "[0:v]", "[0:a]"; t = parts[0][1]
    for p, _ in parts: inputs += ["-i", p]
    for i in range(1, len(parts)):
        fc.append(f"{vcur}[{i}:v]xfade=transition=fade:duration={XFADE}:offset={t - XFADE:.3f}[v{i}]")
        fc.append(f"{acur}[{i}:a]acrossfade=d={XFADE}[a{i}]")
        vcur, acur = f"[v{i}]", f"[a{i}]"; t += parts[i][1] - XFADE
    out = SEG / "take_core.mov"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc), "-map", vcur, "-map", acur,
         "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-c:a", "pcm_s16le", out])
    return out, media_dur(out)


def bridge_clip(take, dur=1.0):
    """The first second of the recording (Pik presenting, before the hellos) under a scrim with one large line."""
    png = SEG / "bridge_title.png"; title_png("Pik joins the call.", png)
    out = SEG / "bridge.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", 0.2, "-t", dur, "-i", take, "-i", png, "-filter_complex",
         f"[0:v]{TAKE_CROP},fps={FPS}[b];[b][1:v]overlay=0:0,format=yuv420p[v]", "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "16", out])
    return out


def conclusion_clip(take, dur=2.0):
    """The presented page itself, big: the conclusion card as the story leaves the call (a still from the take's last frames)."""
    out = SEG / "conclusion.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", CONCL_FRAME, "-i", take, "-frames:v", "1", "-vf", f"{PAGE_CROP},scale={W}:1072:flags=lanczos,pad={W}:{H}:0:4:color=white", SEG / "conclusion.png"])
    run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", dur, "-i", SEG / "conclusion.png", "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-crf", "16", out])
    return out


def zoom_filter(z, cx, cy, secs):
    """A slow push-in (Ken Burns): zoom 1 -> z over `secs`, eased, centred on (cx, cy) of the 1920x1080 frame, then held."""
    n = int(secs * FPS)
    return (f"zoompan=z='1+({z}-1)*(1-cos(PI*min(on/{n},1)))/2':"
            f"x='min(max({cx}-(iw/zoom)/2,0),iw-iw/zoom)':y='min(max({cy}-(ih/zoom)/2,0),ih-ih/zoom)':d=1:s={W}x{H}:fps={FPS}")


def segments(take, core, core_len):
    return [
     dict(name="01_blur",      src=R5/"01_blur.mp4",      dur=3.4, vo=[("01_blur", 1.0)],      note="headline 'The line between roles is blurring.' reveals at 2.25 s; 'blurring' is said at ~2.6 to 3.1 s"),
     dict(name="02_asked",     src=R5/"02_asked.mp4",     dur=7.6, vo=[("02a_asked", 0.15), ("02b_team", 2.5), ("02c_decided", 3.9)],
          note="RECRUIT HOLDINGS reveals 0.25 to 0.85 s under 'We asked people at Recruit Holdings' (0.15 to 2.0); 'Team formation.' pops at 2.5 as it is said; the cards type 3.7 to 6.4; 'Decided from memory.' reveals at 6.45 as the narrator reaches it (~6.3 to 7.6)"),
     dict(name="04_meetpik",   src=R2/"04_meetpik.mp4",   dur=4.3, vo=[("04_meetpik", 0.1)],   note="'Meet Pik.' reveals at 0.76 s on the words; the tagline lines at 1.35 and 1.45"),
     dict(name="04b_meetyui",  src=R5/"04b_meetyui.mp4",  dur=3.6, vo=[("04b_meetyui", 0.2)], note="'Meet Yui.' at 0.25; 'Pik lives where she works.' at 1.9 as the narrator says it; 'her Slack · her email' at 2.6"),
     dict(name="05_mining",    src=R5/"05_mining.mp4",    dur=8.8, vo=[("05_mining", 0.4)],    note="'Her Slack' title at 0.25, the replica legible until the vacuum at 1.2 to 2.85, surprise 'Oh. She took the partner review herself.' typed at 3.1, held to 4.9; 'Her email' at 5.0, vacuum 5.9 to 7.0, surprise typed at 7.3, held to 8.8"),
     dict(name="06_receipts",  src=R5/"06_receipts.mp4",  dur=2.4, vo=[("06_receipts", 0.3)],  note="stubs gather 0.1 to 1.1, one pulse at 1.15, the two unsourced fade and drop from 1.4"),
     dict(name="07a_bridge",   src=SEG/"bridge.mp4",      dur=1.0, note="the recording's first second under a scrim: 'Pik joins the call.'"),
     dict(name="07_meet",      src=core, dur=round(core_len, 2), take=True, note="the real take, own sound; windows " + ", ".join(f"{a:.2f}-{b:.2f}" for a, b in WINDOWS) + " s of tape, 0.3 s dissolves between them"),
     dict(name="07b_concl",    src=SEG/"conclusion.mp4",  dur=2.0, note="the conclusion card, the presented page scaled up, still"),
     dict(name="08_slack",     src=R2/"08_slack_real_pik.mp4", ss=0.8, dur=6.2, vo=[("08_slack", 0.3)], zoom=(1.45, 1130, 720, 3.0),
          note="the whole window, then a 3 s push-in to the composer and the card; the card lands at ~2.2 s, Loop in at ~5.7 s"),
     dict(name="09_ticket",    src=R2/"09_notion_real_pik.mp4", ss=1.4, dur=5.0, vo=[("09_ticket", 0.2)], zoom=(1.5, 960, 720, 2.5),
          note="the board, then a 2.5 s push-in to the row that fills (owner, why, receipts) at ~2.6 to 3.6 s; held"),
     dict(name="11_end",       src=R5/"11_end.mp4",       dur=3.4, vo=[("11_end", 0.1)],       note="headline reveals at 0.3/0.39; 'Pik' on the lime highlight; the credit at 2.0"),
    ]


def build_segment(seg, idx):
    out = SEG / f"{idx:02d}_{seg['name']}.mp4"
    ss, dur = seg.get("ss", 0), seg["dur"]
    src = pathlib.Path(seg["src"]); slate = not src.exists()
    if slate:
        png = SEG / f"slate_{seg['name']}.png"; slate_png(seg["name"], png, f"slate, {dur:.1f} s")
        inputs = ["-loop", "1", "-t", dur, "-i", png]
    else:
        inputs = ["-ss", ss, "-t", dur + 1.0, "-i", src]
    vf = f"[0:v]fps={FPS},scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2"
    if seg.get("zoom"):
        z, cx, cy, secs = seg["zoom"]; vf += "," + zoom_filter(z, cx, cy, secs)
    vf += f",tpad=stop_mode=clone:stop_duration={dur},trim=duration={dur},setpts=PTS-STARTPTS,format=yuv420p[vout]"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", vf, "-map", "[vout]", "-an",
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-r", FPS, out])
    return out, slate


def take_audio(core, dur):
    wav = SEG / "take_audio.wav"
    run(["ffmpeg", "-y", "-loglevel", "error", "-t", dur, "-i", core, "-vn", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo", "-c:a", "pcm_s16le", wav])
    return wav


def envelope_wav(speech, total, path, sr=48000):
    n = int(total * sr) + 1
    g_gap, g_sp = 10 ** (DUCK_GAP / 20), 10 ** (DUCK_SPEECH / 20)
    try:
        import numpy as np
        t = np.arange(n) / sr; env = np.full(n, g_gap); down, up = 0.15, 0.5
        for a, b in speech:
            i0, i1 = int(max(0, a - down) * sr), int(min(total, b + up) * sr); seg_t = t[i0:i1]
            g = np.where(seg_t < a, g_gap + (g_sp - g_gap) * np.clip((seg_t - (a - down)) / down, 0, 1),
                         np.where(seg_t <= b, g_sp, g_sp + (g_gap - g_sp) * np.clip((seg_t - b) / up, 0, 1)))
            env[i0:i1] = np.minimum(env[i0:i1], g)
        fade = np.minimum(np.clip(t / MUSIC_FADE_IN, 0, 1), np.clip((total - t) / MUSIC_FADE_OUT, 0, 1))
        data = (np.clip(env * fade, 0, 1) * 32767).astype("<i2"); stereo = np.repeat(data[:, None], 2, axis=1).tobytes()
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
    ap.add_argument("--take", default=None); ap.add_argument("--windows", default=None, help='kept tape windows "a-b,c-d,..."')
    a = ap.parse_args()
    if not FONT: sys.exit("Geist font not found in ~/Library/Fonts")
    SEG.mkdir(exist_ok=True)
    take = pathlib.Path(a.take) if a.take else find_take()
    if not take or not take.exists(): sys.exit("the take is missing: deck/video/v5/captures/meet_real.mp4")
    windows = [tuple(float(x) for x in w.split("-")) for w in a.windows.split(",")] if a.windows else WINDOWS
    full = media_dur(take); print(f"take {take.name}: {full:.2f}s; kept windows {windows}")
    core, core_len = cut_take(take, windows); print(f"take core {core_len:.2f}s after cuts")
    bridge_clip(take); conclusion_clip(take)
    segs = segments(take, core, core_len)
    total = sum(s["dur"] for s in segs)
    if total > 90.0 + 1e-6: sys.exit(f"total {total:.2f}s exceeds 90.0: tighten the windows or a beat")
    built, t, vo_events, slates, overruns = [], 0.0, [], [], []
    for i, seg in enumerate(segs):
        p, slate = build_segment(seg, i); built.append(p)
        if slate: slates.append(seg["name"])
        for name, off in seg.get("vo", []):
            wav = vo_path(name); d = media_dur(wav)
            if off + d > seg["dur"] + 0.05: overruns.append(f"{name} ({d:.2f}s at +{off}) overruns {seg['name']} ({seg['dur']}s) by {off + d - seg['dur']:.2f}s")
            vo_events.append((wav, t + off, d))
        if seg.get("take"):
            vo_events.append((take_audio(seg["src"], seg["dur"]), t, seg["dur"]))
        seg["start"] = t; t += seg["dur"]
    print(f"total video {t:.2f}s; slates: {slates or 'none'}")
    for o in overruns: print("WARNING narration:", o)
    lst = SEG / "list.txt"; lst.write_text("".join(f"file '{p}'\n" for p in built))
    silent = SEG / "video_only.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent])
    inputs, fc, labels = [], [], []
    for i, (wav, at, _) in enumerate(vo_events):
        inputs += ["-i", wav]
        fc.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(at*1000)}|{int(at*1000)}[a{i}]"); labels.append(f"[a{i}]")
    fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=duration={t:.3f},aformat=sample_rates=48000:channel_layouts=stereo[aout]")
    voice = SEG / "voice.wav"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "[aout]", "-c:a", "pcm_s16le", voice])
    bed = M / "bed.wav"
    if bed.exists():
        speech = sorted((at, at + d) for _, at, d in vo_events)
        env = SEG / "envelope.wav"; envelope_wav(speech, t, env); music = SEG / "music.wav"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", bed, "-i", env, "-filter_complex",
             f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=duration={t:.3f},apad,atrim=duration={t:.3f}[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=duration={t:.3f}[e];[b][e]amultiply[m]",
             "-map", "[m]", "-c:a", "pcm_s16le", music])
        mix = f"[1:a][2:a]amix=inputs=2:normalize=0,alimiter=limit=0.89:level=false,atrim=duration={t:.3f}[final]"; audio_in = ["-i", voice, "-i", music]
    else:
        print("no music/bed.wav: voices only"); mix = f"[1:a]atrim=duration={t:.3f}[final]"; audio_in = ["-i", voice]
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, *audio_in, "-filter_complex", mix, "-map", "0:v", "-map", "[final]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT])
    (D / "TIMING.md").write_text("| start | beat | dur | source | narration (offset, length) | what the eye sees, and where the words land |\n|---|---|---|---|---|---|\n" + "".join(
        f"| {s['start']:5.1f}s | {s['name']} | {s['dur']:.1f}s | {'SLATE' if s['name'] in slates else pathlib.Path(s['src']).name}{' ss ' + str(s['ss']) if s.get('ss') else ''}{' (own audio)' if s.get('take') else ''}{' push-in' if s.get('zoom') else ''} | "
        f"{', '.join(f'{n} @+{o} ({media_dur(vo_path(n)):.2f}s)' for n, o in s.get('vo', [])) or '(no narration)'} | {s.get('note', '')} |\n" for s in segs)
        + f"\nTotal {t:.2f}s. Built by build_v5.py. No caption pills. Take: {take.name} ({full:.1f}s), kept {', '.join(f'{a:.2f}-{b:.2f}' for a, b in windows)} = {core_len:.2f}s after {XFADE}s dissolves; crop {TAKE_CROP}; conclusion still at {CONCL_FRAME}s ({PAGE_CROP}). "
        + f"Music: bed.wav, {DUCK_SPEECH} dB under voice, {DUCK_GAP} dB in gaps. Narration overruns: {'; '.join(overruns) or 'none'}.\n"
        + "Music: Kosmose Vaikus by Kevin MacLeod, incompetech.com, CC BY 4.0.\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
