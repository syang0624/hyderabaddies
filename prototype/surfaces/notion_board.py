"""Notion board surface: a ticket without a suggested owner gets one, with a why and a receipts link, while you watch.

Needs (in <repo>/.env, gitignored, or ~/.config/carl-life-os/.env): PIK_NOTION_TOKEN=ntn_... (internal integration secret),
PIK_NOTION_DB=<database id, or the database's URL>.
Database properties (create these in Notion): a title (usually "Name"), Description (text), Status (select or status, with an
option "Owner suggested"), Suggested owner (text), Why (text), Receipts (url). Connect the integration to the database (... -> Connections).
Run: make notion   (server must be running). Polls every 5 s; writes only rows whose Suggested owner is empty.
Notion API 2025-09: a database holds one or more data sources and rows are queried per data source, so the first one is resolved at start.
"""
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _env  # noqa: E402,F401
from notion_client import Client  # noqa: E402
from notion_client.errors import APIResponseError  # noqa: E402

TOKEN = os.environ.get("PIK_NOTION_TOKEN")
DB = os.environ.get("PIK_NOTION_DB", "")
if not TOKEN or not DB:
    raise SystemExit("set PIK_NOTION_TOKEN and PIK_NOTION_DB in <repo>/.env (gitignored) or ~/.config/carl-life-os/.env")
notion = Client(auth=TOKEN)

NEEDED = {"Description": "rich_text", "Suggested owner": "rich_text", "Why": "rich_text", "Receipts": "url"}
STATUS_TYPES = ("select", "status")
STATUS_DONE = "Owner suggested"


def normalize_id(s):
    """Accept a raw id (with or without dashes) or the database's URL; return the 32-hex id."""
    tail = s.strip().split("?")[0].rstrip("/").rsplit("/", 1)[-1]
    m = re.search(r"[0-9a-f]{32}$", tail.replace("-", "").lower())
    if not m:
        raise SystemExit(f"PIK_NOTION_DB={s!r} is not a Notion database id or URL")
    return m.group(0)


def resolve(db_or_ds_id):
    """Database id -> its first data source id + property schema. A data source id is accepted too."""
    try:
        db = notion.databases.retrieve(database_id=db_or_ds_id)
        sources = db.get("data_sources") or []
        if not sources:
            raise SystemExit("that Notion database has no data source (open it as a full page and check it is a table)")
        ds_id = sources[0]["id"]
    except APIResponseError as e:
        if e.code != "object_not_found":
            raise SystemExit(f"Notion refused ({e.code}): {str(e)[:200]}")
        try:
            notion.data_sources.retrieve(data_source_id=db_or_ds_id)
            ds_id = db_or_ds_id
        except APIResponseError:
            raise SystemExit("Notion cannot find that database. Check PIK_NOTION_DB and connect the integration to the database "
                             "(open the database, ... menu top right -> Connections -> Pik).")
    props = notion.data_sources.retrieve(data_source_id=ds_id).get("properties", {})
    return ds_id, props


def check_schema(props):
    """Return (title property name, status kind or None); exit with a precise list if properties are missing."""
    title = next((k for k, v in props.items() if v.get("type") == "title"), None)
    problems = [] if title else ["no title property (a table always has one; do not delete it)"]
    for name, typ in NEEDED.items():
        p = props.get(name)
        if not p:
            problems.append(f'missing property "{name}" (type: {"Text" if typ == "rich_text" else "URL"})')
        elif p.get("type") != typ:
            problems.append(f'"{name}" is type {p.get("type")}, needs {"Text" if typ == "rich_text" else "URL"}')
    st = props.get("Status")
    status_kind = st.get("type") if st and st.get("type") in STATUS_TYPES else None
    if problems:
        raise SystemExit("Notion board: fix these on the database, then run make notion again:\n  - " + "\n  - ".join(problems))
    return title, status_kind


def text(prop):
    return "".join(t.get("plain_text", "") for t in (prop.get("title") or prop.get("rich_text") or []))


def rt(s):
    return {"rich_text": [{"type": "text", "text": {"content": s[:1900]}}]}


def run_once(ds_id, title, status_kind):
    res = notion.data_sources.query(data_source_id=ds_id, filter={"property": "Suggested owner", "rich_text": {"is_empty": True}})
    for page in res.get("results", []):
        props = page["properties"]
        name = text(props.get(title, {}))
        desc = text(props.get("Description", {}))
        if not name.strip():
            continue
        a = _env.ask(name, context=desc, requester="notion")
        if a.get("follow_up") or not a["people"]:
            notion.pages.update(page_id=page["id"], properties={"Why": rt(f"Pik asks: {a.get('follow_up')}")})
            print(f"[{time.strftime('%H:%M:%S')}] {name!r}: asked a follow-up", flush=True)
            continue
        top = a["people"][0]
        load = top.get("load", {})
        why = "; ".join(top["why"][:2]) + f". Load: {load.get('open_tickets', '?')} tickets, {load.get('hours_booked_this_week', '?')} h this week."
        alts = ", ".join(p["name"] for p in a["people"][1:3])
        props_out = {
            "Suggested owner": rt(f"{top['name']} ({top['role']}, {top['team']})" + (f"  ·  also: {alts}" if alts else "")),
            "Why": rt(why),
            "Receipts": {"url": _env.why_link(name, top["id"])},
        }
        if status_kind:
            props_out["Status"] = {status_kind: {"name": STATUS_DONE}}
        try:
            notion.pages.update(page_id=page["id"], properties=props_out)
        except APIResponseError:  # a status-type property needs the option to exist; a select creates it, so this is the status case
            props_out.pop("Status", None)
            notion.pages.update(page_id=page["id"], properties=props_out)
            print(f'  (add the option "{STATUS_DONE}" to the Status property to see it flip)')
        print(f"[{time.strftime('%H:%M:%S')}] {name!r} -> {top['name']}", flush=True)


if __name__ == "__main__":
    ds_id, props = resolve(normalize_id(DB))
    title, status_kind = check_schema(props)
    print(f"Pik for Notion: watching the board (data source {ds_id[:8]}..., title property {title!r}, "
          f"Status: {status_kind or 'none, skipped'}). Add a ticket; the owner, why and receipts fill in within 5 s.", flush=True)
    print(f"Engine: {_env.API}   'Receipts' links open: {_env.PUBLIC}", flush=True)
    while True:
        try:
            run_once(ds_id, title, status_kind)
        except Exception as e:  # noqa: BLE001
            print("error:", type(e).__name__, str(e)[:160], flush=True)
        time.sleep(5)
