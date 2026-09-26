# Demo plan: the evidence layer, worked backwards from the judging clock

> **Superseded (Sat Sep 26 ~07:45).** The scripts, beats, VP card, truth table and Q&A now live in `PRD.md` §9 and §13; the build order is `PRD.md` §12. Two things to know before quoting anything below: the figures in §2, §4 and §9 are **not cleared** for public use (see `sync.md` §J), and the line "you can bother me anytime" in §6 was Carl's, not the VP's (`sync.md` §D). Kept as the record of the 02:00 plan.

Written Sat Sep 26 ~02:00 PDT, right after the VP meeting. Input: `interviews/5_VP_MEETING_SUMMARY.md`, `STEVEN-RESEARCH.md`, `codex-packet/outputs/00-start-here.md`, `05-saturday-runsheet.md`, and the Day 1 deck (`codex-packet/work/event.txt`). This is a plan for Carl and Steven to argue with, not a decision.

Steven's "defining innovation" riff is now in `interviews/raw/6_steven-innovation_01-30-00.md` (glasses, ~01:30 Sat). Section 1 and the scripts in section 9 are built on it.

## 0. Fix the clock first

The constraints in the Day 1 deck (`event.txt` pp17–19) are not "1.5 min prelim, 3 min final". They are:

| Artifact | Limit | When |
|---|---|---|
| Submitted video or demo link | **≤ 90 seconds** | Sun 11:00 AM, in `#announcements-all` |
| Preliminary pitch | **3 min talk + 1.5 min Q&A**, all teams | Sun 1:30–2:45 PM |
| Final (3 teams) | **6 min talk + 6 min Q&A**, same slides allowed, "add more details", no setup time after prelim results | Sun 3:10–3:55 PM |

So there are three deliverables of increasing length that must nest: the 90-second video is the spine, the prelim wraps it with problem and business, the final adds architecture depth and a second live scenario. Build the 90 seconds first and everything else is packaging.

## 1. The story spine: Steven's definition of innovation

From the glasses, right after the VP meeting:

> "Innovation has to be very careful. The way that we perfectly design for the humans." (01:30:08)
> "Innovation is changing the way you think." (01:30:23)
> "Some innovations, like nukes, killed people. Some innovations actually saved the people." (01:33:38)

That is the whole pitch, and it maps onto the VP meeting cleanly. The careless version of this product exists: covert Slack mining, an AI score, a page 3,000 managers can see and the employee cannot. The VP told us that version is legal and stalled, because it is "creepy" and nobody is accountable to the employee. The careful version changes what a people decision is made of: from what the boss remembers to what the person wrote and did, and it lets the person see the page. Same data, opposite design. That is "changing the way you think" for the evaluator (think in evidence, not impressions) and for the employee (the record is yours, not about you).

Steven's worry at 01:30:41, "how this would land with the American audience": it lands. Two of the four judges built their careers on worker-facing transparency (Glassdoor's co-founder, Indeed's CTO who runs AI ethics monitoring). Careful is not a Japanese hedge here; it is the differentiator. Skip the nukes line on stage; keep "careful" and "changes how you think".

**One sentence:** evidence, with receipts, that both the evaluator and the employee can see, for one high-stakes people decision.

Not "a dashboard that consolidates Salesforce, Gmail and Slack". Consolidation is the plumbing, and the VP said Recruit already has an internal prototype of roughly that (0:56:27), Workday is in the space (0:38:58), and he has "heard this pitch before" (0:37:14). If we pitch consolidation, the Recruit-side judges shrug.

The innovation is in the three things he said he cannot do today, restated as product mechanics:

| What he said (summary timestamps) | Product mechanic | Why it is "innovation" and not a feature |
|---|---|---|
| Rollout to ~3,000 first-line managers is stalled because of misuse risk and accountability to employees, not law (0:44:24, 0:49:34). Covert reading is "creepy" (0:55:14). | **Two-sided mirror.** The employee sees exactly the evidence view the evaluator sees, and can annotate or contest any item. Nothing is shown to a manager that is hidden from the subject. | It flips his blocker into the design. It is the difference between surveillance and a shared record. It is also what a Glassdoor co-founder and an Indeed CTO who runs ethics monitoring will reward. |
| "Will" has no metric, "ない、ないね" (0:29:37). Will Can Must is asked twice a year. | **Declared will vs revealed will.** Declared = the WCM sheet in the person's own words. Revealed = what they voluntarily did in public channels, docs, projects since. The product shows the gap, with sources, and never a score. | Nobody in the space measures will. It is the thing he said HR is "most troubled by" (0:26:10). |
| Meaning drifts as it passes up the manager chain (0:34:26, "Shion likes the US → boss says she loves flying → Saudi Arabia"). | **The employee's own words travel intact.** Every summary line links to the original message, doc or sheet line. The manager's paraphrase is shown next to the source, not instead of it. | Grounded citations are a known LLM technique; applying them to the HR chain of custody is the fresh angle. |
| 800 skill tags scored 1–5, matched to tagged jobs (0:32:26). Still "guesswork" (0:34:48). | **Borrow their taxonomy as the schema.** Do not invent roles or segments. Tags stay; the product attaches evidence and "will" to each tag, so a 4/5 comes with three receipts instead of a number. | Answers the "why is this better than our prototype" question directly: same tags, plus provenance, plus the employee's side. |

The state-representation / POMDP worry ("we don't know which data is useful") is real for a production system and irrelevant for the demo. The demo fixes the decision first, then shows only the evidence that decision needs. Purpose limitation is the VP's own requirement (0:08:09) and it doubles as our answer to "which data".

On "go deep since they don't know": no. He told us covert is what blocks him, two of the four judges built their careers on worker-facing transparency, and the repo is public. The flashy move is the opposite: show the employee's view on stage. That gets the gasp without the ick.

## 2. One decision, one person, one benefit

Pick the highest-stakes people decision he named with a number: **who goes on the two-year Indeed exchange** (0:20:40, cost per person at 0:20:54; keep the figure out of the public deck unless he clears it). Today: the boss's memory, a WCM sheet from months ago, and HR interviewing the person directly to fight a boss who does not want to lose them (0:35:36).

Fictional cast (label as fictional everywhere): a mid-size Recruit-like company, three candidates for one exchange slot, one HR planner (the user), one skeptical line manager. Seed ~200 public Slack messages, a handful of docs, three WCM sheets, three manager notes, ~30 of the 800 tags. Everything traceable, nothing real.

Benefit statement for the README: *"An HR planner picks one of three people for an expensive transfer using each person's own words and work, with every claim linked to its source, and each candidate can see and contest the same page. Today the same decision runs on the manager's paraphrase."*

## 3. The 90-second video, beat by beat

Prerecorded is allowed; say so in the first frame.

| t | Beat | On screen | What must be real |
|---|---|---|---|
| 0–12 | The stuck moment | "Aya has to pick one of three people for a two-year overseas exchange. The decision today: a six-month-old Will Can Must sheet and what each boss remembers." Three near-identical tag radar charts. | Nothing yet. Fixture. |
| 12–25 | The drift | Manager note on candidate B: "loves travel, flexible on location." Beside it, B's own WCM line: "I want to work with the US product team on X." The paraphrase and the source, side by side. | Fixture, but the pairing UI must be the real component. |
| 25–60 | Core transformation | Click B → evidence page. Declared will (sheet), revealed will (four public Slack threads and one doc where B volunteered for US-facing work), tag scores each expanded into 2–3 receipts. Gemini summary of strengths and gaps, every sentence footnoted to a source. Hover a footnote, the original message appears. | **Live.** Extraction, tag grounding and citation must run on the seeded corpus with a real Gemini call on Vertex (`recruit-hackathon-2026-e` works per HANDOFF). |
| 60–75 | The unplanned condition | Aya types a new criterion: "we need someone who will push back on a job-based culture, not absorb it." Ranking and evidence re-order live; a new receipt surfaces for C. Then the turn: **switch to "what B sees"**. Same page. B adds a note to one thread: "I was covering for a teammate here, not volunteering." The note appears on Aya's side. | **Live** re-rank on a free-text criterion (this is what survives Q&A). Employee annotation round-trip must actually persist. |
| 75–90 | The usable artifact and the boundary | One-page decision memo with receipts, plus an audit strip: "Sources used: public channels, shared docs, WCM sheets. Never read: DMs, private channels. Both candidates viewed this page." Fade to: "Fictional company. Seeded data. Extraction, grounding, re-ranking and annotations run live." | Memo generated live from the same evidence; audit strip is derived from the policy config, not typed. |

Someone watching should be able to say the before and after without the words "AI dashboard": *"HR used to decide from the boss's summary; now they decide from the person's own words, and the person can see it."*

## 4. Prelim (180 s) and final (360 s), nested on the same spine

Prelim, roughly following the template order the deck requires (Title, Problem, Inspiration, Solution, Impact, Differentiation, Technical, Roadmap):

| s | Section | Content |
|---|---|---|
| 0–10 | Title | One line: evidence with receipts for people decisions. |
| 10–35 | Problem | A VP of HR at a ~50k-person company told us this week that internal matching still runs on memory and intuition, that "will" has no metric, and that words drift up the chain. (Quote only what he clears; no pilot details, no undisclosed-to-employees line.) |
| 35–55 | Insight | The blocker is not data or legality. It is accountability to the employee. So the product is symmetric by construction. |
| 55–110 | Solution / demo | Play the 25–75 s stretch of the video live if the network holds, else the recording. |
| 110–135 | Impact | Two numbers with labels: the count of managers the customer wants to reach but cannot today (VERIFIED, from the meeting, if cleared); replaced spend on matching and training (RESEARCH / from meeting, time basis unconfirmed). Everything else ILLUSTRATIVE. |
| 135–150 | Differentiation | Same tags as the incumbent prototype, plus provenance, plus the employee's side. Workday scores; we cite. |
| 150–170 | Architecture | One diagram: connectors → policy gate (purpose, allowed sources, DM exclusion) → evidence extractor → tag grounding → citation store → two views (evaluator, subject) → memo. Mark seeded vs live. |
| 170–180 | Roadmap | Pilot on one decision type with one HR COE; extend to onboarding matching and mentor discovery (Shion's pain). |

Q&A (90 s) prepared answers, in the order judges are likely to ask them: who pays and for what decision; why not Workday or the internal prototype; what happens to a wrong summary (the subject sees it and contests; nothing is a score); which data and who consented (public channels, shared docs, sheets; DMs never; the subject sees the same page); what is hard-coded (the corpus) and what runs (extraction, grounding, re-rank, annotation).

Final adds: a second live scenario where a judge supplies the criterion; the architecture slide expands to the policy gate and the citation store; the truth table goes on screen; the Shion mentor-discovery use case as the second decision type (ties Steven's Vouch memo in as the roadmap, not a second product).

## 5. What to build, in order, so Saturday night has a submittable v1

The runsheet's 2:30 PM gate stands. This is what fills the hours before and after it.

1. **Corpus and fixtures (2 h).** Fictional company, three candidates, ~200 Slack-shaped messages in JSON, three docs, three WCM sheets, three manager notes, ~30 tags from a plausible taxonomy. No real names, no real quotes from the VP meeting inside fixtures.
2. **Policy gate (30 min).** A config that lists allowed sources and the decision purpose. The audit strip reads from it. Cheap, and it is the slide that answers the ethics question.
3. **Evidence extractor + grounding (3 h).** Gemini on Vertex: for each candidate and each relevant tag, pull the supporting items, produce a claim, attach source ids. Reject any claim without a source id. This is the key technical idea the rubric wants proven ("PoC shows that the key technical idea works", 30%).
4. **Free-text criterion re-rank (1.5 h).** Take a criterion string, re-score candidates from the evidence, return new receipts. This is the live, unhardcoded beat.
5. **Two views + annotation round-trip (2 h).** Evaluator view, subject view, one shared store. A note added on the subject side shows up on the evaluator side. Persist to a file or SQLite; no auth needed for the demo.
6. **Memo generator + audit strip (1 h).**
7. **Record take 1 of the video (by 10 PM Sat).** Then deck v1 in the template, then the prelim script read aloud with a timer.

Everything else (radar charts, animations, more tags, Gmail connector) is polish and only after the video exists.

## 6. Getting the VP to demo it himself

He offered "you can bother me anytime" (1:03:54). The ask is small and specific: five minutes, his own decision type, our laptop. Give him a card with five steps:

1. Here are three people for one exchange slot. Pick one from the manager notes alone.
2. Open a candidate. Read the declared will next to the manager's paraphrase.
3. Type a criterion in your own words. Watch the evidence re-order.
4. Switch to the employee's view. It is the same page.
5. Would you show this page to a first-line manager? To the employee?

If his answer to step 5 is yes, that is the sign-off, and it is a quote we can ask permission to use. If it is no, the reason he gives is the next build item, and we still have a defensible demo.

Two things to clear with him or Shion before Sunday 11:00, because the repo is public: which of his figures may appear in the deck, and whether "a VP of HR at Recruit" may be named as the source of the problem statement. Do not put the internal pilot's disclosure status or the internal prototype in any public artifact.

## 7. Truth table for the README and the deck

| Component | Status in the demo |
|---|---|
| Company, people, messages, docs, sheets | Fictional, seeded |
| Slack / Gmail / Salesforce connectors | Proposed; the demo reads JSON fixtures shaped like their exports |
| Policy gate and audit strip | Real, config-driven |
| Evidence extraction and tag grounding with citations | Live, Gemini on Vertex |
| Free-text criterion re-ranking | Live |
| Subject annotation round-trip | Live, local store |
| Decision memo | Generated live from the evidence store |
| 800-tag taxonomy | Illustrative subset of ~30; the real taxonomy is the customer's |
| Any score or ranking presented as a verdict | None, by design |

## 8. Added ~02:15 Sat: Claude session logs as an evidence source

Carl's idea, thinking out loud: employees' corporate Claude accounts, and the Claude Code sessions stored locally on their laptops, are a signal nobody in the space uses.

**Use it as evidence of will and judgment, not effort.** What a session shows: which problems the person chose to pick up, how they decomposed them, what they asked for, where they got stuck, what they rejected. That is closer to "revealed will" than any Slack thread, and it is already on the employee's own machine, which makes it the cleanest fit for the two-sided mirror: the employee opts a session in, sees the same summary the evaluator sees, and can redact or annotate before it is shared.

**Do not pitch it as productivity or "how hard they work."** Two reasons, both from this week: the moment it measures effort, people type "complete my job" and paste everything (Carl's own objection, and the gaming problem from the Philippines example at 0:46:51); and covert capture is the exact thing the VP said blocks rollout to 3,000 managers. Session count, token volume and hours are the wrong metrics and would sink the pitch with the Indeed and Glassdoor judges.

**Demo cost.** One extra evidence source in the fixtures: two or three fictional session summaries per candidate (problem, approach, outcome, one quoted prompt), each with a source id, feeding the same extractor. Half a day at most, after the core spine runs. Worth a single line on the architecture slide ("sources: public channels, shared docs, WCM sheets, opted-in AI session summaries") and a strong Q&A answer to "what data no one else has."


## 9. Scripts, timed

Official limits from the Day 1 deck: submitted video ≤ 90 s; prelim 3 min + 1.5 Q&A; final 6 + 6. Carl's working targets are tighter (1.5 min and 3 min), which is fine: a 90-second spine that also serves as the prelim core, and a 3-minute version that is the prelim as delivered and the first half of the final. Word counts assume ~150 spoken words per minute.

### 90 seconds (video, and the prelim core) — ~225 words

Screen cues in brackets. Prototype: `prototype/`, run with `make run-heuristic` or `make run`.

> [Title card] Every year, HR at a fifty-thousand-person company picks who gets the two-year overseas posting. It costs about as much as a house. And the decision runs on what the boss remembers.
>
> [Click Yui Sato] Yui wrote on her own sheet: "I want to work with the US product team on pricing experiments." Her manager wrote: "loves travel, flexible on location." Same person. That is not a data problem. It is a translation problem, and it gets worse at every level up.
>
> Steven said it on the way here: innovation has to be careful. It has to be designed for humans. So we did not build a score. We built receipts.
>
> [Click a footnote chip] Every line links to what she actually did: the partner notes she volunteered to take, the English practice she asked for, the experiment she designed.
>
> [Type a criterion, Re-rank] Type what you actually need, in your own words. The evidence re-orders, and it shows you why.
>
> [What the candidate sees] And here is the careful part. Yui sees the same page. She can add context. [Add note] Her note lands on the evaluator's desk before the decision is made.
>
> [Decision memo] One page. Every claim sourced. What we read. What we never read.
>
> Innovation is changing the way you think. We change what a people decision is made of: from what the boss remembers to what the person did. And we let the person see it.

### 3 minutes (prelim as delivered; first half of the final) — ~450 words

> **Problem (30 s).** This week a VP of HR at a fifty-thousand-person company told us how internal matching works: twice a year, a Will Can Must sheet, a conversation with the boss, and then HR decides from memory. He said "will" has no metric. He said the words change as they pass up the chain. He said this is the thing HR is most troubled by. [Only quote what he clears. No pilot details.]
>
> **Insight (25 s).** Everyone in this space, including the company's own prototype and Workday, is building the same thing: mine the data, produce a score, show managers. It is legal, and it is stalled, because employees find it creepy and nobody is accountable to them. The blocker is not data. It is design. Innovation has to be careful. It has to be designed for the humans in it.
>
> **Demo (90 s).** [The 90-second spine above, live if the network holds, else the recording. Say it is a recording if it is.]
>
> **Impact (25 s).** The customer wants to put this in front of roughly three thousand first-line managers and cannot today. [VERIFIED, from the meeting, if cleared.] The spend it would replace, training and matching systems, is on the order of two hundred million yen a year at their low estimate. [RESEARCH: from the meeting; time basis unconfirmed.] The number that matters more: one wrong posting is a two-year, house-priced mistake for the company and a career detour for the person.
>
> **Differentiation (15 s).** Same skill tags they already have. Plus provenance on every claim. Plus the employee's side of the page. Workday scores. We cite.
>
> **Architecture (20 s).** [Diagram] Sources pass a policy gate: purpose, allowed sources, private messages excluded by config. An extractor produces claims; any claim without a source id is dropped. A criterion re-ranks the evidence; a human decides. Two views over one store. Fixtures are fictional; extraction, re-ranking, annotation and the memo run live.
>
> **Roadmap (10 s).** One decision type with one HR team. Then mentor discovery and onboarding matching, the same engine on a second decision.

### Final (6 min): what to add

The 3-minute script, then: a judge supplies the criterion live; the opted-in AI session summaries as "data no one else has"; the architecture slide expanded to the policy gate and the citation store, with the truth table on screen; the answer to "why not the internal prototype" in one breath. Q&A prep is in `PREP-HOJOON-CHA.md` and section 4.

### Q&A lines to have ready (both rounds)

- **Who pays?** HR COE, for one decision type, replacing part of a matching and training budget it already spends.
- **Why not Workday or their own prototype?** They produce a score for managers. We produce receipts for both sides. The difference is what unblocks rollout.
- **What if the summary is wrong?** The person it is about sees it and contests it before the decision. Nothing is a verdict.
- **Which data?** Public channels, shared docs, sheets already given to HR, AI sessions the person opts in. DMs are excluded by config; the audit strip shows the count of items never read.
- **What is hard-coded?** The company and people. What runs: extraction with citations, re-ranking on a free-text criterion, the annotation round-trip, the memo.
