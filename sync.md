# sync.md: the shared reasoning log

For Carl, Steven, and any agent either of them runs. **Read this instead of re-deriving.** [PRD.md](PRD.md) says *what* to build; this file says *why*, with the evidence each decision rests on, the alternatives that were rejected, and the fact that would reverse it. If an agent is about to research or re-argue something, check §F first: it may already be done.

**How to keep it current:** append to §K as `[HH:MM] [Carl|Steven|agent-name] one line`. Edit a decision entry in §B only by adding a dated "revised:" line under it; never delete history. Timestamps are PDT.

Started Sat Sep 26 2026, ~04:30 PDT, by Claude (Fable 5.1) in Steven's session. Updated ~07:45 after the PR #3 review (fifteen verified findings; PRD v2) and ~14:15 after Carl's live layer and the Ryo interview (PRD v3).

---

## A. State of play (Sat Sep 26, ~14:15 PDT)

- **Repo `syang0624/hyderabaddies`, `origin/main` at `320778d`** (Steven merged Carl's `carl/fable-handoff` at 02:17). **The repo is public.** See §H before adding anything.
- **What exists:** `DEMO-PLAN.md` (Carl + agent, ~02:00: scripts, build order, truth table), `HANDOFF.md` (Carl, updated 02:30), `PREP-HOJOON-CHA.md`, `prototype/` (Sat 02:06: a 588-line stdlib Python server + one HTML page + fixtures; runs in keyword mode; the Gemini path has never been exercised), `interviews/5_VP_MEETING_TRANSCRIPT_RECONCILED.md` (two-source, speaker-labelled, translated) and `5_VP_MEETING_SUMMARY.md`, `interviews/6_STEVEN_INNOVATION_FRAME.md`, `codex-packet/` (Friday's research, ten fictional council rehearsals, two verification passes), `STEVEN-RESEARCH.md` (the Vouch memo, Fri 23:55), `PRD.md` v2 and this file (PR #3, branch `steven/prd-and-sync`; v1 was reviewed by fifteen verifiers and rewritten as v2 at ~07:45).
- **What runs (14:00):** `cd prototype && make run-heuristic` → http://localhost:8787, now with the dark layout, expandable claims, source icons and the evaluator/subject toggle; `make live` runs Carl's live meeting layer (microphone → Gemini 3.8 Live on `us-central1` → `show_candidates` / `note` / `conclude` tool calls → the page re-ranks on the spoken criterion and shows a conclusion pop-up). Gemini and Live need ADC on the demo laptop (the Makefile defaults to Carl's path). Claude on Vertex has zero quota there (429); do not plan on it.
- **What is decided:** everything in §B. In one line: the evidence layer for one high-stakes people decision (who goes on the two-year exchange), with receipts on every claim and the employee seeing the same page; Steven's "careful / designed for humans / changes how you think" frame as the story; four demo beats (drift chain, two-sided mirror, judge-supplied criterion, 2050 epilogue); FastAPI + React/Vite/Tailwind; real Slack in Socket Mode shown live in the final only; email as interface + stub + watcher; SQLite; no score ever presented as a verdict; Sunday's codebase is `prototype/` with the live layer (D28); the product repo is created as a subtree of it at submission and this research repo goes private (D18 revised in D30); the demo opens on the live meeting and the drift chain is demoted (D29).
- **Clock:** submission Sun 11:00 AM PDT in `#announcements-all` (public repo, demo link or ≤ 90 s video, PDF deck); prelim Sun 1:30–2:45 PM (3 + 1.5 min); final 3:10–3:55 PM (6 + 6). Saturday organizer rows: gather 12:30, lunch/mentoring 12:30–2:30 (**Hiro slot already booked 1:30–2:00 PM**, per BRAIN.md and floor audio), work 2:30–5:00, mentoring 5:00–6:00, announcements 6:00–6:40 (**prelim order at 6:30**), tech support 10–11 AM and 8–9 PM, venue locked to hotel-only 0:00–6:00.
- **Who is where:** the VP meeting happened (recording 00:09:40–01:21, 72 minutes of audio, Shion interpreting). No follow-up has been sent to anyone since; every message to the VP, Shion, mentors or judges is a draft until Carl approves the exact text (Carl's rule, HANDOFF).

---

## B. Decision log

Format: **what** · why (evidence) · rejected · confidence · reversal fact.

**D1. Direction: the evidence layer for one high-stakes people decision.**
- Why: the VP's own top pain is team shape and careers as AI dissolves roles (「一番困ってる」 `[R 0:26:10]`, unprompted follow-up `[R 0:26:32–0:26:47]`); will has no metric `[R 0:29:38]`; matching runs on intuition plus an AI skill-tag system `[R 0:31:30–0:33:24]`; paraphrase drifts up the chain and HR's fix is to re-interview `[R 0:34:48–0:35:57]`; evidence exists but accountability, not law, blocks it `[R 0:42:26, 0:44:24, 0:55:14]`; the one idea he endorsed on value was Carl's evidence-for-evaluators reframe `[R 0:56:18–0:56:43]`. PRD §2.
- Rejected: **Vouch as the lead** (Steven's Fri memo: dossier assembly + mentor finder + approval router) because the VP never mentioned mentors, approvals or Salesforce, Indeed already sells candidate summarisation, and the councils scored it lowest on creativity; it survives as the second decision type (PRD §14). **Path B (live experiment)** and **path C (work rehearsal)** from the Codex packet: nothing in the VP meeting supports either. **Consolidation dashboard**: the customer is attempting something like it `[R 0:56:27]`, Workday is in the space `[R 0:38:58]`, "heard this pitch before" `[R 0:37:33]`. **Covert monitoring**: legal but blocked by accountability and "creepy" `[R 0:44:24, 0:55:14]`.
- Confidence: high that the problem is real and his; medium that the two-sided design is what unblocks him (he never said "show the employee"; that is our inference from his blockers); low on demand (no pilot commitment; "would be willing to try?" was never translated).
- Reversal: he or Shion says the internal attempt already shows the employee the page; or a template plus corporate Claude produces an equally trusted page (test in the pilot).

**D2. Story spine: Steven's innovation frame.** "Innovation has to be very careful… designed for the humans… changing the way you think" (`interviews/6_STEVEN_INNOVATION_FRAME.md`, 01:30:08–01:30:23). Steven owns it, Carl reviews before it is said on stage (01:33:49). Rejected: the "nukes" line (01:33:38) on stage; "something that works for a company" (01:32:44) as the primary definition (it pulls against the employee-centred rules). Confidence: high (Steven confirmed "keep that" at 02:30). Reversal: none needed.

**D3. Demo case: who goes on the two-year overseas exchange.** Why: the one people decision the VP quantified `[R 0:20:51–0:21:03]`; rare and high-stakes, so a purpose-locked page is credible instead of a standing profile; the paraphrase problem bites hardest where the boss who writes the note loses the person `[R 0:35:36]`. Rejected: promotion decisions (more sensitive, closer to the internal matters he described); team formation (too broad for 30 hours); mentor discovery (Shion's; roadmap). Confidence: medium-high. Reversal: the VP says exchange selection is not the COE's decision (ask in the self-demo card).

**D4. Four wow beats, in this order: drift chain → two-sided mirror → judge-supplied criterion → 2050 epilogue.** Steven picked all four at 02:45. Why each: the drift chain is a "before" nobody has seen and it is P2 made visible; the mirror is the ethical turn that a Glassdoor co-founder and an Indeed CTO will recognise; the judge-supplied criterion is the standard proof that nothing is hard-coded (the GPT-4 sketch precedent); the epilogue is Steven's 2050 ask kept to five seconds. Rejected: a before/after of tool consolidation (Steven: too common; §D1); radar charts of people; any AI score. Confidence: high on 1–3 as demo mechanics; medium on 4 (framing risk, see D13). Reversal: the drift chain produces boring paraphrases with Gemini at T=0.8 (then use seeded chains labelled as recorded).

**D5. Stack: FastAPI + React/Vite/TypeScript/Tailwind; keep the engine logic; Gemini 3.8 Flash with structured output; honest keyword-mode fallback.** Steven's pick at 02:45 (recommended option). Why: the prototype audit found the stdlib server and inline-JS page throwaway but the policy schema, claim schema, id-validation rule, prompts and fixtures reusable; the interactive beats (hover receipts, view flip, animated re-order, drift stepper) need real components; two people can split API and UI cleanly. Rejected: HTMX (weaker for the beats), Next.js rewrite (rewrite risk with ~30 h), vanilla restyle (least capable). Confidence: high. Reversal: `npm ci` or Vite fails on the venue network (then serve a built `web/dist` from FastAPI).

**D6. Slack: a real app in Socket Mode on a throwaway workspace; simulated pane as fallback; real-or-cut at Sun 09:00.** Steven's pick. Why: "not yet another app" (Steven, 02:30) needs a real intake to be true; Socket Mode needs no public URL; internal apps are exempt from Slack's 2025 rate-limit change; the 3-second ack rule is designable. Rejected: Events API + ngrok (public URL, venue firewall risk); simulated only (the claim would be false). Confidence: medium (venue Wi-Fi). Reversal: the bot cannot post a card by Sun 09:00.

**D7. Email: documented adapter interface + working local stub; real transport proposed.** Why: Mercury's forward-to-an-address pattern is Steven's reference and is cheap to show honestly (drop a JSON message into an inbox folder, watch the annotation arrive with an "email" chip); a real inbound provider is a half-day nobody has. Confidence: high. Reversal: none.

**D8. Storage: SQLite (stdlib) over JSON files.** Why: the Slack process, the email stub and a second laptop all write during the demo; SSE replay needs a monotonic cursor; reset must restore the seeded start without losing the warm LLM cache; the prototype's JSON state produced a positional-id race. Confidence: high.

**D9. No score is ever presented as a verdict; "support" is never shown to subjects and never in the memo.** Why: the VP's stated fear is wrong AI output driving a promotion or transfer `[R 0:48:34]`; Indeed's own Smart Screening ships a "Smart Fit Score" and says hiring stays human, which is the contrast we want; Workday scores. Rejected: silently removing the number from the system (then the audit strip would lie about what exists). Chosen: in present mode the number is hidden and only the bar is shown, the value stays in the evaluator's JSON, and the audit strip states that support values exist. Confidence: high. Reversal: a judge insists a bar is a score anyway (answer in PRD §9.8).

**D10. DMs and private channels are excluded by configuration and counted from a manifest the tool cannot open.** Why: 「すげえ気持ち悪ぃ」 `[R 0:55:14]`; the prototype computed the "never read" count by reading `dm.json`, which is the opposite of the claim. Confidence: high.

**D11. The two-sided mirror: the subject sees the same page, minus numbers, and can contest before the decision.** Why: his blocker is accountability and transparency to employees `[R 0:44:24]` and misuse by managers `[R 0:49:34]`; symmetry is the design that removes both; the subject's note replaces HR's manual re-interview `[R 0:35:57]`. Rejected: an employee-only summary (different layout would invite "what is hidden?"). Confidence: medium-high (inference from his blockers, not his words). Reversal: managers stop writing notes and HR prefers their silence.

**D12. The drift chain as beat one.** Why: P2 with a demo that is about people, not hardware; a judge can supply the sentence; it is the packet's "changed condition changes the consequence" proof in narrative form. Design: three sequential Gemini calls with one persona each, T=0.8, content-word-overlap check with one retry; the "with receipts" variant is code-enforced (`verbatim_ok`). Confidence: medium (quality risk). Reversal: see D4.

**D13. 2050 epilogue, small, framed as "same page, same rules for a mixed workforce", never "HR for robots".** Why: Steven asked for it ("be creative", 02:30); Japan context is citable (Recruit Works 11M shortfall by 2040; Moonshot Goal 3; Telexistence/7-Eleven humanoid target 2029); but the VP's first pain is employees fearing AI will take their jobs `[R 0:04:16]`, so a robots-replace-humans frame would land badly with the customer. Confidence: medium. Reversal: rehearsal shows it costs more than five seconds of attention.

**D14. Keep `prototype/` frozen; build `receipts/`; migrate fixtures with stable, content-addressed ids.** Why: the audit's defect list (fixed audit strings, DM count by reading the file, purpose lock as a label, subject view leaking scores, substring matching, cache ignoring backend, no error states, `make smoke` polluting state, 0.0.0.0 bind) is cheaper to design out than to patch. Confidence: high.

**D15. VP figures and facts appear in public files only as placeholders with transcript timestamps until cleared.** Why: the repo is public; the summary itself said not to commit the transcript; organizer rule on personal information; the VP's own accountability norm. Confidence: high. Reversal: written clearance from him or Shion (§J).

**D16. Product name: "Pik".** Steven, Sat Sep 26 ~19:00 PDT. The working title was "Receipts" (from DEMO-PLAN's line "we did not build a score, we built receipts"). "Receipts" stays as the name of the evidence items: the receipts page and view, the `receipts` field in `/api/ask`, the Notion "Receipts" column. Renamed: the product in PRD/deck prompt, the page title and brand, the Slack app and bot, the Slack and Notion surface strings, the live-listener prompt, and the env var prefix (`PIK_*`; `RECEIPTS_*` still read as a fallback). Interview notes keep the old name as a record of what was said at the time.

**D17. Owner split (proposal, swap freely): A = backend (`api/`, fixtures, Slack, tests) on the laptop where gcloud works; B = frontend (`web/`), video, deck.** Why: the Gemini auth lives on one laptop; the four beats are mostly frontend; the story is Steven's. Confidence: low (your call).

**Decisions added after the PR #3 review (~07:45). Each cites the review finding that forced it; the findings are logged in §K.**

**D18. The product ships from a new public repo (`hyderabaddies-receipts`, product at its root) created at 08:30 Sat; this research repo goes private the same minute.** Why: the transcripts with the VP's internal matters are already on `origin/main`; v1 scaffolded the submission README into this repo and had no step to create a clean one, so Sunday morning would have carried a repo extraction under deadline (review finding 12). Rejected: keep one repo and rewrite history (destructive, and clones keep the blobs). Confidence: high. Reversal: Carl objects at 08:30; then the research files must leave `main` before anything else.

**D19. Keep the prototype's fixture ids (`wcm-rin`, `mn-yui`, `sl-023`) and widen the id pattern; never renumber.** Why: v1's renumbering (`mn-yui → mn-002`) produced the Rin/Yui mix-up in three examples (review finding 2 and F6); nothing needed positional ids. Confidence: high.

**D20. Slack is shown live in the final only; the video's mirror beat is recorded from the phone's web composer; there is no simulated Slack page.** Why: real Slack was scheduled after video take 1, so v1's plan implied a Sunday re-record; the simulated page needed a browser to post as the subject (an impersonation path) and would have carried a false 'real Slack' label in the video (review finding 12, F4). Confidence: high. Reversal: none; if Slack works Sunday it is a bonus in the final.

**D21. The 2050 epilogue is a seeded, badged page rendered through the real components; it does not run the extraction pipeline.** Why: v1 claimed it ran 'through the same pipeline' while its humanoid model lacked the fields the prompt used and keyword mode had no rules for its sources (sweep C3, F7); honesty and scope. Confidence: high.

**D22. Tokens are generated at `make seed`, never committed; `/api/admin/*` and `/api/viewers` are not proxied to the LAN; the service role acts only as the mapped persona; `/audit` and `/drift/examples` are scoped.** Why: v1 exposed every token and the admin routes to anyone on venue Wi-Fi and let a subject read other subjects via Slack and the audit (review finding 4). Confidence: high.

**D23. Validation requires a 5–25-word verbatim quote in the body of a cited item whose role matches the claim kind; revealed will requires the subject as author; the subject's manager's public posts resolve to the paraphrase role; the faithfulness pass runs on every surviving claim in Gemini mode; the receipt variant is checked against the source body.** Why: v1's span check passed empty quotes, header fragments and wrong-role sources, and its verbatim flag was true by construction (review finding 5). Confidence: high.

**D24. Drift has a typed mode (no source chip, a notice read aloud, an input guard for emails and long digit runs); seeded drift chains exist only when `make freeze-drift` captured Gemini output.** Why: a judge's own sentence cannot occur in any fixture, so v1's receipt path would have crashed or shown a `[None]` source; v1 also labelled hand-written chains 'recorded earlier with Gemini' (review findings 10 and 13, sweep C1). Confidence: high.

**D25. Storage: ids are decision-scoped (and backend-scoped where a collision was possible); writes are upserts with seeded rows protected; close deletes every derived row including the LLM cache and blocks every route; reset reopens; the ranking is never warmed.** Why: v1's close left claim text and notes behind, only blocked reads, and its ids collided on warm and on the pre-filled criterion (review findings 6 and 7). Confidence: high.

**D26. The video opens on a disclosure card, every beat has a word budget at 150 wpm, and the end card matches the truth table.** Why: v1's card said the memo ran on Gemini (it is templated), disclosed the recording only at the end, and overran three beats (review finding 6). Confidence: high.

**D28. Sunday's codebase is `prototype/` as Carl built it by 13:40 (plus a ten-item patch list, PRD §11.A); the FastAPI/React design (PRD §11.0–§11.13) is the post-event target.** Why: between 12:50 and 13:40 Carl shipped a dark layout, expandable claims, source icons, collapsible sidebars and the live meeting layer on the prototype; a rewrite now would cost the video. The review's defects that still apply (no quote check, client-only subject view, fixed audit strings, cache by backend, substring match, no error states, smoke pollution, unauthenticated bind) become patches ranked by demo risk. Confidence: high. Reversal: none before Sunday.

**D29. The demo opens on the live meeting (a manager says who they need; the page re-sorts on their words), then receipts, then the two-sided mirror with the line "the employee gets their own evidence deck for free", then the post-call conclusion; the drift chain is demoted to an optional final beat.** Why: Ryo, the first evaluated-side interviewee, understood team formation instantly and could not picture paraphrase drift ("I'm not clear on what is actually the scenarios"); two of three interviewees never raised drift unprompted; Carl's live layer is the strongest live proof we have and the judge can play the hiring manager. Steven picked the four beats at 02:45 with the drift chain first; this reorders them on new evidence. Confidence: medium-high. Reversal: Steven or Carl wants the drift chain back as the opener.

**D30. The product repo is created at submission as `git subtree split -P prototype` (history preserved since Sat 02:06), submitted as the public link; this repo goes private then.** Why: D18's "create the product repo first" sequencing was overtaken by the day; the subtree keeps the proof that nothing predates the opening ceremony and takes fifteen minutes. Owner A, Sun 08:30–09:00, after Carl's yes. Confidence: high.

**Overtaken for Sunday (kept for the roadmap):** D5 (FastAPI/React stack), D6 (real Slack in the final), D7 (email stub), D8 (SQLite), D24's typed drift mode, D25's close/delete. They stay in PRD §11.0–§11.13.

**D27. The prelim's problem statement uses only the VP's unprompted statements and marks our questions as ours.** Why: v1's opening credited 'decides from memory' and 'words change up the chain' to him although §2.4 lists both as led (review finding 3). Confidence: high.

---

## C. Provenance: what came from where

So nobody hunts for a source that does not exist.

| Element | Source | Not from |
|---|---|---|
| The evidence layer, declared vs revealed will, paraphrase beside source, purpose lock, audit strip, no score | VP meeting `[R]` + Carl's reframe `[R 0:55:30]` + DEMO-PLAN (~02:00) | Steven's brief |
| Two-sided mirror | DEMO-PLAN §1, derived from the VP's accountability blocker | The VP's words (he never said "show the employee") |
| Innovation frame | Steven, glasses, 01:30 Sat | The VP |
| **Slack bot, email intake, Mercury hybrid, "operating system for HR", 2050 humanoids, the "walls of text" critique, "fan out agents on best practices", "quantify and help the other judges see value"** | **Steven's spoken brief to this session, ~02:30 Sat** | Any transcript or committed file; the VP never mentioned Slack bots, email, UI, robots or 2050 |
| Four wow beats and their order | Steven's answers at 02:45 to three questions in this session | DEMO-PLAN (which had re-rank + mirror; the drift chain is new) |
| Stack, Slack Socket Mode | Steven's answers at 02:45 | Carl (not consulted; D17 is a proposal) |
| Fixture people and storylines (Aya, Rin, Yui, Kei, Hayashi, Okada, Fujii; Kaede Works; Northwind Labs; exchange-2027) | `prototype/data/*.json`, Sat 02:06 | Real people |
| "Evidence layer" as a phrase | The summarizing agent's inference, ~01:30 | The VP |
| Council verdicts in `codex-packet/outputs/council/` | Fictional rehearsals by agents, Fri night | Any judge |
| D18–D27 (repo split, id policy, Slack in the final only, static 2050, tokens, validation, typed drift, storage, video, prelim wording) | The PR #3 review (six finders, fifteen verifiers, one sweep) run in this session ~05:30–07:00 | Carl (not consulted; D18 in particular needs his yes at 08:30) or the VP |

---

## D. Corrections to existing files (do not repeat these)

| File | Says | Actually | Source |
|---|---|---|---|
| `DEMO-PLAN.md` §6 | The VP offered "you can bother me anytime" | That line was **Carl's** `[R 1:03:51–1:04:00]`; the VP said "Please feel free feel free to reach out" `[R 1:04:27]` | reconciled transcript |
| `5_VP_MEETING_SUMMARY.md` | The two-gaps framing, the Shion → Saudi Arabia example and the willingness-to-pay question were Steven's | They were **Carl's** `[R 0:34:00, 0:34:54, 0:36:36]`; "I think we know what we're doing" was **Steven** `[R 1:11:46]`; "I don't like it as well" was Carl, not Shion | reconciled transcript |
| `DEMO-PLAN.md` §1 | "Indeed's CTO who runs AI ethics monitoring" | Unsupported; it blends the VP's remark about ethics monitoring at Indeed `[R 0:10:27]` with Jim Giles's public background (Google Workspace engineering) | judges research |
| `DEMO-PLAN.md` §9, 3-min script | "two hundred million yen **a year**" while tagging the time basis unconfirmed | No time basis was given `[R 0:38:23, 0:39:34]`; and the figure is not cleared for public use | reconciled transcript |
| `DEMO-PLAN.md` §9 | The 3-minute script is ~450 words | The spoken part is 283 words plus a 90-second demo ≈ 215 s; PRD §9.4 re-times it to 180 s | word count |
| `STEVEN-RESEARCH.md` §3 Module 2 (and the framing this session inherited from it) | "> 1 day / official mission → route to manager first; casual 1-hour ask → go direct" as a rule | Two Shion data points: a week abroad needed the manager first; a one-hour 1-on-1 did not `[2_shion_20-40-00 04:06–05:07]`; PRD §14.2 now says the threshold is the customer's to configure | interview audit |
| `HANDOFF.md` | "24 unresolved spots per chunk" | 24 in total across the ten chunks (1–3 each). **Fixed in HANDOFF.md in PR #3.** | reconcile chunks |
| `.claude/launch.json` | `-C /private/tmp/hyderabaddies/prototype` | Carl's temp path; does not exist on Steven's Mac; the product repo gets its own repo-relative file (PRD §11.10) | prototype audit |
| `HANDOFF.md` line "The pitch scripts are in `DEMO-PLAN.md` section 9" | points at the superseded scripts | **Fixed in PR #3**: points at PRD §9 | this review |
| `DEMO-PLAN.md`, `PREP-HOJOON-CHA.md` | still present as if current, with uncleared figures in DEMO-PLAN §9 | **Banner added in PR #3** on both: superseded by PRD §9 / §9.8; figures not cleared; "bother me anytime" was Carl's | this review |
| `PRD.md` v1 (this PR's first version) | Rin given Yui's manager line and an invented 'Osaka'; VP internal matters restated; prelim misattribution; scoping, storage, Makefile and video defects | **Rewritten as v2** (§K lists all fifteen findings) | PR #3 review |
| `prototype/README.md` "what is real" | "Both the evaluator and X viewed this page" is real | It is a fixed string; nothing tracks views; the "never read" DM count is computed by reading `dm.json` | prototype audit |
| `codex-packet/outputs/05-saturday-runsheet.md` (Fri version) | Check whether the Hiro thread was answered | Booked 1:30–2:00 PM (BRAIN.md; floor audio segment 19-22-49 03:25–03:41); the runsheet was updated Sat 00:30 | packet second pass |

---

## E. Evidence map and ambiguity ledger

**Authoritative sources, in order of trust.** (1) `interviews/5_VP_MEETING_TRANSCRIPT_RECONCILED.md` (two audio sources aligned at 00:09:40, speakers labelled by the model, 243 Japanese lines translated, 24 unresolved spots in total, 1–3 per chunk); (2) `interviews/raw/2_shion_*.json`, `1_koki_*.json` (undiarized; the audit in `codex-packet/work/interview-audit.md` has timestamps); (3) `interviews/5_VP_MEETING_SUMMARY.md` (written from the single-source transcript; check quotes against (1); several attributions wrong, see §D); (4) `DEMO-PLAN.md`, `STEVEN-RESEARCH.md`, `codex-packet/` (analysis, not evidence).

**The five load-bearing passages with three readings each** are in PRD §2.3. **Interviewer-supplied claims** (led, then confirmed with a word): matching from memory `[R 0:31:05–0:31:27]`; the two gaps `[R 0:34:00–0:34:48]`; allocation `[R 0:25:27–0:26:10]`; "understand every person, best team" `[R 0:26:22–0:26:30]`; Japan more AI-averse `[R 0:10:14]`; legal-first vs build-first `[R 0:45:07–0:45:50]`; cross-cultural manager bias `[R 0:41:54]`; private talk "more legit" `[R 1:02:55]`. **Unprompted from the VP:** AI dismantling job categories `[R 0:23:16]`; will has no metric `[R 0:29:38]`; the skill-tag system `[R 0:32:26]`; the boss resisting and HR negotiating `[R 0:35:16–0:35:57]`; potential of Slack/document evidence `[R 0:42:26]`; the line on how much to take `[R 0:43:25]`; accountability over legality `[R 0:44:24]`; wrong-decision risk `[R 0:48:34]`; the pace judgment `[R 0:50:22]`; "creepy" `[R 0:55:14]`; the internal attempt's format `[R 0:56:39–0:56:43]`; private/public split `[R 1:00:26, 1:02:19]`.

**Numbers from the meeting, by placeholder** (values in the transcript at the timestamp; sensitive; not for public artifacts until cleared): `VP-FIG-1` per-person exchange cost `[R 0:20:57–0:21:03]` (currency confirmed yen at 0:21:24–0:21:26; what it includes is not said); `VP-FIG-2` replacement budget `[R 0:38:23, 0:39:34]` (no time basis; scope Japan LMS + matching AI; conditional); `VP-FIG-3` first-line-manager population `[R 0:49:34]`; `VP-FIG-4` years of data in the pilot `[R 0:51:23]` (hedged 「かな」); `VP-FIG-5` tag count `[R 0:32:26]` ("maybe" in the English); `VP-FIG-6` organization size `[R 0:00:47]`. `VP-FACT-1` an internal data-use matter `[R 0:48:06–0:54:18]`; `VP-FACT-2` the internal attempt `[R 0:56:27–0:56:43]`; `VP-FACT-3` an example about AI-screening fairness at a group company `[R 0:11:16]`. None of the FACTs go in any public artifact.

**Ryo (Sat 11:42–12:30, `interviews/INTERVIEW_NOTES.md` §7, `7_RYO_VS_DIRECTIONS.md`; consent given verbally after the interview per Carl; raw 12-00 and 12-20 kept local as personal):** self-built evidence deck every cycle because his boss "didn't see" the work (11-50 00:26–00:44); the 360 "useless", free text empty (03:38–04:00); named the Slack + Docs route himself (01:49); team formation "very specific, easy to understand… very big, very difficult" (12-00 00:47–01:26) with his own HR-needs-an-engineer example (11-50 09:23); drift did not land (11-50 06:33); business hook: talent enablement and internal mobility feeding Indeed hiring (12-00 02:25–03:14); another team may be on a similar idea (12-00 02:25); peer perception is his real wish and has no workaround (02:47–03:08, 04:52). Ask him before quoting him by name.

**Shion's figures** (audit): 3–4 in global TA, new-grad team of 30; 10–15 then 15–20 internal collaborators a year; "like 10 times" a year for an approved-list person; 40 / 30 / 20 candidate counts are "for example". **The "ironically, using Salesforce takes much longer" line** is in the transcript `[2_shion_20-50-00 02:48–03:05]` but the undiarized segment reads as a statement, an assent ("Mmm, yeah") and an interviewer question; check the audio before quoting it as hers.

---

## F. Already researched: do not redo

- **Codex packet (Fri night):** six opportunity ideas across three paths, judge research, interview audit with timestamps, ten fictional council rounds, template requirements. Verified twice (`codex-packet/outputs/PACKET-VERIFICATION.md`): template order and word caps confirmed from the .pptx (Problem + Insight ≤ 200 words, Differentiation ≤ 100, Technical ≤ 150 with a diagram, Roadmap ≤ 75; delete the instructions slide; member names go in the Slack post); all nine slide screenshots match the deck text; 20 of 22 external sources re-fetched, none wrong.
- **Prototype audit (Sat 03:00, this session):** file tree, stack, defects, reusable parts. Summarised in PRD §11 and §12. Do not re-audit.
- **VP evidence brief (Sat 03:30, this session):** every substantive VP statement with timestamps, the interpreter's drifts, the ambiguity ledger, the cultural-nuance inventory. Folded into PRD §2 and §4 and §E here. Do not re-read the 2,260-line transcript to answer "what did he say about X"; grep it for the timestamp cited here.
- **Market and best-practice scan (Sat 03:30, 26 searches):**
  - Workday: talent overview https://www.workday.com/en-gb/products/talent-management/overview.html ; Agent System of Record (Feb 11 2025) https://en-gb.newsroom.workday.com/2025-02-11-The-Next-Generation-of-Workforce-Management-is-Here-Workday-Unveils-New-Agent-System-of-Record ; Illuminate agents (May 19 2025) https://newsroom.workday.com/2025-05-19-Workday-Unveils-Next-Generation-of-Illuminate-Agents-to-Transform-HR-and-Finance-Operations ; Sana (Mar 17 2026) https://www.hr-brew.com/stories/2026/03/17/workday-announces-new-ai-powered-capabilities-powered-by-sana-acquisition ; Bersin analysis (Apr 27 2026) https://joshbersin.com/2026/04/the-reinvention-of-workday-from-system-of-record-to-platform-of-agents/ . Next event: Workday Rising Oct 12–15 2026.
  - Salesforce Agentforce HR Service (May 6 2025) https://www.salesforce.com/news/stories/agentforce-hr-service-announcement/ ; internal Slack rollout https://www.salesforce.com/news/stories/deploying-agentforce-slack-insights/
  - ServiceNow + Moveworks (Mar 10 2025; closed Dec 15 2025) https://newsroom.servicenow.com/press-releases/details/2025/ServiceNow-completes-acquisition-of-Moveworks/default.aspx
  - Rippling AI (staged actions, links to records) https://www.rippling.com/platform/ai ; https://www.rippling.com/blog/inside-rippling-hr-ai
  - Gloat agents https://gloat.com/use-cases-agents/ ; Eightfold talent management https://eightfold.ai/products/talent-management/ ; Glean expert search https://docs.glean.com/tools/glean/expert-search ; Personio Assistant https://www.personio.com/product/assistant/
  - Indeed: Talent Scout / Career Scout (Sep 10 2025) https://www.indeed.com/news/releases/indeed-introduces-new-suite-of-hiring-products-career-scout-talent-scout-premium-sponsored-jobs-and-indeed-connect ; Smart Sourcing https://www.indeed.com/employers/solutions/smart-sourcing ; Smart Screening ("Smart Fit Score", "hiring stays a human process") https://www.indeed.com/employers/solutions/smart-screening ; Recruit Holdings FY2026 Q1 post (Sep 4 2026) https://recruit-holdings.com/en/blog/post_20260904_0001/
  - Intake patterns: Mercury bill pay https://mercury.com/bill-pay ; Mercury receipts (Feb 2025) https://mercury.com/blog/february-2025-product-updates ; Linear email intake https://linear.app/integrations/create-issues-via-email ; Linear Asks https://linear.app/docs/linear-asks ; Zapier parser https://zapier.com/features/parser ; Humaans Slack https://humaans.io/slack ; Lattice (Sep 2 2026) https://lattice.com/blog/fall-winter-2026-product-release ; Donut https://www.donut.com/ ; Leena AI https://leena.ai/ ; Slack 3-second ack https://docs.slack.dev/interactivity/handling-user-interaction ; Slack 2025 rate-limit change (internal apps exempt) https://docs.slack.dev/changelog/2025/05/29/rate-limit-changes-for-non-marketplace-apps ; users.lookupByEmail https://docs.slack.dev/reference/methods/users.lookupByEmail
  - UI patterns: Granola two-tone notes + provenance icon https://docs.granola.ai/article/ai-enhanced-notes ; Hebbia Matrix https://www.hebbia.com/ ; Linear Triage Intelligence https://linear.app/docs/triage-intelligence ; Anthropic Citations API https://claude.com/blog/introducing-citations-api
  - Demo technique precedents: GPT-4 sketch-to-website https://blog.codepen.io/2023/03/15/gpt-4-demo-turns-a-crude-sketch-of-a-my-joke-website-into-a-functional-website-for-revealing-jokes/ ; GPT-4o live interruption https://www.technologyreview.com/2024/05/13/1092358/openais-new-gpt-4o-model-lets-people-interact-using-voice-or-video-in-the-same-model ; iPhone 2007 before/after https://time.com/4628515/steve-jobs-iphone-launch-keynote-2007/ ; Devin honest clock https://cognition.com/blog/introducing-devin ; Duplex handoff https://research.google/blog/google-duplex-an-ai-system-for-accomplishing-real-world-tasks-over-the-phone/ ; the anti-pattern (Gemini "hands-on" video) https://techcrunch.com/2023/12/07/googles-best-gemini-demo-was-faked/
  - Japan 2050: Recruit Works Institute 2040 forecast https://www.works-i.com/english/item/FuturePredictions2040_JP.pdf and https://recruit-holdings.com/en/blog/post_20230926_0001/ ; Moonshot Goal 3 https://www8.cao.go.jp/cstp/english/moonshot/sub3_en.html ; Telexistence × FamilyMart https://www.therobotreport.com/restocking-robots-deployed-in-300-japanese-convenience-stores/ ; Telexistence × 7-Eleven humanoid (Sep 29 2025) https://tx-inc.com/en/blog/2025/09/30/12542/ ; JR West rail robot https://www.railway-technology.com/news/japanese-railway-introduces-infrastructure-robot/ ; Henn na Hotel https://www.forbes.com/sites/samshead/2019/01/16/worlds-first-robot-hotel-fires-half-of-its-robots/ ; Jensen Huang "IT is the HR of AI agents" https://finance.yahoo.com/news/nvidia-jensen-huang-says-over-133641233.html
  - Quantification: ringi survey (Bengo4/CloudSign, n=312, 2024) https://prtimes.jp/main/html/rd/p/000000470.000044347.html ; HR admin pay (secondary, weak) https://hupro-job.com/articles/2088 ; McKinsey 2012 (over-cited) https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-social-economy ; SHRM cost per hire https://www.shrm.org/topics-tools/news/shrm-benchmarking-report-4129-average-cost-per-hire ; SHRM 2025 time to fill https://www.shrm.org/executive-network/insights/people-strategy/state-of-recruiting-2025-insights-to-maximize-recruitment
  - Not verified in that scan: Perplexity/NotebookLM/Attio UI details; Kawasaki/SoftBank/Fanuc humanoid figures; any mentor-coordination time benchmark (none found; measure it in the pilot).
- **Codebase design (Sat 03:15–04:10, planning agent):** repo layout, models, policy gate, LLM layer with prompts, API, Slack, email, frontend, storage, dev, tests, build order, cut lines, truth table, risks. All in PRD §11–§13. Do not redesign; amend.

---

## G. Rules that hold all weekend

1. Every message to another person (VP, Shion, mentors, organizers, judges) is a **draft until Carl approves the exact text**. The 22:49 Friday DM to Shion was sent without review and became this rule.
2. Every demo person, message, document and company is **fictional**; no real Slack text in fixtures; no personal information in prompts (organizer rule, disqualification risk).
3. Every number on a slide carries VERIFIED / RESEARCH / CALCULATED / ILLUSTRATIVE and its inputs × method × source × assumptions line (template slide 05).
4. VP figures and facts stay as placeholders in public files until cleared (§J). Internal matters he described (`VP-FACT-1..3`) and any per-person cost never appear in README, deck, video, fixtures or code.
5. The ten council rounds in `codex-packet/` are fictional rehearsal; never quote them as a judge's view.
6. Nothing about Carl's own career or internship next steps in any file (Carl's rule).
7. Do not commit `.env`, `state/`, `.venv`, `node_modules`.
8. Code written before Friday 5 PM is disqualifying; everything in `prototype/` (Sat 02:06) and the product repo (from Sat 08:30) is new.
9. **Carl posts the submission. No agent submits.** (Runsheet boundary.)
10. **Don't reuse AI-suggested ideas as-is** (Day 1 deck p27): the scripts in PRD §9 are drafts to rewrite in your own words before the stage; the innovation frame is Steven's own.
11. Rule 1 covers tech-support posts too: anything that names a judge or organizer is a draft until Carl approves it.

---

## H. Urgent handling item: the public research repo

`syang0624/hyderabaddies` is public, and `origin/main` already contains `interviews/5_VP_MEETING_TRANSCRIPT_RECONCILED.md`, `5_VP_MEETING_TRANSCRIPT.md`, `5_VP_MEETING_SUMMARY.md` and the raw JSON, which include internal matters he described (`VP-FACT-1..3`), several figures (`VP-FIG-1..4`), and personal details of everyone in the room (hometowns, graduation years, military service). The summary's own first paragraph said not to commit it.

Options, for Carl and Steven to decide (not an agent's call):
1. **Make this repo private now** (`gh repo edit syang0624/hyderabaddies --visibility private --accept-visibility-change-consequences`) and **submit from a fresh public repo** that contains only `receipts/`, the README, the truth table and the PDF. The submission needs *a* public repo, not this one. Recommended: it is one command, reversible, and it stops the leak without rewriting history.
2. Remove the files and rewrite history (`git filter-repo`), then force-push. Destructive, and GitHub caches may keep the old blobs; clones on other machines keep them anyway.
3. Leave it and ask the VP/Shion for retroactive permission. Not recommended.

Whatever you choose, `PRD.md` and `sync.md` are written so they add nothing new to the exposure (placeholders only).

**Decision taken in PRD §11.0 (D18), pending Carl's yes at 08:30 Sat:** option 1. The product repo `hyderabaddies-receipts` is created first thing; this repo goes private the same minute.

---

## I. Who does what next (critical path)

The build order with hours is PRD §12.2 (v3, from 14:15 Sat); this section only names what must not move. **17:00 Sat**: patches 1–7 and 9 in the prototype (quote check, subject scoping, manifest counts, cache by backend, substring fix, error states, present mode, scratch smoke); Gemini-or-keyword decided for the video. **18:40**: live layer verified on the demo laptop with a headset mic; typed fallback works. **22:00**: video take 1 exists; **22:30**: uploaded. **23:30**: deck PDF; **00:00**: prelim read aloud with a timer. **09:00 Sun**: public product repo (subtree of `prototype/`) runs from a clean clone; this repo private. **10:45**: Carl posts. Sleep is on the plan for both.

Before the build: read PRD §0 and §2.3 (ten minutes), then §11 for your side. Tech support windows: Sat 10–11 AM (bring the `llm-check` result), Sat 8–9 PM, Sun 10–11 AM. Mentoring at 1:30–2:00 (Hiro, booked): bring the running keyword-mode UI, not slides, and ask what would make him not believe it. Clearance asks (§J): Carl drafts by 09:00 Sat, sends after he approves, before the 12:30 gather.

---

## J. Clearance list (drafts for Carl; ask through Shion or directly, in writing)

Ask for a yes/no on each, and record the answer here with a timestamp:
1. May we say "the head of HR at a large Japanese enterprise told us this week…" in the pitch, without naming Recruit? Without naming him?
2. May we use the first-line-manager population figure `[VP-FIG-3]` on the impact slide? (If not, we say nothing about that population and nothing about any current rollout.)
3. May we describe the per-person exchange cost `[VP-FIG-1]` as "a two-year, [figure] decision"?
4. May we say the company already spends on training and matching systems in this category, with the replacement figure `[VP-FIG-2]` and the caveat "time basis unconfirmed"?
5. May we mention the skill-tag taxonomy (count and 1–5 scale) `[VP-FIG-5]` as "the taxonomy you already have"?
6. Nothing about the internal matters he described (`VP-FACT-1..3`) will be used; please confirm.
7. Would he do the six-step self-demo (PRD §9.6), five minutes, our laptop?
8. Does anything his team uses today show an employee the evidence a decision about them rests on? (Asked because our differentiation rests on the answer; phrased without reference to any internal project.)

Owner: Carl. Draft by 09:00 Sat; send only after Carl approves the exact text; before the 12:30 gather. Record each answer here with a timestamp.

---

## K. Log (append-only)

- [04:30] [agent: Claude, Steven's session] PRD.md and sync.md written from the approved plan; three exploration reports (prototype audit, VP evidence brief, market scan) and one design pass folded in; nothing committed. Files changed: PRD.md (new), sync.md (new), HANDOFF.md (two-line pointer). Nothing sent to anyone.
- [12:45] [agent: Claude, Carl's session] Ryo (Recruit product org, manages 5-6 PMs / 30-40 people) interviewed 11:42-12:30 on how he is evaluated; distilled in `interviews/INTERVIEW_NOTES.md` §7, compared in `interviews/7_RYO_VS_DIRECTIONS.md`. Headline: he hand-builds an evidence deck every cycle and calls the 360 useless; team formation landed, drift chain did not. Suggests leading with team formation and demoting the drift chain. Raw 11-40, 11-50 committed; 12-00, 12-20 kept local (personal). Consent given verbally after the interview (Carl). Nothing sent to anyone.
- [05:30–07:00] [agent: Claude, Steven's session] PR #3 reviewed with the code-review skill at max effort: six finder angles, fifteen verifiers (fourteen CONFIRMED, one PLAUSIBLE), one sweep. Findings, most severe first: (1) VP internal facts and figures restated despite the placeholder rule; (2) Rin's examples used Yui's manager line and an invented 'Osaka'; (3) the prelim credited our led framings to the VP; (4) scoping leaks via the Slack service role, `/audit`, `/drift/examples` and the Vite proxy exposing tokens and admin routes to the LAN; (5) the span check passed empty quotes, header fragments and wrong-role sources; (6) the video end card overclaimed, disclosed late and overran beat windows; (7) close left data behind and ids collided on warm and on the pre-filled criterion; (8) ViewFlip overwrote the evaluator's token and logged a false subject view; (9) the Slack handlers 422'd and linked the phone to localhost; (10) the judge-typed drift sentence broke the receipt path and skipped the personal-information rule; (11) `make warm`/`reset` sent an empty token and `video-mode` continued on stale state; (12) the submission repo was undecided and Slack in the video implied a Sunday re-record; (13) seeded drift chains claimed Gemini provenance and the 2050 page could not run the pipeline; (14) rules claimed 'in code' rested on prompts and rerank output was never validated; (15) template labels, the submission owner, the AI-ideas rule and the clearance asks were missing. All fixed in PRD v2 (D18–D27); nothing sent to anyone.
- [07:45] [agent] PRD.md rewritten as v2 (1,560 lines); sync.md updated (§A, §B D18–D27, §C, §D, §E, §G, §H, §I, §J); HANDOFF.md two fixes; banners on DEMO-PLAN.md and PREP-HOJOON-CHA.md. Pushed to the PR #3 branch.
- [14:15] [agent: Claude, Steven's session] PR #3 (v1) was merged by Steven at 12:36 while v2 was being written, so v2 landed on the branch only. Read Carl's 12:50–13:40 commits (prototype UI v2/v3, live meeting layer, Makefile ADC default, README) and the Ryo files. PRD v3 on branch `steven/prd-v3` from `main`: §0 build state, §2 P5 (Ryo), §9 beats reordered (live meeting opens; drift demoted), §11.A patch list for the prototype (Sunday's plan), §12 re-timed from 14:15, §13.1 truth table for what runs; the v2 design kept as §11.0–§11.13 (post-event target). D28–D30 added. Nothing sent to anyone.
- [19:05] [agent: Claude, Steven's session] Product renamed Receipts → Pik (D16 updated): PRD, deck prompt, UI title/brand, Slack manifest and bot strings, Notion watcher strings, live prompt, env var names (`PIK_*`, old names still read). Slack app/bot display name and the Notion integration name are renamed by Steven in those UIs. Earlier today: PR #6 merged (Slack bot + Notion watcher live, both seeded with fictional history via `make seed-slack` / `make seed-notion`; `make people` no longer overwrites the committed fixture).
