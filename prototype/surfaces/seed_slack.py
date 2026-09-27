"""Seed the demo Slack workspace so its channels look lived-in: fictional Kaede Works messages from the fixtures
(data/slack.json and the generated receipts in data/people.json), posted as their fictional authors.

Needs three bot scopes beyond the bot's usual four: chat:write.customize (post under a name), channels:manage (create channels),
channels:join. Add them under OAuth & Permissions, reinstall the app, then: make seed-slack   (DRY=1 previews, FORCE=1 re-seeds
a channel that already has messages from this bot). Timestamps are "now"; Slack does not allow backdating.
Everything posted is fictional: no real people, no real messages.
"""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _env  # noqa: E402,F401
from slack_sdk import WebClient  # noqa: E402
from slack_sdk.errors import SlackApiError  # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data"
DRY = os.environ.get("DRY") == "1"
FORCE = os.environ.get("FORCE") == "1"
PER_CHANNEL = int(os.environ.get("PER_CHANNEL", "5"))   # generated receipts per channel, on top of the fixture messages
PAUSE = 1.05                                             # chat.postMessage allows about one message per second

TOKEN = os.environ.get("PIK_SLACK_BOT_TOKEN")
if not TOKEN:
    raise SystemExit("set PIK_SLACK_BOT_TOKEN in <repo>/.env (gitignored) or ~/.config/carl-life-os/.env")
client = WebClient(token=TOKEN)

company = json.loads((DATA / "company.json").read_text())
people = json.loads((DATA / "people.json").read_text())
fixture_msgs = json.loads((DATA / "slack.json").read_text())

NAMES = {c["id"]: c["name"] for c in company["candidates"]}
NAMES.update({"okada": "Okada", "fujii": "Fujii", "hayashi": "Hayashi", "northwind-pm": "Northwind PM"})
PALETTE = [":large_blue_circle:", ":large_green_circle:", ":large_orange_circle:", ":large_purple_circle:",
           ":large_yellow_circle:", ":red_circle:", ":white_circle:", ":large_brown_circle:"]


RENAME = {"search": "search-relevance"}  # Slack refuses conversations.create(name="search") with name_taken


def chan(m):
    n = m["channel"].lstrip("#")
    return RENAME.get(n, n)


def avatar(name):
    return PALETTE[sum(map(ord, name)) % len(PALETTE)]


def plan():
    """All messages to post, oldest first: every fixture message, plus PER_CHANNEL generated receipts per channel."""
    msgs = [{"channel": m["channel"], "name": NAMES.get(m["author"], m["author"].title()), "date": m["date"], "text": m["text"]}
            for m in fixture_msgs]
    per = {}
    for p in people:
        if p["id"] in NAMES:
            continue  # the three candidates already speak through the fixture messages
        for r in p.get("receipts", []):
            if r.get("source") == "slack" and r.get("channel"):
                per.setdefault(r["channel"], []).append({"channel": r["channel"], "name": p["name"], "date": r["date"], "text": r["text"]})
    for ch, lst in per.items():
        seen, picked = set(), []
        for m in sorted(lst, key=lambda m: m["date"]):
            if m["name"] in seen or m["text"] in {x["text"] for x in picked}:
                continue  # one message per person per channel, no duplicate lines
            seen.add(m["name"]); picked.append(m)
            if len(picked) >= PER_CHANNEL:
                break
        msgs.extend(picked)
    msgs.sort(key=lambda m: m["date"])
    return msgs


def channels_by_name():
    out = {}
    cursor = None
    while True:
        r = client.conversations_list(types="public_channel", limit=200, exclude_archived=True, cursor=cursor)
        for c in r["channels"]:
            out[c["name"]] = c
        cursor = r.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break
    return out


def ensure_channel(name, existing):
    if name in existing:
        c = existing[name]
    else:
        try:
            c = client.conversations_create(name=name)["channel"]
        except SlackApiError as e:
            if e.response.get("error") != "name_taken":
                raise
            c = client.conversations_create(name=f"{name}-team")["channel"]  # a private or reserved name we cannot see
            print(f"  #{name} is taken; using #{name}-team")
        existing[c["name"]] = c
        print(f"  created #{c['name']}")
    if not c.get("is_member"):
        client.conversations_join(channel=c["id"])
        c["is_member"] = True
    return c


def already_seeded(channel_id, me):
    r = client.conversations_history(channel=channel_id, limit=20)
    # real posts only: the bot's own "joined the channel" line has subtype channel_join and no bot_id
    return any(m.get("bot_id") and m.get("subtype") in (None, "bot_message") for m in r.get("messages", []))


def main():
    me = client.auth_test()
    msgs = plan()
    wanted = sorted({chan(m) for m in msgs})
    print(f"workspace {me.get('team')}, posting as bot {me.get('user')} with names on top. {len(msgs)} messages across {len(wanted)} channels:")
    for ch in wanted:
        n = sum(1 for m in msgs if chan(m) == ch)
        print(f"  #{ch:<22} {n:>3} messages")
    if DRY:
        print("DRY=1: nothing posted. First five:")
        for m in msgs[:5]:
            print(f"  {m['date']} {m['channel']:<20} {m['name']:<16} {m['text'][:70]}")
        return
    existing = channels_by_name()
    skip, actual = set(), {}
    for ch in wanted:
        try:
            c = ensure_channel(ch, existing)
            actual[ch] = c
        except SlackApiError as e:
            err = e.response.get("error")
            if err == "missing_scope":
                raise SystemExit(f"missing scope {e.response.get('needed')}: add channels:manage and channels:join under OAuth & Permissions, reinstall, retry")
            raise
        if not FORCE and already_seeded(c["id"], me["user_id"]):
            print(f"  #{ch}: already has messages from this bot, skipping (FORCE=1 to add anyway)")
            skip.add(ch)
    posted = 0
    for m in msgs:
        ch = chan(m)
        if ch in skip:
            continue
        try:
            client.chat_postMessage(channel=actual[ch]["id"], text=m["text"], username=m["name"], icon_emoji=avatar(m["name"]))
        except SlackApiError as e:
            err = e.response.get("error")
            if err == "missing_scope":
                raise SystemExit("missing scope chat:write.customize: add it under OAuth & Permissions, reinstall the app, retry")
            if err == "ratelimited":
                time.sleep(int(e.response.headers.get("Retry-After", "5")))
                client.chat_postMessage(channel=actual[ch]["id"], text=m["text"], username=m["name"], icon_emoji=avatar(m["name"]))
            else:
                raise
        posted += 1
        if posted % 10 == 0:
            print(f"  {posted}/{len(msgs)} posted")
        time.sleep(PAUSE)
    print(f"done: {posted} messages posted. The bot is a member of every seeded channel, so asks work there.")


if __name__ == "__main__":
    main()
