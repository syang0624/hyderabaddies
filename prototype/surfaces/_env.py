"""Load RECEIPTS_* settings from ~/.config/carl-life-os/.env (never from the repo). Surfaces import this first."""
import os
from pathlib import Path

ENV = Path.home() / ".config" / "carl-life-os" / ".env"
if ENV.exists():
    for line in ENV.read_text().splitlines():
        if line.startswith("RECEIPTS_") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

API = os.environ.get("RECEIPTS_API", "http://localhost:8787")
PUBLIC = os.environ.get("RECEIPTS_PUBLIC_URL", API)  # what a link in Slack/Notion should point at (LAN ip for a phone)


def ask(question, context="", requester=None, k=3):
    import json
    import urllib.request
    req = urllib.request.Request(f"{API}/api/ask", data=json.dumps({"question": question, "context": context, "requester": requester, "k": k}).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def why_link(question, person_id=None):
    from urllib.parse import quote
    return f"{PUBLIC}/?q={quote(question)}" + (f"&focus={person_id}" if person_id else "")
