"""Pik joins a Google Meet as a participant named "Pik" and presents the composed screen.

DRAFT, NOT RUNNABLE (Sat 2026-09-26 22:45 PDT). Carl forbids Playwright's bundled browser ("Google Chrome
for Testing") for anything with a window or a login. The bot's browser must be Dia, on a separate Dia
profile named "Pik"; the launch path (Bot.launch and signin below) is being reworked to drive that. Until
then main() refuses to start. The Meet steps (name, mic/camera off, Ask to join, re-knock, present, leave)
are kept as they are; steps 1-6 were checked against the real Meet UI before the stop.

A headed Chromium (Playwright, persistent profile) opens two tabs: the Pik page in present mode
(http://localhost:8787/?present=1) and the Meet. It joins as a guest named "Pik" with camera and
microphone off, waits for the host to admit it, then presents the Pik tab. Chromium picks that tab
by itself (--auto-select-tab-capture-source-by-title=Pik), so no picker needs a click.

The bot neither hears nor speaks in the Meet. `make live` on the laptop listens to the room and
speaks the follow-up through the laptop speaker; the bot is presence plus the presented screen.

Run:  deck/video/pw/bin/python prototype/meet_bot.py https://meet.google.com/abc-defg-hij
      (from the repo root; Ctrl-C stops presenting, leaves the call and closes the window)
Opts: --pik-url URL (default http://localhost:8787/?present=1), --name Pik,
      --admit-timeout 300 (seconds to wait for the host to click Admit)

Every step prints one line and saves prototype/state/meet_bot/NN_step.png. A failed step prints
the reason and exits non-zero (1 = a step failed, 2 = denied, removed or the call ended).

Why --use-fake-ui-for-media-stream is NOT passed: with it, getDisplayMedia skips the tab picker
and hands Meet Chromium's fake green test pattern instead of the Pik tab (checked 2026-09-26).
Camera and microphone are granted to meet.google.com through the context instead, and the fake
microphone reads a silent wav so no test tone can leak even if the mute toggle misses.
"""
from __future__ import annotations

import argparse
import asyncio
import re
import signal
import struct
import sys
import time
import wave
from pathlib import Path

from playwright.async_api import TimeoutError as PWTimeout
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "state" / "meet_bot"
PROFILE = Path.home() / ".local" / "state" / "pik-meet-profile"
SILENCE = PROFILE.parent / "pik-meet-silence.wav"


class StepFailed(Exception):
    def __init__(self, reason: str, code: int = 1):
        super().__init__(reason)
        self.code = code


class Bot:
    def __init__(self, args):
        self.args = args
        self.n = 0
        self.t0 = time.time()
        self.ctx = None
        self.pik = None
        self.meet = None
        self.presenting = False
        self.in_call = False

    # ---------- output ----------
    async def shot(self, name: str, page=None):
        self.n += 1
        page = page or self.meet or self.pik
        path = SHOTS / f"{self.n:02d}_{name}.png"
        try:
            await page.screenshot(path=str(path), timeout=10_000)
        except Exception as e:  # noqa: BLE001
            print(f"   (screenshot {path.name} failed: {type(e).__name__})", flush=True)
            return None
        return path

    def say(self, msg: str):
        print(f"[{time.time() - self.t0:6.1f}s] {msg}", flush=True)

    async def fail(self, step: str, reason: str, code: int = 1):
        await self.shot(f"FAIL_{step}")
        raise StepFailed(f"{step}: {reason}", code)

    # ---------- helpers ----------
    async def first_visible(self, page, locators, timeout=0.0):
        """Return the first locator (from a list of candidates) that is visible, polling until timeout."""
        end = time.time() + timeout
        while True:
            for loc in locators:
                try:
                    if await loc.count() and await loc.first.is_visible():
                        return loc.first
                except Exception:  # noqa: BLE001
                    pass
            if time.time() >= end:
                return None
            await asyncio.sleep(0.4)

    async def page_says(self, page, patterns) -> str | None:
        try:
            body = await page.locator("body").inner_text(timeout=3000)
        except Exception:  # noqa: BLE001
            return None
        for p in patterns:
            m = re.search(p, body, re.I)
            if m:
                return m.group(0)
        return None

    def leave_button(self):
        m = self.meet
        return [m.get_by_role("button", name=re.compile(r"^leave call", re.I)),
                m.locator('[aria-label="Leave call"]'),
                m.locator('button[aria-label*="Leave call" i]')]

    def present_buttons(self):
        m = self.meet
        return [m.get_by_role("button", name=re.compile(r"^(share screen|present now|present)$", re.I)),
                m.locator('button[aria-label*="Share screen" i]'),
                m.locator('button[aria-label*="Present now" i]'),
                m.locator('[role="button"][aria-label*="Present" i]:not([aria-label*="Stop" i])')]

    def stop_present_buttons(self):
        m = self.meet
        return [m.get_by_role("button", name=re.compile(r"stop (presenting|sharing)", re.I)),
                m.locator('[aria-label*="Stop presenting" i]'),
                m.locator('[aria-label*="Stop sharing" i]')]

    async def dismiss_popups(self):
        """Close Meet's one-off dialogs (tips, 'Got it', 'Dismiss') that can cover the toolbar."""
        for loc in [self.meet.get_by_role("button", name=re.compile(r"^(got it|dismiss|close|ok|no thanks|not now)$", re.I))]:
            try:
                for i in range(min(await loc.count(), 3)):
                    b = loc.nth(i)
                    if await b.is_visible():
                        await b.click(timeout=1500)
            except Exception:  # noqa: BLE001
                pass

    # ---------- steps ----------
    async def launch(self, pw):
        SHOTS.mkdir(parents=True, exist_ok=True)
        for old in SHOTS.glob("[0-9][0-9]_*.png"):
            old.unlink()
        PROFILE.mkdir(parents=True, exist_ok=True)
        if not SILENCE.exists():
            with wave.open(str(SILENCE), "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000)
                w.writeframes(struct.pack("<h", 0) * 16000 * 5)
        self.ctx = await pw.chromium.launch_persistent_context(
            str(PROFILE), headless=False, viewport={"width": 1440, "height": 900},
            args=["--use-fake-device-for-media-stream",
                  f"--use-file-for-fake-audio-capture={SILENCE}",
                  "--auto-select-tab-capture-source-by-title=Pik",
                  "--disable-blink-features=AutomationControlled",
                  "--window-size=1440,1000"],
            ignore_default_args=["--enable-automation", "--mute-audio"],
        )
        await self.ctx.grant_permissions(["camera", "microphone"], origin="https://meet.google.com")
        self.ctx.on("close", lambda _: print("   (browser context closed)", flush=True))
        self.ctx.on("page", lambda p: p.on("close", lambda pg: print(f"   (tab closed: {pg.url[:60]})", flush=True)))
        self.say(f"01 launched headed Chromium, profile {PROFILE}")

    async def open_pik(self):
        self.pik = self.ctx.pages[0] if self.ctx.pages else await self.ctx.new_page()
        try:
            await self.pik.goto(self.args.pik_url, wait_until="domcontentloaded", timeout=15_000)
        except Exception as e:  # noqa: BLE001
            await self.fail("pik_page", f"could not open {self.args.pik_url} ({type(e).__name__}); is the server up? cd prototype && make run-heuristic")
        await asyncio.sleep(1.5)
        title = await self.pik.title()
        if not title.startswith("Pik"):
            await self.pik.evaluate("document.title = 'Pik'")
            title = await self.pik.title()
            self.say(f"02 Pik page open; title was not 'Pik...', set it to {title!r}")
        else:
            self.say(f"02 Pik page open, title {title!r}")
        await self.shot("pik_page", self.pik)

    async def open_meet(self):
        if self.meet is None:
            self.meet = await self.ctx.new_page()
        try:
            await self.meet.goto(self.args.url, wait_until="domcontentloaded", timeout=30_000)
        except Exception as e:  # noqa: BLE001
            await self.fail("open_meet", f"could not open {self.args.url} ({type(e).__name__})")
        if "accounts.google.com" in self.meet.url:
            await self.fail("open_meet", "Meet redirected to Google sign-in: anonymous join is not allowed for this meeting. "
                                         "Sign this bot window into a Google account by hand, then re-run.")
        # wait for the pre-join screen: a join button, the name field, or a refusal
        join = await self.first_visible(self.meet, self.join_buttons() + self.name_fields(), timeout=30)
        refusal = await self.page_says(self.meet, [r"sign in to join", r"check your meeting code",
                                                   r"meeting code (is )?invalid", r"this meeting has ended"])
        if refusal:
            await self.fail("open_meet", f"Meet says {refusal!r}. If it asks for sign-in: sign the bot window into a Google account by hand and re-run.")
        if join is None:
            if await self.page_says(self.meet, [r"you can.t join this (video )?call"]):
                await self.fail("open_meet", "Meet says \"You can't join this video call\" before knocking: this meeting does not take "
                                             "anonymous guests. Host controls -> Meeting access -> Open, or meet_bot.py --signin", code=2)
            await self.fail("open_meet", "no pre-join screen (no name field, no join button) within 30 s")
        self.say("03 Meet pre-join screen loaded")
        await self.shot("prejoin")

    def name_fields(self):
        m = self.meet
        return [m.get_by_role("textbox", name=re.compile(r"your name|name", re.I)),
                m.locator('input[aria-label*="name" i]'),
                m.locator('input[placeholder*="name" i]')]

    def join_buttons(self):
        m = self.meet
        return [m.get_by_role("button", name=re.compile(r"^(ask to join|join now|join anyway|join)$", re.I)),
                m.locator('button:has-text("Ask to join")'),
                m.locator('button:has-text("Join now")')]

    async def set_name(self):
        field = await self.first_visible(self.meet, self.name_fields(), timeout=5)
        if field is None:
            self.say("04 no name field: this profile is signed in, Meet will show the account's name (not 'Pik')")
            await self.shot("no_name_field")
            return
        # the "Sign in with your Google account ... Got it" tip can pop up mid-typing and steal focus: close it, then fill and verify
        val = ""
        for _ in range(4):
            await self.dismiss_popups()
            await field.click()
            await field.fill(self.args.name)
            await asyncio.sleep(0.6)
            val = await field.input_value()
            if val == self.args.name:
                break
        if val != self.args.name:
            await self.fail("name", f"name field holds {val!r}, wanted {self.args.name!r}")
        self.say(f"04 typed name {self.args.name!r}")
        await self.shot("name")

    async def devices_off(self):
        m = self.meet
        results = {}
        for dev in ("microphone", "camera"):
            off_btn = await self.first_visible(m, [
                m.get_by_role("button", name=re.compile(rf"turn off {dev}", re.I)),
                m.locator(f'[role="button"][aria-label*="Turn off {dev}" i]'),
                m.locator(f'[data-is-muted="false"][aria-label*="{dev}" i]')], timeout=4)
            if off_btn is not None:
                await off_btn.click()
                await asyncio.sleep(0.8)
            on_btn = await self.first_visible(m, [
                m.get_by_role("button", name=re.compile(rf"turn on {dev}", re.I)),
                m.locator(f'[role="button"][aria-label*="Turn on {dev}" i]'),
                m.locator(f'[data-is-muted="true"][aria-label*="{dev}" i]')], timeout=3)
            if on_btn is not None:
                results[dev] = "off"
            else:
                # Meet sometimes hides the toggles when no device is in use; "Continue without microphone and camera" also counts
                results[dev] = "unconfirmed"
        await self.shot("devices_off")
        if results["microphone"] != "off":
            cont = await self.first_visible(m, [m.get_by_role("button", name=re.compile(r"continue without (microphone|mic)", re.I))], timeout=1)
            if cont is not None:
                await cont.click()
                results["microphone"] = results["camera"] = "off (continued without devices)"
        if results["microphone"] == "unconfirmed":
            # the fake mic reads a silent wav, so nothing audible can go out; say so rather than stop the demo
            self.say("05 WARNING: could not confirm the microphone toggle is off (the bot's mic is a silent file, so nothing is sent)")
        self.say(f"05 microphone {results['microphone']}, camera {results['camera']}")

    async def ask_to_join(self):
        btn = await self.first_visible(self.meet, self.join_buttons(), timeout=10)
        if btn is None:
            await self.fail("join", "no 'Ask to join' / 'Join now' button")
        label = (await btn.inner_text()).strip() or "join"
        await btn.click()
        self.say(f"06 clicked {label!r}")
        await self.shot("asked_to_join")

    async def wait_admitted(self) -> bool:
        """True once in the call. False when Meet refused the knock outright (it does this while nobody is
        in the call yet), so the caller can knock again. Fails on a host's Deny or when the time runs out."""
        told = False
        while time.time() < self.deadline:
            if await self.first_visible(self.meet, self.leave_button()) is not None:
                # the lobby has no Leave call button, so this means we are in the call
                self.in_call = True
                await asyncio.sleep(2)
                await self.dismiss_popups()
                self.say("07 admitted: in the call")
                await self.shot("in_call")
                return True
            denied = await self.page_says(self.meet, [r"denied your request", r"removed from the (meeting|call)", r"call has ended", r"meeting has ended"])
            if denied:
                await self.fail("admit", f"Meet says {denied!r}", code=2)
            refused = await self.page_says(self.meet, [r"you can.t join this (video )?call", r"no one responded to your request"])
            if refused:
                await self.shot("refused")
                try:  # leave the refusal page at once; it runs a countdown back to the Meet home screen
                    await self.meet.goto("about:blank", timeout=5000)
                except Exception:  # noqa: BLE001
                    pass
                return False
            if not told:
                self.say("   waiting for the host to click Admit ...")
                told = True
            await asyncio.sleep(1)
        await self.fail("admit", f"not admitted within {self.args.admit_timeout:.0f} s")

    async def knock_until_admitted(self):
        """Knock, and knock again while Meet refuses. An anonymous guest who knocks before anyone is in the call
        gets "You can't join this video call" at once (seen 2026-09-26 on minerva.edu and somach.life meetings)."""
        self.deadline = time.time() + self.args.admit_timeout
        tries = 0
        while True:
            tries += 1
            await self.open_meet()  # re-uses the Meet tab on later tries (closing it took the whole context down)
            await self.set_name()
            await self.devices_off()
            await self.ask_to_join()
            if await self.wait_admitted():
                return
            left = self.deadline - time.time()
            if left < 20:
                await self.fail("admit", f"Meet refused the knock {tries} time(s) with \"You can't join this video call\". "
                                         "Is the host in the call? If yes, this meeting does not let anonymous guests in: host controls -> "
                                         "Meeting access -> Open, or sign the bot profile in (meet_bot.py --signin).", code=2)
            self.say(f"   Meet refused knock {tries} (\"You can't join this video call\"; is the host in the call yet?). Knocking again in 10 s, {left:.0f} s left")
            await asyncio.sleep(10)

    async def present(self):
        m = self.meet
        await m.bring_to_front()
        await self.dismiss_popups()
        # the toolbar hides after a few seconds of no mouse movement; nudge it
        await m.mouse.move(720, 700)
        await m.mouse.move(720, 850)
        btn = await self.first_visible(m, self.present_buttons(), timeout=10)
        if btn is None:
            await self.fail("present", "no 'Share screen' / 'Present now' button in the toolbar")
        await btn.click()
        self.say("08 clicked Share screen / Present now")
        # older Meet opens a menu (Your entire screen / A window / A tab); newer Meet goes straight to the picker
        tab_item = await self.first_visible(m, [m.get_by_role("menuitem", name=re.compile(r"a tab|tab$", re.I)),
                                                m.locator('li:has-text("A tab")'),
                                                m.get_by_text(re.compile(r"^a tab$", re.I))], timeout=2.5)
        if tab_item is not None:
            await tab_item.click()
            self.say("   picked 'A tab' from the menu")
        # Chromium auto-picks the tab titled Pik; confirm Meet thinks we are presenting
        end = time.time() + 20
        while time.time() < end:
            stop = await self.first_visible(m, self.stop_present_buttons())
            txt = await self.page_says(m, [r"you.re presenting", r"you are presenting", r"presenting to everyone"])
            if stop is not None or txt:
                self.presenting = True
                await m.bring_to_front()
                await asyncio.sleep(1.5)
                await self.shot("presenting")
                self.say(f"09 presenting the Pik tab ({txt or 'Stop presenting button visible'})")
                return
            await asyncio.sleep(0.5)
        await self.fail("present", "Meet never showed 'You're presenting' within 20 s (did the tab picker open? is a tab titled 'Pik' open?)")

    async def hold(self, stop: asyncio.Event):
        self.say("10 live. Ctrl-C to stop presenting and leave the call.")
        await self.pik.bring_to_front()  # the window shows the composed screen; the captured tab keeps rendering
        retries = 0
        while not stop.is_set():
            try:
                await asyncio.wait_for(stop.wait(), timeout=5)
                break
            except asyncio.TimeoutError:
                pass
            if await self.first_visible(self.meet, self.leave_button()) is None:
                bad = await self.page_says(self.meet, [r"removed from the (meeting|call)", r"you left the (meeting|call)", r"call has ended", r"meeting has ended"])
                if bad:
                    await self.fail("hold", f"Meet says {bad!r}", code=2)
                continue  # toolbar hidden or a transient state; check again in 5 s
            if await self.first_visible(self.meet, self.stop_present_buttons()) is None and \
                    not await self.page_says(self.meet, [r"you.re presenting", r"you are presenting"]):
                retries += 1
                if retries > 3:
                    await self.fail("hold", "the presentation stopped and 3 re-presents failed")
                self.say(f"   presentation stopped (host or Chrome ended it); re-presenting, try {retries}")
                self.presenting = False
                await self.present()
                await self.pik.bring_to_front()

    async def leave(self):
        if self.meet is None:
            return
        try:
            if self.presenting:
                btn = await self.first_visible(self.meet, self.stop_present_buttons(), timeout=2)
                if btn is not None:
                    await btn.click(timeout=3000)
                    self.say("   stopped presenting")
            if self.in_call:
                await self.meet.mouse.move(720, 850)
                btn = await self.first_visible(self.meet, self.leave_button(), timeout=3)
                if btn is not None:
                    await btn.click(timeout=3000)
                    await asyncio.sleep(1.5)
                    self.say("   left the call")
                    await self.shot("left")
                else:
                    self.say("   WARNING: no Leave call button found; closing the window drops the bot from the call")
        except Exception as e:  # noqa: BLE001
            self.say(f"   WARNING: leave step raised {type(e).__name__}: {e}")


async def signin() -> int:
    """Launch the same Chromium on the same profile WITHOUT Playwright attached, so Google's sign-in page sees an
    ordinary browser. A person types the credentials; this script never sees them."""
    import subprocess
    async with async_playwright() as pw:
        exe = pw.chromium.executable_path
    PROFILE.mkdir(parents=True, exist_ok=True)
    print(f"opening {exe} on {PROFILE}. Sign in at accounts.google.com, then close the window.", flush=True)
    rc = subprocess.call([exe, f"--user-data-dir={PROFILE}", "--no-first-run", "--no-default-browser-check",
                          "https://accounts.google.com/"])
    print(f"window closed (exit {rc}). Now run: meet_bot.py <meet url>. Meet will show the account's name, not 'Pik'.", flush=True)
    return 0 if rc == 0 else 1


async def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("url", nargs="?", default="", help="Google Meet link, e.g. https://meet.google.com/abc-defg-hij")
    ap.add_argument("--pik-url", default="http://localhost:8787/?present=1")
    ap.add_argument("--name", default="Pik")
    ap.add_argument("--admit-timeout", type=float, default=300)
    ap.add_argument("--signin", action="store_true",
                    help="open the bot's profile in a plain Chromium window (no automation attached) so a person can sign it "
                         "into a Google account by hand; close the window when done. The url argument is ignored.")
    args = ap.parse_args()
    print("meet_bot.py is a DRAFT: its launch path uses Playwright's bundled Chromium, which Carl does not allow. "
          "It is being reworked to drive a separate Dia profile named 'Pik'. Nothing was launched.", file=sys.stderr)
    return 1
    if args.signin:  # noqa: unreachable until the Dia launch path lands
        return await signin()
    if not re.match(r"^https://meet\.google\.com/[a-z]{3}-[a-z]{4}-[a-z]{3}", args.url):
        print(f"not a Meet link: {args.url!r} (want https://meet.google.com/abc-defg-hij)", file=sys.stderr)
        return 1

    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set)

    bot = Bot(args)
    code = 0
    async with async_playwright() as pw:
        try:
            await bot.launch(pw)
            steps = [bot.open_pik, bot.knock_until_admitted, bot.present]
            for step in steps:
                if stop.is_set():
                    raise StepFailed("stopped by Ctrl-C before the bot was presenting")
                await step()
            await bot.hold(stop)
            bot.say("stopping (Ctrl-C)")
        except StepFailed as e:
            print(f"FAILED {e}  (screenshots in {SHOTS})", file=sys.stderr, flush=True)
            code = e.code
        except PWTimeout as e:
            print(f"FAILED playwright timeout: {e}", file=sys.stderr, flush=True)
            await bot.shot("FAIL_timeout")
            code = 1
        except Exception as e:  # noqa: BLE001
            print(f"FAILED {type(e).__name__}: {e}", file=sys.stderr, flush=True)
            if bot.ctx:
                await bot.shot("FAIL_exception")
            code = 1
        finally:
            await bot.leave()
            if bot.ctx:
                try:
                    await bot.ctx.close()
                except Exception:  # noqa: BLE001
                    pass
    return code


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
