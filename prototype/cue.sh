#!/bin/bash
# The cue for the hard-coded Meet take. Run from anywhere (a terminal off screen): starts Pik's 36 s clock on the presented page.
#   pik-cue            -> the hackathon take
#   pik-cue reset      -> clean state + Pik back to rest (before another take)
NAME=${1:-hackathon}
if [[ "$NAME" == "reset" ]]; then
  curl -sf -X POST localhost:8787/api/reset -H 'Content-Type: application/json' -d '{"people": true}' >/dev/null && : > "$(cd "$(dirname "$(readlink -f "$0")")" && pwd)/state/live.jsonl" && echo "reset: reload the Pik tab (Cmd-R) and it is armed again"; exit
fi
# the prompter: after the cue, print each human line at the second it is due (from scripts/<name>.json holds); keep this terminal off screen
prompt() {
  local t0=$(date +%s.%N)
  while IFS='|' read -r at who line; do
    while (( $(echo "$(date +%s.%N) - $t0 < $at" | bc -l) )); do sleep 0.2; done
    printf '\n\033[1m%5.1fs  %s:\033[0m %s\n' "$at" "$who" "$line"
  done <<'LINES'
0.0|Pik|(speaks 4 s) Since you're on that, I can help. What does the person need to have done?
4.5|STEVEN|Someone who has run a cross-team event, and can present the outcome to the exec team.
13.7|Pik|(speaks 7 s) Two people have receipts for that. Rin presented the pricing roadmap... Yui ran the Northwind syncs in English.
21.0|CARL|What did Rin actually do?
26.2|Pik|(speaks 6.5 s) Rin wrote: I'll present the pricing analytics roadmap to the exec team on the ninth...
33.0|STEVEN|Great. Let's ask Rin and Yui this week.
38.5|Pik|(speaks 3 s) Filed. Rin and Yui can see this same page.
42.0|CARL|Thanks, Pik.  (hold two seconds, then stop the recording)
LINES
}
r=$(curl -sf -X POST localhost:8787/api/take -H 'Content-Type: application/json' -d "{\"name\": \"$NAME\"}") && { echo "cue sent: $r"; prompt; } || { echo "cue FAILED: is the server on :8787 and scripts/$NAME.json there?"; exit 1; }
