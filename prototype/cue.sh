#!/bin/bash
# The cue for the hard-coded Meet take. Run from anywhere (a terminal off screen): starts Pik's 36 s clock on the presented page.
#   pik-cue            -> the hackathon take
#   pik-cue reset      -> clean state + Pik back to rest (before another take)
NAME=${1:-hackathon}
if [[ "$NAME" == "reset" ]]; then
  curl -sf -X POST localhost:8787/api/reset -H 'Content-Type: application/json' -d '{"people": true}' >/dev/null && : > "$(dirname "$0")/state/live.jsonl" && echo "reset: reload the Pik tab (Cmd-R) and it is armed again"; exit
fi
r=$(curl -sf -X POST localhost:8787/api/take -H 'Content-Type: application/json' -d "{\"name\": \"$NAME\"}") && echo "cue sent: $r" || { echo "cue FAILED: is the server on :8787 and scripts/$NAME.json there?"; exit 1; }
