"""Tiny stdlib HTTP server for the evidence-layer demo. No framework needed.

Run:  python3 server.py            (http://localhost:8787)
Env:  MODE=heuristic|gemini|auto  PORT=8787
"""
from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

sys.path.insert(0, str(Path(__file__).parent))
import engine  # noqa: E402
import auth  # noqa: E402  (signed sessions; only enforced when PIK_AUTH=1)

HERE = Path(__file__).parent
UI = HERE / "ui"
SCRIPTS = HERE / "scripts"
VENDOR = UI / "vendor"
PORT = int(os.environ.get("PORT", "8787"))
VENV_PY = HERE / ".venv" / "bin" / "python"
TAKE = {"proc": None, "name": None}  # one transcript replay running at a time
TAKE_LOCK = threading.Lock()  # ThreadingHTTPServer: two POST /api/take at once must not both spawn


class BadRequest(ValueError):
    pass


def _spawn_take(name: str):
    """Truncate state/live.jsonl and replay scripts/<name>.json through live_script.py (needs the venv: live.py imports sounddevice and genai).
    One take at a time: a running replay is terminated first, and the spawn is serialised so a double-fired POST cannot start two."""
    if not re.fullmatch(r"[a-z0-9_]{1,40}", name):
        raise ValueError("take names are lowercase letters, digits and underscore")
    script = SCRIPTS / f"{name}.json"
    if not script.is_file():
        raise FileNotFoundError(f"no scripts/{name}.json")
    py = VENV_PY if VENV_PY.exists() else Path(sys.executable)
    with TAKE_LOCK:
        old = TAKE["proc"]
        if old is not None and old.poll() is None:
            old.terminate()
            try:
                old.wait(timeout=2)
            except subprocess.TimeoutExpired:
                old.kill()
        (engine.STATE / "live.jsonl").write_text("")
        env = dict(os.environ, MODE=engine.MODE if engine.MODE != "auto" else "heuristic", SPEAK="0")
        proc = subprocess.Popen([str(py), str(HERE / "live_script.py"), str(script)], cwd=str(HERE), env=env,
                                stdout=sys.stderr, stderr=sys.stderr)
        TAKE["proc"], TAKE["name"] = proc, name
        return proc.pid


def _take_state():
    proc = TAKE["proc"]
    code = proc.poll() if proc is not None else None
    return {"name": TAKE["name"], "running": bool(proc is not None and code is None), "pid": proc.pid if proc else None,
            "exit_code": code, "python": str(VENV_PY if VENV_PY.exists() else sys.executable), "venv": VENV_PY.exists()}


# ---- the meeting surfaces: Join Meet / Open Slack / Open task board, and the listener the page starts (one at a time) ----
LISTEN = {"proc": None}  # the live.py this server started (the page's mic button)
LISTEN_LOCK = threading.Lock()  # two clicks at once must not start two listeners (three at once caused chaos before)
LISTENER_RX = re.compile(r"(^|[ /])live\.py(\s|$)")  # live.py, never live_script.py or live_sim.py
LISTENER_LOG = engine.STATE / "listener.log"
LISTENER_PID = engine.STATE / "listener.pid"  # so a restarted server still knows the page started it
_SETTINGS = {}
_SETTINGS_LOCK = threading.Lock()


def _settings():
    """PIK_* settings as surfaces/_env.py resolves them (process env first, then <repo>/.env, prototype/.env,
    ~/.config/carl-life-os/.env), read once. The loader writes into os.environ; the keys it added are taken back out,
    so the tokens in those files never reach this server's children."""
    with _SETTINGS_LOCK:
        return _settings_locked()


def _settings_locked():
    if not _SETTINGS:
        before = set(os.environ)
        sys.path.insert(0, str(HERE / "surfaces"))
        try:
            import _env  # noqa: F401
        finally:
            sys.path.remove(str(HERE / "surfaces"))
        _SETTINGS.update({k: v for k, v in os.environ.items() if k.startswith("PIK_")})
        _SETTINGS["_loaded"] = "1"
        for k in set(os.environ) - before:
            os.environ.pop(k, None)
    return _SETTINGS


def _notion_url(db: str):
    """PIK_NOTION_DB as a link: a URL or a 32-hex id (dashes allowed) -> https://www.notion.so/<id>; a URL without one is used as is."""
    db = (db or "").strip()
    m = re.search(r"[0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{12}", db)
    if m and (db.startswith(("http://", "https://")) or m.group(0) == db):
        return "https://www.notion.so/" + m.group(0).replace("-", "")
    return db if db.startswith(("http://", "https://")) else "https://www.notion.so"


def _ps():
    """(pid, command line) for every process; raises when ps cannot run (then nothing is claimed about what runs)."""
    r = subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True, text=True, timeout=5)
    if r.returncode != 0:
        raise RuntimeError(f"ps failed: {r.stderr.strip()[:120]}")
    rows = []
    for line in r.stdout.splitlines():
        pid, _, cmd = line.strip().partition(" ")
        if pid.isdigit():
            rows.append((int(pid), cmd.strip()))
    return rows


def _is_listener(cmd: str):
    """live.py run by a Python interpreter; a shell, an editor or `grep ... live.py` naming the file is not a listener."""
    return "python" in cmd.split(" ", 1)[0].rsplit("/", 1)[-1].lower() and bool(LISTENER_RX.search(cmd))


def _page_pid():
    proc = LISTEN["proc"]
    if proc is not None:
        if proc.poll() is None:
            return proc.pid
        LISTEN["proc"] = None
    try:
        return int(LISTENER_PID.read_text().strip())
    except (OSError, ValueError):
        return None


def _listener_state(ps=None):
    mine = _page_pid()
    found = [pid for pid, cmd in (ps if ps is not None else _ps()) if _is_listener(cmd) and pid != os.getpid()]
    if not found:
        return {"running": False, "pid": None, "started_by": None}
    pid = mine if mine in found else found[0]
    return {"running": True, "pid": pid, "started_by": "page" if pid == mine else "external"}


def _log_tail(n=5):
    try:
        return engine.redact("\n".join(LISTENER_LOG.read_text(errors="replace").splitlines()[-n:]))
    except OSError:
        return ""


def _listen_on():
    with LISTEN_LOCK:
        st = _listener_state()
        if st["running"]:  # page or external: never a second one
            return dict(ok=True, **st)
        if not VENV_PY.exists():
            return {"ok": False, "running": False, "pid": None, "started_by": None, "error": "run make setup first"}
        cfg = _settings()
        env = dict(os.environ, MODE="heuristic", SPEAK=cfg.get("PIK_LISTEN_SPEAK") or "1", PYTHONUNBUFFERED="1")
        if cfg.get("PIK_MIC"):
            env["MIC"] = cfg["PIK_MIC"]
        if not env.get("GOOGLE_APPLICATION_CREDENTIALS"):  # the Makefile's ADC default, so the button works like `make live`
            adc = [c for c in (Path.home() / ".config/carl-life-os/gcloud-tmuc/application_default_credentials.json",
                               Path.home() / ".config/gcloud/application_default_credentials.json") if c.is_file()]
            if adc:
                env["GOOGLE_APPLICATION_CREDENTIALS"] = str(adc[0])
        with LISTENER_LOG.open("w") as log:
            proc = subprocess.Popen([str(VENV_PY), "live.py"], cwd=str(HERE), env=env, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT)
        LISTEN["proc"] = proc
        LISTENER_PID.write_text(str(proc.pid))
        end = time.time() + 3
        while time.time() < end and proc.poll() is None:
            time.sleep(0.1)
        if proc.poll() is not None:
            LISTEN["proc"] = None
            LISTENER_PID.unlink(missing_ok=True)
            return {"ok": False, "running": False, "pid": None, "started_by": None,
                    "error": _log_tail() or f"the listener exited with code {proc.returncode} and wrote nothing to state/listener.log"}
        return {"ok": True, "running": True, "pid": proc.pid, "started_by": "page"}


def _stop_page_listener(pid):
    """SIGINT (live.py stops its stream and prints 'stopped'), SIGKILL after 3 s."""
    proc = LISTEN["proc"]
    if proc is not None and proc.pid == pid:
        proc.send_signal(signal.SIGINT)
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=3)
    else:  # started by this page under an earlier server run: not our child, so poll it
        try:
            os.kill(pid, signal.SIGINT)
            end = time.time() + 3
            while time.time() < end:
                os.kill(pid, 0)
                time.sleep(0.1)
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    LISTEN["proc"] = None
    LISTENER_PID.unlink(missing_ok=True)


def _listen_off():
    """(http code, body). Stops only what the page started; an external listener belongs to its terminal."""
    with LISTEN_LOCK:
        st = _listener_state()
        if not st["running"]:
            LISTENER_PID.unlink(missing_ok=True)
            return 200, dict(ok=True, **st)
        if st["started_by"] == "external":
            return 409, dict(ok=False, error="the listener was started outside the page; stop it with Ctrl-C in its terminal", **st)
        _stop_page_listener(st["pid"])
        st = _listener_state()
        return 200, dict(ok=st["started_by"] != "page", **st)


def _surfaces():
    cfg = _settings()
    ps = _ps()
    return {"meet": {"url": cfg.get("PIK_MEET_URL") or "https://meet.google.com/new"},
            "slack": {"url": cfg.get("PIK_SLACK_URL") or "https://slack.com/signin", "running": any("surfaces/slack_bot.py" in c for _, c in ps)},
            "notion": {"url": cfg.get("PIK_NOTION_URL") or _notion_url(cfg.get("PIK_NOTION_DB", "")), "running": any("surfaces/notion_board.py" in c for _, c in ps)},
            "listener": _listener_state(ps)}


class H(BaseHTTPRequestHandler):
    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _text(self, s, ctype="text/plain; charset=utf-8", code=200):
        body = s.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _file(self, f: Path, ctype: str, cache=True):
        if not f.is_file():
            return self._json({"error": "not found"}, 404)
        body = f.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        if cache:
            self.send_header("Cache-Control", "public, max-age=86400")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        return self.wfile.write(body)

    # ---- sessions (additive: with PIK_AUTH unset and no cookie, every branch below is a no-op) ----
    def _session(self):
        if not hasattr(self, "_sess"):
            self._sess = auth.from_headers(self.headers)
        return self._sess

    def _redirect(self, location, cookie=None):
        self.send_response(302)
        self.send_header("Location", location)
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _gate(self, path):
        """PIK_AUTH=1: no session -> pages go to /login, APIs get a 401 with the login path. Returns True when handled."""
        if not auth.AUTH or auth.is_public(path) or self._session():
            return False
        if path.startswith("/api/"):
            self._json({"error": "sign in first", "login": "/login"}, 401)
        else:
            self._redirect("/login?next=" + self.path.replace("&", "%26"))
        return True

    def _subject(self):
        """The signed-in subject's id, or None (an evaluator, a guest, or no session)."""
        s = self._session()
        return s["id"] if s and s.get("role") == "subject" else None

    def _page(self, name):
        return self._text((UI / name).read_text(), "text/html; charset=utf-8")

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        try:
            b = json.loads(self.rfile.read(n) or b"{}")
        except (ValueError, UnicodeDecodeError) as e:
            raise BadRequest(f"body is not JSON: {str(e)[:80]}")
        if not isinstance(b, dict):
            raise BadRequest("body must be a JSON object")
        return b

    def log_message(self, fmt, *args):  # quieter
        sys.stderr.write("%s %s\n" % (self.command, self.path))

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        p = u.path
        try:
            if p == "/api/context":  # public: the sign-in card shows it before anyone has a session
                return self._json(engine.context())
            if self._gate(p):
                return
            subj = self._subject()
            if p in ("/", "/index.html"):
                if subj and q.get("as", [""])[0] != subj:  # a signed-in subject gets their own page, nothing else
                    q2 = dict(q, **{"as": [subj]})
                    return self._redirect("/?" + urlencode({k: v[0] for k, v in q2.items()}))
                return self._page("index.html")
            if p == "/login":
                return self._page("login.html")
            if p == "/logout":
                return self._redirect("/login", auth.set_cookie_header(None))
            if p == "/settings":
                if subj:
                    return self._json({"error": "settings are for evaluators"}, 403)
                return self._page("settings.html")
            if p == "/stats":
                return self._page("stats.html")
            if p == "/api/session":
                s = self._session()
                return self._json({"session": s, "auth_required": auth.AUTH, "people": auth.people(),
                                   "extraction": engine.extraction_status(), "backend": engine.backend_name()})
            if p == "/api/byok":
                if subj:
                    return self._json({"error": "settings are for evaluators"}, 403)
                return self._json(engine.byok_public())
            if p == "/api/stats":
                return self._json(engine.stats())
            if p == "/api/surfaces":
                return self._json(_surfaces())
            if p.startswith("/api/source/"):
                if subj:
                    return self._json({"error": "the subject sees only their own page"}, 403)
                kind = p[len("/api/source/"):]
                if kind not in engine.SOURCE_KINDS:
                    return self._json({"error": f"unknown source {kind!r}; one of {sorted(engine.SOURCE_KINDS)}"}, 404)
                try:
                    limit = int(q.get("limit", ["50"])[0] or 50)
                except ValueError:
                    raise BadRequest("limit must be a whole number")
                return self._json(engine.source_items(kind, limit, q.get("q", [""])[0], q.get("person", [""])[0]))
            if subj and (p in ("/api/people", "/api/graph", "/api/cities") or (p.startswith("/api/people/") and p.rsplit("/", 1)[1] != subj)
                         or (p.startswith("/api/evidence/") and p.rsplit("/", 1)[1] != subj) or (p.startswith("/api/memo/") and p.rsplit("/", 1)[1] != subj)):
                return self._json({"error": "the subject sees only their own page"}, 403)
            if p.startswith("/fonts/") and p.endswith(".woff2") and "/" not in p[7:]:
                return self._file(UI / "fonts" / p[7:], "font/woff2")
            if p.startswith("/vendor/") and re.fullmatch(r"[A-Za-z0-9_.-]+\.(js|json)", p[8:]):
                return self._file(VENDOR / p[8:], "application/javascript; charset=utf-8" if p.endswith(".js") else "application/json; charset=utf-8")
            if p.startswith("/scripts/") and re.fullmatch(r"[A-Za-z0-9_]+\.json", p[9:]):
                return self._file(SCRIPTS / p[9:], "application/json; charset=utf-8", cache=False)
            if p == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
                return
            if p == "/api/company":
                c = engine.load("company.json")
                c["backend"] = engine.backend_name()
                if subj:
                    q = dict(q, view=["subject"], cid=[subj])
                if q.get("view", [""])[0] == "subject":
                    # the subject sees only themselves: no other candidates, no tag scores, no ranking
                    cid = q.get("cid", [""])[0]
                    c["candidates"] = [x for x in c["candidates"] if x["id"] == cid]
                    if not c["candidates"]:
                        gp = engine.get_person(cid)  # generated or added people have a page too
                        if not gp:
                            return self._json({"error": "unknown subject"}, 404)
                        c["candidates"] = [{"id": gp["id"], "name": gp["name"], "role": gp["role"], "team": gp["team"], "manager": None, "tenure_years": gp.get("tenure_years")}]
                    c.pop("tag_scores", None)
                    c["view"] = "subject"
                return self._json(c)
            if p == "/api/people":
                qq = q.get("q", [""])[0].lower()
                rows = [{k: v for k, v in x.items() if k != "receipts"} for x in engine.people() if not qq or qq in (x["name"] + " " + x["role"] + " " + x["team"]).lower()]
                return self._json({"count": len(rows), "people": rows[:int(q.get("limit", ["1000"])[0])]})
            if p.startswith("/api/people/"):
                pid = p.rsplit("/", 1)[1]
                gp = engine.get_person(pid)
                return self._json(gp) if gp else self._json({"error": "unknown person"}, 404)
            if p == "/api/cities":
                return self._json(engine.cities())
            if p == "/api/graph":
                return self._json(engine.graph())
            if p == "/api/audit":
                return self._json(engine.audit())
            if p == "/api/live":
                f = engine.STATE / "live.jsonl"
                rows = [json.loads(l) for l in f.read_text().splitlines() if l.strip()] if f.exists() else []
                since = float(q.get("since", ["0"])[0])
                return self._json({"events": [r for r in rows if r["t"] > since], "now": max([r["t"] for r in rows], default=0)})
            if p.startswith("/api/evidence/"):
                cid = p.rsplit("/", 1)[1]
                force = q.get("force", ["0"])[0] == "1"
                mode = q.get("mode", [None])[0]
                try:
                    ev = engine.extract_claims(cid, force=force, mode=mode)
                except engine.LLMUnavailable as e:
                    return self._json({"error": str(e), "code": "llm_unavailable"}, 503)
                items = {it["id"]: dict(it, rendered=engine.item_text(it)) for it in engine.items_for(cid)}
                return self._json({"evidence": ev, "items": items, "annotations": [a for a in engine.annotations() if a["candidate"] == cid]})
            if p.startswith("/api/memo/"):
                cid = p.rsplit("/", 1)[1]
                return self._text(engine.memo(cid, q.get("criterion", [None])[0]), "text/markdown; charset=utf-8")
            if p == "/api/annotations":
                return self._json([a for a in engine.annotations() if not subj or a["candidate"] == subj])
            if p == "/api/take":
                return self._json(_take_state())
            return self._json({"error": "not found"}, 404)
        except BadRequest as e:
            return self._json({"error": str(e)}, 400)
        except Exception as e:  # noqa: BLE001
            return self._json({"error": f"{type(e).__name__}: {e}"}, 500)

    def do_POST(self):
        u = urlparse(self.path)
        p = u.path
        try:
            if self._gate(p):
                return
            b = self._body()
            subj = self._subject()
            if p == "/api/login":
                try:
                    s = auth.new_session(str(b.get("who") or ""), str(b.get("workspace") or "Kaede Works"))
                except ValueError as e:
                    return self._json({"error": str(e)}, 400)
                body = json.dumps({"ok": True, "session": s, "next": f"/?as={s['id']}" if s["role"] == "subject" else "/"}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Set-Cookie", auth.set_cookie_header(s))
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                return self.wfile.write(body)
            if p == "/api/logout":
                body = b'{"ok": true}'
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Set-Cookie", auth.set_cookie_header(None))
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                return self.wfile.write(body)
            if p == "/api/byok":
                if subj:
                    return self._json({"error": "settings are for evaluators"}, 403)
                if b.get("clear"):
                    return self._json(engine.clear_byok())
                try:
                    return self._json(engine.save_byok(str(b.get("kind") or "api"), str(b.get("api_key") or ""), str(b.get("project") or ""), str(b.get("location") or "")))
                except ValueError as e:
                    return self._json({"error": str(e)}, 400)
            if p == "/api/byok/test":
                if subj:
                    return self._json({"error": "settings are for evaluators"}, 403)
                return self._json(engine.test_key())
            if p == "/api/listen":
                if subj:
                    return self._json({"error": "the subject never starts the listener"}, 403)
                if not isinstance(b.get("on"), bool):
                    raise BadRequest('send {"on": true} or {"on": false}')
                if b["on"]:
                    return self._json(_listen_on())
                code, body = _listen_off()
                return self._json(body, code)
            if p == "/api/end":
                if subj:
                    return self._json({"error": "the subject never sees the ask or the memo of the meeting"}, 403)
                stopped = False
                with LISTEN_LOCK:
                    st = _listener_state()
                    if st["running"] and st["started_by"] == "page":
                        _stop_page_listener(st["pid"])
                        stopped = True
                kind, src = engine.end_source()
                if not kind:
                    return self._json({"ok": False, "error": "nothing to summarise yet: ask Pik something first", "listener_stopped": stopped})
                return self._json(dict(ok=True, **engine.meeting_memo(kind, src), listener_stopped=stopped))
            if subj and p in ("/api/ask", "/api/rank", "/api/chat", "/api/people", "/api/take", "/api/reset", "/api/snapshot"):
                return self._json({"error": "the subject never sees the ask, the ranking or the records"}, 403)
            if p == "/api/rank":
                if b.get("view") == "subject" or u.query.find("view=subject") >= 0:
                    return self._json({"error": "the subject never sees a ranking"}, 403)
                return self._json(engine.rank(b.get("criterion", "")))
            if p == "/api/annotate":
                if subj and b.get("candidate") != subj:
                    return self._json({"error": "a note goes on your own page"}, 403)
                return self._json(engine.annotate(b["candidate"], b["source_id"], subj or b.get("author", "subject"), b["text"]))
            if p == "/api/snapshot":
                # dev only: the page posts a PNG data URL of itself (html2canvas) for deck stills
                import base64, re as _re
                name = _re.sub(r"[^a-z0-9_-]", "", (b.get("name") or "still").lower())
                data = b.get("data", "")
                if "," in data:
                    out = Path(__file__).parent.parent / "deck" / "assets" / f"{name}.png"
                    out.parent.mkdir(parents=True, exist_ok=True)
                    out.write_bytes(base64.b64decode(data.split(",", 1)[1]))
                    return self._json({"ok": True, "path": str(out), "bytes": out.stat().st_size})
                return self._json({"error": "no data"}, 400)
            if p == "/api/ask":
                if b.get("view") == "subject" or u.query.find("view=subject") >= 0:
                    return self._json({"error": "the subject never sees the ask"}, 403)
                pool = b.get("pool")
                pool = [str(x) for x in pool] if isinstance(pool, list) and pool else None
                t0 = time.time()
                a = engine.ask(b.get("question", ""), b.get("context", ""), b.get("requester"), int(b.get("k", 3)), pool)
                # the ask log (stats): the surface names itself; older surfaces are recognised by what they always sent
                surface = b.get("surface") or ("notion" if b.get("requester") == "notion" else "slack" if b.get("context") == "slack" else "api")
                engine.log_ask(str(surface), b.get("question", ""), (time.time() - t0) * 1000, a)
                return self._json(a)
            if p == "/api/chat":
                fn = engine.parse_command_llm if engine.MODE == "gemini" else engine.parse_command
                t0 = time.time()
                d = fn(b.get("text", ""), b.get("requester"))
                if isinstance(d, dict) and d.get("intent") == "ask" and isinstance(d.get("ask"), dict):  # the page's input bar asks through here
                    engine.log_ask(str(b.get("surface") or "page"), b.get("text", ""), (time.time() - t0) * 1000, d["ask"])
                return self._json(d)
            if p == "/api/people":
                try:
                    person = engine.add_person(b, b.get("requester") or b.get("by"), b.get("said"))
                except engine.RecordError as e:
                    return self._json({"error": str(e), "missing": e.missing}, e.code)
                return self._json({"person": person}, 201)
            if p == "/api/take":
                try:
                    pid = _spawn_take(str(b.get("name") or "meet"))
                except (ValueError, FileNotFoundError) as e:
                    return self._json({"error": str(e)}, 400 if isinstance(e, ValueError) else 404)
                return self._json({"ok": True, "pid": pid, "name": TAKE["name"], "venv": VENV_PY.exists()})
            if p == "/api/view":
                return self._json({"views": engine.views(b["candidate"]), "ok": bool(engine.record_view(b["candidate"], b.get("who", "evaluator")))})
            if p == "/api/reset":
                engine.reset(people_only=bool(b.get("people")))
                return self._json({"ok": True, "scope": "people" if b.get("people") else "all"})
            return self._json({"error": "not found"}, 404)
        except BadRequest as e:
            return self._json({"error": str(e)}, 400)
        except Exception as e:  # noqa: BLE001
            return self._json({"error": f"{type(e).__name__}: {e}"}, 500)

    def do_PATCH(self):
        p = urlparse(self.path).path
        try:
            if self._gate(p):
                return
            if self._subject():
                return self._json({"error": "the subject never edits the records"}, 403)
            b = self._body()
            if p.startswith("/api/people/"):
                pid = p.rsplit("/", 1)[1]
                try:
                    person, changed = engine.edit_person(pid, b, b.get("requester") or b.get("by"), b.get("said"))
                except engine.RecordError as e:
                    return self._json({"error": str(e), "missing": e.missing}, e.code)
                return self._json({"person": person, "changed": changed})
            return self._json({"error": "not found"}, 404)
        except BadRequest as e:
            return self._json({"error": str(e)}, 400)
        except Exception as e:  # noqa: BLE001
            return self._json({"error": f"{type(e).__name__}: {e}"}, 500)

    def do_DELETE(self):
        u = urlparse(self.path)
        p = u.path
        q = parse_qs(u.query)
        try:
            if self._gate(p):
                return
            if self._subject():
                return self._json({"error": "the subject never edits the records"}, 403)
            b = self._body() if self.headers.get("Content-Length") else {}
            if p.startswith("/api/people/"):
                pid = p.rsplit("/", 1)[1]
                try:
                    removed = engine.remove_person(pid, b.get("requester") or b.get("by") or q.get("requester", [None])[0], b.get("said"))
                except engine.RecordError as e:
                    return self._json({"error": str(e)}, e.code)
                return self._json({"ok": True, "removed": removed})
            return self._json({"error": "not found"}, 404)
        except BadRequest as e:
            return self._json({"error": str(e)}, 400)
        except Exception as e:  # noqa: BLE001
            return self._json({"error": f"{type(e).__name__}: {e}"}, 500)


if __name__ == "__main__":
    print(f"evidence layer demo: http://localhost:{PORT}  backend={engine.backend_name()}  mode={engine.MODE}  auth={'on (PIK_AUTH=1)' if auth.AUTH else 'off'}  {engine.extraction_status()}")
    ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
