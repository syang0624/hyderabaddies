#!/usr/bin/env python3
"""Stitch the Pik 90-second video, V6: V5's structure and real Meet take, with Carl and Steven's V6 notes.

V6 over V5: an upbeat launch narrator (Puck, Gemini Live, narrate_v6.py, "Pick" in every TTS input), soft card entrances in
the html beats (fade, small rise, 0.98 -> 1, ~700 ms ease-out, ~120 ms stagger), the mining beat tightened 8.8 -> 7.6 s by
trimming holds, two push-ins on Pik's shared screen inside the Meet (when the two people land, when Rin's evidence shows:
1.0 -> 1.35 over 0.6 s, hold, ease back), the two human name labels on the Meet tiles blurred for the whole Meet (bridge
included), and a new end: "Tailor a task force to every task." with three people cards stacking, then V5's tagline.
Inputs: renders/ (V6 html beats, render.py), ../v2/renders (Meet Pik, the two real tail takes), vo/ (narrate_v6.py),
../v3/music/bed.wav, captures/meet_real.mp4 (1920x1240, 63 s). Output: <scratch>/pik_demo_90s_v6.mp4 (1920x1080, 30 fps, H.264 + AAC).
Writes TIMING.md with every start, offset and the visual event each narration line lands on.
Run: python3 build_v6.py [--recut]
"""
import subprocess, pathlib, glob, shlex, sys, wave, struct, argparse
D = pathlib.Path(__file__).resolve().parent
R6, R2 = D / "renders", D.parent / "v2" / "renders"
VO, M, C = D / "vo", D.parent / "v3" / "music", D / "captures"
SEG = D / "_seg"
OUT = D.parent.parent / "pik_demo_90s_v6.mp4"
FONT = next(iter(glob.glob(str(pathlib.Path.home()/"Library/Fonts/Geist-SemiBold.ttf")) + glob.glob(str(pathlib.Path.home()/"Library/Fonts/Geist-Medium.ttf"))), None)
MONO = next(iter(glob.glob(str(pathlib.Path.home()/"Library/Fonts/GeistMono-Regular.ttf"))), FONT)
W, H, FPS = 1920, 1080, 30
PAGE, INK, MUTE = (0xFA, 0xFA, 0xFA), (0x17, 0x17, 0x17), (0x88, 0x88, 0x88)
DUCK_SPEECH, DUCK_GAP = -26.0, -18.0
MUSIC_FADE_IN, MUSIC_FADE_OUT = 2.0, 3.0
XFADE = 0.3
TAKE_CROP = "crop=1920:1080:0:136"
PAGE_CROP = "crop=1350:754:34:274"
WINDOWS = [(9.30, 25.55), (29.55, 39.95), (42.45, 52.50), (54.50, 60.85)]
CONCL_FRAME = 60.2
# privacy (organiser notice): the two human name labels on the Meet tiles, in the cropped 1920x1080 frame (x, y, w, h).
# "Steven Yang" sits at ~1422-1562 x 605-640, "Carl Vincent Ladres Kho" at ~1422-1690 x 893-925 (measured on frames). "Pik" stays.
BLUR_BOXES = [(1414, 594, 200, 56), (1414, 880, 300, 56)]
# push-ins on the presented page (1352x758 at 34,137; centre 710,516), in take-core frames at 30 fps:
# A = "Two people have receipts for that..." lands at core 17.0 s, Pik reads it until ~23.3 s;
# B = "Rin wrote: I'll present the pricing analytics roadmap..." (Rin's evidence, the quote lit) lands at ~27.25 s, read until ~33.0 s.
ZOOM_Z, ZOOM_CX, ZOOM_CY, ZOOM_RAMP = 1.35, 710, 516, 18   # 18 frames = 0.6 s in, same out
ZOOMS = [(510, 708), (819, 1011)]
# narration tempo per line (atempo <= 1.1; Puck's natural pace is already brisk)
TEMPO = {"02a_asked": 1.10, "04_meetpik": 1.10, "04b_meetyui": 1.10, "10_taskforce": 1.10, "11_end": 1.10}
TEMPO_DEFAULT = 1.08


def run(cmd):
    print(" ".join(shlex.quote(str(c)) for c in cmd)[:260]); subprocess.run([str(c) for c in cmd], check=True)


def media_dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


def loudness(p, ss=None, dur=None):
    """Integrated loudness (LUFS) of a file or a slice of it, from ffmpeg's ebur128 summary."""
    cmd = ["ffmpeg", "-nostats"] + (["-ss", str(ss)] if ss is not None else []) + (["-t", str(dur)] if dur is not None else []) + ["-i", str(p), "-vn", "-af", "ebur128", "-f", "null", "-"]
    txt = subprocess.run(cmd, capture_output=True, text=True).stderr
    tail = txt[txt.rfind("Summary:"):]
    for line in tail.splitlines():
        if line.strip().startswith("I:"): return float(line.split()[1])
    sys.exit(f"no loudness for {p}")


LINE_LUFS = -16.0   # every narration line is brought to the same loudness (the Live model's takes vary by ~4 dB)


def vo_path(name):
    """The line at its tempo and a fixed loudness: vo/<name>.wav -> atempo -> static gain to LINE_LUFS -> _seg/vo6_<name>_x<rate>.wav (cached)."""
    src = VO / f"{name}.wav"
    if not src.exists(): sys.exit(f"missing narration {src} (run narrate_v6.py)")
    rate = TEMPO.get(name, TEMPO_DEFAULT)
    if rate > 1.1: sys.exit(f"{name}: atempo {rate} > 1.1")
    out = SEG / f"vo6n_{name}_x{rate:.2f}.wav"
    if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
        tmp = SEG / f"vo6t_{name}.wav"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", f"atempo={rate}", "-ar", "48000", "-ac", "1", tmp])
        gain = LINE_LUFS - loudness(tmp)
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-af", f"volume={gain:.2f}dB,alimiter=limit=0.89:level=false", "-ar", "48000", "-ac", "1", out])
        tmp.unlink()
    return out


def find_take():
    for ext in ("mp4", "mov", "MOV", "MP4", "mkv"):
        p = C / f"meet_real.{ext}"
        if p.exists(): return p
    return None


def blur_chain(inp, out):
    """filtergraph text: blur each BLUR_BOXES region of stream `inp` in place, output label `out`."""
    n = len(BLUR_BOXES); parts = [f"{inp}split={n + 1}[bb0]" + "".join(f"[bs{i}]" for i in range(n))]
    cur = "[bb0]"
    for i, (x, y, w, h) in enumerate(BLUR_BOXES):
        parts.append(f"[bs{i}]crop={w}:{h}:{x}:{y},boxblur=luma_radius=14:luma_power=3:chroma_radius=7:chroma_power=3[bz{i}]")
        nxt = out if i == n - 1 else f"[bo{i}]"
        parts.append(f"{cur}[bz{i}]overlay={x}:{y}{nxt}"); cur = nxt
    return ";".join(parts)


def title_png(text, path, size=96, scrim=0.55):
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


def cut_take(take, windows, recut):
    out = SEG / "take_core.mov"
    if out.exists() and not recut and abs(media_dur(out) - (sum(b - a for a, b in windows) - XFADE * (len(windows) - 1))) < 0.05:
        print(f"reusing {out.name} (pass --recut to rebuild)"); return out, media_dur(out)
    parts = []
    for i, (a, b) in enumerate(windows):
        p = SEG / f"take_part{i}.mov"
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", a, "-to", b, "-i", take, "-vf", f"{TAKE_CROP},fps={FPS},format=yuv420p",
             "-af", "aformat=sample_rates=48000:channel_layouts=stereo", "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-c:a", "pcm_s16le", p])
        parts.append((p, media_dur(p)))
    inputs = []; fc = []; vcur, acur = "[0:v]", "[0:a]"; t = parts[0][1]
    for p, _ in parts: inputs += ["-i", p]
    for i in range(1, len(parts)):
        fc.append(f"{vcur}[{i}:v]xfade=transition=fade:duration={XFADE}:offset={t - XFADE:.3f}[v{i}]")
        fc.append(f"{acur}[{i}:a]acrossfade=d={XFADE}[a{i}]")
        vcur, acur = f"[v{i}]", f"[a{i}]"; t += parts[i][1] - XFADE
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc), "-map", vcur, "-map", acur,
         "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-c:a", "pcm_s16le", out])
    return out, media_dur(out)


def meet_fx(core):
    """The take core with the name labels blurred throughout and the two push-ins on the presented page. Audio untouched."""
    out = SEG / "take_fx.mov"
    nfr = int(round(media_dur(core) * FPS))
    cuts = [0]; [cuts.extend(z) for z in ZOOMS]; cuts.append(nfr)
    pieces = len(cuts) - 1
    fc = [blur_chain("[0:v]", "[bl]"), f"[bl]split={pieces}" + "".join(f"[p{i}]" for i in range(pieces))]
    labels = []
    for i in range(pieces):
        a, b = cuts[i], cuts[i + 1]; chain = f"[p{i}]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS"
        if (a, b) in ZOOMS:
            n = b - a
            p = f"min(min(on/{ZOOM_RAMP},({n - 1}-on)/{ZOOM_RAMP}),1)"
            z = f"1+({ZOOM_Z}-1)*(1-cos(PI*{p}))/2"
            cx, cy = 2 * ZOOM_CX, 2 * ZOOM_CY
            chain += (f",scale={2 * W}:{2 * H}:flags=lanczos,zoompan=z='{z}':x='min(max({cx}-(iw/zoom)/2,0),iw-iw/zoom)':"
                      f"y='min(max({cy}-(ih/zoom)/2,0),ih-ih/zoom)':d=1:s={W}x{H}:fps={FPS},setpts=PTS-STARTPTS")
        chain += f",setsar=1,format=yuv420p[q{i}]"; fc.append(chain); labels.append(f"[q{i}]")
    fc.append("".join(labels) + f"concat=n={pieces}:v=1:a=0[v]")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", core, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "0:a",
         "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-r", FPS, "-c:a", "pcm_s16le", out])
    got = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                              "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip() or 0)
    if got != nfr: sys.exit(f"meet_fx: {got} frames out, expected {nfr}")
    return out


def bridge_clip(core, dur=1.0):
    """The Meet's first frame (take core frame 0, labels blurred) held under a scrim with one large line. V5 used the recording's
    first second, where the macOS Dock is still on screen; the core's first frame is clean and the Meet then starts from it."""
    png = SEG / "bridge_title.png"; title_png("Pik joins the call.", png)
    out = SEG / "bridge.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", core, "-i", png, "-filter_complex",
         f"[0:v]trim=end_frame=1,setpts=PTS-STARTPTS,fps={FPS}[c0];" + blur_chain("[c0]", "[b0]") + f";[b0]tpad=stop_mode=clone:stop_duration={dur},trim=duration={dur}[b];"
         "[b][1:v]overlay=0:0,format=yuv420p[v]", "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "16", "-r", FPS, out])
    return out


def conclusion_clip(take, dur):
    out = SEG / "conclusion.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", CONCL_FRAME, "-i", take, "-frames:v", "1", "-vf", f"{PAGE_CROP},scale={W}:1072:flags=lanczos,pad={W}:{H}:0:4:color=white", SEG / "conclusion.png"])
    run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", dur, "-i", SEG / "conclusion.png", "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-crf", "16", out])
    return out


def zoom_filter(z, cx, cy, secs):
    n = int(secs * FPS)
    return (f"zoompan=z='1+({z}-1)*(1-cos(PI*min(on/{n},1)))/2':"
            f"x='min(max({cx}-(iw/zoom)/2,0),iw-iw/zoom)':y='min(max({cy}-(ih/zoom)/2,0),ih-ih/zoom)':d=1:s={W}x{H}:fps={FPS}")


CONCL_DUR = 0.8


def segments(fx, core_len):
    za, zb = [(a / FPS, b / FPS) for a, b in ZOOMS]
    return [
     dict(name="01_blur",      src=R6/"01_blur.mp4",      dur=98 / FPS, vo=[("01_blur", 0.92)], note="headline 'The line between roles is blurring.' reveals at 2.25 s; 'blurring' lands at ~2.6 to 3.1 s"),
     dict(name="02_asked",     src=R6/"02_asked.mp4",     dur=7.4, vo=[("02a_asked", 0.1), ("02b_team", 2.6), ("02c_decided", 4.0)],
          note="RECRUIT HOLDINGS reveals 0.25 to 0.85 s under 'We asked people at Recruit Holdings'; 'Team formation.' pops at 2.5, said at 2.6; the three quote cards arrive softly together at 3.70/3.82/3.94 (700 ms ease-out, 0.98 -> 1, 24 px rise) and type in turn from 3.95/4.55/5.15; they stack from 6.3; 'Decided from memory.' reveals at 6.45 as the narrator reaches it"),
     dict(name="04_meetpik",   src=R2/"04_meetpik.mp4",   dur=130 / FPS, vo=[("04_meetpik", 0.08)], note="'Meet Pik.' reveals at 0.76 s on the words; the tagline lines at 1.35 and 1.45"),
     dict(name="04b_meetyui",  src=R6/"04b_meetyui.mp4",  dur=3.8, vo=[("04b_meetyui", 0.15)], note="disc and 'Meet Yui.' arrive softly at 0 and 0.12 s; 'Pik lives where she works.' at 1.75 as the narrator reaches it; 'her Slack · her email' at 1.87"),
     dict(name="05_mining",    src=R6/"05_mining.mp4",    dur=7.6, vo=[("05_mining", 0.4)],
          note="tightened from 8.8 s (holds trimmed, no speed-up): 'Her Slack' at 0.25, vacuum 1.0 to 2.9, 'Oh. She took the partner review herself.' typed at 2.9, held to 4.25; 'Her email' at 4.35, vacuum 4.85 to 6.25, surprise typed at 6.2, held to 7.6"),
     dict(name="06_receipts",  src=R6/"06_receipts.mp4",  dur=2.4, vo=[("06_receipts", 0.25)], note="the eight stubs arrive softly, 120 ms apart (0.04 to 1.6 s); one pulse at 1.35; the two unsourced fall away from 1.6"),
     dict(name="07a_bridge",   src=SEG/"bridge.mp4",      dur=1.0, note="the Meet's first frame held under a scrim: 'Pik joins the call.' (name labels blurred; V5's bridge showed the macOS Dock)"),
     dict(name="07_meet",      src=fx, dur=round(core_len, 2), take=True,
          note="the real take, own sound; windows " + ", ".join(f"{a:.2f}-{b:.2f}" for a, b in WINDOWS) + f" s of tape, 0.3 s dissolves; both human name labels blurred throughout; push-in A {za[0]:.2f}-{za[1]:.2f} s (answer 'Two people have receipts for that...'), push-in B {zb[0]:.2f}-{zb[1]:.2f} s (Rin's evidence), each 1.0 -> {ZOOM_Z} over 0.6 s, held, eased back over 0.6 s"),
     dict(name="07b_concl",    src=SEG/"conclusion.mp4",  dur=CONCL_DUR, note="the conclusion card, the presented page scaled up, still"),
     dict(name="08_slack",     src=R2/"08_slack_real_pik.mp4", ss=0.8, dur=6.2, vo=[("08_slack", 0.3)], zoom=(1.45, 1130, 720, 3.0),
          note="the whole window, then a 3 s push-in to the composer and the card; the card lands at ~2.2 s, Loop in at ~5.7 s"),
     dict(name="09_ticket",    src=R2/"09_notion_real_pik.mp4", ss=1.4, dur=4.3, vo=[("09_ticket", 0.2)], zoom=(1.5, 960, 720, 2.5),
          note="the board, then a 2.5 s push-in to the row that fills (owner, why, receipts) at ~2.6 to 3.6 s; held"),
     dict(name="11_end",       src=R6/"11_end.mp4",       dur=6.6, vo=[("10_taskforce", 0.05), ("11_end", 2.8)],
          note="'Tailor a task force / to every task.' arrives softly at 0.12/0.24 as it is said; three people cards (Rin Mori, Yui Sato, Yuto Murakami) arrive 120 ms apart from 0.52 and settle into a fanned stack 1.5 to 2.2; phase fades up and out 2.55 to 2.93; the V5 tagline reveals at 3.0/3.09 under 'Because the future of your work depends on who you Pick' (said from 2.8, a 0.3 s breath after the task-force line); 'Pik' on the lime highlight; the bot at 3.4; the credit at 4.3"),
    ]


def build_segment(seg, idx):
    out = SEG / f"v6_{idx:02d}_{seg['name']}.mp4"
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
    """The music gain envelope (ducked under every voice, fades in/out), computed per 10 ms block (no numpy needed)."""
    import array
    g_gap, g_sp = 10 ** (DUCK_GAP / 20), 10 ** (DUCK_SPEECH / 20); down, up = 0.15, 0.5
    blk = sr // 100; nb = int(total * 100) + 1
    out = array.array("h")
    for k in range(nb):
        tt = (k + 0.5) / 100; g = g_gap
        for a, b in speech:
            if a - down <= tt < a: g = min(g, g_gap + (g_sp - g_gap) * (tt - (a - down)) / down)
            elif a <= tt <= b: g = g_sp
            elif b < tt <= b + up: g = min(g, g_sp + (g_gap - g_sp) * (tt - b) / up)
        g *= min(1.0, max(0.0, tt / MUSIC_FADE_IN), max(0.0, (total - tt) / MUSIC_FADE_OUT))
        v = int(max(0.0, min(1.0, g)) * 32767); out.extend([v, v] * blk)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(out.tobytes())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--recut", action="store_true", help="re-cut the take core from the recording")
    a = ap.parse_args()
    if not FONT: sys.exit("Geist font not found in ~/Library/Fonts")
    SEG.mkdir(exist_ok=True)
    take = find_take()
    if not take or not take.exists(): sys.exit("the take is missing: captures/meet_real.mp4")
    full = media_dur(take); print(f"take {take.name}: {full:.2f}s; kept windows {WINDOWS}")
    core, core_len = cut_take(take, WINDOWS, a.recut); print(f"take core {core_len:.2f}s after cuts")
    fx = meet_fx(core); bridge_clip(core); conclusion_clip(take, CONCL_DUR)
    segs = segments(fx, core_len)
    total = sum(s["dur"] for s in segs)
    frames = sum(round(s["dur"] * FPS) for s in segs)
    if total > 90.0 + 1e-6 or frames > 90 * FPS: sys.exit(f"total {total:.3f}s / {frames} frames exceeds 90.0 s")
    built, t, vo_events, slates, overruns = [], 0.0, [], [], []
    for i, seg in enumerate(segs):
        p, slate = build_segment(seg, i); built.append(p)
        if slate: slates.append(seg["name"])
        for name, off in seg.get("vo", []):
            wav = vo_path(name); d = media_dur(wav)
            if off + d > seg["dur"] + 0.02: overruns.append(f"{name} ({d:.2f}s at +{off}) overruns {seg['name']} ({seg['dur']}s) by {off + d - seg['dur']:.2f}s")
            vo_events.append((wav, t + off, d))
        if seg.get("take"):
            vo_events.append((take_audio(core, seg["dur"]), t, seg["dur"]))
        seg["start"] = t; t += seg["dur"]
    print(f"total video {t:.2f}s; slates: {slates or 'none'}")
    for o in overruns: print("WARNING narration:", o)
    if slates: sys.exit(f"slates in the cut: {slates}")
    lst = SEG / "list_v6.txt"; lst.write_text("".join(f"file '{p}'\n" for p in built))
    silent = SEG / "video_only_v6.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent])
    inputs, fc, labels = [], [], []
    for i, (wav, at, _) in enumerate(vo_events):
        inputs += ["-i", wav]
        fc.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(at*1000)}|{int(at*1000)}[a{i}]"); labels.append(f"[a{i}]")
    fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,apad,atrim=duration={t:.3f},aformat=sample_rates=48000:channel_layouts=stereo[aout]")
    voice = SEG / "voice_v6.wav"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "[aout]", "-c:a", "pcm_s16le", voice])
    bed = M / "bed.wav"
    if not bed.exists(): sys.exit("music bed missing: ../v3/music/bed.wav")
    speech = sorted((at, at + d) for _, at, d in vo_events)
    env = SEG / "envelope_v6.wav"; envelope_wav(speech, t, env); music = SEG / "music_v6.wav"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", bed, "-i", env, "-filter_complex",
         f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=duration={t:.3f},apad,atrim=duration={t:.3f}[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=duration={t:.3f}[e];[b][e]amultiply[m]",
         "-map", "[m]", "-c:a", "pcm_s16le", music])
    gain = 0.0
    for attempt in range(3):   # static trim to about -16 LUFS integrated (measured, then corrected once or twice)
        mix = f"[1:a][2:a]amix=inputs=2:normalize=0,volume={gain:.2f}dB,alimiter=limit=0.89:level=false,atrim=duration={t:.3f}[final]"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", voice, "-i", music, "-filter_complex", mix, "-map", "0:v", "-map", "[final]",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{t:.3f}", "-movflags", "+faststart", OUT])
        got = loudness(OUT); print(f"integrated loudness {got:.1f} LUFS at trim {gain:+.2f} dB")
        if abs(got + 16.0) <= 0.3: break
        gain += -16.0 - got
    (D / "TIMING.md").write_text("| start | beat | dur | source | narration (offset, length after tempo) | what the eye sees, and where the words land |\n|---|---|---|---|---|---|\n" + "".join(
        f"| {s['start']:5.2f}s | {s['name']} | {s['dur']:.2f}s | {pathlib.Path(s['src']).name}{' ss ' + str(s['ss']) if s.get('ss') else ''}{' (own audio)' if s.get('take') else ''}{' push-in' if s.get('zoom') else ''} | "
        f"{', '.join(f'{n} @+{o} ({media_dur(vo_path(n)):.2f}s, x{TEMPO.get(n, TEMPO_DEFAULT):.2f})' for n, o in s.get('vo', [])) or '(no narration)'} | {s.get('note', '')} |\n" for s in segs)
        + f"\nTotal {t:.2f}s. Built by build_v6.py. Narrator: Puck (Gemini Live on Vertex, narrate_v6.py), \"Pick\" in every TTS input; atempo {TEMPO_DEFAULT} default, 1.10 on 02a_asked, 04_meetpik, 04b_meetyui, 10_taskforce, 11_end. "
        + f"Take: {take.name} ({full:.1f}s), kept {', '.join(f'{a:.2f}-{b:.2f}' for a, b in WINDOWS)} = {core_len:.2f}s after {XFADE}s dissolves; crop {TAKE_CROP}; "
        + f"name labels blurred (boxblur r14 x3) at {BLUR_BOXES} for the whole Meet and the bridge; push-ins at core frames {ZOOMS} (z {ZOOM_Z}, centre {ZOOM_CX},{ZOOM_CY}); conclusion still at {CONCL_FRAME}s ({PAGE_CROP}). "
        + f"Music: bed.wav, {DUCK_SPEECH} dB under voice, {DUCK_GAP} dB in gaps. Narration overruns: {'; '.join(overruns) or 'none'}.\n"
        + "Music: Kosmose Vaikus by Kevin MacLeod, incompetech.com, CC BY 4.0.\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
