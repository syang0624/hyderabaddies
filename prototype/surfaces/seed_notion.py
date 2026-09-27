"""Seed the Notion Tickets board so it looks lived-in: ten fictional Kaede Works tickets, some Done, some In progress,
three new ones with no owner (the board watcher fills those within 5 s while you watch).

Owners, whys and receipts links come from the engine (/api/ask), the same call the watcher makes, so nothing is invented here.
Needs RECEIPTS_NOTION_TOKEN and RECEIPTS_NOTION_DB (see notion_board.py) and the engine running.
Run: make seed-notion   (DRY=1 previews). A ticket whose title already exists on the board is skipped.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _env  # noqa: E402
import notion_board as nb  # noqa: E402  (reuses its client, id resolution and schema check)

DRY = os.environ.get("DRY") == "1"

# (title, description, status). status None = leave the owner empty so the watcher fills it live.
TICKETS = [
    ("Q2 pricing test write-up for the exec review", "3% increase held retention flat in SMB. Include what we would do differently.", "Done"),
    ("Sequential stopping rule for the Q3 pricing test", "Small enterprise sample. Share the simulation notebook with Northwind.", "Done"),
    ("Post-mortem for the Saturday platform incident", "Timeline, root cause, the two follow-ups, by Monday.", "Done"),
    ("Onboarding guide for customer interviews, for the two new joiners", "How we recruit, run and write up interviews.", "Done"),
    ("Northwind holdout design: answer their two open questions", "From the May sync notes. They need a reply before the Q3 test starts.", "In progress"),
    ("Cohort retention deck refresh for the exec review", "Update the elasticity section with Q2 numbers.", "In progress"),
    ("SMB churn: customer interview synthesis", "Eight interviews done, four to go.", "In progress"),
    ("Design crit for checkout flow v3", "Thursday slot. Needs someone who has run one before.", None),
    ("Search relevance regression triage", "Top queries dropped 4% CTR after the ranker change.", None),
    ("Run the Northwind sync in English next week", "The regular host is on leave.", None),
]


def existing_titles(ds_id, title_prop):
    titles, cursor = set(), None
    while True:
        kw = {"start_cursor": cursor} if cursor else {}
        r = nb.notion.data_sources.query(data_source_id=ds_id, **kw)
        for page in r.get("results", []):
            titles.add(nb.text(page["properties"].get(title_prop, {})).strip())
        cursor = r.get("next_cursor")
        if not r.get("has_more") or not cursor:
            break
    return titles


def main():
    ds_id, props = nb.resolve(nb.normalize_id(nb.DB))
    title_prop, status_kind = nb.check_schema(props)
    have = existing_titles(ds_id, title_prop)
    print(f"board has {len(have)} tickets" + (f": {sorted(have)}" if have else ""))
    for title, desc, status in TICKETS:
        if title in have:
            print(f"  skip (exists): {title}")
            continue
        page = {title_prop: {"title": [{"type": "text", "text": {"content": title}}]}, "Description": nb.rt(desc)}
        owner = "(watcher fills it)"
        if status:
            a = _env.ask(title, context=desc, requester="seed")
            if a["people"] and not a.get("follow_up"):
                top = a["people"][0]
                load = top.get("load", {})
                alts = ", ".join(p["name"] for p in a["people"][1:3])
                page["Suggested owner"] = nb.rt(f"{top['name']} ({top['role']}, {top['team']})" + (f"  ·  also: {alts}" if alts else ""))
                page["Why"] = nb.rt("; ".join(top["why"][:2]) + f". Load: {load.get('open_tickets', '?')} tickets, {load.get('hours_booked_this_week', '?')} h this week.")
                page["Receipts"] = {"url": _env.why_link(title, top["id"])}
                owner = top["name"]
            if status_kind:
                page["Status"] = {status_kind: {"name": status}}
        print(f"  {status or 'new':<12} {title:<58} -> {owner}")
        if not DRY:
            nb.notion.pages.create(parent={"type": "data_source_id", "data_source_id": ds_id}, properties=page)
    print("DRY=1: nothing written." if DRY else "done. The three new tickets get an owner from the watcher within 5 s (make notion must be running).")


if __name__ == "__main__":
    main()
