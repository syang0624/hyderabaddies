#!/usr/bin/env python3
"""Render the HTML beats to mp4, frame by frame, deterministically.

Each deck/video/v6/html/<id>_<name>.html (V6 beats; assets from ../../v2/html/assets) is a 1920x1080 page that exposes window.seek(ms) and window.DURATION_MS.
For every frame at 30 fps this calls seek(t), screenshots, then ffmpeg encodes renders/<id>_<name>.mp4 (H.264, yuv420p).
Run:  deck/video/pw/bin/python deck/video/v5/render.py           # every beat present in html/
      deck/video/pw/bin/python deck/video/v5/render.py 01 02     # only ids starting with these
Frames go to _frames/<beat>/ (git-ignored) and are deleted after a successful encode unless --keep.
"""
import sys, pathlib, subprocess, math, time, shutil, argparse
from playwright.sync_api import sync_playwright
D = pathlib.Path(__file__).resolve().parent
HTML, REND, FR = D / "html", D / "renders", D / "_frames"
FPS = 30

def render(html: pathlib.Path, keep: bool, browser):
    name = html.stem
    frames = FR / name
    if frames.exists(): shutil.rmtree(frames)
    frames.mkdir(parents=True)
    ctx = browser.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    pg = ctx.new_page()
    pg.goto(html.resolve().as_uri() + "?t=0")
    pg.wait_for_function("window.__ready === true", timeout=15000)
    dur = pg.evaluate("window.DURATION_MS")
    n = int(math.ceil(dur / 1000 * FPS))
    t0 = time.time()
    for i in range(n):
        pg.evaluate(f"window.seek({i * 1000 / FPS:.3f})")
        pg.screenshot(path=str(frames / f"{i:05d}.jpg"), type="jpeg", quality=96)
    ctx.close()
    out = REND / f"{name}.mp4"; REND.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "%05d.jpg"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "medium", "-r", str(FPS), str(out)], check=True)
    if not keep: shutil.rmtree(frames)
    print(f"{name}: {n} frames, {dur/1000:.1f}s, {time.time()-t0:.0f}s -> {out}")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("ids", nargs="*"); ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    pages = sorted(p for p in HTML.glob("[0-9][0-9]*_*.html"))
    if a.ids: pages = [p for p in pages if any(p.name.startswith(i) for i in a.ids)]
    if not pages: sys.exit("no beats matched")
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        for h in pages: render(h, a.keep, b)
        b.close()

if __name__ == "__main__":
    main()
