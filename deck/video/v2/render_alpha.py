#!/usr/bin/env python3
"""Render a seek(ms) page either as a TRANSPARENT overlay composited onto a real take, or as an opaque clip at a given size.

Overlay pages (html/overlay_*.html) have no body background; every frame is screenshotted with omit_background=True to an
RGBA PNG and ffmpeg lays the frames over the take (H.264 yuv420p, the take's duration). Opaque pages (the avatar loop)
are screenshotted at --size and encoded on their own.
Usage:
  deck/video/pw/bin/python deck/video/v2/render_alpha.py overlay_notion --over renders/09_notion_real.mp4 --out renders/09_notion_real_pik.mp4
  deck/video/pw/bin/python deck/video/v2/render_alpha.py avatar_loop --size 640x480 --out renders/pik_avatar_loop.mp4
Frames go to _frames/<page>/ (git-ignored) and are removed after a successful encode unless --keep.
"""
import argparse, math, pathlib, shutil, subprocess, sys, time
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).resolve().parent
HTML, FR = D / "html", D / "_frames"
FPS = 30


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page"); ap.add_argument("--over"); ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1920x1080"); ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    html = HTML / f"{a.page}.html"
    if not html.exists():
        sys.exit(f"no such page: {html}")
    w, h = (int(x) for x in a.size.split("x"))
    out = (D / a.out) if not pathlib.Path(a.out).is_absolute() else pathlib.Path(a.out)
    frames = FR / a.page
    if frames.exists(): shutil.rmtree(frames)
    frames.mkdir(parents=True)
    t0 = time.time()
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg = ctx.new_page()
        pg.goto(html.as_uri() + "?t=0")
        pg.wait_for_function("window.__ready === true", timeout=15000)
        dur = pg.evaluate("window.DURATION_MS")
        n = int(round(dur / 1000 * FPS))
        for i in range(n):
            pg.evaluate(f"window.seek({i * 1000 / FPS:.3f})")
            pg.screenshot(path=str(frames / f"{i:05d}.png"), omit_background=bool(a.over))
        ctx.close(); b.close()
    out.parent.mkdir(parents=True, exist_ok=True)
    if a.over:
        take = (D / a.over) if not pathlib.Path(a.over).is_absolute() else pathlib.Path(a.over)
        fc = f"[1:v]format=rgba[ov];[0:v][ov]overlay=0:0:shortest=1:format=auto,format=yuv420p[v]"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(take), "-framerate", str(FPS), "-i", str(frames / "%05d.png"),
                        "-filter_complex", fc, "-map", "[v]", "-an", "-t", f"{dur/1000:.3f}",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "17", "-r", str(FPS), "-movflags", "+faststart", str(out)], check=True)
    else:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "%05d.png"),
                        "-vf", "format=yuv420p", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "17", "-r", str(FPS), "-movflags", "+faststart", str(out)], check=True)
    if not a.keep: shutil.rmtree(frames)
    print(f"{a.page}: {n} frames, {dur/1000:.2f}s, {time.time()-t0:.0f}s -> {out}")


if __name__ == "__main__":
    main()
