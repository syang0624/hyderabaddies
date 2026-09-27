#!/usr/bin/env python3
"""Render a Pik deck folder to a static PDF, one PNG per slide, and NOTES.md from the slides' speaker notes.

    cd /Users/carl/CODELocalProjects/hyderabaddies/deck
    video/pw/bin/python site/render_pdf.py --png-dir /tmp/pik_render --no-notes
        # renders the canonical deck, "final/Pik Pitch Deck/", to deck/hyderabaddies.pdf (the submission PDF)
        # and copies the same PDF to deck/Pik_deck_final.pdf, so only one deck PDF is in circulation

Options: --site DIR (default "deck/final/Pik Pitch Deck"; deck/site is the earlier version), --png-dir DIR (default <site>/_render,
keep it outside git), --pdf PATH (default deck/hyderabaddies.pdf), --also PATH (default deck/Pik_deck_final.pdf; "" to skip),
--no-notes, --allow-receipt (the earlier deck/site says "receipt"; the final deck never does).
Headless Chromium only (Playwright). Opens index.html?print=1, which stacks every slide in its final build state at 1920x1080.
PDF metadata: title "hyderabaddies", no author (organisers' privacy notice: the team name only, no individual names).
Exits non-zero if the page logged an error, a slide is not 1920x1080, a source line overflows, a [TBD] is still on a slide,
a team member's name is visible on a slide, or "receipt" appears in the final deck (slides or notes).
"""
import argparse
import pathlib
import re
import shutil
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
DECK = HERE.parent
FINAL = DECK / "final" / "Pik Pitch Deck"
NAMES = re.compile(r"Carl Kho|Carl Vincent|Ladres|Steven Yang", re.I)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=str(FINAL))
    ap.add_argument("--png-dir", default=None)
    ap.add_argument("--pdf", default=str(DECK / "hyderabaddies.pdf"))
    ap.add_argument("--also", default=str(DECK / "Pik_deck_final.pdf"))
    ap.add_argument("--no-notes", action="store_true")
    ap.add_argument("--allow-receipt", action="store_true")
    a = ap.parse_args()
    site = pathlib.Path(a.site).resolve()
    png_dir = pathlib.Path(a.png_dir or (site / "_render"))
    png_dir.mkdir(parents=True, exist_ok=True)
    for old in png_dir.glob("*.png"):
        old.unlink()

    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        pg.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))
        pg.on("console", lambda m: errors.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
        pg.goto((site / "index.html").as_uri() + "?print=1")
        pg.wait_for_function("window.__deckReady===true", timeout=60000)
        pg.wait_for_timeout(600)
        info = pg.evaluate(
            """() => [...document.querySelectorAll('.slide')].map(s => {
                const r = s.getBoundingClientRect();
                const h1 = s.querySelector('h1') || s.querySelector('.sub');
                return {name: s.dataset.name || s.id, label: (s.querySelector('.prog')||{}).textContent || '',
                        title: h1 ? h1.textContent.trim() : '', w: r.width, h: r.height,
                        tbd: (s.innerText.match(/\\[TBD[^\\]]*\\]/g) || []),
                        words: (() => { const m = s.querySelector('.m').cloneNode(true); m.querySelectorAll('aside,canvas,svg,.formulas,.src').forEach(e => e.remove()); const t = m.innerText.replace(/\\s+/g, ' ').trim(); return t ? t.split(' ').length : 0 })(),
                        srcLen: (s.querySelector('.src') || {textContent: ''}).textContent.length,
                        srcOver: (() => { const e = s.querySelector('.src'); return e ? e.scrollWidth > e.clientWidth + 1 : false })(),
                        visible: s.innerText, notes: [...s.querySelectorAll('.notes p')].map(p => p.textContent).join(' '),
                        steps: [...s.querySelectorAll('.notes p')].map(p => ({n: +p.dataset.step, text: p.textContent.trim()}))}
            })"""
        )
        files = []
        for i, el in enumerate(pg.query_selector_all(".slide")):
            f = png_dir / f"{i + 1:02d}_{slug(info[i]['name'])}.png"
            el.screenshot(path=str(f))
            files.append(f)
        b.close()

    bad = [s for s in info if round(s["w"]) != 1920 or round(s["h"]) != 1080]
    for s in bad:
        errors.append(f"slide {s['name']} is {s['w']}x{s['h']}, not 1920x1080")

    ims = [Image.open(f).convert("RGB") for f in files]
    # the organisers' privacy notice: the team name only; Pillow writes no Author entry when none is given
    ims[0].save(a.pdf, save_all=True, append_images=ims[1:], resolution=96.0, quality=95, title="hyderabaddies")
    size = pathlib.Path(a.pdf).stat().st_size
    if a.also:
        shutil.copyfile(a.pdf, a.also)

    for s in info:
        if s["srcOver"]:
            errors.append(f"slide {s['name']}: the source line overflows its 1600 px")
        if NAMES.search(s["visible"]):
            errors.append(f"slide {s['name']}: a team member's name is visible (privacy notice: team name only)")
        if not a.allow_receipt and re.search(r"receipt", s["visible"] + " " + s["notes"], re.I):
            errors.append(f"slide {s['name']}: the word 'receipt' appears (the final deck never says it)")

    if not a.no_notes:
        out = ["# Pik deck, speaker notes and build cues", "",
               f"Generated by `deck/site/render_pdf.py` from the `<aside class=\"notes\">` of each slide in `{site.name}/index.html`; edit the HTML, not this file.",
               "Keys: Right or Space = next build step, then next slide. Left = back. N = notes drawer. Digits jump to a slide. `?slide=N` opens one. Click = next step.", ""]
        for s in info:
            out.append(f"## {s['label'] or s['name']}: {s['name']}")
            if s["title"]:
                out.append(f"*{s['title']}*")
            out.append("")
            for st in s["steps"]:
                cue = "On arrival" if st["n"] == 0 else ("Judges" if st["n"] == 99 else ("Full metrics" if st["n"] == 97 else f"Keypress {st['n']}"))
                out.append(f"- **{cue}.** {st['text']}")
            out.append("")
        (site / "NOTES.md").write_text("\n".join(out), encoding="utf-8")

    tbd = [(s["name"], s["tbd"]) for s in info if s["tbd"]]
    print(f"slides: {len(files)}  pdf: {a.pdf}  pages: {len(ims)}  size: {size/1e6:.1f} MB  pngs: {png_dir}" + (f"  copied to: {a.also}" if a.also else ""))
    print("visible words per slide (title included; source line, formula lines and canvas text excluded):")
    for s in info:
        flag = "  SOURCE LINE OVERFLOWS" if s["srcOver"] else ""
        print(f"  {s['label'] or s['name']:>10}  {s['name']:<28} {s['words']:>4} words   src {s['srcLen']:>3} chars{flag}")
    for name, t in tbd:
        print(f"[TBD] still on slide {name}: {t}")
        errors.append(f"[TBD] on slide {name}: a placeholder must never ship")
    if errors:
        print("PAGE ERRORS (the render is not clean):", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
