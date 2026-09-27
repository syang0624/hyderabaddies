# Meet rehearsal (Pik in a Google Meet)

**Status, Sat Sep 26 22:55 PDT: works in Dia up to one click.** Tested on a live call (meet.google.com/pcg-dqab-tgi): the host (carl@somach.life, Dia profile "Somach Systems, Inc.") created the call; Pik joined from the signed-out Dia profile "O-Intuition" as a guest named **Pik**; the host admitted it (two participants); Pik opened the live screen (`localhost:8787/?present=1`, title "Pik") and clicked Share screen, and the share picker listed the Pik tab. The pick itself needs a real click (Chrome's rule). Everything runs in Dia; no other browser. `meet_bot.py` (Chromium) is removed; it is in git history (a9f3db6).

## Terminals, in order (from `prototype/`)

| # | Command | Ready when |
|---|---|---|
| 1 | `make run-heuristic` (usually already up on :8787) | `http://localhost:8787/?present=1` loads, tab title "Pik" |
| 2 | `MIC="MacBook" SPEAK=1 make live` | terminal prints `status: listening on <mic> via gemini-3.8-live`. Then reload the Pik tab; the old conclusion clears |
| 3 | `./meet_dia.sh` (new call) or `./meet_dia.sh <meet link>` (your call) | prints `SHARE PICKER OPEN`; click the **Pik** tab, then **Share** |

## Carl's hand steps

1. Once per Dia launch: Dia must run with `--enable-applescript-javascript` (quit Dia, then `open -a Dia --args --enable-applescript-javascript`; tabs restore).
2. `./meet_dia.sh` makes the call as carl@somach.life and admits Pik by itself. It takes the keyboard for one second to type "Pik". To use your own call instead, pass its link and click **Admit** when Pik knocks.
3. When it prints `SHARE PICKER OPEN`: in Pik's Meet tab click the **Pik** tab, then **Share**. The composed screen is now what the call sees.
4. Steven joins the same link from his laptop (mic on). Carl's host tab stays muted: `make live` hears the room through the laptop mic.

## The five beats (Steven = manager, Carl = HR planner; lines from `live_sim.py`)

| Who | Line | The presented screen |
|---|---|---|
| Steven | "Sure. So for the Northwind exchange slot. Honestly I need someone who will push back on the job-based culture over there instead of just absorbing it. And they have to hold their own in English in meetings." | The question, then three people tiles |
| Carl | "Got it. One constraint from my side: the posting starts April 2027, and we cannot lose anyone from pricing before the Q1 close." | A constraint chip on the tiles it touches |
| Carl | "Actually, we also need someone good for this. Just someone good." | Pik's one follow-up question, shown and spoken once through the laptop speaker |
| Steven | "I keep coming back to Yui. What did she actually write about this herself, and what did her manager write about her?" | Yui's own words (verbatim) beside the manager's note (paraphrase) |
| Steven | "Okay. Looking at this, Yui's own words say she wants exactly that, and she has been running the Northwind sync in English. Let's set up calls with Yui and Kei this week, and ask Yui whether her manager's note about being flexible on location is actually true. That's it for today, thanks." | The conclusion prints: who to talk to, next steps, what to ask |

**Audio.** Pik neither hears nor speaks in the Meet. `make live` listens on the laptop mic, and the follow-up comes out of the laptop speaker, in the room. With Carl's Meet mic off, remote participants see the screen change but hear nothing. Not built: `--use-file-for-fake-audio-capture=<wav>` would play a wav as the bot's mic, but it loops from launch with no timing and needs the Chromium path. LoomAudioDevice (2 in, 2 out) has not been tested as a loopback.

## If Gemini Live drops

1. Say the line again, once.
2. Type the criterion into the "What matters" box on the Pik tab and press Enter. This works only until the composed screen covers the box. Badge that take "typed".
3. Stop `make live`, then run `make live-sim`. It forces SPEAK=0: `say -o` writes wav files and nothing plays. It is **not** an offline replay. It streams the seven scripted lines into the same Gemini Live session, so it needs Vertex too. It runs on its own clock (about 2 minutes, 8 s after each line), not on your cue. It covers a dead mic, not a dead Gemini. A real offline replay (a saved `live.jsonl` stepped beat by beat) is not built.

**Disclosure (one line).** Live: Gemini 3.8 Live hears the call and composes the screen, and the engine ranks and pulls receipts on every line. Fixed: the company and people (Kaede Works, 200 fictional people), the memo template, and Pik's join steps, which are scripted in Dia (AppleScript).
