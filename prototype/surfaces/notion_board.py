"""Notion board surface: a ticket without a suggested owner gets one, with a why and a receipts link, while you watch.

Needs (in ~/.config/carl-life-os/.env): RECEIPTS_NOTION_TOKEN=secret_..., RECEIPTS_NOTION_DB=<database id>.
Database properties (create these in Notion): Name (title), Description (rich text), Status (select),
Suggested owner (rich text), Why (rich text), Receipts (url). Share the database with the integration.
Run: make notion   (server must be running). Polls every 5 s; writes only rows whose Suggested owner is empty.
"""
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _env  # noqa: E402,F401
from notion_client import Client  # noqa: E402

TOKEN = os.environ.get("RECEIPTS_NOTION_TOKEN")
DB = os.environ.get("RECEIPTS_NOTION_DB")
if not TOKEN or not DB:
    raise SystemExit("set RECEIPTS_NOTION_TOKEN and RECEIPTS_NOTION_DB in ~/.config/carl-life-os/.env")
notion = Client(auth=TOKEN)


def text(prop):
    return "".join(t.get("plain_text", "") for t in (prop.get("title") or prop.get("rich_text") or []))


def rt(s):
    return {"rich_text": [{"type": "text", "text": {"content": s[:1900]}}]}


def run_once():
    res = notion.databases.query(database_id=DB, filter={"property": "Suggested owner", "rich_text": {"is_empty": True}})
    for page in res.get("results", []):
        props = page["properties"]
        name = text(props.get("Name", {}))
        desc = text(props.get("Description", {}))
        if not name.strip():
            continue
        a = _env.ask(name, context=desc, requester="notion")
        if a.get("follow_up") or not a["people"]:
            notion.pages.update(page_id=page["id"], properties={"Why": rt(f"Receipts asks: {a.get('follow_up')}")})
            print(f"[{time.strftime('%H:%M:%S')}] {name!r}: asked a follow-up")
            continue
        top = a["people"][0]
        load = top.get("load", {})
        why = "; ".join(top["why"][:2]) + f". Load: {load.get('open_tickets','?')} tickets, {load.get('hours_booked_this_week','?')} h this week."
        alts = ", ".join(p["name"] for p in a["people"][1:3])
        props_out = {
            "Suggested owner": rt(f"{top['name']} ({top['role']}, {top['team']})" + (f"  ·  also: {alts}" if alts else "")),
            "Why": rt(why),
            "Receipts": {"url": _env.why_link(name, top["id"])},
        }
        try:
            props_out["Status"] = {"select": {"name": "Owner suggested"}}
            notion.pages.update(page_id=page["id"], properties=props_out)
        except Exception:  # noqa: BLE001  (no such select option)
            props_out.pop("Status", None)
            notion.pages.update(page_id=page["id"], properties=props_out)
        print(f"[{time.strftime('%H:%M:%S')}] {name!r} -> {top['name']}")


if __name__ == "__main__":
    print("Receipts for Notion: watching the board. Add a ticket; the owner, why and receipts fill in within 5 s.")
    while True:
        try:
            run_once()
        except Exception as e:  # noqa: BLE001
            print("error:", type(e).__name__, str(e)[:160])
        time.sleep(5)
