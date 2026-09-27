#!/bin/bash
# Relaunch Dia with the flags Pik needs in a Google Meet. Tabs restore; unsent text in any tab is lost.
#
#   prototype/dia_pik.sh          # demo mode: AppleScript JS on, Pik's tab auto-picked when sharing
#   prototype/dia_pik.sh --face   # same plus a fake camera that shows Pik's face. Google Meet REFUSED the guest join with it on
#                                 # ("You can't join this video call", Sat 23:00), so it is off by default; kept for a signed-in Pik account
#   prototype/dia_pik.sh --plain  # back to a normal Dia (only AppleScript JS stays on)
#
# --face applies to ALL of Dia while it is on: every profile's camera is Pik's face and every mic is silent. Run --plain after.
# The laptop mic that `make live` listens on is not affected (that is sounddevice, not Dia).
set -euo pipefail
Y4M="$HOME/.local/state/pik-meet/pik_camera.y4m"
FLAGS=(--enable-applescript-javascript)
MODE=${1:-}
if [[ "$MODE" != "--plain" ]]; then
  FLAGS+=(--auto-select-tab-capture-source-by-title=Pik --autoplay-policy=no-user-gesture-required)  # the Pik tab may play Pik's voice on a terminal cue with no click first
fi
if [[ "$MODE" == "--face" ]]; then
  [[ -f "$Y4M" ]] || { echo "dia_pik: $Y4M is missing; build it from deck/video/v2/renders/pik_avatar_loop.mp4 (see MEET_REHEARSAL.md)" >&2; exit 1; }
  FLAGS+=(--use-fake-device-for-media-stream "--use-file-for-fake-video-capture=$Y4M")
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
