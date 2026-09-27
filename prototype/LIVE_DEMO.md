# Live demo, feature by feature (if a judge says "run it live")

Written Sat Sep 26 23:20 PDT. Everything below was run tonight on Carl's Mac against the engine on :8787. Company and people are fictional (Kaede Works; Rin Mori, Yui Sato, Kei Tanaka plus 197 generated). What is live: Gemini 3.8 Live hears the call and composes the screen by tool calls; the engine ranks on evidence overlap and pulls verbatim receipts; Slack and Notion are the real apps. What is fixed: the company, the people, the memo template. Say that first.

## Before the demo (10 minutes, one terminal tab each, from `prototype/`)

| # | Command | Ready when |
|---|---|---|
| 1 | `make run-heuristic` | `open http://localhost:8787` shows the receipts page |
| 2 | `make slack` (tokens in `<repo>/.env`; add `PIK_SLACK_INLINE=1` in front to answer in the channel, not a thread) | prints `⚡️ Bolt app is running!` |
| 3 | `make notion` | prints `Pik for Notion: watching the board` |
| 4 | `MIC="MacBook" SPEAK=1 make live` (only for the Meet feature; start it right before) | prints `listening on MacBook Pro Microphone via gemini-3.8-live` |

Then in Dia: the Pik screen `http://localhost:8787/?present=1` (this is what you show), Slack `#growth-analytics` in recruit-demo, the Notion Tickets board. `make reset` between runs clears cached rankings. If the room is loud, put the laptop mic toward the speaker; the listener hears everything, including Korean.

Kill switch: Ctrl-C in tab 4 stops the listener; the page shows "Listener off".

## 1. Meet: it hears the call (Gemini 3.8 Live)

Show `?present=1`. Say, at speaking pace, in any order:

| You say | What appears (within ~2 s) |
|---|---|
| "I need someone who will push back on the job-based culture instead of absorbing it, and they have to hold their own in English in meetings." | The question, then three tiles re-sorted, Yui first, one receipt line each |
| "One constraint: nobody leaves pricing before the Q1 close." | A constraint chip; the tile it touches dims with the reason |
| "Actually, just someone good." | The ask block, and Pik says it out loud once, naming the words it could not match |
| "What did Yui actually write about this herself?" | Yui's own words, verbatim, with the source, beside her manager's note |
| "Okay, let's set up calls with Yui and Kei this week and ask Yui about the location note." | The conclusion prints: people to talk to, next steps, what to ask |

It also reacts off script. Since 23:15 it answers any request about people or work, in English, Japanese or Korean: "who knows system design here?", "who could take the customer interviews for Northwind onboarding?", "誰が英語で会議をリードできる？", "Pik, who ran the last incident?" Names are matched through the company's own 25 skill tags (the model maps your words onto them; the engine does the rest). Small talk gets nothing. If nothing on file matches, Pik says which words it could not find and asks what the person would actually do.

For the judges: the model never names a person itself. Every tile and quote carries a source id the engine returned; the page drops anything without one and counts the drops in the footer.

Fallbacks, in order: say the line again once; type the criterion in the "What matters" box on the non-present page (`http://localhost:8787`) and press Enter; screen-share `deck/video/v2/meet_stage_demo.mp4` and speak to `STAGE_CUES.md`.

## 2. Slack: ask where you already are

In `#growth-analytics` (or any channel the bot is in; it is in ten), type: `who's best to run pricing experiments with the US product team?` Enter. Under a second: Pik's card (Yui Sato, her tags, two verbatim receipts with sources, load, two alternates, the no-score footer). Press **Loop in Yui**: Pik posts the loop-in with the question. **Why? See the receipts** opens her page on the laptop. A judge can type their own question; anything starting with "who" or "whom" and containing best / should / for / can triggers it, or @-mention the app. If the words match nothing, Pik posts "Pik asks: ..." instead of a name.

Other good lines: `who should take the Northwind onboarding interviews?`, `who can review the pricing doc in English today?`

## 3. Notion: the ticket fills itself

On the Tickets board add a row: Name `Pricing page A/B test with the Northwind team`, Description `Design the test with their PM and write the readout in English.` Within 5 s the watcher fills Suggested owner (Yui Sato, alternates), Why (tags, one verbatim receipt with its source, load) and Receipts (the link). Leave Suggested owner empty; that is the trigger. A vague ticket gets "Pik asks: ..." in Why instead of an owner, which is the honest behaviour, so if a judge types one, say so.

## 4. The receipts page: the why behind every name

`http://localhost:8787` (not present mode). Type what matters in the box, Enter: the three cards re-order and the matching receipts light up. Open a receipt: the quote, word for word, with the source. Toggle **As the candidate**: the same receipts, no rank, no other names; add a note and it lands on the evaluator's page. Print the memo: every claim footnoted, plus what was read and never read. `?as=yui` on a phone on the same Wi-Fi shows the candidate view (set `PIK_PUBLIC_URL` to the laptop's LAN address so the Slack and Notion links open there).

## 5. For the technical judge

`make ask Q="someone who can run the Northwind sync in English"` prints the ranking with why and load from the same `/api/ask` every surface calls. `curl -X POST localhost:8787/api/ask -d '{"question":"..."}'` is the whole API. One engine, thin surfaces, no surface ranks on its own.

## What to say when it misfires

- It heard the room but put nothing up: it decided there was no request. Ask a "who" question.
- It asked a question instead of naming someone: nothing on file matched those words. That is the design; wrong AI output should not drive a decision.
- The listener dropped: Ctrl-C, run tab 4 again, reload the page. Ten seconds.
