#!/bin/bash
# Relaunch Dia with the flags Pik needs to sit in a Google Meet. Tabs restore; unsent text in any tab is lost.
#
#   prototype/dia_pik.sh          # demo mode: AppleScript JS on, Pik's tab auto-picked when sharing, autoplay for Pik's voice
#   prototype/dia_pik.sh --plain  # back to a normal Dia (only AppleScript JS stays on)
#
# The laptop mic that `make live` listens on is not affected (that is sounddevice, not Dia).
set -euo pipefail
FLAGS=(--enable-applescript-javascript)
MODE=${1:-}
if [[ "$MODE" != "--plain" ]]; then
  FLAGS+=(--auto-select-tab-capture-source-by-title=Pik --autoplay-policy=no-user-gesture-required)
fi
if pgrep -xq Dia; then
  osascript -e 'tell application "Dia" to quit' || true
  for _ in $(seq 1 30); do pgrep -xq Dia || break; sleep 1; done
  pgrep -xq Dia && { echo "dia_pik: Dia did not quit (a tab may be asking to save). Close it, then rerun." >&2; exit 1; }
fi
open -a /Applications/Dia.app --args "${FLAGS[@]}"
for _ in $(seq 1 30); do sleep 1; r=$(osascript -e 'tell application "Dia" to execute active tab of front window javascript "1+1"' 2>/dev/null || true); [[ "$r" == "2" ]] && break; done
[[ "$r" == "2" ]] || { echo "dia_pik: Dia is back but not accepting JavaScript yet; wait a few seconds and try prototype/meet_dia.sh" >&2; exit 1; }
echo "Dia relaunched with: ${FLAGS[*]}"
