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

## For the video agent: one URL per take

Start the server (`make run-heuristic` on 8787, or `PORT=8799 MODE=heuristic python3 server.py`), open the URL at 1920x1080, record. Both takes carry the mono badge **scripted**. Nothing under `deck/` is touched by these.

| Beat | URL | What happens |
|---|---|---|
| 06_meet (UI-SPEC §8, 19.0 s) | `/?present=1&take=meet` | 1.5 s after load the page POSTs `/api/take {name:"meet"}`; the server truncates `state/live.jsonl` and spawns `.venv/bin/python live_script.py scripts/meet.json`, which replays `scripts/meet.json` through live.py's `emit` / `compose` / `place` / `filed` (same rows Gemini Live writes, through the real `engine.ask`). Both take URLs reset people.json to the base file at load, so the graph and counts match the rest frames whatever ran before. If the replay exits before writing a row (for example without `prototype/.venv`), the header shows a coral n/a after 3 s; `GET /api/take` reports `exit_code`. A row that fails inside the replay writes a status `row at N failed (...)`, shown as a header n/a, and the composed screen stays. Page time ≈ 2.3 s + the row's `at` (1.5 s page delay + ~0.6 s process spawn + up to 0.8 s poll). Rows land at 0.0 status, 0.9 heard, 2.9 compose (tiles A–Z, Yui 29 / Kei 29 / Rin nothing on file), 4.7 receipt (Yui own words, wcm-yui), 7.2 heard, 8.0 ask bar, 10.5 manager paraphrase under the own-words card (the ask clears), 11.2 heard, 12.7 conclusion card, 15.2 `Filed · 1 question to Yui · Yui and Kei can see this page`, 18.7 end. The end row keeps the screen (status Filed, antenna down); cut anywhere after it. |
| 08_crud (UI-SPEC §9, 5.5 s) | `/?present=1&admin=1&take=crud` | The page POSTs `/api/reset {people:true}` before it builds the graph and the strip (people.json back to `data/people.base.json`, people-log and tombstones cleared; annotations, caches and the filed record survive), then types `scripts/crud.json` `sentence` at `type_ms` (22 ms/char) into the real input from ≈0.3 s, presses Enter at ≈2.2 s (real `POST /api/chat`, draft tile: Will blank, 0 receipts, read-scope line, Singapore pin outlined), waits 0.8 s and presses the real Confirm (`POST /api/people` → record row, hollow node flies into Pricing, Singapore 30→31 with a clock, panel `Mika Ono · added by Aya Nakamura · <date> · Pik collects from allowlisted channels only. DMs never.`). Mika Ono is new on every run: the take is re-recordable without a manual reset, and closing the tab resets people.json again (a `pagehide` beacon), so the next page load counts 200. |
| 08b_mirror | `/?as=yui&present=1` | Yui's page, full width, no other names, no numbers. `record_candidate.py`'s selectors are kept: `.stub`, `input[id^="an-"]`, the following-sibling **Add note** button (`POST /api/annotate`). The note shows on the evaluator's page as `note from Yui Sato · <date>`. `make reset` (full reset) deletes annotations; `make people-reset` does not. |
| 07_slack why link | `/?q=<question>&focus=yui` | `POST /api/ask`, tiles A–Z, Yui's panel open. Under three content words the tiles say `Too few words to count · Pik asks instead` and print no number. |
| before | `/?present=1&before=1` | accepted, no-op (at rest). |

Scripted vs computed (UI-SPEC §15): the meet.json times and the two manager lines, the tile order (A–Z), the demo names, the typing speed and the 350 ms graph cadence are hard-coded; the three confidence numbers and their covered/missing lists (`engine.coverage`), the receipts on the tiles and in the panel, the audit counts, the city counts and the node positions (seeded force, 300 ticks, then stopped) are computed at record time. Badges: seeded (rin/yui/kei), simulated (the 197 generated colleagues), added by <name> · <date>, scripted / live (source), keyword mode / read by Gemini (engine), rules / gemini (parser). `?nonum=1` renders the bar without the number.

Libraries: d3 v7 (ISC), vendored at `ui/vendor/d3.min.js` behind `/vendor/` with a jsDelivr fallback; topojson-client and world-atlas land-110m from jsDelivr with a 3 s timeout and a dotted-grid fallback, so no take depends on the network.

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

API: `GET /api/company`, `GET /api/evidence/{id}?force=1`, `POST /api/rank {criterion}`, `POST /api/annotate {candidate, source_id, author, text}`, `GET /api/memo/{id}?criterion=`, `GET /api/audit`, `POST /api/reset`. Added for the Pik screen: `POST /api/ask {question, pool?, k?}` (rows carry `confidence`, `asked`, `covered`, `missing`; `view=subject` → 403), `GET /api/graph`, `GET /api/cities`, `GET /api/people/{id}`, `POST /api/people`, `PATCH /api/people/{id}`, `DELETE /api/people/{id}`, `POST /api/chat {text, requester}` (a draft, never a write), `POST /api/take {name}`, `POST /api/reset {people?:true}`, static `/scripts/{name}.json` and `/vendor/{file}.js`.
