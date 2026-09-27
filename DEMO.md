# Running Pik yourself

Pik answers "who is the best person for this?" from what people actually wrote and did, with the receipt attached, inside the tools a team already uses: a Google Meet, a Slack channel, a ticket board. Nobody is scored. The person named sees the same page.

Everything below runs on one laptop. The company (Kaede Works) and its 200 people are fictional fixtures under `prototype/data/`. What runs live: the meeting listener (Gemini 3.8 Live on Vertex AI), the engine's ranking on evidence overlap and its verbatim receipts, the Slack bot, the Notion watcher, the page.

## 0. One-time setup (5 minutes)

```bash
cd prototype
make setup                                   # venv + google-genai + sounddevice + slack_bolt + notion-client
gcloud auth application-default login        # any Google account with access to the Vertex project
cp ../.env.example ../.env                   # then paste the Slack and Notion tokens (never commit .env)
```

Vertex project and model are set in `Makefile` (`GCP_PROJECT`, `LIVE_MODEL`); change them if you run this outside our project.

## 1. Start the product (every time, three terminal tabs, in this order)

| tab | command | ready when it prints |
|---|---|---|
| 1 | `make run-heuristic` | nothing; `open http://localhost:8787` shows the page (`make run-gemini` uses Gemini 3.8 Flash for extraction instead of the keyword engine) |
| 2 | `PIK_SLACK_INLINE=1 make slack` | `Bolt app is running!` |
| 3 | `make notion` | `Pik for Notion: watching the board` |

Then in the browser: `http://localhost:8787/?present=1` is the screen you show. `make reset` clears cached rankings between runs.

## 2. The Meet, live (the listener hears the call)

```bash
cd prototype && MIC="MacBook" SPEAK=1 make live     # tab 4; prints "listening on ... via gemini-3.8-live"
```
Reload the present page once after it prints that. Then talk. Anything about people or work makes the screen react within one to two seconds; words drift in as they are heard, people appear only where their own receipts cover the words, a receipt flashes when someone asks what a person actually wrote, the conclusion prints when the speakers agree. Pik speaks only when addressed by name ("Pik, ...") or when the engine has one follow-up question. `SPEAK=0` mutes its voice.

To have Pik sit inside a real Google Meet as its own participant presenting this screen: `prototype/dia_pik.sh` once (relaunches the Dia browser with the flags it needs), then `prototype/meet_dia.sh` (creates the call, joins Pik, presents).

Lines that work well on the fixtures:
- "For the Northwind slot I need someone who will push back on the job-based culture instead of just absorbing it, and they have to hold their own in English in meetings."
- "One constraint: nobody leaves pricing before the Q1 close."
- "Actually, just someone good." (Pik asks its one question out loud)
- "What did Yui actually write about this herself?"
- "Who has been running the Northwind syncs in English?" / "Who mentors the juniors on SQL?" / "Who should present the pricing roadmap to the exec team?"

If the listener drops: Ctrl-C, run it again, reload the page. Typing the same sentence into the page's input bar goes through the same engine and renders the same way.

## 3. Slack

In any channel the bot is in (it is in ten of the demo workspace's channels), type: `who's best to run pricing experiments with the US product team?` Pik answers in under a second: the person, their tags, two verbatim receipts with sources, load, two alternates, and the no-score footer. Press **Loop in Yui**; Pik posts the loop-in. **Why? See the receipts** opens her page. Any "who ... best / should / for / can" sentence triggers it, or an @-mention.

## 4. Notion (the ticket fills itself)

On the Tickets board add a row with a Name and a Description and leave "Suggested owner" empty. Within 5 seconds the watcher fills Suggested owner, Why (tags, one verbatim receipt with its source, load) and Receipts (the link). A vague ticket gets "Pik asks: ..." instead of an owner. Wording that names Yui on the fixtures: Name `Pricing page A/B test with the Northwind team`, Description `Design the test with their PM and write the readout in English.`

## 5. The page itself

`http://localhost:8787`: type what matters, Enter; the map grows the same way the call does. Click a receipts-by-source card for the drawer of that person's receipts. `?as=yui` is what Yui sees: the same receipts, no other names, a note box on each line that lands on the evaluator's page before the decision is made. `curl -X POST localhost:8787/api/ask -d '{"question":"..."}'` is the whole API; every surface calls it and never ranks on its own.

## What to say when asked

- Where does the data come from? Public Slack channels, shared docs, Will Can Must sheets, opted-in AI sessions, and manager notes only beside the person's own words. DMs and private channels are never opened; the audit counts them from a manifest.
- Is that a score? No. "2 of 7 words have a receipt" is coverage of the ask by that person's own receipts, never sorted by, never shown to the person as a rank.
- What if it is wrong? The person sees the same page and can contest a line before the decision. A claim whose quote is not in its source is dropped and counted.
