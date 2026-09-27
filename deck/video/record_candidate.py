#!/usr/bin/env python3
"""Record the candidate's view (?as=yui): the same receipts, no rank, and Yui adds a note that lands on the evaluator's page.
Output: captures/candidate.webm (1920x1080). Usage: $PW record_candidate.py
"""
import asyncio, pathlib, shutil, json
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).parent / "captures"
NOTE = "I'd rather build the team here first. The location line was Okada's guess, not mine."
async def main():
    ann = ROOT/"prototype"/"state"/"annotations.json"
    if ann.exists(): ann.write_text("[]")   # start with no notes so the one we add is the only one
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width":1920,"height":1080}, device_scale_factor=1,
                                  record_video_dir=str(OUT), record_video_size={"width":1920,"height":1080})
        pg = await ctx.new_page()
        await pg.goto("http://localhost:8787/?as=yui&present=1")
        await pg.wait_for_timeout(2500)
        stub = pg.locator('.stub').first
        await stub.scroll_into_view_if_needed()
        await pg.wait_for_timeout(1200)
        await stub.click()                      # opens the receipt: source line + note box
        await pg.wait_for_timeout(1200)
        inp = stub.locator('input[id^="an-"]').first
        await inp.click()
        await pg.wait_for_timeout(400)
        await inp.type(NOTE, delay=38)
        await pg.wait_for_timeout(600)
        btn = inp.locator('xpath=following-sibling::button[1]')
        await btn.click()
        await pg.wait_for_timeout(3000)
        await pg.screenshot(path=str(OUT/"_candidate_end.png"))
        path = await pg.video.path()
        await ctx.close(); await b.close()
        dst = OUT/"candidate.webm"; shutil.move(path, dst); print("wrote", dst)
asyncio.run(main())
