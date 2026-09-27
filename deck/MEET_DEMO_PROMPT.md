# New thread: the Google Meet wow moment (generative screen, Gemini 3.8 Live)

Run `date` first, `git pull` second. Repo: `~/CODELocalProjects/hyderabaddies` (public `syang0624/hyderabaddies`; commit as Carl Kho <carl@somach.life>, no attribution lines; pull before every push; Steven pushes too). Deadline: Sun Sep 27, 11:00 AM PDT (public repo + video ≤ 90 s + PDF deck). Prelim Sun 13:30 (3 min + 1.5 Q&A).

Read in this order, nothing else first: `PRD.md` Part A (§0 to §7), `PRD.md` §9.3a, `prototype/README.md`, `prototype/live.py`, `prototype/ui/index.html`, `interviews/INTERVIEW_NOTES.md` §7 (Ryo) and §9 (Hiro), `interviews/5_VP_MEETING_SUMMARY.md` §2 and §4. The Figma tools are connected in this environment; Carl's sketch file is https://www.figma.com/design/1md8EyJXD30RKXXYb1pAoo/Untitled?node-id=1-6 (read it with the Figma tool, do not web-fetch it).

## The scenario (grounded in the interviews; fictional names on screen, always)
Two people on a call: the head of HR and a hiring manager at a large Japanese company (Carl and Steven play them; on screen the company is "Kaede Works (fictional)", the people are Rin, Yui, Kei from `prototype/data/company.json`, 197 more in `data/people.json`). They are choosing one person for a two-year overseas exchange. Today that runs on a twice-yearly sheet, the manager's paraphrase, and memory (the VP, unprompted); the evaluated person builds their own deck of what the boss did not see (Ryo); managers pitch people from memory for days a quarter (Hiro). Receipts is a silent third participant. It never scores anyone and it asks one follow-up when the ask is vague. Nothing about the VP's figures or internal matters goes on any public artifact (PRD §15, `sync.md` §J); no interviewee is named.

## The wow: the screen is composed live, from primitives, as they talk
Today `live.py` has three tools (`show_candidates`, `note`, `conclude`) and the page reacts to events. Build the next step: **the model composes the shared screen** by editing a small layout document through tool calls, and the page renders it. Five primitives, no more: `question` (the ask, as heard), `people` (up to three tiles with a one-line why each), `receipt` (one claim with its source, verbatim), `constraint` (a chip: "nobody leaves pricing before Q1"), `ask` (the bot's follow-up, shown and spoken). Tools: `compose(blocks)` replaces the document; `patch(op, block)` adds, replaces or removes one block. The engine (`engine.ask`, `engine.rank`, `extract_claims`) supplies every name and every receipt; the model only decides what is on screen and in what order. A block that names a person or a quote must carry a source id the engine returned, or the page drops it (same rule as claims).

Low cognitive load is the brief: a manager with a full plate must follow it with the sound off. One block appears at a time. Nothing scrolls. Big type, black and white (the current palette; keep `ui/index.html`'s tokens). The screen starts empty except the question. Present mode (`?present=1`) is what gets shared in the Meet.

## Beats (rehearse with `make live-sim`; it must stay green)
1. The manager states the need ("push back on a job-based culture, hold their own in English") → `question` then `people` (three tiles, re-sorted, one why each) within about a second.
2. HR adds a constraint ("nobody leaves pricing before the Q1 close") → `constraint` chip; a tile that violates it dims with the reason.
3. Someone says something vague ("just someone good") → `ask` block, spoken once through the laptop speaker (`SPEAK=1`), then silence.
4. They lean toward Yui → `receipt` blocks under her tile: her own words beside her manager's paraphrase, verbatim, with the source.
5. They agree on next steps → the conclusion prints (existing printer), receipts attached.
Everything above already works as events except the composition layer; keep the current events and add the document on top, so nothing regresses.

## Constraints that do not move
- One engine (`prototype/engine.py`, `/api/ask`). Surfaces never rank. Add to the engine if you must, and say so in the commit.
- `make live-sim` after every change to `live.py`; last runs 6/6, 0 drops. Add a beat for `compose` to the sim script.
- No new frameworks: stdlib server, one HTML page, `google-genai`, `sounddevice`. Third-party stays disclosed in `prototype/README.md`.
- Never play audio in your own tests (`SPEAK=0`); live voice tests are Carl's.
- Look at the real page in the browser before saying anything is done; hand Carl at most three items at a time.
- Steven owns Slack and Notion (issue syang0624/hyderabaddies#5); Carl is cutting the video (`deck/VIDEO_PROMPT.md`). Update `PRD.md` §4 and §11.A when the composition tools land.
