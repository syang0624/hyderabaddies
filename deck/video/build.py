#!/usr/bin/env python3
"""Stitch the Pik 90-second video: Figma renders + prototype captures + Pexels b-roll + Gemini TTS narration + burned captions.

Inputs (all in deck/video/): renders/*.mp4 (Figma Motion exports), captures/*.webm (Playwright), vo/*.wav (narrate.py),
broll/*.mp4 (Pexels, see BROLL below for ids and licence). Output: pik_90s_v1.mp4.
Change the SEGMENTS table to re-time; every VO line is placed relative to its segment start.
Run: python3 build.py   (needs ffmpeg; ~2 min)
"""
import subprocess, pathlib, glob, shlex, sys
D = pathlib.Path(__file__).parent
R, C, V, B = D/"renders", D/"captures", D/"vo", D/"broll"
OUT = D/"pik_90s_v1.mp4"
FONT = next(iter(glob.glob(str(pathlib.Path.home()/"Library/Fonts/Geist-Medium.ttf")) + glob.glob(str(pathlib.Path.home()/"Library/Fonts/Geist-*.ttf"))), None)
MONO = next(iter(glob.glob(str(pathlib.Path.home()/"Library/Fonts/GeistMono-Regular.*"))), FONT)
W, H, FPS = 1920, 1080, 30

# Pexels clips (free licence, no attribution required): id -> local file
BROLL = {"shibuya": B/"pexels_6574285.mp4", "office": B/"pexels_3246669.mp4",
         "smile1": B/"pexels_8202010.mp4", "smile2": B/"pexels_8636292.mp4", "meeting": B/"pexels_7692854.mp4"}

# One row per beat. src: file; dur: seconds kept (trim from `ss`); under: b-roll multiplied under a white-background Figma clip;
# vo: [(file, offset_from_segment_start)]; caps: [(text, start, end)] relative to the segment.
SEGMENTS = [
 dict(name="00_disclosure", src=R/"00_disclosure.mp4", dur=3.0),
 dict(name="01_blur",  src=R/"01_blur.mp4", dur=4.0, under=[("shibuya", 0, 4.0)],
      vo=[("01_blur", 0.3)]),
 dict(name="02_asks",  src=R/"02_asks.mp4", dur=8.0, under=[("office", 0, 2.9), ("smile1", 2.9, 5.5), ("smile2", 5.5, 8.0)],
      vo=[("02_asks", 0.4)]),
 dict(name="03_meet",  src=R/"03_meetpik.mp4", dur=4.5, vo=[("03_meet", 0.3)]),
 dict(name="04a_mining", src=R/"04a_mining.mp4", dur=11.0, vo=[("04_mining", 1.4)],
      caps=[("It reads what she already wrote and shipped, in the places your company allows.", 0.8, 5.6),
            ("Every line keeps its source. DMs are never read.", 6.6, 11.0)]),
 dict(name="04b_receipts", src=R/"04b_receipts.mp4", dur=6.5, vo=[("04b_receipts", 0.6)],
      caps=[("Six receipts, word for word. Two lines had no source, so they are dropped.", 0.6, 6.5)]),
 dict(name="05_zoom", src=R/"05_zoom.mp4", dur=5.5, vo=[("05_zoom", 2.0)]),
 dict(name="06_meet", src=C/"meet_replay.webm", ss=0.5, dur=19.0, vo=[("06_manager", 1.0), ("06b_manager2", 11.0)],
      caps=[("PLACEHOLDER TAKE: the real recording of Carl and Steven goes here.", 0.0, 1.4),
            ("Heard the criterion. Re-sorted on their words. No score.", 2.8, 7.4),
            ("Pik asks one follow-up out loud when the ask is vague.", 7.6, 10.6),
            ("What the meeting concluded. Receipts attached.", 13.0, 19.0)]),
 dict(name="07_slack", src=R/"07_slack.mp4", dur=7.0, vo=[("07_slack", 0.4)]),
 dict(name="08_candidate", src=C/"candidate.webm", ss=2.5, dur=6.5, vo=[("08_cand", 0.3)],
      caps=[("Yui sees the same receipts. No rank, no other names. She answers first.", 0.4, 6.5)]),
 dict(name="09_beyond", src=R/"09_beyond.mp4", dur=6.5, vo=[("09_beyond", 0.0)]),
 dict(name="10_end", src=R/"10_end.mp4", dur=6.5, vo=[("10_end", 0.5)]),
]

def run(cmd):
    print(" ".join(shlex.quote(str(c)) for c in cmd)[:400]); subprocess.run([str(c) for c in cmd], check=True)

def esc(t):  # ffmpeg drawtext escaping
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")

def caption_png(text, light, path):
    """Render one caption as a transparent PNG with PIL (ffmpeg here has no drawtext)."""
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(FONT, 38)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    x0, y0, x1, y1 = tmp.textbbox((0, 0), text, font=font)
    tw, th = x1 - x0, y1 - y0
    pad = 20
    im = Image.new("RGBA", (tw + 2*pad, th + 2*pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width-1, im.height-1), radius=10, fill=(255,255,255,222) if light else (0,0,0,150))
    d.text((pad - x0, pad - y0), text, font=font, fill=(0,0,0,255) if light else (255,255,255,255))
    im.save(path); return im.height

def broll_under(under, dur):
    """Return a filter_complex fragment producing [bg] : greyscale, lifted b-roll cut to the slots."""
    parts, labels = [], []
    for i, (key, a, b) in enumerate(under):
        parts.append(f"[b{i}:v]trim=start=1:duration={b-a:.3f},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                     f"fps={FPS},hue=s=0,eq=brightness=0.18:contrast=0.9,format=rgb24[u{i}]")
        labels.append(f"[u{i}]")
    parts.append("".join(labels) + f"concat=n={len(under)}:v=1:a=0,trim=duration={dur},setpts=PTS-STARTPTS[bgraw]")
    parts.append(f"color=white@0.62:s={W}x{H}:d={dur}[wh];[bgraw][wh]overlay=format=auto[bg]")
    return ";".join(parts)

def build_segment(seg, idx):
    out = D/"_seg"/f"{idx:02d}_{seg['name']}.mp4"; out.parent.mkdir(exist_ok=True)
    ss, dur = seg.get("ss", 0), seg["dur"]
    inputs = ["-ss", ss, "-t", dur + 0.5, "-i", seg["src"]]
    fc = []
    if seg.get("under"):
        for key, a, b in seg["under"]:
            inputs += ["-i", BROLL[key]]
        fc.append(broll_under(seg["under"], dur))
        # Figma clip has a white background: multiply it over the lifted b-roll so black type stays black
        fc.append(f"[0:v]fps={FPS},scale={W}:{H},format=rgb24[fg];[bg][fg]blend=all_mode=multiply[v0]")
    else:
        fc.append(f"[0:v]fps={FPS},scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,format=rgb24[v0]")
    caps = seg.get("caps", [])
    light = seg["name"] not in ("04a_mining", "06_meet", "07_slack", "08_candidate")
    nb = len(seg.get("under", []))
    cur = "[v0]"
    for j, (text, a, b) in enumerate(caps):
        png = out.parent / f"cap_{idx:02d}_{j}.png"; caption_png(text, light, png)
        inputs += ["-i", png]
        fc.append(f"{cur}[{1+nb+j}:v]overlay=(W-w)/2:H-150-h:enable='between(t,{a},{b})'[c{j}]"); cur = f"[c{j}]"
    fc.append(f"{cur}trim=duration={dur},setpts=PTS-STARTPTS,format=yuv420p[vout]")
    # relabel: the b-roll inputs are 1..n, so reference them as b{i}: map input index i+1
    filt = ";".join(fc)
    for i in range(nb):
        filt = filt.replace(f"[b{i}:v]", f"[{i+1}:v]")
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", filt, "-map", "[vout]", "-an",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", FPS, out])
    return out

def main():
    if not FONT: sys.exit("Geist font not found; put Geist*.ttf in prototype/ui/fonts or ~/Library/Fonts")
    segs, t, vo_events = [], 0.0, []
    for i, seg in enumerate(SEGMENTS):
        segs.append(build_segment(seg, i))
        for name, off in seg.get("vo", []):
            vo_events.append((V/f"{name}.wav", t + off))
        seg["start"] = t; t += seg["dur"]
    print(f"total video {t:.1f}s")
    # concat video
    lst = D/"_seg"/"list.txt"; lst.write_text("".join(f"file '{p}'\n" for p in segs))
    silent = D/"_seg"/"video_only.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent])
    # mix narration at absolute offsets, no music
    inputs, fc, labels = [], [], []
    for i, (wav, at) in enumerate(vo_events):
        inputs += ["-i", wav]
        fc.append(f"[{i+1}:a]aformat=sample_rates=48000:channel_layouts=mono,adelay={int(at*1000)}|{int(at*1000)}[a{i}]"); labels.append(f"[a{i}]")
    fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=duration={t:.3f}[aout]")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, *inputs, "-filter_complex", ";".join(fc),
         "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT])
    (D/"TIMING.md").write_text("| start | beat | dur | narration |\n|---|---|---|---|\n" + "".join(
        f"| {s['start']:5.1f}s | {s['name']} | {s['dur']:.1f}s | {', '.join(n for n,_ in s.get('vo',[])) or '(silent)'} |\n" for s in SEGMENTS)
        + f"\nTotal {t:.1f}s. Built by build.py; b-roll ids: " + ", ".join(f"{k}={v.name}" for k,v in BROLL.items()) + "\n")
    print("wrote", OUT)

if __name__ == "__main__":
    main()
