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

The page's mic button starts the same listener without a terminal (`PIK_MIC` and `PIK_LISTEN_SPEAK` in `.env` stand in for `MIC` and `SPEAK`). If the listener drops: Ctrl-C, run it again, reload the page. Typing the same sentence into the page's input bar goes through the same engine and renders the same way.

## 3. Slack

In any channel the bot is in (it is in ten of the demo workspace's channels), type: `who's best to run pricing experiments with the US product team?` Pik answers in under a second: the person, their tags, two verbatim receipts with sources, load, two alternates, and the no-score footer. Press **Loop in Yui**; Pik posts the loop-in. **Why? See the receipts** opens her page. Any "who ... best / should / for / can" sentence triggers it, or an @-mention.

## 4. Notion (the ticket fills itself)

On the Tickets board add a row with a Name and a Description and leave "Suggested owner" empty. Within 5 seconds the watcher fills Suggested owner, Why (tags, one verbatim receipt with its source, load) and Receipts (the link). A vague ticket gets "Pik asks: ..." instead of an owner. Wording that names Yui on the fixtures: Name `Pricing page A/B test with the Northwind team`, Description `Design the test with their PM and write the readout in English.`

## 5. The page itself

`http://localhost:8787`: type what matters, Enter; the map grows the same way the call does. Click a receipts-by-source card for the drawer of that person's receipts. `?as=yui` is what Yui sees: the same receipts, no other names, a note box on each line that lands on the evaluator's page before the decision is made. `curl -X POST localhost:8787/api/ask -d '{"question":"..."}'` is the whole API; every surface calls it and never ranks on its own.

## Judge walkthrough, five minutes, one laptop

One person, one laptop, no shared project: sign in, bring your own key, ask, read the receipts, contest a line as the person named, read the numbers.

```bash
cd prototype
make setup                  # once, only for the Gemini path: venv + google-genai (keyword mode needs nothing)
make run-auth               # PIK_AUTH=1 MODE=auto on http://localhost:8787; every page and API now needs a session
```

1. Open `http://localhost:8787`. It redirects to `/login`. A "Today's context" card above the form names the decision (one exchange slot at Northwind Labs, starting April 2027); **Got it** hides it on this browser. Workspace stays "Kaede Works"; pick **Aya Nakamura, HR planner** (role: evaluator) and sign in. The page is the same one as before, with an identity chip (name, role, Settings, Stats, Sign out) and an extraction line in the header.
2. Open **Settings** (`/settings`). Paste a Gemini API key (or switch to Vertex and give a project id and location, using the ADC of the shell that started the server). **Save**, then **Test key**: the model name, the latency and ok, or the error text. The header now reads "Extraction: gemini-3.8-flash via your key". The key lives in `prototype/state/byok.json` (git-ignored, mode 600), is read by the server at request time, and is returned masked. Without a key the header reads "keyword mode, no key" and everything still works.
3. Back on the page, type one of these and press Enter: "Who has been running the Northwind syncs in English?" or "Who mentors the juniors on SQL?" Tiles appear only where a person's own receipts cover the words.
4. Click a receipts-by-source card on the right: the drawer lists that person's receipts, each with its source.
5. **Activity cards** (Slack, Docs, Sheets, Sessions): hover one for its three most recent receipts; click it for the full source list, newest first (34, 5, 3 and 4 items on the fixtures). Manager notes and DMs are never listed.
6. **Join Meet**, **Open Slack**, **Open task board** open the call, the demo Slack workspace and the Notion board (URLs from `.env`: `PIK_MEET_URL`, `PIK_SLACK_URL`, `PIK_NOTION_URL`).
7. The **mic button** starts the Gemini 3.8 Live listener (`live.py`) from the page and stops it again; talk and the screen reacts as in section 2. One listener at a time: one already running in a terminal is shown, not doubled. Needs `make setup` and Google ADC; its log is `state/listener.log`; `PIK_LISTEN_SPEAK=0` mutes Pik's voice.
8. **End meeting** stops the listener and shows the memo: the question, who to talk to and why (their verbatim receipts with sources), the next step, the questions to ask first. It follows the conclusion the meeting filed, or the last question asked when nothing was concluded.
9. **Sign out** (the chip). Sign in as **Yui Sato** (role: subject). You land on `/?as=yui` and cannot leave it: the same receipts, no other names, and `/api/ask`, `/api/rank`, other people's pages and `/settings` answer 403. Open a line, type a note ("I took this so nobody had to reshuffle; it was not a request to travel."), **Add note**.
10. Sign out, sign in as Aya again, click Yui's card: the note is on the evaluator's page, before any decision.
11. Open **Stats** (`/stats`). Three rates, each with its formula in mono under it: **dropped-claim share** (claims dropped as unsourced or unfaithful over claims proposed, from the evidence caches; 0 in keyword mode, nonzero when Gemini proposes a quote that is not in its source), **contest rate** (notes over receipt lines shown), **asks per surface** (page, slack, notion, meet, api, with the server-side latency of each). The never-read counts come from `data/manifest.json`, never from opening the files. `make stats COOKIE=<curl cookie jar>` prints the same numbers in a terminal.

Everything above is additive. With `PIK_AUTH` unset (`make run-heuristic`, `make run`), nothing asks for a session, `?as=yui` and `?present=1` behave exactly as before, and the Slack bot, the Notion watcher and the listener keep calling the same engine; they now name their surface in the ask log, nothing else changed.

## What to say when asked

- Where does the data come from? Public Slack channels, shared docs, Will Can Must sheets, opted-in AI sessions, and manager notes only beside the person's own words. DMs and private channels are never opened; the audit counts them from a manifest.
- Is that a score? No. "2 of 7 words have a receipt" is coverage of the ask by that person's own receipts, never sorted by, never shown to the person as a rank.
- What if it is wrong? The person sees the same page and can contest a line before the decision. A claim whose quote is not in its source is dropped and counted.
