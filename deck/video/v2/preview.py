#!/usr/bin/env python3
"""Contact sheet of one beat at chosen times, for eyeballing before a full render.
Usage: deck/video/pw/bin/python deck/video/v2/preview.py 01 [t_ms ...] -> _frames/preview_<id>.png (6 stills default)"""
import sys, pathlib, math, subprocess
from playwright.sync_api import sync_playwright
D = pathlib.Path(__file__).resolve().parent
bid = sys.argv[1]; html = next(D.glob(f"html/{bid}*.html"))
out = D / "_frames"; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(html.as_uri() + "?t=0"); pg.wait_for_function("window.__ready === true")
    dur = pg.evaluate("window.DURATION_MS")
    ts = [float(t) for t in sys.argv[2:]] or [dur * k / 6 for k in range(6)]
    files = []
    for i, t in enumerate(ts):
        pg.evaluate(f"window.seek({t})"); f = out / f"pv_{bid}_{i}.png"; pg.screenshot(path=str(f)); files.append(f)
    b.close()
from PIL import Image, ImageDraw
cols = 2; rows = math.ceil(len(files) / cols); W, H = 960, 540
sheet = Image.new("RGB", (cols * W, rows * H), "white")
for i, f in enumerate(files):
    im = Image.open(f).resize((W, H)); ImageDraw.Draw(im).text((12, 8), f"{bid} t={ts[i]/1000:.2f}s", fill=(200, 40, 40))
    sheet.paste(im, ((i % cols) * W, (i // cols) * H)); f.unlink()
dst = out / f"preview_{bid}.png"; sheet.save(dst); print(dst)
