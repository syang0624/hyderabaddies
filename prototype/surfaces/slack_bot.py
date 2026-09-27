"""Slack surface: ask in a channel, get the best person with receipts, one button to loop them in.

Needs (in <repo>/.env, gitignored, or ~/.config/carl-life-os/.env): PIK_SLACK_BOT_TOKEN=xoxb-..., PIK_SLACK_APP_TOKEN=xapp-... (Socket Mode).
Scopes: app_mentions:read, channels:history, channels:read, chat:write. Invite the bot to the channel.
Run: make slack   (server must be running: make run-heuristic)

Triggers: @mention the bot, or a message in a channel it is in that starts with "who" and contains "best"/"should"/"for".
Never speaks otherwise. The named person is fictional; the "mention" is text, not a real Slack user.
"""
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _env  # noqa: E402,F401
from slack_bolt import App  # noqa: E402
from slack_bolt.adapter.socket_mode import SocketModeHandler  # noqa: E402
from slack_sdk.errors import SlackApiError  # noqa: E402

BOT = os.environ.get("PIK_SLACK_BOT_TOKEN")
APP = os.environ.get("PIK_SLACK_APP_TOKEN")
if not BOT or not APP:
    raise SystemExit("set PIK_SLACK_BOT_TOKEN and PIK_SLACK_APP_TOKEN in <repo>/.env (gitignored) or ~/.config/carl-life-os/.env")

try:
    app = App(token=BOT)  # Bolt calls auth.test here, so a wrong bot token fails now, not on the first ask
except Exception as e:
    raise SystemExit(f"Slack rejected PIK_SLACK_BOT_TOKEN: {e}\nRe-copy the Bot User OAuth Token (xoxb-...) from OAuth & Permissions after installing the app to the workspace.")
ME = app.client.auth_test().get("user_id")  # the bot's own user id, so a message that @mentions it is answered once, not twice
ASK = re.compile(r"^\s*(who|whom)\b.*\b(best|should|for|can)\b", re.I)


def card(question, a):
    if a.get("follow_up") or not a["people"]:
        return [{"type": "section", "text": {"type": "mrkdwn", "text": f"*Pik asks:* {a.get('follow_up') or 'What would this person actually do in the first month?'}"}}]
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
    try:
        a = _env.ask(question, context="slack")
    except Exception as e:  # noqa: BLE001  (engine down: say so instead of silence)
        say(username="Pik", text=f"Pik: the engine at {_env.API} is not answering ({type(e).__name__}). Start it with `make run-heuristic`.", thread_ts=thread_ts)
        return
    answer = a["people"][0]["name"] if a["people"] else f"asks: {a.get('follow_up')}"
    print(f"[{time.strftime('%H:%M:%S')}] ask {question!r} -> {answer}", flush=True)
    say(username="Pik", blocks=card(question, a), text=f"Pik: {answer}", thread_ts=thread_ts)


@app.event("app_mention")
def on_mention(event, say):
    q = re.sub(r"<@[^>]+>", "", event.get("text", "")).strip()
    handle(q, say, event.get("thread_ts") or event.get("ts"))


@app.message(ASK)
def on_ask(message, say):
    if ME and f"<@{ME}>" in message.get("text", ""):
        return  # on_mention answers this one
    handle(message.get("text", ""), say, message.get("thread_ts") or message.get("ts"))


@app.event("message")
def on_other_message(body, logger):
    """Every channel message the bot can see reaches here after the ASK matcher; stay silent, and keep Bolt from
    printing an 'Unhandled request' block per message."""


@app.action("loop_in")
def on_loop(ack, body, say):
    ack()
    name, why = body["actions"][0]["value"].split("|", 1)
    say(username="Pik", text=f"@{name}, looping you in. {why}".strip(), thread_ts=body.get("message", {}).get("thread_ts") or body.get("message", {}).get("ts"))


@app.action("why")
def on_why(ack):
    ack()


if __name__ == "__main__":
    print(f"Pik for Slack: listening (Socket Mode) as <@{ME}>. Ask 'who is best for ...' in a public channel I am in, or @mention me.")
    print(f"Engine: {_env.API}   'Why?' links open: {_env.PUBLIC}")
    try:
        SocketModeHandler(app, APP).start()
    except SlackApiError as e:
        raise SystemExit(f"Slack rejected PIK_SLACK_APP_TOKEN ({e.response.get('error')}).\nIt must be an App-Level Token (xapp-...) with the connections:write scope: Basic Information -> App-Level Tokens -> Generate.")
