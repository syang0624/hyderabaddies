"""Sign-in for the judge walkthrough. Stdlib only. Off unless PIK_AUTH=1; a session, when one exists, still
selects the subject view (what ?as=<id> gives) so a signed-in person cannot see other names.

Session = base64url(JSON) + "." + HMAC-SHA256 over it, keyed by a per-run secret written to state/session_secret
(state/ is git-ignored). Restarting the server signs everyone out, which is what a demo wants.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from http.cookies import SimpleCookie
from pathlib import Path

import engine

AUTH = os.environ.get("PIK_AUTH") == "1"
COOKIE = "pik_session"
TTL = 12 * 3600
_SECRET_FILE = engine.STATE / "session_secret"


def _secret() -> bytes:
    """A fresh secret per server run (the file is rewritten at import)."""
    s = secrets.token_bytes(32)
    _SECRET_FILE.write_bytes(s)
    try:
        os.chmod(_SECRET_FILE, 0o600)
    except OSError:
        pass
    return s


SECRET = _secret()


def people():
    """Who can sign in: the planner, the team leads (the managers in the fixtures), the three named people, a guest."""
    company = engine.load("company.json")
    pl = company["decision"].get("planner") or {}
    rows = []
    if pl.get("id"):
        rows.append({"id": pl["id"], "name": pl["name"], "role": "evaluator", "title": pl.get("role", "HR planner")})
    managers = sorted({c.get("manager") for c in company["candidates"] if c.get("manager")})
    for m in managers:
        reports = [c["name"].split()[0] for c in company["candidates"] if c.get("manager") == m]
        rows.append({"id": f"lead-{m.lower()}", "name": m, "role": "evaluator", "title": f"team lead ({', '.join(reports)})"})
    for c in company["candidates"]:
        rows.append({"id": c["id"], "name": c["name"], "role": "subject", "title": c["role"]})
    rows.append({"id": "guest", "name": "Guest", "role": "evaluator", "title": "read-only evaluator"})
    return rows


def person(pid: str):
    return next((p for p in people() if p["id"] == pid), None)


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")


def _unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def sign(session: dict) -> str:
    body = _b64(json.dumps(session, separators=(",", ":")).encode())
    mac = hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest()
    return f"{body}.{mac}"


def verify(token: str):
    try:
        body, mac = token.split(".", 1)
        if not hmac.compare_digest(hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest(), mac):
            return None
        s = json.loads(_unb64(body))
        if s.get("exp", 0) < time.time():
            return None
        return s
    except Exception:  # noqa: BLE001  (a torn cookie is just "not signed in")
        return None


def new_session(pid: str, workspace: str = "Kaede Works"):
    p = person(pid)
    if not p:
        raise ValueError(f"unknown person {pid!r}; pick one of {[x['id'] for x in people()]}")
    return {"id": p["id"], "name": p["name"], "role": p["role"], "title": p["title"],
            "workspace": (workspace or "Kaede Works").strip()[:60], "at": time.time(), "exp": time.time() + TTL}


def from_headers(headers):
    raw = headers.get("Cookie")
    if not raw:
        return None
    try:
        c = SimpleCookie()
        c.load(raw)
    except Exception:  # noqa: BLE001
        return None
    m = c.get(COOKIE)
    return verify(m.value) if m else None


def set_cookie_header(session: dict | None) -> str:
    if session is None:
        return f"{COOKIE}=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax"
    return f"{COOKIE}={sign(session)}; Path=/; Max-Age={TTL}; HttpOnly; SameSite=Lax"


# paths anyone may open even when PIK_AUTH=1
PUBLIC_PREFIXES = ("/login", "/logout", "/api/login", "/api/logout", "/api/session", "/fonts/", "/vendor/", "/favicon.ico")


def is_public(path: str) -> bool:
    return any(path == p or path.startswith(p) for p in PUBLIC_PREFIXES)
