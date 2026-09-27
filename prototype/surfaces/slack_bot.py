"""Slack surface: ask in a channel, get the best person with receipts, one button to loop them in.

Needs (in ~/.config/carl-life-os/.env): RECEIPTS_SLACK_BOT_TOKEN=xoxb-..., RECEIPTS_SLACK_APP_TOKEN=xapp-... (Socket Mode).
Scopes: app_mentions:read, channels:history, channels:read, chat:write. Invite the bot to the channel.
Run: make slack   (server must be running: make run-heuristic)

Triggers: @mention the bot, or a message in a channel it is in that starts with "who" and contains "best"/"should"/"for".
Never speaks otherwise. The named person is fictional; the "mention" is text, not a real Slack user.
"""
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _env  # noqa: E402,F401
from slack_bolt import App  # noqa: E402
from slack_bolt.adapter.socket_mode import SocketModeHandler  # noqa: E402

BOT = os.environ.get("RECEIPTS_SLACK_BOT_TOKEN")
APP = os.environ.get("RECEIPTS_SLACK_APP_TOKEN")
if not BOT or not APP:
    raise SystemExit("set RECEIPTS_SLACK_BOT_TOKEN and RECEIPTS_SLACK_APP_TOKEN in ~/.config/carl-life-os/.env")

app = App(token=BOT)
ASK = re.compile(r"^\s*(who|whom)\b.*\b(best|should|for|can)\b", re.I)


def card(question, a):
    if a.get("follow_up") or not a["people"]:
        return [{"type": "section", "text": {"type": "mrkdwn", "text": f"*Receipts asks:* {a.get('follow_up') or 'What would this person actually do in the first month?'}"}}]
    top, alts = a["people"][0], a["people"][1:3]
    load = top.get("load", {})
    why = "\n".join(f"• {w}" for w in top["why"][:3])
    rec = "\n".join(f"> {r['text']}  _({r['source']})_" for r in top["receipts"][:2])
    blocks = [
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*{top['name']}*, {top['role']}, {top['team']}\n{why}"}},
        {"type": "context", "elements": [{"type": "mrkdwn", "text": f"On their plate: {load.get('open_tickets', '?')} open tickets, {load.get('hours_booked_this_week', '?')} h booked this week · {top.get('availability', '')}"}]},
    ]
    if rec:
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": rec}})
    if alts:
        blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text": "Also: " + " · ".join(f"{p['name']} ({p['role']})" for p in alts)}]})
    blocks.append({"type": "actions", "elements": [
        {"type": "button", "text": {"type": "plain_text", "text": f"Loop in {top['name'].split()[0]}"}, "style": "primary", "action_id": "loop_in",
         "value": f"{top['name']}|{top['why'][0] if top['why'] else ''}"},
        {"type": "button", "text": {"type": "plain_text", "text": "Why? See the receipts"}, "url": _env.why_link(question, top["id"]), "action_id": "why"},
    ]})
    blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text": "Order is evidence overlap with your words, minus load. Not a score. The person sees the same receipts."}]})
    return blocks


def handle(question, say, thread_ts=None):
    a = _env.ask(question, context="slack")
    say(blocks=card(question, a), text=f"Receipts: {a['people'][0]['name'] if a['people'] else a.get('follow_up')}", thread_ts=thread_ts)


@app.event("app_mention")
def on_mention(event, say):
    q = re.sub(r"<@[^>]+>", "", event.get("text", "")).strip()
    handle(q, say, event.get("ts"))


@app.message(ASK)
def on_ask(message, say):
    handle(message.get("text", ""), say, message.get("ts"))


@app.action("loop_in")
def on_loop(ack, body, say):
    ack()
    name, why = body["actions"][0]["value"].split("|", 1)
    say(text=f"@{name}, looping you in. {why}".strip(), thread_ts=body.get("message", {}).get("thread_ts") or body.get("message", {}).get("ts"))


@app.action("why")
def on_why(ack):
    ack()


if __name__ == "__main__":
    print("Receipts for Slack: listening (Socket Mode). Ask 'who is best for ...' in a channel I am in, or @mention me.")
    SocketModeHandler(app, APP).start()
