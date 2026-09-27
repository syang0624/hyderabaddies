"""Tiny stdlib HTTP server for the evidence-layer demo. No framework needed.

Run:  python3 server.py            (http://localhost:8787)
Env:  MODE=heuristic|gemini|auto  PORT=8787
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).parent))
import engine  # noqa: E402

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
            if p in ("/", "/index.html"):
                return self._text((UI / "index.html").read_text(), "text/html; charset=utf-8")
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
                return self._json(engine.annotations())
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
            b = self._body()
            if p == "/api/rank":
                if b.get("view") == "subject" or u.query.find("view=subject") >= 0:
                    return self._json({"error": "the subject never sees a ranking"}, 403)
                return self._json(engine.rank(b.get("criterion", "")))
            if p == "/api/annotate":
                return self._json(engine.annotate(b["candidate"], b["source_id"], b.get("author", "subject"), b["text"]))
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
                return self._json(engine.ask(b.get("question", ""), b.get("context", ""), b.get("requester"), int(b.get("k", 3)), pool))
            if p == "/api/chat":
                fn = engine.parse_command_llm if engine.MODE == "gemini" else engine.parse_command
                return self._json(fn(b.get("text", ""), b.get("requester")))
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
    print(f"evidence layer demo: http://localhost:{PORT}  backend={engine.backend_name()}  mode={engine.MODE}")
    ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
