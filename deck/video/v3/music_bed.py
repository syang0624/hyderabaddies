#!/usr/bin/env python3
"""Cut the music bed for V3 from Carl's pick: "Kosmose Vaikus" by Kevin MacLeod (incompetech.com, CC BY 4.0).

Picks the calmest 92 s of the track (the 92 s window with the flattest short-term loudness, EBU R128 "S", no swell),
normalises it to -16 LUFS integrated (so build_v3.py's envelope gains are relative to the -16 LUFS narration), and writes
music/bed.wav (48 kHz stereo) and music/BED.md (the window, the gain, the stats). Never plays anything.
Run: python3 deck/video/v3/music_bed.py [--src music/kosmose_vaikus.m4a] [--len 96] [--start N to force a window]
"""
import argparse, json, pathlib, re, statistics, subprocess
D = pathlib.Path(__file__).resolve().parent
M = D / "music"


def ebur_profile(src):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(src), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    pts = []
    for line in r.stderr.splitlines():
        m = re.search(r"t:\s*([\d.]+)\s+TARGET.*?M:\s*(-?[\d.]+|-inf)\s+S:\s*(-?[\d.]+|-inf)", line)
        if m:
            pts.append((float(m.group(1)), float(m.group(3)) if m.group(3) != "-inf" else -70.0))
    integ = re.search(r"I:\s*(-?[\d.]+) LUFS", r.stderr.split("Summary:")[-1] if "Summary:" in r.stderr else r.stderr)
    return pts, float(integ.group(1)) if integ else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(M / "kosmose_vaikus.m4a"))
    ap.add_argument("--len", type=float, default=96.0, help="seconds to cut (the video is 90 s; the rest is tail for the fade)")
    ap.add_argument("--start", type=float, default=None, help="force the window start (seconds)")
    ap.add_argument("--target", type=float, default=-16.0, help="integrated LUFS of bed.wav before ducking")
    a = ap.parse_args()
    pts, _ = ebur_profile(a.src)
    total = pts[-1][0]
    if a.start is None:
        best = None
        for s0 in range(15, int(total - a.len - 8)):
            seg = [S for t, S in pts if s0 <= t < s0 + a.len]
            if len(seg) < 100:
                continue
            sd, mx, mean = statistics.pstdev(seg), max(seg), statistics.mean(seg)
            score = sd + 0.15 * (mx - mean)  # flat first, then no peak above the mean
            if best is None or score < best[0]:
                best = (score, s0, sd, mx, mean, min(seg))
        _, start, sd, mx, mean, mn = best
    else:
        start = a.start
        seg = [S for t, S in pts if start <= t < start + a.len]
        sd, mx, mean, mn = statistics.pstdev(seg), max(seg), statistics.mean(seg), min(seg)
    cut = M / "bed_cut.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{start:.2f}", "-t", f"{a.len:.2f}", "-i", a.src,
                    "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(cut)], check=True)
    _, integ = ebur_profile(cut)
    gain = a.target - integ
    bed = M / "bed.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(cut), "-af", f"volume={gain:.2f}dB", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(bed)], check=True)
    cut.unlink()
    _, integ2 = ebur_profile(bed)
    prof = []
    for s0 in range(0, int(a.len), 8):
        seg = [S for t, S in pts if start + s0 <= t < start + s0 + 8]
        if seg:
            prof.append(f"| {s0:3d}-{s0+8:3d} s | {statistics.mean(seg)+gain:6.1f} | {max(seg)+gain:6.1f} |")
    (M / "BED.md").write_text(
        "# The music bed (`bed.wav`)\n\n"
        "Music: Kosmose Vaikus by Kevin MacLeod, incompetech.com, CC BY 4.0. Carl's pick (Sat Sep 26, ~23:50 PDT); the file is `kosmose_vaikus.m4a` beside this.\n\n"
        f"- Window: {start:.1f} s to {start + a.len:.1f} s of the {total:.0f} s track, chosen by `music_bed.py` as the flattest {a.len:.0f} s of short-term loudness "
        f"(std {sd:.2f} LU, max {mx:.1f}, mean {mean:.1f}, min {mn:.1f} LUFS in the source), so there is no swell under the cut.\n"
        f"- Gain {gain:+.2f} dB to {integ2:.1f} LUFS integrated (target {a.target:.0f}); build_v3.py then multiplies it by the duck envelope "
        "(-26 dB under narration, -18 dB in gaps, 2 s fade in, 3 s fade out on the end card).\n"
        "- Never played here; checked by ffprobe/ebur128 only.\n\n"
        "| bed seconds | mean S (LUFS, after gain) | max S |\n|---|---|---|\n" + "\n".join(prof) + "\n")
    json.dump({"start": start, "len": a.len, "gain_db": round(gain, 2), "integrated_lufs": integ2}, open(M / "bed.json", "w"), indent=1)
    print(f"window {start:.1f}s (+{a.len:.0f}s) std {sd:.2f} max {mx:.1f} mean {mean:.1f} | gain {gain:+.2f} dB -> {integ2:.1f} LUFS -> {bed}")


if __name__ == "__main__":
    main()
