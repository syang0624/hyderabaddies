#!/usr/bin/env python3
"""Capture every product-page beat of the V3 video from the Pik screen, in one re-runnable script, no hand steps.

Starts (or reuses) the prototype server of THIS checkout on --port, then records with headless Chromium (Playwright,
1920x1080, never a visible window) into captures/:

  meet    /?present=1            Choreography A replayed through prototype/live_script.py (live.py compose/place/emit, the real
                                 engine fills tiles, quotes and coverage). The rows are prototype/scripts/meet.json's rows re-timed to
                                 the V3 narration (vo/07_manager, 07_english, 07_manager2*), written to captures/meet_v3.json first.
                                 -> meet_v3.webm + meet_v3_timeline.json (beat_ss, beat_len, vo offsets, when each block became visible)
  crud    /?present=1&admin=1    Choreography B: the sentence and typing speed from prototype/scripts/crud.json typed into the real
                                 input, Enter (real POST /api/chat), the real Confirm (real POST /api/people). -> crud.webm + crud_timeline.json
  mirror  /?as=yui&present=1     Yui's page; a note typed under her manager's line and pressed (real POST /api/annotate). -> mirror.webm + mirror_timeline.json
  stage   /?present=1            The stage Meet video: scripts/stage_v3.json (holds for the live lines) through live_script.py.
                                 -> stage_v3.webm + stage_v3_timeline.json (marks for STAGE_CUES.md)

Each recording starts with --lead seconds of the page at rest. Timelines record when things were actually visible (polled every
50 ms), not the plan. The server it starts is stopped by its own PID at the end; a server it found running is left alone.
Run:  deck/video/pw/bin/python deck/video/v3/capture_ui.py [--port 8793] [--beats meet,crud,stage,mirror] [--m2 alt|full]
Needs prototype/.venv (live.py imports sounddevice and google-genai): `cd prototype && make setup`, or symlink the main checkout's.
"""
import argparse, asyncio, json, os, pathlib, shutil, socket, subprocess, sys, time, urllib.request
from playwright.async_api import async_playwright

D = pathlib.Path(__file__).resolve().parent
ROOT = D.parents[2]
PROTO = ROOT / "prototype"
VENV_PY = PROTO / ".venv" / "bin" / "python"
C, V, SCRIPTS = D / "captures", D / "vo", D / "scripts"
LIVE = PROTO / "state" / "live.jsonl"
REST = 1.0          # seconds of the page at rest at the top of the Meet beat before the status row
JCUT = 1.4          # the manager's first line starts this long before the Meet cut (over the receipts beat)
NOTE = "That location line was Okada's guess, not mine. Ask me first."
STAGE_L3 = "Actually, we also need someone good for this. Just someone good."


def log(*a):
    print(f"[capture {time.strftime('%H:%M:%S')}]", *a, flush=True)


def ffdur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout.strip())


def vo_dur(name):
    w = V / f"{name}.wav"
    if not w.exists():
        sys.exit(f"[capture] missing narration {w} (run narrate_v3.py first)")
    return ffdur(w)


def http(port, path, body=None):
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}", data=json.dumps(body).encode() if body is not None else None,
                                 method="POST" if body is not None else "GET", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


def listening(port):
    s = socket.socket(); s.settimeout(0.3)
    try:
        s.connect(("127.0.0.1", port)); return True
    except OSError:
        return False
    finally:
        s.close()


def ensure_server(port):
    """Reuse a server already answering on the port (must be this checkout's prototype: /api/company is checked), else start one."""
    if listening(port):
        try:
            http(port, "/api/company"); log(f"reusing the server on :{port}"); return None
        except Exception as e:  # noqa: BLE001
            sys.exit(f"[capture] :{port} is taken by something that is not the prototype ({e}); pick another --port")
    logf = (C / "_server.log").open("a")
    proc = subprocess.Popen([sys.executable if not VENV_PY.exists() else str(VENV_PY), "server.py"], cwd=str(PROTO),
                            env=dict(os.environ, PORT=str(port), MODE="heuristic", SPEAK="0"), stdout=logf, stderr=logf)
    for _ in range(60):
        time.sleep(0.25)
        if listening(port):
            try:
                http(port, "/api/company"); log(f"started server pid {proc.pid} on :{port}"); return proc
            except Exception:  # noqa: BLE001
                pass
    proc.terminate(); sys.exit("[capture] the server did not come up; see captures/_server.log")


def meet_rows(m2_choice):
    """prototype/scripts/meet.json's rows, re-timed to the V3 narration. Returns (rows, vo offsets in beat seconds, beat_len)."""
    src = json.loads((PROTO / "scripts" / "meet.json").read_text())["rows"]
    by = {}
    for r in src:
        k = r["op"] if r["op"] in ("compose", "conclude", "filed") else f"{r['op']}:{(r.get('block') or {}).get('id', '')}"
        if r["op"] in ("status", "heard"):
            k = f"{r['op']}:{sum(1 for x in src[:src.index(r)] if x['op'] == r['op'])}"
        by[k] = r
    need = ["status:0", "heard:0", "compose", "place:r1", "place:a1", "place:r2", "heard:2", "conclude", "filed", "status:1"]
    missing = [k for k in need if k not in by]
    if missing:
        sys.exit(f"[capture] prototype/scripts/meet.json changed shape; cannot find rows {missing} (keys: {sorted(by)})")
    m1, en = vo_dur("07_manager"), vo_dur("07_english")
    m2_id = "07_manager2_alt" if m2_choice == "alt" else "07_manager2"
    m2 = vo_dur(m2_id)
    # beat seconds
    e1 = m1 - JCUT                    # manager 1 ends
    t_en = e1 + 0.25                  # the narrator: the English point, over the receipts
    e2 = t_en + en
    t_m2 = e2 + 0.2                   # the manager concludes
    e3 = t_m2 + m2
    t_concl = e3 - 0.5                # the page polls every 0.8 s: a row lands ~0.6 s later, so the card shows as the last words land
    t_filed = t_concl + 0.8
    beat_len = round(t_concl + 2.3, 2)  # the conclusion card gets ~1.7 s, the filed line ~1.0 s
    t_mgr_receipt = max(t_en + 0.58 * en - 0.5, e1 + 3.2)  # Okada's note lands as the narrator reaches "Her manager wrote"
    heard2 = dict(by["heard:2"])
    if m2_choice == "alt":
        heard2["text"] = "Okay, let's set up calls with Yui and Kei this week, and ask Yui about that location note."
    plan = [  # (beat second, source row)
        (REST + 0.3, by["status:0"]), (REST + 1.2, by["heard:0"]), (REST + 3.2, by["compose"]), (REST + 5.0, by["place:r1"]),
        (max(REST + 7.3, t_en + 1.2), by["place:a1"]), (t_mgr_receipt, by["place:r2"]), (e3 - 0.6, heard2),
        (t_concl, by["conclude"]), (t_filed, by["filed"]), (t_concl + 2.4, by["status:1"]),
    ]
    rows = [dict(r, at=round(t - REST, 2)) for t, r in plan]  # script seconds = beat seconds - REST
    vo = {"07_manager": -JCUT, "07_english": round(t_en, 2), m2_id: round(t_m2, 2)}
    return rows, vo, beat_len, dict(m1=m1, en=en, m2=m2, m2_id=m2_id)


async def wait_marks(pg, checks, t0, marks, until, poll=0.05):
    """Poll the DOM until `until` seconds after t0; record the first second each named check is true."""
    pending = dict(checks)
    while time.time() < t0 + until and pending:
        for name, js in list(pending.items()):
            try:
                ok = await pg.evaluate(js)
            except Exception:  # noqa: BLE001
                ok = False
            if ok:
                marks[name] = round(time.time() - t0, 2); log(f"  {marks[name]:6.2f}s  {name}"); del pending[name]
        await asyncio.sleep(poll)
    for name in pending:
        log(f"  NOT SEEN: {name}")


async def new_page(pw, tmpdir):
    b = await pw.chromium.launch()
    ctx = await b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1,
                              record_video_dir=str(tmpdir), record_video_size={"width": 1920, "height": 1080})
    return b, ctx, await ctx.new_page()


async def settle_page(pg, url, lead):
    """goto, wait for the drawn page (the map's land paths and the status pill; the subject page has neither), then `lead` seconds at rest. Returns seconds since goto."""
    t_go = time.time()
    await pg.goto(url)
    await pg.wait_for_function("(document.querySelectorAll('#map svg path').length > 0 && !!(document.querySelector('#status')||{}).textContent) || document.body.classList.contains('subjectonly')", timeout=20000)
    await pg.wait_for_timeout(int(lead * 1000))
    return time.time() - t_go


async def replay(script_path, t0_hint=None):
    if not VENV_PY.exists():
        sys.exit(f"[capture] {VENV_PY} missing: `cd prototype && make setup` (live.py imports sounddevice and google-genai)")
    return subprocess.Popen([str(VENV_PY), str(PROTO / "live_script.py"), str(script_path)], cwd=str(PROTO),
                            env=dict(os.environ, MODE="heuristic", SPEAK="0"), stdout=(C / "_replay.log").open("a"), stderr=subprocess.STDOUT)


async def finish(pg, ctx, b, name):
    path = await pg.video.path()
    await ctx.close(); await b.close()
    dst = C / f"{name}.webm"; shutil.move(path, dst)
    log(f"wrote {dst} ({ffdur(dst):.1f}s)")
    return dst


# the Pik screen since f7d96aa: the heard line lives in the #inbar input, people are nodes on the map, a receipt adds its source hub
MEET_CHECKS = {
    "listening": "document.querySelector('#status') && /listening/i.test(document.querySelector('#status').textContent)",
    "question": "((document.querySelector('#ask')||{}).value||'').length > 20",
    "tiles": "document.querySelectorAll('#map .person').length >= 3",
    "own_words": "document.querySelectorAll('#map .hub').length >= 1",
    "ask": "!!document.querySelector('#askbar .asks')",
    "manager_note": "[...document.querySelectorAll('#map .hub text')].some(t => /note/i.test(t.textContent)) && /paraphrase/i.test((document.querySelector('#rcard')||{}).textContent||'')",
    "conclusion": "!!document.querySelector('#concl.on')",
    "filed": "!!document.querySelector('#concl .filed.on')",
}


async def cap_meet(pw, port, lead, m2_choice):
    rows, vo, beat_len, d = meet_rows(m2_choice)
    script = C / "meet_v3.json"
    script.write_text(json.dumps({"name": "meet_v3", "source": "prototype/scripts/meet.json re-timed by capture_ui.py to the V3 narration",
                                  "durations": d, "rows": rows}, indent=1, ensure_ascii=False))
    log(f"meet: m1 {d['m1']:.2f} en {d['en']:.2f} m2 {d['m2']:.2f} ({d['m2_id']}); beat {beat_len}s; rows at {[r['at'] for r in rows]}")
    http(port, "/api/reset", {"people": True}); LIVE.write_text(""); (PROTO / "state" / "annotations.json").write_text("[]")  # no note from a mirror take on the evaluator's page
    if True:
        b, ctx, pg = await new_page(pw, C / "_tmp")
        t_ctx = time.time()
        await settle_page(pg, f"http://127.0.0.1:{port}/?present=1", lead)
        proc = await replay(script)
        t0 = time.time(); settle = t0 - t_ctx
        marks = {}
        await wait_marks(pg, MEET_CHECKS, t0 - REST, marks, until=beat_len + 1.5)  # marks in beat seconds
        await asyncio.sleep(max(0, t0 + rows[-1]["at"] + 1.5 - time.time()))
        if proc.poll() is None:
            proc.terminate()
        dst = await finish(pg, ctx, b, "meet_v3")
    tl = dict(beat_ss=round(settle - REST, 3), beat_len=beat_len, rest=REST, jcut=JCUT, vo=vo, durations=d, marks=marks,
              rows=[(r["at"] + REST, r["op"], (r.get("block") or {}).get("id", "")) for r in rows], webm=dst.name, recorded=time.strftime("%Y-%m-%d %H:%M:%S"))
    (C / "meet_v3_timeline.json").write_text(json.dumps(tl, indent=1))
    log("wrote captures/meet_v3_timeline.json")


async def cap_crud(pw, port, lead):
    spec = http(port, "/scripts/crud.json")
    sentence, tms = spec["sentence"], int(spec.get("type_ms", 22))
    http(port, "/api/reset", {"people": True}); LIVE.write_text("")
    if True:
        b, ctx, pg = await new_page(pw, C / "_tmp")
        t_ctx = time.time()
        await settle_page(pg, f"http://127.0.0.1:{port}/?present=1&admin=1", lead)
        await pg.evaluate("S.source='scripted';renderFoot()")  # the footer badge the page's own ?take=crud sets
        inp = pg.locator("#ask")
        await inp.click(); await inp.fill("")
        n_before = await pg.evaluate("document.querySelectorAll('#map .person').length")
        t0 = time.time(); settle = t0 - t_ctx
        marks = {"type_start": 0.0}
        await inp.type(sentence, delay=tms)
        marks["type_end"] = round(time.time() - t0, 2)
        await asyncio.sleep(0.1)
        await pg.keyboard.press("Enter"); marks["enter"] = round(time.time() - t0, 2)
        await wait_marks(pg, {"draft": "!!document.querySelector('#draft.on') && !!document.querySelector('#confirm')"}, t0, marks, until=6)
        await asyncio.sleep(0.8)
        await pg.click("#confirm"); marks["confirm"] = round(time.time() - t0, 2)
        await wait_marks(pg, {"added": "/added by/i.test((document.querySelector('#rcard')||{}).textContent||'')",
                              "node_home": f"document.querySelectorAll('#map .person').length >= {n_before + 1}"}, t0, marks, until=6)
        await asyncio.sleep(2.5)
        dst = await finish(pg, ctx, b, "crud")
    http(port, "/api/reset", {"people": True})  # Mika Ono leaves with the take; the next page load counts 200 again
    tl = dict(beat_ss=round(settle - 0.3, 3), marks=marks, sentence=sentence, type_ms=tms, webm=dst.name, recorded=time.strftime("%Y-%m-%d %H:%M:%S"))
    (C / "crud_timeline.json").write_text(json.dumps(tl, indent=1)); log("wrote captures/crud_timeline.json", marks)


async def cap_mirror(pw, port, lead):
    ann = PROTO / "state" / "annotations.json"
    ann.write_text("[]")
    if True:
        b, ctx, pg = await new_page(pw, C / "_tmp")
        t_ctx = time.time()
        await settle_page(pg, f"http://127.0.0.1:{port}/?as=yui&present=1", lead)
        stubs = pg.locator(".stub")
        n = await stubs.count()
        target = stubs.first
        for i in range(n):  # the manager's line about location, if the subject page shows it; else her own words
            txt = (await stubs.nth(i).inner_text()).lower()
            if "flexible on location" in txt or "loves travel" in txt:
                target = stubs.nth(i); break
        t0 = time.time(); settle = t0 - t_ctx
        marks = {}
        await target.scroll_into_view_if_needed(); await asyncio.sleep(0.6)
        inp = target.locator('input[id^="an-"]').first
        await inp.click(); marks["type_start"] = round(time.time() - t0, 2)
        await inp.type(NOTE, delay=38); marks["type_end"] = round(time.time() - t0, 2)
        await asyncio.sleep(0.5)
        await inp.locator("xpath=following-sibling::button[1]").click(); marks["press"] = round(time.time() - t0, 2)
        await wait_marks(pg, {"landed": "document.querySelectorAll('.note').length > 0"}, t0, marks, until=6)
        await asyncio.sleep(2.5)
        dst = await finish(pg, ctx, b, "mirror")
    tl = dict(settle=round(settle, 3), beat_ss=round(settle + marks["press"] - 1.6, 3), marks=marks, note=NOTE, webm=dst.name, recorded=time.strftime("%Y-%m-%d %H:%M:%S"))
    (C / "mirror_timeline.json").write_text(json.dumps(tl, indent=1)); log("wrote captures/mirror_timeline.json", marks)


STAGE_CHECKS = {
    "tiles": MEET_CHECKS["tiles"],
    "chips": "document.querySelectorAll('#map .kw.constraint').length >= 2",  # constraints are keyword nodes with a lock glyph
    "ask": MEET_CHECKS["ask"],
    "receipts": "document.querySelectorAll('#map .hub').length >= 2",  # her own words and Okada's note, each a source hub on the map
    "conclusion": MEET_CHECKS["conclusion"],
    "filed": MEET_CHECKS["filed"],
}


async def cap_stage(pw, port, lead):
    script = SCRIPTS / "stage_v3.json"
    spec = json.loads(script.read_text())
    ask_text = next(r["block"]["text"] for r in spec["rows"] if r["op"] == "place" and r["block"].get("type") == "ask")
    sys.path.insert(0, str(PROTO)); os.environ.setdefault("MODE", "heuristic")
    import engine  # noqa: E402
    live_fu = engine.ask(STAGE_L3)["follow_up"]
    if live_fu != ask_text:
        log(f"WARNING: engine.ask(L3) now asks {live_fu!r}, the stage script and vo/stage_followup.wav say {ask_text!r}; update both")
    end = float(spec.get("duration", 78.0))
    http(port, "/api/reset", {"people": True}); LIVE.write_text(""); (PROTO / "state" / "annotations.json").write_text("[]")  # the stage line asks Yui; her note must not already be on screen
    if True:
        b, ctx, pg = await new_page(pw, C / "_tmp")
        t_ctx = time.time()
        await settle_page(pg, f"http://127.0.0.1:{port}/?present=1", lead)
        proc = await replay(script)
        t0 = time.time(); settle = t0 - t_ctx
        marks = {}
        await wait_marks(pg, STAGE_CHECKS, t0, marks, until=end)
        await asyncio.sleep(max(0, t0 + end + 0.8 - time.time()))
        if proc.poll() is None:
            proc.terminate()
        dst = await finish(pg, ctx, b, "stage_v3")
    tl = dict(settle=round(settle, 3), end=end, follow_up=ask_text, engine_follow_up=live_fu, marks=marks, lines=spec["lines"],
              cues=[(r["at"], r["op"]) for r in spec["rows"]], webm=dst.name, recorded=time.strftime("%Y-%m-%d %H:%M:%S"))
    (C / "stage_v3_timeline.json").write_text(json.dumps(tl, indent=1)); log("wrote captures/stage_v3_timeline.json", marks)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8793)
    ap.add_argument("--beats", default="meet,crud,stage,mirror", help="mirror last: its note persists in state/annotations.json")
    ap.add_argument("--lead", type=float, default=2.5, help="seconds at rest before anything moves")
    ap.add_argument("--m2", default="alt", choices=["alt", "full"], help="the manager's closing line: alt (shorter, 18 words) or the full meet.json line")
    a = ap.parse_args()
    C.mkdir(exist_ok=True); (C / "_tmp").mkdir(exist_ok=True)
    proc = ensure_server(a.port)
    try:
        async with async_playwright() as pw:
            for beat in [x.strip() for x in a.beats.split(",") if x.strip()]:
                log(f"== {beat}")
                await {"meet": cap_meet, "crud": cap_crud, "mirror": cap_mirror, "stage": cap_stage}[beat](pw, a.port, a.lead, *([a.m2] if beat == "meet" else []))
    finally:
        if proc is not None:
            proc.terminate(); log(f"stopped server pid {proc.pid}")
        shutil.rmtree(C / "_tmp", ignore_errors=True)
    # what is on disk now, so a stale capture is obvious: each timeline's `recorded` stamp next to its webm's mtime
    log("== captures on disk")
    for name in ("meet_v3", "crud", "stage_v3", "mirror"):
        tl, wv = C / f"{name}_timeline.json", C / f"{name}.webm"
        rec = json.loads(tl.read_text()).get("recorded", "?") if tl.exists() else "no timeline"
        mt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(wv.stat().st_mtime)) if wv.exists() else "no webm"
        stale = "" if tl.exists() and wv.exists() and abs(wv.stat().st_mtime - time.mktime(time.strptime(rec, "%Y-%m-%d %H:%M:%S"))) < 120 else "   <- STALE or missing"
        log(f"  {name:9s} recorded {rec}   webm {mt}{stale}")


if __name__ == "__main__":
    asyncio.run(main())
