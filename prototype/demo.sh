#!/bin/bash
# The whole Pik demo in ONE terminal. Ctrl-C stops everything it started.
#   8787  the page, open mode   (the Meet presents this; Slack and Notion link here)
#   8788  the page with sign-in (one-to-one demos: /login, /settings, /stats)
#   Slack bot and Notion watcher, when ../.env has their tokens
# Earlier copies on 8787/8788 and earlier bots are stopped first, so nothing runs twice.
set -u
P1=${PAGE_PORT:-8787}; P2=${LOGIN_PORT:-8788}   # overridable for testing
cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")"
PY=.venv/bin/python
[ -x "$PY" ] || { echo "demo: no prototype/.venv; run: make setup" >&2; exit 1; }
for f in "$HOME/.config/carl-life-os/gcloud-tmuc/application_default_credentials.json" "$HOME/.config/gcloud/application_default_credentials.json"; do
  [ -z "${GOOGLE_APPLICATION_CREDENTIALS:-}" ] && [ -f "$f" ] && export GOOGLE_APPLICATION_CREDENTIALS="$f"
done

for port in $P1 $P2; do
  pids=$(lsof -nP -iTCP:$port -sTCP:LISTEN -t 2>/dev/null)
  [ -n "$pids" ] && { echo "demo: stopping the old server on :$port"; kill $pids 2>/dev/null; }
done
if [ -z "${SKIP_BOTS:-}" ]; then
  pkill -f "surfaces/slack_bot.py" 2>/dev/null && echo "demo: stopped an old Slack bot"
  pkill -f "surfaces/notion_board.py" 2>/dev/null && echo "demo: stopped an old Notion watcher"
fi
sleep 1

trap 'trap - INT TERM; echo; echo "demo: stopping everything"; kill 0' INT TERM
run() { local tag=$1; shift; ( "$@" 2>&1 | sed -u "s/^/[$tag] /" ) & }
run page  env PORT=$P1 MODE=heuristic "$PY" server.py
run login env PORT=$P2 MODE=heuristic PIK_AUTH=1 "$PY" server.py
if [ -n "${SKIP_BOTS:-}" ]; then
  echo "demo: SKIP_BOTS set, Slack and Notion stay off"
elif [ -s ../.env ]; then
  run slack  env PIK_SLACK_INLINE=1 "$PY" surfaces/slack_bot.py
  run notion "$PY" surfaces/notion_board.py
else
  echo "demo: no .env at the repo root, so Slack and Notion stay off (copy .env.example to .env and add tokens)"
fi

ok=0
for _ in $(seq 1 40); do
  curl -sf localhost:$P1/api/context >/dev/null && curl -sf localhost:$P2/api/context >/dev/null && { ok=1; break; }
  sleep 0.5
done
if [ $ok -ne 1 ]; then echo "demo: FAILED, the servers did not answer in 20 s; read the [page] and [login] lines above" >&2; kill 0; exit 1; fi

URL=http://localhost:$P2/login
if [ -z "${NO_OPEN:-}" ]; then if [ -d /Applications/Dia.app ]; then open -a Dia "$URL"; else open "$URL"; fi; fi
cat <<TXT

  Pik is running.
  One-to-one demo : $URL   (sign in as Aya Nakamura, HR planner; later as Yui Sato to see her side)
  Open page       : http://localhost:$P1            present mode: http://localhost:$P1/?present=1
  On the page     : a preset ask on the input bar, the mic to talk, End meeting for the memo,
                    hover or click Slack / Docs / Sheets / Sessions for the sources, the receipts count for what Pik reads.
  Slack           : "who's best to run pricing experiments with the US product team?" in a channel with the bot
  Notion          : add a ticket with a Name and a Description, leave the owner empty
  Fine-tune       : make -C $(cd .. && pwd)/finetune ask Q="Who offered to facilitate the look-back session about A/B tests on what we charge?"
  Stop            : Ctrl-C here

TXT
wait
