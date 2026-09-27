"""Load RECEIPTS_* settings from the first .env that has them: <repo>/.env, <repo>/prototype/.env (both gitignored),
then ~/.config/carl-life-os/.env. Surfaces import this first. Never commit a .env."""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent            # prototype/surfaces
ENV_FILES = [HERE.parent.parent / ".env", HERE.parent / ".env", Path.home() / ".config" / "carl-life-os" / ".env"]
for env in ENV_FILES:
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("RECEIPTS_") and "=" in line:
                k, v = line.split("=", 1)
                v = v.strip().strip('"').strip("'")
                if v:  # an empty "KEY=" line means unset, so a later file or the default still applies
                    os.environ.setdefault(k.strip(), v)

API = os.environ.get("RECEIPTS_API") or "http://localhost:8787"
PUBLIC = (os.environ.get("RECEIPTS_PUBLIC_URL") or API).rstrip("/")  # what a link in Slack/Notion should point at (LAN ip for a phone)


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
