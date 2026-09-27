#!/bin/bash
# Pik joins a Google Meet as its own participant, in Carl's Dia (no other browser), and opens the live screen to present.
#
#   prototype/meet_dia.sh                      # host creates a new call in Dia profile 2 (carl@somach.life), Pik joins from profile 4
#   prototype/meet_dia.sh https://meet.google.com/abc-defg-hij   # join an existing call instead (the host admits Pik by hand)
#
# Needs: Dia launched with --enable-applescript-javascript (quit Dia, then: open -a Dia --args --enable-applescript-javascript),
#        the engine on :8787 (make run-heuristic), Accessibility for this terminal (System Events types the guest name).
# Profiles (Dia window profiles, 1-based): 2 = "Somach Systems, Inc." (host), 4 = "O-Intuition" (signed out of Google, so
# Meet asks for a guest name). Change HOST_P / PIK_P if Dia's order changes.
# The one hand step: in Pik's Meet tab the share picker opens; click the "Pik" tab, then Share. Chrome requires a real click there.
set -euo pipefail
HOST_P=${HOST_P:-2}; PIK_P=${PIK_P:-4}; URL=${1:-}
STATE="$(cd "$(dirname "$0")" && pwd)/state/meet_dia"; mkdir -p "$STATE"
log() { echo "$(date +%H:%M:%S) $*"; }
die() { echo "meet_dia: $*" >&2; exit 1; }

js() {  # js <tab-id> <javascript>  -> result (osascript prints text results in quotes; they are stripped)
  osascript - "$1" "$2" <<'AS' | sed -e 's/^"//' -e 's/"$//'
on run argv
  set tid to item 1 of argv
  set code to item 2 of argv
  tell application "Dia"
    repeat with w in windows
      repeat with p in profiles of w
        repeat with t in tabs of p
          if (id of t) is tid then return (execute t javascript code)
        end repeat
      end repeat
    end repeat
  end tell
  return "NO TAB"
end run
AS
}
newtab() { osascript -e 'tell application "Dia"' -e "set t to make new tab at end of tabs of profile $1 of front window with properties {URL:\"$2\"}" -e 'return id of t' -e 'end tell'; }
focustab() { osascript -e 'tell application "Dia" to activate' -e 'tell application "Dia"' -e 'repeat with w in windows' -e 'repeat with p in profiles of w' -e 'repeat with t in tabs of p' -e "if (id of t) is \"$1\" then focus t" -e 'end repeat' -e 'end repeat' -e 'end repeat' -e 'end tell' >/dev/null; }
click_label() {  # click the first button whose aria-label or text starts with $2
  js "$1" "(function(){var b=[].slice.call(document.querySelectorAll('button,[role=button]')).filter(function(e){return ((e.getAttribute('aria-label')||e.innerText||'').trim()).indexOf('$2')===0})[0]; if(!b) return 'none'; b.click(); return 'ok'})()"
}

PROBE=$(newtab "$PIK_P" "about:blank"); sleep 1
js_ok=$(js "$PROBE" "1+1" 2>&1 || true)
osascript -e 'tell application "Dia"' -e 'repeat with w in windows' -e 'repeat with p in profiles of w' -e 'repeat with t in tabs of p' -e "if (id of t) is \"$PROBE\" then close t" -e 'end repeat' -e 'end repeat' -e 'end repeat' -e 'end tell' >/dev/null 2>&1 || true
[[ "$js_ok" == *"enable-applescript-javascript"* ]] && die "Dia is not accepting JavaScript from AppleScript. Run prototype/dia_pik.sh (relaunches Dia with the flag)."
curl -fsS -o /dev/null http://localhost:8787/ || die "the engine is not on :8787; run make run-heuristic"

HOST=""
if [[ -z "$URL" ]]; then
  HOST=$(newtab "$HOST_P" "https://meet.google.com/new"); log "host tab opened (profile $HOST_P)"
  for i in $(seq 1 30); do sleep 1; URL=$(js "$HOST" "location.href"); [[ "$URL" =~ meet.google.com/[a-z]{3}-[a-z]{4}-[a-z]{3} ]] && break; done
  [[ "$URL" =~ meet.google.com/[a-z]{3}-[a-z]{4}-[a-z]{3} ]] || die "no meeting link from meet.google.com/new (got $URL)"
  URL=$(echo "$URL" | grep -oE 'https://meet.google.com/[a-z]{3}-[a-z]{4}-[a-z]{3}')
  sleep 3
  # Meet in Dia joins the host straight in with mic and camera ON: turn both off before anything else.
  for l in "Turn off microphone" "Turn off camera"; do r=$(click_label "$HOST" "$l"); log "host: $l -> $r"; done
  devs=$(js "$HOST" "JSON.stringify([].slice.call(document.querySelectorAll('button')).map(function(e){return e.getAttribute('aria-label')||''}).filter(function(x){return /^Turn (on|off) (microphone|camera)/.test(x)}))")
  [[ "$devs" == *"Turn off"* ]] && die "host mic or camera is still on: $devs. Turn them off in the host tab."
  log "host in the call, mic and camera off: $URL"
fi
echo "$URL" > "$STATE/url"

PIK=$(newtab "$PIK_P" "$URL"); log "Pik tab opened (profile $PIK_P)"
for i in $(seq 1 45); do sleep 1; [[ "$(js "$PIK" "String(!!document.querySelector('input[type=text]'))")" == "true" ]] && break; done
[[ "$(js "$PIK" "String(!!document.querySelector('input[type=text]'))")" == "true" ]] || die "Pik's tab shows no name field; is profile $PIK_P signed in to Google? (it must be signed out)"
# With dia_pik.sh's fake camera, Pik joins with its face on camera and its (silent) mic off. Without it, Meet shows "Continue without
# microphone and camera" (guest, no devices) and we take that.
click_label "$PIK" "Continue without microphone and camera" >/dev/null || true
click_label "$PIK" "Got it" >/dev/null || true
for l in "Turn off microphone" "Turn off camera"; do r=$(click_label "$PIK" "$l"); log "Pik: $l -> $r (none = no such device, fine)"; done
devs=$(js "$PIK" "JSON.stringify([].slice.call(document.querySelectorAll('button')).map(function(e){return e.getAttribute('aria-label')||''}).filter(function(x){return /^Turn (on|off) (microphone|camera)/.test(x)}))")
[[ "$devs" == *"Turn off"* ]] && die "Pik's mic or camera is still on: $devs"
focustab "$PIK"; sleep 0.8
js "$PIK" "(function(){var i=document.querySelector('input[type=text]'); i.focus(); i.select(); document.execCommand('delete'); return 'ok'})()" >/dev/null
osascript -e 'tell application "System Events" to keystroke "Pik"'   # Meet enables "Ask to join" only after real typing
sleep 0.8
r=$(js "$PIK" "(function(){var j=[].slice.call(document.querySelectorAll('button')).filter(function(e){return /Ask to join/.test(e.innerText||'') && !e.disabled})[0]; if(!j) return 'disabled'; j.click(); return 'ok'})()")
[[ "$r" == "ok" ]] || die "Ask to join stayed disabled; type Pik in the name field of Pik's Meet tab and click Ask to join"
log "Pik asked to join"

if [[ -n "$HOST" ]]; then
  for i in $(seq 1 20); do sleep 1
    r=$(click_label "$HOST" "Admit"); [[ "$r" == "ok" ]] && sleep 1.5 && click_label "$HOST" "Admit Pik" >/dev/null && break
  done
  log "host admitted Pik"
else
  log "click Admit in your own Meet tab now"
fi
for i in $(seq 1 60); do sleep 1; [[ "$(js "$PIK" "String(!!document.querySelector('[aria-label^=\"Leave call\"]'))")" == "true" ]] && break; done
[[ "$(js "$PIK" "String(!!document.querySelector('[aria-label^=\"Leave call\"]'))")" == "true" ]] || die "Pik was not admitted within 60 s"
log "Pik is in the call"

APP=$(newtab "$PIK_P" "http://localhost:8787/?present=1"); sleep 3
log "Pik screen open in profile $PIK_P: $(js "$APP" "document.title")"
focustab "$PIK"; sleep 0.8
click_label "$PIK" "Share screen" >/dev/null
presenting=false
for i in $(seq 1 12); do sleep 1; [[ "$(js "$PIK" "String(/Stop presenting|You're presenting|You are presenting/.test(document.body.innerText))")" == "true" ]] && presenting=true && break; done
if $presenting; then
  log "Pik is presenting its tab (auto-picked; Dia was launched by dia_pik.sh)"
else
  log "SHARE PICKER OPEN in Pik's Meet tab: click the 'Pik' tab, then Share. (Launch Dia with prototype/dia_pik.sh to skip this.)"
fi
printf 'host=%s\npik=%s\napp=%s\nurl=%s\n' "$HOST" "$PIK" "$APP" "$URL" > "$STATE/tabs"
