# Evidence layer, prototype

Evidence with receipts, for one people decision, that the evaluator and the subject both see. Fictional company, fictional people, seeded data. Extraction, re-ranking, annotations and the memo run live.

Written Sat Sep 26 2026 during Innovation Cup, after the opening ceremony. Third-party components: `google-genai` (Apache-2.0), only in Gemini mode. Everything else is the Python standard library and one HTML file.

## Run it on a Mac in 60 seconds

```bash
cd prototype
make run-heuristic          # no credentials, no network, deterministic
open http://localhost:8787
```

With Gemini on Vertex (the Recruit project):

```bash
cd prototype
make setup                                  # once: venv + google-genai
gcloud auth application-default login       # once
export GCP_PROJECT=recruit-hackathon-2026-e # default already
export GEMINI_MODEL=gemini-3.8-flash        # default already
make run                                    # auto: Gemini if it answers, else heuristic
```

`make run-gemini` forces Gemini and fails loudly if credentials or quota are missing. `make reset` clears cached evidence, the last ranking and annotations. `make smoke` hits every endpoint on a running server. The header of the page shows which backend answered.

## The live meeting layer (the wow moment)

Two people on a call, an HR planner and a hiring manager. The manager says who they need. The shared screen re-sorts the candidates on those words and shows the receipts. When they agree on a next step, a pop-up shows what the meeting concluded: who to talk to, next steps, questions to ask before deciding.

```bash
cd prototype
make setup                    # once: google-genai + sounddevice
make run-heuristic            # terminal 1, the page
make live                     # terminal 2, mic -> gemini-3.8-live (Vertex, us-central1) -> tool calls
```

`MIC="MacBook" make live` picks an input device by name. Events land in `state/live.jsonl`; the page polls `/api/live`. Nothing is recorded to disk except those events. `SPEAK=0 make live` never plays audio (the sim forces this).

### The screen is composed live, from five primitives

The model does not draw; it edits a small layout document and the page renders it. Two tools: `compose(blocks)` replaces the document, `patch(op, block)` adds, replaces or removes one block (`conclude` is the third tool, unchanged). Five block types, no more:

| Block | The model supplies | The engine fills in |
|---|---|---|
| `question` | the ask, as heard | nothing |
| `people` | `criterion` | up to three tiles from `engine.ask` (name, role, one why, source id), in the engine's order |
| `receipt` | `person`, `kind` (`own_words`, `manager`, `claim`), `about` | the verbatim quote, its source label and id (`engine.receipt_for`) |
| `constraint` | the chip text | which tiles it touches, from facts on file: team, location, availability (`engine.constraint`) |
| `ask` | the follow-up (or the engine's `follow_up` when the ask is too vague to fill tiles) | spoken once through the speaker when `SPEAK=1`, then silence |

The model never names a person or quotes anyone itself. A tile or a receipt must carry a source id the engine returned; the page checks it against the evidence store (and, for a receipt, that the quote is in the source) and drops it otherwise, counting the drops in the footer. The screen starts empty except the question; blocks appear one at a time; nothing scrolls. A `compose` carries the question and the constraint chips forward unless the model removes them; a changed question re-runs the tiles on the new words; an `ask` sits over the last tiles until a receipt or fresh tiles answer it. `?present=1` is what gets shared in the Meet; Esc hides the composed screen outside present mode.

`make live-sim` speaks a seven-line scripted call (macOS `say`, never through the speakers) into the same session and grades which blocks landed after each line: question + people, constraint, people (Japanese), ask, receipt, conclude. The old events (`show_candidates`, `note`, `follow_up`, `conclude`) are still emitted beside `compose` / `patch`, so the page underneath keeps working.

## The engine behind every surface (Meet, Slack, Jira)

One engine, three thin surfaces. A surface asks one question and renders the answer; it never ranks on its own.

```bash
make people                 # once: the fictional company, 200 people -> data/people.json
make ask Q="who can run the Northwind sync in English"
curl -s -X POST localhost:8787/api/ask -H 'Content-Type: application/json' -d '{"question":"best person for the pricing write-up","context":"Jira ticket PRC-214","requester":"aya"}'
```

Response: `{"people":[{"id","name","role","team","location","languages","why":[...],"receipts":[{"text","source","source_id"}],"load":{"open_tickets","hours_booked_this_week"},"availability","support"}], "follow_up": null | "one clarifying question", "criterion", "considered", "note"}`.
`follow_up` is set when the words are too vague to rank; then `people` is empty and the surface asks the question instead of guessing. Order is evidence overlap with the words minus a load penalty; `support` is never shown to the person named. The "why" behind any name is the receipts page: `/?as=<id>` for the person, `/` for the evaluator.

`GET /api/people?q=engineer` lists people (no receipts) for pickers.

## Surfaces: Slack and a Notion board (both call `/api/ask`, nothing else)

```bash
make slack     # Socket Mode bot: ask "who is best for ..." in a channel it is in, or @mention it -> best person, why, load, alternates, "Loop in" button, "Why? See the receipts" link
make notion    # board watcher: a ticket whose "Suggested owner" is empty gets an owner, a why and a receipts link within 5 s
```

Secrets live in `.env` at the repo root (gitignored; copy `.env.example`) or in `~/.config/carl-life-os/.env`, never committed: `PIK_SLACK_BOT_TOKEN`, `PIK_SLACK_APP_TOKEN`, `PIK_NOTION_TOKEN`, `PIK_NOTION_DB`, optional `PIK_PUBLIC_URL` (a LAN address so links open from a phone). Third-party: `slack_bolt` (MIT), `notion-client` (MIT). The people are fictional, so a "mention" is text and the board's owner is a text property; a Jira or Linear assignee field would need real users.

The "why" link opens the receipts page with the question prefilled: `/?q=<question>&focus=<person id>`.

## The 90-second demo, click by click

1. Page opens on Rin. Read the two boxes at the top: her own Will Can Must line beside her manager's paraphrase.
2. Click **Yui Sato**. Own words: "I want to work with the US product team on pricing experiments." Manager: "loves travel, flexible on location." Same person.
3. Scroll the evidence list. Every claim has a footnote chip; click one and the original message, doc, sheet line or opted-in AI session appears.
4. In the criterion box type something the fixtures did not plan for, and press **Re-rank on evidence**. Ranking and receipts re-order. Fit is a re-ordering of evidence, never a verdict.
5. Press **What the candidate sees**. Same page. Open the source under any claim and add a note ("I took this so nobody had to reshuffle, it was not a request to travel"). Switch back to the evaluator view; the note is there.
6. Press **Decision memo**. One page with receipts, the candidate's notes, and the audit strip: what was used, what was never read.


## What is real and what is seeded

| Component | Status |
|---|---|
| Company, people, Slack messages, docs, WCM sheets, manager notes, AI session summaries | Fictional, seeded in `data/` |
| Slack / Gmail / Salesforce connectors | Proposed. The demo reads JSON shaped like their exports |
| Policy gate (`policy.json`) and audit strip | Real, config-driven. `dm.json` exists on disk and is never read |
| Claim extraction with source ids | Live. Gemini on Vertex, or keyword mode. Claims without a valid source id are dropped and counted |
| Free-text criterion re-ranking | Live |
| Subject annotation round-trip | Live, stored in `state/annotations.json` |
| Decision memo | Generated live from the evidence store |
| 800-tag taxonomy | Illustrative subset of 25 tags in `data/company.json` |

## Layout

```
prototype/
  policy.json      allowed and excluded sources, purpose, rules
  engine.py        gate -> items -> claims with receipts -> rank -> annotate -> memo
  server.py        stdlib HTTP server, JSON API + static UI
  ui/index.html    evaluator view, subject view, criterion box, memo
  data/            fixtures (fictional)
  state/           caches and annotations (gitignored)
```

API: `GET /api/company`, `GET /api/evidence/{id}?force=1`, `POST /api/rank {criterion}`, `POST /api/annotate {candidate, source_id, author, text}`, `GET /api/memo/{id}?criterion=`, `GET /api/audit`, `POST /api/reset`. Added for the Pik screen: `POST /api/ask {question, pool?, k?}` (rows carry `confidence`, `asked`, `covered`, `missing`; `view=subject` → 403), `GET /api/graph`, `GET /api/cities`, `GET /api/people/{id}`, `POST /api/people`, `PATCH /api/people/{id}`, `DELETE /api/people/{id}`, `POST /api/chat {text, requester}` (a draft, never a write), `POST /api/reset {people?:true}`, static `/vendor/{file}.js`.
Judge walkthrough (all additive, see `DEMO.md`): `GET /login`, `POST /api/login {who, workspace}` (signed cookie; `PIK_AUTH=1` makes every other route require it, pages redirect to `/login`, APIs answer 401), `GET /logout`, `GET /api/session`; `GET /settings`, `GET|POST /api/byok {kind: api|vertex, api_key | project, location}` (stored in `state/byok.json`, returned masked), `POST /api/byok/test`; `GET /stats`, `GET /api/stats`. A signed-in subject is pinned to `/?as=<id>` and gets 403 on the ask, the ranking and other people's pages. `/api/ask` accepts `surface` (page, slack, notion, meet, api) and appends one row per ask to `state/asks.jsonl`.

Meeting controls (additive; the page's mic button, End meeting, the surface buttons and the Activity lists):
- `GET /api/context`: `{workspace, decision, detail}` from `policy.json` and the decision it names; public, the sign-in card reads it.
- `GET /api/surfaces`: Meet, Slack and Notion URLs from `.env` (`PIK_MEET_URL`, `PIK_SLACK_URL`, `PIK_NOTION_URL`), whether the Slack bot and the Notion watcher run, and the listener's `{running, pid, started_by: page|external}`.
- `POST /api/listen {on: true|false}`: starts `live.py` (MODE=heuristic, `SPEAK` from `PIK_LISTEN_SPEAK`, `MIC` from `PIK_MIC`, log in `state/listener.log`) or stops the one the page started; never a second listener; one started in a terminal answers 409; subject 403.
- `POST /api/end {}`: stops the page's listener and returns `{question, memo_markdown, people, concluded, listener_stopped}`, the memo of the meeting's filed conclusion or, without one, of the last ask; subject 403.
- `GET /api/source/{slack|docs|sheets|sessions}?limit=50&q=&person=`: every item of that allowed source, newest first, `count` before the limit (34, 5, 3, 4 on the fixtures); manager notes and DMs are never listed; subject 403.
