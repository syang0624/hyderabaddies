#!/usr/bin/env python3
"""Stitch the Pik 90-second video, V2: HTML beats rendered by render.py + the Meet capture + Vertex narration + burned captions.

Inputs (deck/video/v2/): renders/<id>.mp4 (render.py, or the sibling's product replicas), captures/meet_replay.webm (record_meet.py),
vo/*.wav (narrate_vertex.py). Output: pik_90s_v2.mp4 (1920x1080, 30 fps, H.264 + AAC). Writes TIMING.md.
The SEGMENTS table is the edit: one row per beat; dur is the seconds kept; vo offsets are relative to the segment start
(negative = starts inside the previous beat, a J-cut); caps are (text, start, end) relative to the segment. A missing render
becomes a bone slate that says the beat id, so timing can be checked before every beat lands.
Run: python3 build_v2.py   (needs ffmpeg + PIL + Geist in ~/Library/Fonts; ~1 min)
"""
import subprocess, pathlib, glob, shlex, sys, json
D = pathlib.Path(__file__).resolve().parent
R, C, V = D/"renders", D/"captures", D/"vo"
OUT = D/"pik_90s_v2.mp4"
FONT = next(iter(glob.glob(str(pathlib.Path.home()/"Library/Fonts/Geist-Medium.ttf")) + glob.glob(str(pathlib.Path.home()/"Library/Fonts/Geist-*.ttf"))), None)
MONO = next(iter(glob.glob(str(pathlib.Path.home()/"Library/Fonts/GeistMono-Regular.ttf"))), FONT)
W, H, FPS = 1920, 1080, 30
BONE, INK = (0xEF, 0xEA, 0xE2), (0x2B, 0x25, 0x21)
TL = json.loads((C/"meet_timeline.json").read_text()) if (C/"meet_timeline.json").exists() else {"vo": {"07_manager": -1.8, "07_meet": 7.5, "07_manager2": 11.4}, "settle": 1.8}
MEET_SS = TL.get("settle", 1.8) + 0.2  # the page clock starts after goto + settle inside the recording

SEGMENTS = [
 dict(name="00_disclosure", src=R/"00_disclosure.mp4", dur=2.2, light=True),
 dict(name="01_blur",       src=R/"01_blur.mp4",       dur=5.2, light=True, vo=[("01_blur", 0.3)]),
 dict(name="02_asked",      src=R/"02_asked.mp4",      dur=8.2, light=True, vo=[("02_asked", 0.15)],
      caps=[("Team formation. Internal mobility. Decided from memory.", 0.8, 5.8)]),
 dict(name="03_asks",       src=R/"03_asks.mp4",       dur=6.8, light=True, vo=[("03_asks", 0.1)],
      caps=[("Same question, every week.", 4.7, 6.8)]),
 dict(name="04_meetpik",    src=R/"04_meetpik.mp4",    dur=4.0, light=True, vo=[("04_meetpik", 0.1)]),
 dict(name="05_mining",     src=R/"05_mining.mp4",     dur=11.5, light=True, vo=[("05_mining", 0.6)],
      caps=[("It reads what she already did.", 0.8, 5.2), ("Every line keeps its source. DMs never.", 5.6, 11.3)]),
 dict(name="06_receipts",   src=R/"06_receipts.mp4",   dur=4.3, light=True, vo=[("06_receipts", 0.1)],
      caps=[("Two hundred people. Always current.", 2.7, 4.3)]),
 dict(name="07_meet",       src=C/"meet_replay.webm", ss=MEET_SS, dur=18.9, light=False,
      vo=[("07_manager", TL["vo"]["07_manager"]), ("07_meet", TL["vo"]["07_meet"]), ("07_manager2", TL["vo"]["07_manager2"])],
      caps=[("Heard the criterion. Re-sorted on their words. No score.", 8.4, 11.6),
            ("Her own words, and what her manager wrote. Both attached.", 12.0, 15.6),
            ("What the meeting concluded. Receipts attached.", 17.6, 18.9)]),
 dict(name="08_slack",      src=R/"08_slack.mp4",      dur=8.0, light=True, vo=[("08_slack", 0.4)],
      caps=[("Ask where you already are. One press to loop her in.", 0.8, 7.6)]),
 dict(name="09_ticket",     src=R/"09_ticket.mp4",     dur=9.5, light=False, vo=[("09_ticket", 0.4)],
      caps=[("One click to assign. The why is attached.", 1.0, 9.2)]),
 dict(name="10_verticals",  src=R/"10_verticals.mp4",  dur=6.8, light=True, vo=[("10_verticals", 0.15)],
      caps=[("Anywhere the wrong person on the job is expensive.", 3.6, 6.8)]),
 dict(name="11_end",        src=R/"11_end.mp4",        dur=4.6, light=True, vo=[("11_end", 0.3)]),
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
    ss, dur = seg.get("ss", 0), seg["dur"]
    src = seg["src"]; slate = not pathlib.Path(src).exists()
    if slate:
        png = out.parent / f"slate_{seg['name']}.png"; slate_png(seg["name"], png)
        inputs = ["-loop", "1", "-t", dur, "-i", png]
    else:
        inputs = ["-ss", ss, "-t", dur + 1.0, "-i", src]
    # scale/pad to the frame, hold the last frame if the clip is shorter than dur
    fc = [f"[0:v]fps={FPS},scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,"
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
    inputs, fc, labels = [], [], []
    for i, (wav, at) in enumerate(vo_events):
        inputs += ["-i", wav]
        fc.append(f"[{i+1}:a]aformat=sample_rates=48000:channel_layouts=mono,adelay={int(at*1000)}|{int(at*1000)}[a{i}]"); labels.append(f"[a{i}]")
    fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=duration={t:.3f}[aout]")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, *inputs, "-filter_complex", ";".join(fc),
         "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT])
    (D/"TIMING.md").write_text("| start | beat | dur | source | narration (offset) | captions |\n|---|---|---|---|---|---|\n" + "".join(
        f"| {s['start']:5.1f}s | {s['name']} | {s['dur']:.1f}s | {'SLATE' if s['name'] in slates else pathlib.Path(s['src']).name} | "
        f"{', '.join(f'{n} @{o:+.1f}' for n,o in s.get('vo',[])) or '(silent)'} | {' / '.join(c[0] for c in s.get('caps',[])) or ''} |\n" for s in SEGMENTS)
        + f"\nTotal {t:.1f}s. Built by build_v2.py. Slates: {', '.join(slates) or 'none'}.\n")
    print("wrote", OUT)

if __name__ == "__main__":
    main()
