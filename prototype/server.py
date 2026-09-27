"""Tiny stdlib HTTP server for the evidence-layer demo. No framework needed.

Run:  python3 server.py            (http://localhost:8787)
Env:  MODE=heuristic|gemini|auto  PORT=8787
"""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).parent))
import engine  # noqa: E402

UI = Path(__file__).parent / "ui"
PORT = int(os.environ.get("PORT", "8787"))


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

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

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
                f = UI / "fonts" / p[7:]
                if not f.is_file():
                    return self._json({"error": "not found"}, 404)
                body = f.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "font/woff2")
                self.send_header("Cache-Control", "public, max-age=86400")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                return self.wfile.write(body)
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
                        return self._json({"error": "unknown subject"}, 404)
                    c.pop("tag_scores", None)
                    c["view"] = "subject"
                return self._json(c)
            if p == "/api/people":
                qq = q.get("q", [""])[0].lower()
                rows = [{k: v for k, v in x.items() if k != "receipts"} for x in engine.people() if not qq or qq in (x["name"] + " " + x["role"] + " " + x["team"]).lower()]
                return self._json({"count": len(rows), "people": rows[:int(q.get("limit", ["50"])[0])]})
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
            return self._json({"error": "not found"}, 404)
        except Exception as e:  # noqa: BLE001
            return self._json({"error": f"{type(e).__name__}: {e}"}, 500)

    def do_POST(self):
        p = urlparse(self.path).path
        try:
            b = self._body()
            if p == "/api/rank":
                if b.get("view") == "subject" or urlparse(self.path).query.find("view=subject") >= 0:
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
                return self._json(engine.ask(b.get("question", ""), b.get("context", ""), b.get("requester"), int(b.get("k", 3))))
            if p == "/api/view":
                return self._json({"views": engine.views(b["candidate"]), "ok": bool(engine.record_view(b["candidate"], b.get("who", "evaluator")))})
            if p == "/api/reset":
                engine.reset()
                return self._json({"ok": True})
            return self._json({"error": "not found"}, 404)
        except Exception as e:  # noqa: BLE001
            return self._json({"error": f"{type(e).__name__}: {e}"}, 500)


if __name__ == "__main__":
    print(f"evidence layer demo: http://localhost:{PORT}  backend={engine.backend_name()}  mode={engine.MODE}")
    ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
