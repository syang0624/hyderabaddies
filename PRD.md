# PRD: Receipts, the evidence layer for people decisions

Working title **Receipts**. Team hyderabaddies: Carl Kho, Steven Yang. Recruit Innovation Cup 2026, San Francisco (DG717). Written Sat Sep 26 2026, ~04:00 PDT, by Claude (Fable 5.1) in Steven's session from the approved plan. Status: **v1, buildable**. Companion file: [sync.md](sync.md) holds the reasoning behind every decision here, with evidence pointers, so nobody has to re-derive it.

---

## 0. How to read this document

- **Purpose.** Anyone can build, demo and pitch this product from this file without asking a question. If something is missing, add it here, not in chat.
- **Deadline.** Sunday Sep 27, **11:00 AM PDT**, posted in Slack `#announcements-all`: (1) public GitHub repository link, (2) demo link or video **≤ 90 seconds**, (3) deck as PDF. No changes after; late is disqualified. Preliminary pitch Sun 1:30–2:45 PM (**3 min + 1.5 min Q&A**, all teams, order announced Sat 6:30 PM). Final Sun 3:10–3:55 PM (**6 min + 6 min Q&A**, three teams, same slides allowed with more detail, **no setup time after prelim results**). Source: Day 1 deck pp17–19 (`codex-packet/work/event.txt`).
- **Rubric.** Potential Impact 40% (social impact and business potential together), Creativity & Innovation 30%, Technical Architecture 30% ("PoC shows that the key technical idea works", "clear path to making the solution work in practice"). Deck p14.
- **Number labels.** The organizer template (slide 05) requires every number to carry one of four labels and its "inputs × method × source × assumptions". This document uses the same labels everywhere: **VERIFIED** (we observed or measured it ourselves; an interview statement carries its transcript timestamp), **RESEARCH** (a published source, with URL), **CALCULATED** (formula shown, inputs labelled), **ILLUSTRATIVE** (assumed, and the slide says so).
- **Fictional-data rule.** Every person, message, document, sheet and company in the demo is invented. The company is "Kaede Works (fictional)". No real names, no real Slack text, no personal information in prompts (Day 1 deck p27). This is an organizer rule and a disqualification risk, not a preference.
- **Public-repo rule.** This repository (`syang0624/hyderabaddies`) is public. Facts and figures the VP gave us in a private, late-night, interpreted conversation are referenced here by transcript timestamp and a placeholder tag such as `[VP-FIG-2]`, and are **not restated** until he or Shion clears them (§15). Nothing about internal matters he described (`[VP-FACT-1..3]`, indexed in `sync.md` §E) or any per-person cost goes into README, deck, video, fixtures or code comments. `[VP-FIG-n]` and `[VP-FACT-n]` tags are indexed in `sync.md` §E with their transcript timestamps. If the repo is made private (recommended in `sync.md`), the placeholders can be filled in a private copy of this file; the public artifacts still need clearance.
- **Conventions.** "VP" = Hidetoshi Ebina, VP and Head of HR COE at Recruit Co., Ltd. (organizing team; title from public listings, never spoken on tape). `[R h:mm:ss]` = offset into `interviews/5_VP_MEETING_TRANSCRIPT_RECONCILED.md`; the recording started at about 00:09:40 PDT Sat, so wall-clock ≈ 00:09:40 + offset. `[2_shion_20-40-00 03:13]` = raw interview file in `interviews/raw/` and its own offset. Japanese quotes are the VP's words; the English after them is a translation, not the in-room interpretation, unless marked.
- **What "evidence layer" means here.** The phrase was coined by the summarizing agent at ~01:30 Sat as an inference; on tape the nearest words are Carl's "collects all of the evidence" `[R 0:55:30]` and Shion's rendering 「決定の根拠にするとか」 ("as grounds for a decision") `[R 0:56:18]`. We use it as the product's job, not as something the VP said.

---

## 1. The product in one paragraph

**Receipts** is a purpose-locked evidence page for one high-stakes people decision. For each person being considered, it assembles what they themselves wrote (**declared will**), what they chose to do (**revealed will**) and what their manager wrote about them (**the paraphrase**), from sources a policy file explicitly allows, and turns them into short claims that each carry a verbatim receipt from a named source. The evaluator reads the evidence against a criterion typed in her own words; the person being evaluated sees the **same page** and can add context or contest a line before the decision is made; the decision memo carries every footnote and an audit strip of what was read and what was never read. **No score is presented as a verdict; a human decides.** The demo decision: an HR planner at a fictional Japanese company choosing one of three people for a two-year overseas exchange. It is reachable from Slack (a real bot), by email (an interface with a stub), and on the web (the page itself), so nobody has to open yet another system to start. The longer arc: this is the first module of an evidence-first HR operating system, with a 2050 epilogue where the same page and the same rules cover a mixed workforce of humans and humanoid workers.

One sentence for the deck: **evidence, with receipts, that both the evaluator and the employee can see, for one high-stakes people decision.**

---

## 2. Problem definition

### 2.1 The decision, and how it is made today

**The decision.** Who goes on the two-year exchange between the Japanese parent company and its US partner. It is expensive, it is a two-year commitment, and it changes a career. The VP named the exchange himself as the company's main tool for merging two opposite working cultures `[R 0:13:48–0:19:11]`, gave its length as two years `[R 0:20:51]` and its per-person cost `[VP-FIG-1, R 0:20:57–0:21:03; sensitive, not cleared]`. The demo company's version, "exchange-2027, one slot at the US partner Northwind Labs, starts April 2027", is fictional and keeps that shape.

**How it is made today, in the VP's own account.**

| Step | What happens | Source |
|---|---|---|
| Twice a year, each employee fills a **Will / Can / Must** sheet under the MBO process, discusses it with their direct boss, and HR sees it | The only structured input about what a person wants | Shion `[R 0:29:58–0:30:24, 0:51:14]`; VP: "MBO system" `[R 0:30:03]` |
| "Will" has **no metric**; HR "always asks" | 「ない、ないね。ただ、常に問うようにはしてます。」 | VP `[R 0:29:38–0:29:43]` |
| Matching people to roles ran on **human intuition**; HR is now scoring a few hundred AI-generated skill tags per person on a 1–5 scale and matching tagged jobs `[VP-FIG-5]` | 「人の勘でマッチングしてたところを…AIで今補助しよう」 | VP `[R 0:31:30–0:33:24]` |
| The boss's paraphrase travels up; HR interviews the person directly to catch drift and negotiates with a boss who does not want to lose them | 「2 つ目の問題を防いでます」 | VP `[R 0:35:16–0:35:57]` |
| No evaluation input other than the boss exists today | 「今はない。」 | VP, answering Carl `[R 0:41:49]` |
| Using workplace data beyond the boss's evaluation is limited today by accountability to employees, not by law | 「理屈上は使えます…説明責任、透明性」 | VP `[R 0:44:24]`; internal specifics `[VP-FACT-1, R 0:48:06–0:55:14]` are not for public artifacts |

**Why this decision and not another.** It is the one people decision the VP quantified, it is made rarely enough that a purpose-locked page is credible (not a standing profile), and it is where the paraphrase problem bites hardest: the boss who writes the note is the boss who loses the person.

### 2.2 The four pains, each with its evidence

| # | Pain | Evidence (who said it, where) | Product mechanic |
|---|---|---|---|
| P1 | **Will is invisible.** The company cannot see what people want to do; it asks twice a year and remembers. | VP: no metric `[R 0:29:38]`; the biggest management topic is which careers and team shapes reach an organization nobody can yet describe `[R 0:26:32–0:26:47]`; teams must form around people who "really want to do this" 「合理的じゃないこと」 included `[R 0:24:36–0:25:10]` | Declared will (the sheet, in the person's words) next to revealed will (what they volunteered for), each with receipts |
| P2 | **Meaning drifts up the chain.** A person's words are paraphrased at every level; HR's only defense is to interview the person again. | VP: 「どっちもそうです」 to the two-gaps framing `[R 0:34:48]`; HR's workaround `[R 0:35:36–0:35:57]`. Note: the framing and the "Shion → loves flying → Saudi Arabia" example were Carl's `[R 0:34:00–0:34:54]`, so this is a led confirmation plus an unprompted description of the workaround | The paraphrase is shown beside the source, never instead of it; the drift chain makes the loss visible |
| P3 | **Evidence exists but cannot be used.** Slack and documents could show whether the boss's rating is right; the blocker is not law but accountability and "creepiness" toward employees. | VP: 「ポテンシャリティとしてはすごくあると思ってる」 `[R 0:42:26]`; 「理屈上は使えます…説明責任、透明性」 `[R 0:44:24]`; 「すげえ気持ち悪ぃ」 `[R 0:55:14]` | Purpose lock, allowlisted sources, DMs excluded by config, the audit strip, and the two-sided mirror |
| P4 | **A wrong AI output can push a wrong promotion or transfer.** | VP: the thing he most wants to avoid `[R 0:48:34]` | No score as verdict; claims dropped when unsupported; the subject can contest before the decision |

### 2.3 Five load-bearing passages, three readings each

This was a 72-minute conversation after midnight, interpreted consecutively and only partly, with several of our questions never translated before he answered. Steven's instruction for this document: put the alternative readings side by side; do not take the convenient one. The full ledger is in `sync.md` §E; here are the five that carry the product.

| Passage | Reading A (strong) | Reading B (moderate) | Reading C (weak) | What the product bets on |
|---|---|---|---|---|
| 「それが一番困ってる」 `[R 0:26:10]`, "Yes, exactly" `[R 0:26:30]` | Operational team formation under blurred roles is his number-one problem | The problem is strategic: what the ideal organization is and which careers lead there; "allocation" was Steven's word, untranslated | Conversational agreement with a laugh to an English framing | **B.** The product serves one decision inside that strategic problem; it does not claim to form teams. Against C: he had steered to this topic himself `[R 0:23:12]` and called it the hottest management topic unprompted |
| 「どっちもそうです」 `[R 0:34:48]` | Both gaps (gut feel; drift up the chain) are live pains | Both are true in principle, and HR already mitigates the second by interviewing the person | Polite agreement to a two-part leading question | **B.** Drift is real and has a manual workaround; Receipts automates the workaround (the person's words travel intact) rather than claiming HR is helpless |
| "That's right" `[R 0:31:27]` after Shion's 「思いついた順」 | Matching from memory is today's pain | The problem is known and the skill-tag system already targets it, so we must beat the internal tags | Assent to a leading 「…しかないんじゃないか？」 | **B.** We adopt their taxonomy as the schema and add provenance; we do not claim they have no system |
| The endorsement `[R 0:56:18–0:56:43]`: Shion 「決定の根拠にするとか」, VP 「めちゃくちゃあると思う」, "It's very good value, I think so", then a remark that something similar is being attempted internally `[VP-FACT-2]` | Evidence as grounds for decisions has high value to him | "We do a lot of that already": the value is real, we would be a second supplier | A courteous close at ~01:05 after an hour | **Between A and B.** The only idea he endorsed on value; no pilot commitment exists ("would be willing to try?" was never translated). The difference we must show is the employee's side of the page, which nothing he described has |
| The replacement-budget passage `[VP-FIG-2, R 0:38:23, 0:39:34]` | Willingness to pay for a team-formation tool | A replacement budget: he would bet his current Japan spend on training systems plus matching AI only if the product replaced all of it | A hypothetical price with no time basis, said right after "I've heard this before" and before "many players, Workday" | **B.** Use it only as "the customer already spends on this category", label the time basis unconfirmed, never as our ARR |

### 2.4 What we supplied and he agreed to (do not present as his findings)

Led by us and confirmed with a word or two: matching from memory `[R 0:31:05–0:31:27]`; the two gaps `[R 0:34:00–0:34:48]`; "allocation" `[R 0:25:27–0:26:10]`; "understand every person, best team for every department" `[R 0:26:22–0:26:30]`; Japan being more AI-averse (「言ってくれてる通り」, "just as you said") `[R 0:10:14]`; legal-first Korea/Japan vs build-first SF `[R 0:45:07–0:45:50]`. His own, unprompted: AI dismantling job categories `[R 0:23:16]`; will has no metric; the skill-tag system; the boss resisting transfers and HR negotiating; accountability over legality; the pace judgment 「見極め」 `[R 0:50:22]`; "creepy"; the private/public split for wearables `[R 1:00:26, 1:02:19]`; and the format of the internal idea: 「志恩さんはこういう人です…実は、GmailとかSlackでこういうやり取りをしてるからです」 (a statement about a person, then the exchanges that show it) `[R 0:56:39–0:56:43]`, which is exactly the shape of an evidence card.

### 2.5 What is not the problem

- **Tool consolidation.** "Salesforce + Slack + Excel + Gmail in one dashboard" is plumbing, it is common, and the VP said something like it is being attempted internally `[R 0:56:27]`, that Workday is entering the space `[R 0:38:58]`, and that he has "heard this pitch before" `[R 0:37:33]`. Steven's brief (02:30 Sat) says the same: too common, and it does not beat robotic arms.
- **Recruiting throughput.** Indeed already sells AI sourcing and screening (Recruit Holdings results post, Sep 4 2026, verified). A candidate-summary product is a substitution question waiting to happen.
- **Covert monitoring.** Legal at the company, and it still would not ship, because employees would find it creepy and managers might misuse it `[R 0:44:24, 0:49:34, 0:55:14]`. Steven's "runs in the background without people knowing" `[R 0:43:36]` and Carl's "more quiet with the data collection" `[R 0:47:11]` were both answered with accountability, not enthusiasm. The careless version of this product is the default everyone builds.
- **Scoring people.** Indeed's Smart Screening ships a "Smart Fit Score" and says hiring stays a human process. Workday scores. The VP's fear is a wrong score driving a wrong decision. We cite instead.

### 2.6 The bet, in one line

The blocker is design, not data: the same data, shown to both sides with receipts, for one named purpose, is something a one-sided design cannot do and the vendors do not do.

---

## 3. The innovation frame, and the rules it produces

Steven's frame, captured on the glasses right after the meeting (`interviews/6_STEVEN_INNOVATION_FRAME.md`, ~01:30 Sat; attribution inferred, wording may be misheard):

> "Innovation has to be very careful. The way that we perfectly design for the humans." (01:30:08)
> "Innovation is changing the way you think." (01:30:23)
> "I guess we can define innovation as something that works for a company." (01:32:44)

Steven owns the story; Carl reviews it before it is said aloud (01:33:49). Skip the "nukes" line on stage. Steven's own worry, "how this would land with the American audience" (01:30:41), is answered in §4.

**How the frame becomes product rules.** Each rule is enforced in code, not in a prompt or a slide.

| Frame | Rule | Where it lives |
|---|---|---|
| Careful | **No score is presented as a verdict.** Ranking re-orders evidence for a stated criterion; the number is "how much of the evidence bears on the criterion", never shown to the subject, never in the memo | `RankRow.support` scoping; memo template |
| Careful | **Citations or nothing.** A claim without a valid source id is dropped; a claim whose quote is not found verbatim in its source is checked, and dropped if unsupported; the dropped list is visible | `services/evidence.py`, span check |
| Careful | **Purpose limitation.** The page exists for one named decision; the policy's purpose must equal the decision id or the server refuses; closing the decision deletes derived data | `policy.purpose` lock, `/close` → 410 |
| Careful | **DMs and private channels are never read**, by configuration, and the audit strip proves it by counting them from a manifest without opening the file | `Corpus.excluded_paths`, `manifest.json` |
| Designed for humans | **Two-sided mirror.** The subject sees the same page the evaluator sees, minus the support number, and can add context or contest any line; the note lands on the evaluator's side before the decision | server-side scoping by role, live annotations over SSE |
| Designed for humans | **The person's words travel intact.** Every summary line links to the original; the manager's paraphrase is shown next to the source, never instead of it | claim `quote`, WillStrip, drift chain "with receipts" |
| Designed for humans | **A human decides.** The memo ends in open questions to ask the person, not a recommendation | memo template |
| Changes how you think | **Declared vs revealed will** as first-class kinds, shown apart | `ClaimKind` |
| Changes how you think | **Borrow the customer's taxonomy** (their skill tags) as the schema and attach receipts to it, instead of inventing a new profile | `Decision.tags`, tag chips on claims |
| Works for a company | **Invisible UX.** Start from Slack or email; the page is where the decision is made, not one more system to log into | intake adapters (§7) |

---

## 4. The cultural insight, and why it lands with each judge

Steven's point in the 02:30 brief: the pitch touches the pain "in a more nuanced way via the cultural differences conversation", and that nuance may open the eyes of the American judges. The inventory below is what we actually have on tape; the columns say who raised it and whether the VP confirmed it, so nobody over-claims on stage.

| Nuance | On tape | Raised by | VP confirmed? |
|---|---|---|---|
| Employees fear AI will take their jobs; management cannot judge the pace | `[R 0:04:16–0:04:34]` | VP | Unprompted |
| Fear of being read and evaluated from Slack; the current work is deciding which data is used for which purpose and announcing it | `[R 0:07:38–0:08:06]` | VP | Unprompted |
| Japan learns from US backlash cases to find how far social consensus allows | `[R 0:15:18]` | VP | Unprompted (his recollection of an Amazon case; do not repeat as fact) |
| **CEO-ship** ("everyone works as if they were the business owner", blurry job boundaries) versus the US partner's job-based, fast-decision model; the two are "opposite" | `[R 0:18:04–0:19:11]` | VP | Unprompted |
| People exchange is the only integration tool the company has found | `[R 0:17:05–0:17:36]` | VP | Unprompted |
| **Accountability and transparency to employees matter more than legality** | `[R 0:44:24]` | VP | Unprompted |
| Company policy would allow using everything; employees would find it **creepy** | `[R 0:54:57–0:55:14]` | VP, after Steven's DM point | Unprompted |
| Private and public talk are mixed; they must be separated | `[R 1:00:26, 1:02:19]` | VP | Unprompted |
| Japan is more AI-averse than the US | `[R 0:10:14]` | Steven | "just as you said" |
| Korea/Japan ask about legal limits first; SF builds first | `[R 0:45:07–0:45:50]` | Steven, Shion | 「そう思う」 |
| A week of travel abroad needs the manager first; a one-hour 1-on-1 runs on personal connection | `[2_shion_20-40-00 04:06–05:07]` | Shion | Not the VP |
| A formal "data council" meeting must approve any new use of HR data across teams | `[2_shion_20-40-00 02:24–02:54]` | Shion | Not the VP |
| Mentor discovery runs on "human knowledge", asking other HR "do you know this person?" | `[2_shion_20-40-00 01:24–01:54, 06:07–06:27]` | Shion | Not the VP |
| "PM decides, because you can debate all day"; approvals shrinking to "one Slack away" but nobody wants to be the approver | `[1_koki_20-00-00 05:39–07:05; 1_koki_19-56-22 00:36–01:46]` | Koki | Not the VP |

Words that appear nowhere in our evidence and should not be used as observed facts: ringi, nemawashi, hanko, honne/tatemae. The ringi approval survey in §10 is external RESEARCH, cited as such.

**The insight in one sentence for the stage:** in this company the constraint on using workplace evidence is not law or data; it is accountability to the employee, and the version that ignores that cannot ship. So the careful design is not a hedge; it is the only version that can.

**Judge map.** Public backgrounds only (from `codex-packet/work/judges-research.md`, verified Sep 26); nothing here predicts how anyone will judge, and the fictional council transcripts are never to be quoted as a judge's view.

| Judge | Public background | The part of Receipts that speaks to that background | The question to expect |
|---|---|---|---|
| Jim Giles, CTO, Indeed | Led Google Docs/Sheets/Slides/Drive engineering; founded the Workspace AI platform; "how technology can improve the way work gets done" | Grounded citations applied to the HR chain of custody; a product that lives inside existing tools (Slack/email intake) | "How is this not Smart Screening pointed inward?" Answer: it produces receipts for both sides, not a fit score for one |
| Robert Hohman, co-founder and former CEO, Glassdoor | Built a company on making workplace information visible to workers | The two-sided mirror: the employee sees the page | "Why would an employer show the employee this?" Answer: because the covert version is blocked by exactly that asymmetry (P3) |
| Damien Contreras, Google Cloud, Strategic AI | Authored a live Godot + Gemini game demo with a published repo; proportionality of data collection | A live changed-condition demo on Gemini with a visible truth table; DMs excluded by config and counted from a manifest | "Is data collection necessary and proportionate?" Answer: purpose lock, allowlist, delete-on-close |
| Ho Joon Cha, Applied AI Architect, OpenAI | May 2026 webinar on workspace agents, approvals, safeguards, governance | The model extracts and explains; software validates, scopes and deletes; the human decides | "What does the model decide?" Answer: nothing consequential; every claim is validated and the ranking is not a verdict |

(`PREP-HOJOON-CHA.md` has the fuller Q&A prep for the OpenAI judge and applies to the others.)


---

## 5. Users and personas

All demo people are fictional and already exist in `prototype/data/company.json`; keep the names so the storylines survive the migration.

| Persona | Who | What they need from Receipts | Demo identity |
|---|---|---|---|
| **HR planner (evaluator)** | Aya Nakamura, HR planner in the COE at Kaede Works. Owns the exchange decision. Today she has three Will/Can/Must sheets, three manager notes and what she remembers. | See each person's own words next to the manager's paraphrase; read the evidence against the criterion she actually has; take one page into the decision meeting with receipts; know what was and was not read. | `aya`, role `evaluator`, token `demo-aya` |
| **The subject** | Rin Mori (senior marketing analyst, Growth, manager Hayashi; wants to stay and lead the Tokyo pricing analytics team), Yui Sato (product operations, Pricing, manager Okada; wants to work with the US product team on pricing experiments, paraphrased by her manager as "loves travel, flexible on location"), Kei Tanaka (software engineer, Platform, manager Fujii; pushed back on the job-based reorg, ran a one-owner pilot that cut lead time 6.1 → 3.4 days, "hard to release") | See exactly what the evaluator sees about them; add context or contest a line before the decision; never see a number about themselves or anyone else. | `rin` / `yui` / `kei`, role `subject`, tokens `demo-rin` etc. |
| **Line manager** | Hayashi, Okada, Fujii. Author the paraphrases. | See their own reports' pages; understand that their note is shown next to the source, not instead of it. (Read-only in the demo; no manager token needed for the video.) | role `manager` (optional) |
| **Executive sponsor** | The VP (real): runs HR strategy, systems, payroll and recruiting for his organization `[VP-FIG-6, R 0:00:47–0:01:27]`; decides the pace of AI rollout; blocked by accountability to employees. | A version of his own idea (statement + the exchanges behind it) that he could show to a first-line manager and to the employee without it being creepy. §9.6 gives him a five-step card. | Not a demo identity |
| **Recruiter (roadmap)** | Shion (real): assembles candidate dossiers for engineer mentors by exporting Salesforce to Excel and using corporate Claude; finds mentors by word of mouth; a week abroad needs the manager first `[2_shion_20-40-00, 20-50-00]`. | The same engine on a second decision type: "who should mentor these interns", with the mentor's own opt-in and the manager's approval as a first-class step. Roadmap, not Sunday. | None |
| **Observer** | A judge holding the phone during the demo. | See the audit strip and the subject view; supply a criterion or a sentence. | `obs`, role `observer` |
| **2050 fleet supervisor (epilogue)** | Same Aya, 2050, deciding which humanoid unit to reassign to the Osaka site. | The same page, with declared capability (the manifest) beside revealed performance (task logs), incident reports as "gaps", telemetry excluded by policy. | `reassign-2050`, subject `hw-07` |

---

## 6. Jobs to be done and the user pipeline

**JTBD 1 (evaluator):** "When I have to choose one person for an expensive, career-shaping posting, help me decide from what each person actually said and did, so that I am not deciding from a paraphrase, and let me show my reasoning."

**JTBD 2 (subject):** "When a decision about me is being made, let me see the same evidence the decider sees and correct it before the decision, so that a bad summary does not become my career."

**JTBD 3 (sponsor):** "Let me put workplace evidence in front of managers without it being creepy or misused, so that workplace evidence can be used for decisions at all."

### 6.1 The pipeline

```
intake (Slack / email / web)
  → policy gate (allowed sources only; DMs never opened; opt-in enforced; purpose == decision)
  → extraction (LLM proposes claims with kind, source ids, verbatim quote)
  → validation (drop no-source, bad-kind, too-long; re-kind declared/paraphrase if the source role disagrees)
  → faithfulness (verbatim span check; LLM second pass for the rest; drop unsupported)
  → evidence page (evaluator view; subject view scoped server-side)
  → criterion re-rank (support per subject, receipts, full claim order)
  → annotation (subject adds context / contests; lands live on the evaluator side)
  → decision memo (footnotes to every source; open questions; no numbers)
  → audit strip (used / never read from manifest; rules; view events; dropped counts; backend per page)
  → close (derived data deleted; page returns 410 with the retention note)
```

### 6.2 Sequence: the evaluator starts from Slack

```mermaid
sequenceDiagram
    participant Aya as Aya (Slack)
    participant Bot as Receipts bot (Socket Mode)
    participant API as FastAPI
    participant Corpus as Corpus + policy
    participant LLM as Gemini (Vertex)
    participant Web as Browser (evaluator view)
    Aya->>Bot: /receipts exchange-2027 rin
    Bot->>API: POST /decisions/exchange-2027/intake {channel: slack, action: open_page, on_behalf_of: aya}
    API->>Corpus: load allowed sources only (dm.json never opened)
    API->>LLM: extract claims (schema ExtractionOut) if not cached
    LLM-->>API: claims with quotes
    API->>API: validate ids/kinds, span check, faithfulness, store
    API-->>Bot: IntakeResult {page_url, top_receipts}
    Bot-->>Aya: ephemeral card: declared / paraphrase / revealed + "Open evidence page" + "Add context"
    Aya->>Web: opens page_url
    Web->>API: GET page (Bearer demo-aya); POST views
```

### 6.3 Sequence: the subject contests a line, from a phone

```mermaid
sequenceDiagram
    participant Rin as Rin (Slack on phone, or email)
    participant Bot as Receipts bot / email stub
    participant API as FastAPI
    participant SSE as SSE stream
    participant Aya as Aya's browser
    Rin->>Bot: "Add context" on mn-002 (modal) or email "[receipts] add context: mn-002 !contest"
    Bot->>API: POST /intake {action: add_context, on_behalf_of: rin, payload: {target: mn-002, text, contests: true}}
    API->>API: scope: rin may annotate only her own page
    API->>API: store Annotation(origin=slack|email); append event annotation.created
    API-->>SSE: event: annotation.created
    SSE-->>Aya: LiveBadge "Rin added context · 3 s ago"; claim card shows the note beside the paraphrase
```

### 6.4 Sequence: the drift chain (judge-supplied sentence)

```mermaid
sequenceDiagram
    participant J as Judge (types a sentence)
    participant Web as DriftPage
    participant API as FastAPI
    participant LLM as Gemini
    J->>Web: sentence (8–300 chars), optional source id
    Web->>API: POST /decisions/exchange-2027/drift
    API->>LLM: level 1 persona (team lead) paraphrase
    API->>LLM: level 2 persona (department manager) paraphrase of level 1
    API->>LLM: level 3 persona (division head) paraphrase of level 2
    API->>LLM: receipt framing per level (quote inserted verbatim by code)
    API-->>Web: DriftChain {drift[3], receipt[3], lost[], added[], verbatim_ok}
    Web-->>J: stepper: original → L1 → L2 → L3 with struck words; toggle "same sentence, with a receipt"
```

### 6.5 Sequence: close

`POST /decisions/{d}/close` (evaluator) deletes pages, claims, rankings, annotations, view events, drift chains and events for that decision, sets `status=closed`; every later GET returns 410 with the retention note from `policy.json`. This is purpose limitation as behaviour, not as a sentence on a slide.

---

## 7. Surfaces: the debate and the decision

Steven's constraint (02:30 brief): "One thing I don't want is being yet another app they have to open… Salesforce, everything is already taking their time." His reference: Mercury, where you can categorize in the UI or just forward the bill to an address and it is handled; "great UX is invisible"; and "why choose one or the other? Make it a hybrid."

### 7.1 The debate

| Option | For | Against | Demo risk | Build cost (Sun 11:00) |
|---|---|---|---|---|
| **A. Slack bot only** | Zero new UI; lives where HR already talks (Koki: "heavily use Slack"; Shion asks mentors by DM) | A Block Kit card cannot show three columns of evidence, hover receipts or a drift chain; the decision page has to exist somewhere | Socket Mode needs venue internet to Slack; 3-second ack rule | ~6 h incl. workspace setup |
| **B. Email intake only** | Mercury's pattern exactly; works for people who live in mail; no Slack admin needed | Inbound mail needs a provider webhook or IMAP polling and sender verification; slow to demo; the decision page still has to exist | Low if stubbed; high if real | Stub ~1 h; real ~5 h |
| **C. Web app only** | The page is the product; hover receipts, view flip, animation, drift stepper all need a real UI | It is "one more app"; the pitch loses the invisible-UX line | Lowest | Already required |
| **D. Hybrid (Mercury pattern)** | The page exists once; every intake adapter produces the same `IntakeRequest` and returns a link; starting from Slack or mail costs the user nothing | Three surfaces to keep truthful in the truth table | Slack real-or-cut at Sun 09:00; email stubbed | Web (required) + Slack (~6 h) + email stub (~1 h) |

**Decision: D.** Build the web page fully (it is where the four wow beats happen), build the Slack app for real in Socket Mode on a throwaway workspace (it is the opening beat and the "no new app" proof), ship the email adapter as a documented interface with a working local stub (so the architecture is honest and the roadmap slide is true), and keep a simulated Slack pane as the fallback if the real bot is not posting cards by Sunday 09:00. The truth table says which transport was used.

### 7.2 Slack, exactly

- Command: `/receipts <decision-id> <subject-id>` (e.g. `/receipts exchange-2027 rin`). The bot acknowledges within 3 seconds, calls the API's intake endpoint, and replies with an ephemeral Block Kit card: header (subject and decision), a context line with the purpose and the never-read count, three quoted lines (declared will `wcm-…`, manager's paraphrase `mn-…`, revealed will `sl-…`), and two buttons: **Open evidence page** (URL) and **Add context** (opens a modal).
- Modal: shows the targeted source's rendered text, a multiline field (max 500 chars), and one checkbox "I contest this reading". Submission becomes an `Annotation` with `origin=slack` and the author role from `SLACK_ROLE_MAP`; the evaluator's browser receives it live.
- Identity: Slack user ids map to demo personas through `SLACK_ROLE_MAP="U0AAAA:aya,U0BBBB:rin"`. Unmapped users are refused with the purpose message. **Slack display names are never rendered anywhere**, so a throwaway workspace with real account names cannot leak into the demo.
- The Slack process never writes the database; it is an HTTP client of the API with a service token, so the API stays the single writer and live updates stay truthful.
- Platform facts that shape this: Slack requires an acknowledgement within 3 seconds and allows follow-ups for 30 minutes; internal (non-Marketplace) apps are exempt from the 2025 rate-limit change, so build it as an internal app; do not plan on mining Slack history (that is both rate-limited and the thing the VP called creepy). Sources: Slack developer docs on interactivity and the May 29 2025 rate-limit change (`sync.md` §F).
- Manifest, handlers and card JSON: §11.6.

### 7.3 Email, exactly (interface + stub for Sunday; transport proposed)

- Address convention: `receipts+<decision-id>+<subject-id>@kaede.example`. Subject line `[receipts] open` or `[receipts] add context: <source-id>` with an optional `!contest` suffix. The first paragraph of the body is the annotation text. Sender maps to a persona via `EMAIL_ROLE_MAP`; unknown senders are rejected with the purpose message.
- Stub: a watcher over `state/inbox/*.json` converts a dropped message file into an `IntakeRequest(channel="email")`, posts it to the API, and moves the file to `state/inbox/handled/`. `make email-demo` drops a fixture message; the annotation appears live with an "email" origin chip. This is enough to show the pattern truthfully in the final's 6 minutes.
- Real implementation (not built; say "proposed"): Gmail API watch with Pub/Sub push, or IMAP IDLE; SPF/DKIM verification; allowlisted senders (Mercury's approved-vendor pattern); SMTP reply with the page link and purpose text; attachments ignored; bodies never stored beyond the annotation text.

### 7.4 Web, exactly

Routes and components in §8. The web page is the only place where the drift chain, hover receipts, the view flip and the memo live, so every intake ends in a link to it. In present mode (`?present=1`) the developer chrome is hidden and type is larger for projection.

---

## 8. UI and UX specification

The current `prototype/ui/index.html` reads as walls of text because each evidence row is a templated sentence wrapping a quoted message with no grouping; the memo is raw markdown in a `<pre>`; the ranking is crammed into a 260 px sidebar; and there is no summary, no hierarchy, and no way to see a source without reading it inline. Everything below exists to fix that.

### 8.1 Design principles for this UI

1. **Summary first, receipts on demand.** A card is one claim of ≤ 25 words; its sources are chips; the source text appears in a popover on hover or focus, never inline.
2. **Three colours carry the meaning**: teal for the person's own words (declared), amber for what they chose to do (revealed), violet for the manager's paraphrase; emerald marks a verified receipt; rose marks a gap or a dropped claim. Nothing else is coloured.
3. **The subject sees the same cards.** The subject view is the evaluator view minus the support number and minus other people, not a different layout.
4. **Copy the patterns that already work**: Granola's two-tone authorship with a per-line provenance icon; Hebbia's source chip per cell; Linear's "why" on hover with accept/dismiss; Rippling's rule that every number links to its record. Sources in `sync.md` §F.
5. **Honest badges everywhere**: which backend produced this artefact (Gemini or keyword mode), whether a claim was span-checked, whether an annotation or drift example is seeded.
6. **Nothing that looks like a verdict.** No radar charts of people, no summed scores, no ranking medals. Support bars are labelled "evidence support for this criterion" and never appear in the memo or to subjects.

### 8.2 Routes

| Route | Page | Who |
|---|---|---|
| `/` → `/d/exchange-2027` | DecisionHome | evaluator, observer |
| `/d/:decisionId` | DecisionHome: purpose banner, three candidate cards, criterion bar, ranking strip (evaluator only), audit strip | |
| `/d/:decisionId/p/:subjectId` | EvidencePage: the page | evaluator (all), subject (own only) |
| `/d/:decisionId/drift` | DriftPage | evaluator, observer |
| `/d/:decisionId/memo/:subjectId` | MemoPage | evaluator; subject (own, no numbers) |
| `/2050` → `/d/reassign-2050/p/hw-07` | EpiloguePage (EvidencePage with 2050 labels and a year banner) | evaluator |
| `/slack` | SlackSimPage (fallback transport) | anyone |
| Query flags | `?present=1` hides dev chrome and enlarges type; `?token=` sets the viewer then is stripped from the URL | |

### 8.3 Screens (wireframe descriptions)

**DecisionHome.** Top: `PurposeBanner` in one line: "exchange-2027 · Two-year exchange to Northwind Labs, one slot · This page exists for this decision only · Sources: public Slack, shared docs, WCM sheets, manager notes, opted-in AI sessions · Never read: DMs (41, counted from manifest), private channels." Middle: three `CandidateCard`s side by side, each with name, role, team, tenure, claim count, backend badge, and a small line "viewed by Rin: not yet" / "viewed by Rin: 13:58, 2 notes". Below: sticky `CriterionBar` (one input, placeholder "What do you actually need? In your own words.", pre-filled in present mode with "someone who will push back on a job-based culture rather than absorb it", a Re-read button). Then `RankingStrip` (evaluator only): three rows, name, a thin bar labelled "evidence support for this criterion", one-sentence rationale with claim-id chips, and 1–4 receipt chips. Bottom: `AuditStrip`.

**EvidencePage (evaluator).** Header: subject name, role, team, `views` sentence ("Aya viewed this page 2 times, last 14:02. Rin has not viewed it yet."), a `ViewFlip` button "See what Rin sees" that opens the subject's URL with the subject token in a second window (a real second identity, server-scoped). `WillStrip`: three columns, one card each: **Declared will (own words)** teal, **Revealed will (what they chose to do)** amber, **Manager's paraphrase** violet; each card is one claim with a `SourceChip` beneath; for Yui the strip is the whole argument in one glance ("work with the US product team on pricing experiments" vs "loves travel, flexible on location"). Sticky `CriterionBar`. `EvidenceList`: one `ClaimCard` per claim in ranking order (FLIP animation on re-rank, 350 ms), each with a kind pill, the claim text, chips, a faithfulness mark (emerald check "verbatim receipt"; amber "partially supported"), tag chips from the customer's taxonomy, an `AnnotationThread` if any (subject notes in violet-tinted cards with an origin chip "Slack" / "email" / "web"), and an inline `AnnotationComposer`. Receipt claims for the current criterion get an emerald left rail and a rank pip. `DroppedClaimsDisclosure`: a collapsed line "2 claims dropped: 1 had no source, 1 was not supported by its source" that expands to the struck-through list, because the dropped list is the technical proof. `PageFooter`: backend, model, corpus hash, generated-at.

**EvidencePage (subject).** Same components. Differences, all enforced server-side: only own page; no support number anywhere; the ranking strip is absent; a top banner "This is exactly what Aya sees about you. Add context or contest any line; she sees it before the decision."; the composer is always visible; a "contest" checkbox on each card.

**SourcePopover.** On hover or focus of a chip after 300 ms: the rendered source (`[sl-023] Slack #pricing 2026-05-14 by yui: …`), date, channel and visibility, an opt-in mark for sessions, and for WCM sheets the seeded Can-level for the tag in question (the only place a 1–5 number appears; never summed). Click pins the popover and highlights every claim citing that id.

**DriftPage.** `DriftInput`: a text field (8–300 chars) with three example chips (one per candidate, seeded), an optional source-id field, a Run button. `DriftStepper`: four cards left to right: **Original** (green, with the source chip), **L1 team lead, weekly report line**, **L2 department manager, headcount note**, **L3 division head, slide label**; each shows the persona title, the one-sentence paraphrase, and a `WordDiff` with dropped words struck in rose and added words in amber; beneath, `LostAddedSummary` ("Lost: stay, Osaka, two years, lead, pricing experiments, short visits · Added: mobile"). A toggle **"Same sentence, with a receipt"** re-runs the stepper in receipt mode: at every level the original sentence sits in green quotation marks with its source chip, with only the persona's framing around it. Badge: "Gemini 3.8 Flash, 3 calls" or "simulated (no LLM)".

**MemoPage.** Rendered markdown (react-markdown + remark-gfm) as cards: Decision and purpose; Declared will; Revealed will; Manager's paraphrase (beside the source); Strengths; Gaps; Notes from the person (annotations, with origin); Open questions to ask them; What was read / never read; Views. Footnote markers render as `SourceChip`s. An optional "AI summary from the claims above (Gemini)" box, ≤ 60 words, no numbers. Buttons: copy as markdown, print.

**AuditStrip.** One row of small tiles: Purpose; Policy version; Used sources with counts (e.g. "Slack public: 118", "WCM: 3", "Sessions: 6 of 9 opted in"); Never read with counts and "counted from manifest, sha 9c1e…"; Rules (five one-liners); Views per role; Dropped counts; Backend per page; Retention note.

**EpiloguePage.** The same EvidencePage with labels from `reassign-2050`: "Declared capability (manifest)", "Revealed performance (task logs)", "Supervisor's note", "Strength", "Incident"; a banner "Kaede Works, 2050. Unit HW-07. Same page, same rules."; sources: capability manifest, task logs, maintenance logs, incident reports, supervisor notes; excluded: `telemetry_private.json` (never read, counted from manifest). It is fixture-driven and small; it exists to make the point that the accountability mirror is about the workforce, not about carbon.

**SlackSimPage.** A Slack-styled window rendered from `slack_sim.json` (scripted conversation, the card, the modal) that calls the same intake endpoint with `channel: slack_sim`. Badge: "simulated Slack transport". Used only if the real bot is cut.

### 8.4 Component tree (props)

- `AppShell{children}`: header with product mark, decision title, `BackendBadge{health}`, `ViewerSwitcher{viewers, current, onChange}` (names only in present mode), `EpilogueToggle{active}`.
- `DecisionHome` → `PurposeBanner{decision, policy}`, `CandidateRow{subjects, pages, views}` → `CandidateCard{subject, claimCount, backend, viewedBySubject, onOpen}`, `CriterionBar{value, onSubmit, pending, lastRanking}`, `RankingStrip{ranking, subjects}`, `AuditStrip{audit}`.
- `EvidencePage` → `SubjectHeader{subject, labels, views}`, `WillStrip{declared, revealed, paraphrase, labels}`, `CriterionBar`, `EvidenceList{claims, order, items, annotations, highlightIds, onAnnotate}` → `ClaimCard{claim, rank, isReceipt, faithfulness, annotations, onAnnotate}` → `SourceChip{sourceId, item}` + `SourcePopover{item, tagScores?}`, `AnnotationThread{annotations}`, `AnnotationComposer{target, onSubmit, canContest}`, `LiveBadge{count, pulse, lastFrom}`, `ViewFlip{viewerRole, subjectId}`, `DroppedClaimsDisclosure{dropped}`, `PageFooter{backend, model, corpusHash, generatedAt}`.
- `DriftPage` → `DriftInput{value, onRun, examples, onPickExample}`, `DriftStepper{chain, mode, step, onStep}` → `WordDiff{before, after}`, `LostAddedSummary{lost, added}`.
- `MemoPage` → `MemoView{markdown, footnotes, summary}`, `MemoActions{onCopy, onPrint}`.
- `EpiloguePage` (EvidencePage + banner), `SlackSimPage` → `SlackWindow{script}`.
- Shared: `Skeleton`, `EmptyState{title, hint}`, `ErrorState{error, onRetry}` (on `llm_unavailable` offers "use keyword mode" which retries with `X-Allow-Heuristic: 1`), `Toast`.

### 8.5 State and data

TanStack Query for all server data (`api/queries.ts`: `useDecision`, `usePage`, `useRanking`, `useAnnotations`, `useAudit`, `useDrift`, `useMemo`). `ViewerContext` (`state/viewer.tsx`: token, role, present; localStorage). `useDecisionEvents(decisionId)` (`api/sse.ts`) opens one `EventSource` per decision and invalidates `['page', d, p]`, `['annotations', d, p]`, `['ranking', d]`, `['audit', d]` on matching events; a 10-second poll on annotations is the fallback so the live badge never depends on SSE alone. Types come from the API's OpenAPI (`make types` → `web/src/api/schema.d.ts`). No other global store.

### 8.6 Interactions that must feel right

- Criterion submit → skeleton "reading receipts…" on the ranking strip → list re-orders with layout animation, receipt cards get the emerald rail and rank pip; the `WillStrip` stays fixed so the eye has an anchor.
- Annotation submit → optimistic append; SSE confirms; the other viewer's `LiveBadge` pulses and the card scrolls into view once.
- Drift → cards reveal as the response arrives (or all at once if streaming is cut); the receipt toggle swaps the stepper without leaving the page.
- Hover chip → popover; click chip → pinned popover and highlight of every claim citing that id; Escape closes.
- Keyboard: chips and cards are focusable; popovers open on focus; `prefers-reduced-motion` disables the layout animation.

### 8.7 Tokens

Tailwind v4 `@theme` in `web/src/styles/tokens.css`; hex values copied from `prototype/ui/index.html :root` so the video and the old spike match: `--color-paper`, `--color-ink`, `--color-muted`, `--color-declared` (teal), `--color-revealed` (amber), `--color-paraphrase` (violet), `--color-strength`, `--color-gap` (rose), `--color-receipt` (emerald), `--color-dropped` (grey, struck), `--radius-card: 14px`, `--font-sans: "Inter", system-ui`. Type scale: 14 px body, 16 px claim text, 12 px chips and meta, 22 px page titles; present mode multiplies by 1.15.

### 8.8 Copy (exact strings)

- Purpose banner: "This page exists for this decision only. It is deleted when the decision closes."
- Subject banner: "This is exactly what {planner} sees about you. Add context or contest any line; they see it before the decision."
- Criterion placeholder: "What do you actually need? In your own words."
- Ranking label: "Evidence support for this criterion (not a score of the person)."
- Dropped disclosure: "{n} claims dropped: {a} had no source, {b} were not supported by their source."
- Live badge: "{name} added context · {t} ago"
- Views: "{planner} viewed this page {n} times, last {hh:mm}. {subject} has not viewed it yet." / "{subject} viewed it {n} times, last {hh:mm}, and left {k} notes."
- Backend badges: "Gemini 3.8 Flash · reachable · checked {hh:mm}" / "keyword mode (no LLM)" / per artefact "read by Gemini" / "keyword mode".
- Closed: "This page was deleted when the decision closed. {retention note}"
- Epilogue banner: "Kaede Works, 2050. Unit HW-07. Same page, same rules."

### 8.9 States

Loading skeletons per card; empty ("No claims yet. Refresh to read the sources."); error card with code and retry; stale hint when the page's corpus hash differs from the audit's; heuristic badge; 410 closed state; offline SSE indicator ("live updates paused, polling").

### 8.10 Anti-walls-of-text rules (enforced by schema, prompt, or component)

Claim text ≤ 25 words (prompt and `max_length=220`); one claim per card; sources as chips, never as inline lists; memo sections ≤ 6 bullets and summary ≤ 60 words; drift steps one sentence each; audit strip is counts plus one line per tile; popovers instead of inline paragraphs; no paragraph longer than three lines without a disclosure; the subject view reuses the same cards.

---

## 9. Demo design

### 9.1 The problem the demo has to solve

Other teams will show robotic arms and glasses that translate Japanese live. A before/after of "Salesforce + Slack + Excel + Gmail merged into one" will not beat that (Steven, 02:30). What can: a moment the audience has never seen, about people, that visibly responds to something a judge typed, and that ends with a page they would want to be shown if it were about them. The demo proves one claim: **a people decision can be made of receipts instead of paraphrases, and the person can see it.**

### 9.2 The four beats, in order, with proof obligations

| # | Beat | What the audience sees | What must be real | Fallback |
|---|---|---|---|---|
| 1 | **The drift chain** | One sentence an employee wrote goes up three manager levels and comes out as two words ("Rin — mobile"). Struck words in rose, added in amber. Then the same sentence goes up with a receipt and survives every level in green. A judge may type the sentence. | Three sequential Gemini calls, one persona each, on the typed sentence; the receipt variant is code-enforced (`verbatim_ok`). | Seeded chains labelled "recorded earlier with Gemini"; heuristic drift labelled "simulated (no LLM)". |
| 2 | **The two-sided mirror** | "See what Rin sees": the same page, no numbers. From a phone, Rin adds context to the manager's line ("I said I want to stay in Osaka; 'flexible on location' is not what I wrote") and contests it. On Aya's screen the badge lights and the note sits beside the paraphrase. | Server-scoped subject view (different token, different response); annotation persisted; SSE delivery to the evaluator's browser. | Web composer on the phone instead of Slack; 10-second poll if SSE stalls. |
| 3 | **Judge-supplied criterion** | A judge types what they would actually need; the evidence list re-orders with new receipts; the support bar is labelled as evidence support, not a score. | Live re-rank call over the stored claims; `ordered_claim_ids` drives the animation. | Keyword mode, labelled. |
| 4 | **2050 epilogue** | One toggle: the same page for unit HW-07, declared capability beside revealed performance, incidents as gaps, private telemetry never read. Five seconds. | Fixture-driven through the same pipeline and components. | Static page from seeded claims. |

Supporting beats that carry the four: the WillStrip contrast for Yui (own words vs "loves travel"); hover a chip to see the source; the dropped-claims disclosure ("1 claim dropped: not supported by its source"); the memo with footnotes and the audit strip ("DMs: 41, never read, counted from manifest").

### 9.3 The 90-second video, beat by beat (submitted artifact; prerecorded is allowed and the first frame says so)

Record at 1920×1080, browser 1440 px wide at 110% zoom, `?present=1`, after `make video-mode` (everything warm; the typed criterion and the drift sentence are the only live calls).

| t (s) | Beat | On screen | Real / seeded |
|---|---|---|---|
| 0–8 | Stuck moment | Purpose banner; three candidate cards; caption "Aya has to pick one of three people for a two-year overseas exchange. Today: a six-month-old sheet and what each boss remembers." | Seeded |
| 8–22 | Drift chain | Yui's own sentence → team lead → department manager → division head: "Yui — travel-ready"; struck and added words; lost/added summary | Live (warmed) |
| 22–38 | Receipts | Yui's page: WillStrip (own words vs manager's paraphrase); hover a chip; verbatim-receipt marks | Live extraction, cached |
| 38–50 | Criterion | Type "someone who will push back on a job-based culture rather than absorb it"; list re-orders; Kei's pushback and pilot surface as receipts | Live |
| 50–68 | Mirror | "See what Rin sees"; second window; Rin adds context from Slack on a phone; badge lights on Aya's screen; note beside the paraphrase | Live (real Slack or sim, labelled) |
| 68–80 | Memo + audit | One page; footnote chips; audit strip: used, never read (DMs 41), dropped 1, rules | Live |
| 80–90 | Epilogue + card | 2050 toggle for two seconds; end card: "Fictional company. Seeded data. Extraction, drift, re-ranking, annotations and the memo run live on Gemini. Recorded {date}." | Seeded |

**Narration (≤ 225 words; the existing DEMO-PLAN script is 221 and fits; this is the revision with the drift beat):**

> [0–8] Every year HR picks who gets the two-year overseas posting. It changes a career. And the decision runs on what the boss remembers.
>
> [8–22] Watch one sentence travel. Yui wrote: "I want to work with the US product team on pricing experiments." Her team lead. Her department. Her division head. "Travel-ready." Six words lost. That is not a data problem. It is a translation problem, and it happens at every level.
>
> [22–38] Steven said it on the way here: innovation has to be careful. Designed for the humans in it. So we did not build a score. We built receipts. Every line links to what she actually wrote or did. Hover it. It is there, word for word.
>
> [38–50] Type what you actually need, in your own words. The evidence re-orders, and it shows you why.
>
> [50–68] And here is the careful part. Yui sees the same page. Rin sees hers. Rin adds context from her phone: "I said I want to stay." Her note lands on the evaluator's desk before the decision is made.
>
> [68–80] One page. Every claim sourced. What we read. What we never read.
>
> [80–90] Innovation is changing the way you think. We changed what a people decision is made of: from what the boss remembers to what the person did. And we let the person see it. Same rules in 2050.

### 9.4 Preliminary pitch, 180 seconds (template order; ≤ 450 words including the demo narration)

| s | Section | Content |
|---|---|---|
| 0–8 | Title | "Receipts. Evidence, with receipts, that both the evaluator and the employee can see, for one high-stakes people decision." |
| 8–35 | Problem | "This week the head of HR at a large Japanese enterprise told us how internal placement works: twice a year a Will-Can-Must sheet, a conversation with the boss, and then HR decides from memory. Will has no metric. The words change as they pass up the chain. He called it the thing HR is most troubled by." (Quote only what is cleared; no figures unless cleared.) |
| 35–55 | Insight | "Everyone in this space, Workday included, builds the same thing: mine the data, produce a score, show managers. It is legal, and it does not ship, because employees find it creepy and nobody is accountable to them. The blocker is not data. It is design. Innovation has to be careful." |
| 55–125 | Solution (demo) | Play the video from 8 s to 78 s, or run beats 1–3 live if the network holds. Say "this is a recording" if it is. |
| 125–147 | Impact | Two numbers with labels: the measured one ("in our demo corpus, N of M model-proposed claims were dropped for lacking a verbatim source: that is the reliability number", VERIFIED at demo time) and the stakes one (the population of first-line managers the customer wants to reach and cannot today, VERIFIED from the meeting, **only if cleared**; otherwise "thousands of first-line managers"). One sentence on cost of a wrong posting: "a two-year commitment" (money only if cleared). |
| 147–160 | Differentiation | "Same skill tags the customer already has. Plus a verbatim receipt on every claim. Plus the employee's side of the page. Workday scores. We cite." |
| 160–172 | Architecture | One diagram: sources → policy gate (purpose, allowlist, DMs excluded by config) → extractor → span check → citation store → two views over one store → memo. "Fixtures are fictional. Extraction, drift, re-ranking, annotations and the memo run live." |
| 172–180 | Roadmap | "One decision type with one HR team. Then mentor discovery and onboarding on the same engine. Same rules for a mixed workforce in 2050." |

Word budget: 180 s at 150 wpm = 450 words. The narration above is ~200 words; the video narration inside it is ~150; the remaining slots have ~100 words of headroom. Rehearse with a timer; cut Insight first if over.

### 9.5 Final, 360 seconds: what to add to the prelim

1. **Judge-supplied drift sentence** (live): "Give me one sentence you would write on your own review." Run it. Then the receipt variant.
2. **Judge-supplied criterion** (live).
3. **Email intake** (`make email-demo`): a message dropped in the inbox becomes an annotation with an "email" chip. Thirty seconds, proves the hybrid.
4. **Cultural insight, 40 s**: CEO-ship vs job-based; accountability over legality; "creepy" (paraphrased; nothing internal). This is the part that "opens eyes": the constraint is social, and the careful design is the only one that ships.
5. **Architecture deep-dive with the truth table on screen** (§13): what is seeded, what runs, what is proposed; the dropped list as the reliability proof; the manifest as the never-read proof.
6. **2050 epilogue, 30 s**: the same page for HW-07; "the accountability mirror is about the workforce, not about carbon"; Japan context numbers with labels (§14).
7. **Why not the internal approach or Workday, in one breath**: "They produce a score for managers. We produce receipts for both sides. That difference is what unblocks rollout."

### 9.6 The VP self-demo card (only if he is reachable and willing; every message to him is a draft for Carl to approve)

His actual offer on tape was "Please feel free to reach out" `[R 1:04:27]` (the line "you can bother me anytime" was Carl's). Ask through Shion, in writing, for five minutes on our laptop with his own decision type. The card:

1. Here are three people for one exchange slot. Pick one from the manager notes alone.
2. Open a candidate. Read the declared will next to the manager's paraphrase.
3. Type a criterion in your own words. Watch the evidence re-order.
4. Switch to the employee's view. It is the same page.
5. Would you show this page to a first-line manager? To the employee?

A yes on step 5 is the sign-off, and a quote we can ask permission to use. A no gives the next build item. Either way, ask which figures and which phrasing of the problem may appear in public.

### 9.7 Contingencies

| Failure | Detection | Response |
|---|---|---|
| Gemini unreachable at demo time | `/health` badge; `make llm-check` at 14:30 and again at 09:00 Sun | `MODE=auto` falls back to keyword mode for a whole artefact, badged; drift uses seeded chains labelled "recorded earlier with Gemini"; never mix backends in one artefact |
| Slack Socket Mode fails on venue Wi-Fi | Bot does not ack | Phone opens the subject page on the LAN and uses the web composer; or `SlackSimPage`; truth table edited to "simulated transport" |
| SSE stalls behind a proxy or hotspot | Live badge stale | 10-second annotation poll; heartbeat every 15 s; `since` replay on reconnect |
| Projector mirror hides the second window | Rehearsal | Use the phone as the subject device; or `?present=1` split layout |
| Latency on a live call | Progress state after 12 s | 45-second budget then labelled fallback; rehearse the fallback once on purpose |
| Demo state polluted by a rehearsal | `make reset` restores the seeded start; `make smoke` and tests use a scratch state dir | Run `make video-mode` before every take |
| Venue network dead | Everything | Play the recording; say so |

### 9.8 Q&A lines (both rounds)

- **Who pays?** The HR COE, for one decision type, inside a matching-and-training budget line it already spends on. Priced per decision cycle, not per seat (hypothesis, §10.3).
- **Why not Workday or the customer's own attempt?** They produce a score for managers. We produce receipts for both sides. The difference is what unblocks rollout to first-line managers.
- **What if the summary is wrong?** The person it is about sees it and contests it before the decision; unsupported claims are dropped and the dropped list is visible; nothing is a verdict.
- **Isn't "support" a score?** It is how much of the listed evidence bears on the criterion the planner typed; it is never aggregated, never in the memo, never shown to the subject. We can hide the number and keep the bar.
- **Which data, and who consented?** Public channels, shared documents, sheets the employee already gave HR, AI sessions the employee opted in. DMs and private channels are excluded by configuration and counted from a manifest the tool cannot open. The subject sees the same page.
- **How do you know DMs were not read?** The API process has no code path that opens the excluded files; a test asserts it; the audit strip shows the manifest hash.
- **What if the model hallucinates?** Every claim must carry a verbatim span from its cited source; span mismatch triggers a second check; failure drops the claim into the visible dropped list. That list is our reliability metric.
- **Won't managers write less if the employee can see it?** The paraphrase is shown beside the source anyway; the manager's note becomes a reading, not the record. Today HR re-interviews the person to catch drift; this makes that the default.
- **What is hard-coded?** The company and people. What runs: extraction with citations, faithfulness, re-ranking on a free-text criterion, the drift chain, the annotation round-trip, the memo, the audit strip.
- **How does this scale past one decision?** Each decision is its own purpose-locked page with its own policy; the taxonomy is the customer's; connectors replace fixtures. The second decision type is mentor discovery (§14).
- **Why 2050?** Because the accountability mirror is a property of the workforce, not of humans only; a robot's manifest and logs are the same declared-vs-revealed shape, and the excluded telemetry is the same never-read line.

---

## 10. Quantification and business value

Steven's instruction: the thing to get done is "quantifying and helping the other judges see value in it." Every number below has a label and its inputs × method × source × assumptions line. Numbers from the VP conversation are referenced by placeholder until cleared (§15).

### 10.1 The numbers

| Tag | Number | Label | Inputs × method × source × assumptions | Where it goes |
|---|---|---|---|---|
| N1 | Demo corpus: 3 people, ~120 public Slack messages, 5 docs, 3 WCM sheets, 3 manager notes, 9 AI-session summaries (6 opted in), 41 DMs never read | ILLUSTRATIVE (fixture sizes; the counts themselves are VERIFIED at demo time by the audit strip) | Fixture files × manifest count × `fixtures/decisions/exchange-2027/manifest.json` × fictional | Audit strip; truth table |
| N2 | **Claims dropped for lacking a verbatim source: N of M** model-proposed claims (measure at demo time) | VERIFIED (system measurement) | Extraction output × span check + faithfulness pass × `dropped_claims` table × Gemini 3.8 Flash on the demo corpus | **Primary impact number** (technical credibility) |
| N3 | The first-line-manager population the customer wants to reach and cannot today | VERIFIED (interview) | `[VP-FIG-3, R 0:49:34]` × his statement × sensitive × **clearance required**; say "thousands" otherwise | Impact slide if cleared |
| N4 | Per-person cost of the two-year exchange | VERIFIED (interview) | `[VP-FIG-1, R 0:20:57–0:21:03]` × his statement × what it includes is not stated × **clearance required** | Stakes line if cleared; otherwise "a two-year commitment" |
| N5 | Current spend the customer would consider replacing (Japan training systems + matching AI) | VERIFIED (interview), time basis unconfirmed | `[VP-FIG-2, R 0:39:34]` × his "low estimate" × scope moved from Tokyo HQ to Japan during the exchange × conditional on replacing all of it × **clearance required** | "The customer already spends on this category" only; never as our revenue |
| N6 | In a 2024 survey of 312 users of a Japanese e-signature product, 73.5% said formal approval requests (ringi) take a day or more; 52.5% take 2–3 days; the top pain is "too many approvers" (41.0%) | RESEARCH | Bengo4.com / CloudSign survey, Sep 25–Oct 31 2024, n = 312, digitally mature respondents; not this customer | Cultural context; the "approval chain" line in the final |
| N7 | Loaded cost of an hour of HR administrative staff time in Japan ≈ ¥2,500–3,000 | CALCULATED from a WEAK RESEARCH input | ¥4.934M average annual income for HR administration (MHLW job-tag site, FY2023 wage survey, via a secondary page) ÷ 2,000 h × 1.15–1.20 employer on-costs | Only inside a formula, with the caveat |
| N8 | Knowledge workers spend ~20% of the week finding information or colleagues | RESEARCH (2012, widely over-cited) | McKinsey Global Institute, "The social economy", 2012 | Avoid on stage; background only |
| N9 | Labour supply shortfall of about 11 million by 2040; ~3.41 million by 2030 | RESEARCH | Recruit Works Institute, "未来予測2040", March 2023; Recruit's own think tank | 2050 slide only |
| N10 | Government target: AI robots that learn, adapt and act alongside people by 2050; 2030 milestone of robots more than 90% of people feel comfortable with | RESEARCH | Cabinet Office Moonshot Goal 3 | 2050 slide only |
| N11 | Evaluator time per candidate: today vs Receipts | ILLUSTRATIVE until timed | `t_today` = minutes assembling sheet + notes + asking around (ask Aya's real counterpart); `t_receipts` = review minutes of the generated page including contest handling; hours freed = cycles × candidates × (t_today − t_receipts) ÷ 60 | Do not put a number on the slide until measured; show the formula |
| N12 | "A large Japanese enterprise" of roughly fifty thousand people | RESEARCH | Recruit Holdings employee count ≈ 47–49.5K (PitchBook, via STEVEN-RESEARCH.md) | Say "large Japanese enterprise" unless naming the customer is cleared |

**Slide 05 recommendation.** Primary number: N2, because it is ours, measured, and answers the 30% technical criterion ("PoC shows the key technical idea works"). Second number: N3 if cleared. Third: the N11 formula with blanks, labelled ILLUSTRATIVE, to show we know what to measure in a pilot. Show the "inputs × method × source × assumptions" line under each, as the template requires.

### 10.2 Social impact and business potential (the 40%)

**Social impact.** The people decision becomes something the person can see and correct. Concretely: the drift the VP described (the boss's paraphrase deciding a two-year posting) is replaced by the person's own words with receipts; the covert version that already exists inside the customer becomes unnecessary. The population affected in one customer: every employee considered for placement, and the first-line managers who cannot be given analytics today (N3). Beyond one customer: any organization where evaluation data is held above the people it describes, which in Japan is shaped by the accountability norm the VP named `[R 0:44:24]` and the fear of being read `[R 0:07:38]`.

**Business potential.** Buyer: the HR Centre of Excellence, which owns HR strategy and systems `[R 0:01:16]`. Entry: one decision type per year with a purpose-locked page (exchange or transfer selection), because that is a bounded, high-stakes, rare event where a page-per-decision is credible. Expansion: mentor discovery for interns (Shion's workflow), onboarding matching, then every placement decision. The customer already spends on this category (N5) and told us the space has many players and Workday; our position is not "replace the matching system" (he said he would bet only if everything were replaced) but "the receipts layer on top of the taxonomy you already have". Recruit's grand-prize acceleration program explicitly offers "User Validation (PoC) leveraging Recruit's and Indeed's assets" (Day 1 deck p21); the pilot in §14 is designed to fit it.

**Pricing hypothesis (ILLUSTRATIVE).** Per decision cycle (a purpose-locked page for one decision type, all subjects, all evaluators), not per seat, so the buyer pays for the decision it cares about and nothing runs as a standing profile. The number is unknown; the reversal fact is a customer saying the category budget is fully committed to the matching vendor.

### 10.3 Competitive positioning (market scan, Sep 26; URLs in `sync.md` §F)

| Player | What they ship | What they do not do | The one-line gap |
|---|---|---|---|
| Workday (Skills Cloud, Talent Marketplace, HiredScore; Agent System of Record; Sana front door) | Skills graph, mobility matching, agents registered like staff; Sana reaches into Slack/Salesforce | A cited, two-sided evidence page for one decision; anything for people without a Workday seat | Scores and matches inside its own system, for its own users |
| Eightfold | "Digital Twin" from work-app signals; career coach agent | The subject's side; provenance to the sentence; purpose lock | The nearest thing to revealed will, built for the employer |
| Gloat | Mentor matching; Policy Navigator with citations | Chat or email intake; evidence pages | Marketplace destination, not a decision page |
| Glean | Expert search from what people authored; inherits source permissions | Anything the viewer could not already open; no HR policy | The mentor sees nothing from Salesforce by design |
| Rippling AI | Every number links to its record; every action staged for a human | Expert finding; enterprise HR | The trust UX to copy, mid-market, own data only |
| Salesforce Agentforce HR | Employee self-service in Slack (time off, cases, escalation) | Decisions about people; evidence | Answers employees about their own records |
| ServiceNow + Moveworks | Intake and case routing at scale | Person-to-person matching; cited dossiers | Routes tickets to queues |
| Indeed Smart Sourcing / Smart Screening / Talent Scout | AI matching, outreach, a "Smart Fit Score", "hiring stays a human process" | The internal last mile: placement, transfers, mentors, the subject's view | External candidate flow up to the ATS |
| The customer's own attempt | `[VP-FACT-2, R 0:56:27–0:56:43]`: a statement about a person followed by the exchanges that show it | The employee's side of the page | Not for public artifacts; ask before mentioning |

**"Why not Workday" in one breath:** they produce a score for managers; we produce receipts for both sides; the difference is what unblocks rollout.

Watch item: Workday Rising, Oct 12–15 2026, two weeks after the event.

### 10.4 What would make the business case false

- The customer's own attempt already shows the employee the page (nothing he said suggests it; ask).
- A branching template plus corporate Claude produces an equally trusted page in the evaluator's own time (the packet's baseline objection; test it in the pilot).
- Managers refuse to write notes if the subject can see them, and HR prefers their silence to the receipts.
- No HR team will buy per decision; they only buy platforms (then Receipts is a feature of a matching vendor, and the accelerator's PoC is how to find out).

---

## 11. Architecture and codebase

Design pass by the planning agent (Sat 03:15–04:10), reconciled with the prototype audit. Everything below is specified so the two of you can build in parallel: A owns `receipts/api` (engine, LLM, Slack, fixtures, tests), B owns `receipts/web` (UI, video, deck). The old `prototype/` stays frozen as reference; nothing imports from it.

### 11.1 Repo layout

```
hyderabaddies/
├── README.md                                   # product, truth table, OSS disclosure, run in 3 commands (submission README)
├── PRD.md  sync.md                             # this spec and the reasoning log
├── .claude/launch.json                         # repo-relative api/web configs (replaces the /private/tmp one)
├── .gitignore                                  # receipts/api/.venv, receipts/web/node_modules, receipts/state/, .env
├── prototype/                                  # FROZEN Friday spike; add one README line: "superseded by receipts/"
└── receipts/
    ├── Makefile                                # setup/api/web/dev/slack/warm/reset/smoke/test/build/types/llm-check/video-mode
    ├── .env.example
    ├── docs/{DEMO_SCRIPT,TRUTH_TABLE,SLACK_SETUP,INTAKE,ARCHITECTURE}.md
    ├── fixtures/                               # READ-ONLY; the API opens only files named in a policy.json
    │   ├── company.json                        # {"id":"kaede","name":"Kaede Works (fictional)","decisions":["exchange-2027","reassign-2050"]}
    │   ├── viewers.json                        # demo identities, roles, demo tokens (aya, rin, yui, kei, obs)
    │   ├── personas.json                       # drift personas, 3 levels
    │   ├── slack_sim.json                      # scripted fake-Slack conversation for the fallback page
    │   └── decisions/
    │       ├── exchange-2027/
    │       │   ├── decision.json               # title, purpose, planner, subjects[3], tags, tag_scores, labels
    │       │   ├── policy.json                 # allowlist with per-source role, excluded sources, rules, retention
    │       │   ├── manifest.json               # GENERATED by scripts/build_manifest.py: count + sha256 per file (incl. dm.json)
    │       │   ├── slack.json                  # ~120 msgs sl-001..sl-120 with explicit `mentions`
    │       │   ├── docs.json wcm.json manager_notes.json sessions.json
    │       │   ├── dm.json                     # EXCLUDED; on disk to prove it is never opened
    │       │   └── seed/{annotations,drift_examples,email_rin}.json   # marked seeded
    │       └── reassign-2050/
    │           ├── decision.json policy.json manifest.json
    │           ├── capability_manifest.json task_logs.json maintenance.json incidents.json supervisor_notes.json
    │           ├── telemetry_private.json      # EXCLUDED
    │           └── seed/claims.json            # fallback so the epilogue is never empty
    ├── api/
    │   ├── pyproject.toml                      # fastapi, uvicorn[standard], pydantic>=2, google-genai, slack-bolt, python-dotenv, pytest, httpx
    │   ├── evidence/
    │   │   ├── __init__.py  __main__.py        # `python -m evidence` → uvicorn evidence.api.app:app
    │   │   ├── config.py                       # Settings from env/.env
    │   │   ├── ids.py                          # id regexes, claim_id(), ranking_id(), drift_id(), cache_key(), corpus_hash()
    │   │   ├── models.py                       # Pydantic v2 domain models (§11.2)
    │   │   ├── policy.py                       # load_policy(), PolicyViolation, excluded-path guard, purpose lock
    │   │   ├── corpus.py                       # Corpus: allowed files only, opt-in filter, items_for(), render(), hash
    │   │   ├── store.py                        # SQLite WAL; schema §11.9; reset(); close_decision()
    │   │   ├── events.py                       # in-process broadcaster + durable `events` table for SSE replay
    │   │   ├── llm/{client,schemas,prompts,heuristic,cache}.py
    │   │   ├── services/{evidence,faithfulness,ranking,memo,drift,audit,annotations,views,scoping,intake}.py
    │   │   ├── api/{app,deps,errors,sse,routes_decisions,routes_pages,routes_rankings,routes_annotations,routes_drift,routes_intake,routes_admin}.py
    │   │   └── intake/{base,email_stub,slack_app,slack_blocks}.py
    │   ├── scripts/{build_manifest,seed,smoke,llm_check,gen_slack_fixture}.py
    │   └── tests/{conftest,test_policy_gate,test_ids,test_faithfulness,test_drift,test_scoping,test_golden_storylines,test_api_smoke}.py
    └── web/
        ├── package.json                        # react, react-dom, react-router-dom, @tanstack/react-query, motion, react-markdown, remark-gfm, tailwindcss, @tailwindcss/vite
        ├── vite.config.ts                      # host:true, 5173, proxy /api → 127.0.0.1:8787
        ├── index.html tsconfig.json
        └── src/
            ├── main.tsx App.tsx routes.tsx
            ├── styles/tokens.css               # @import "tailwindcss"; @theme {...}
            ├── api/{schema.d.ts (GENERATED via openapi-typescript),client,queries,sse}.ts
            ├── state/viewer.tsx
            ├── components/                     # §8.4
            └── pages/{DecisionHome,EvidencePage,DriftPage,MemoPage,EpiloguePage,SlackSimPage}.tsx
```

**Fixture migration from `prototype/data/`.** Copy the five fixture files, keep the people, channels, authors and the three storylines, and renumber ids to the new pattern (`wcm-rin` → `wcm-001`, `mn-yui` → `mn-002`, and so on; Slack `sl-001..sl-034` keep their numbers, new messages continue to `sl-120`). Add a `mentions` array to every Slack message (built offline by `gen_slack_fixture.py`, hand-checked for the three storylines). Add `visibility` to every item. Remove `tag_scores` from the candidate objects and put them under `decision.tag_scores` keyed by subject then tag id.

### 11.2 Domain model (`api/evidence/models.py`)

**Id conventions (`ids.py`).** Stable and content-addressed, never positional.

| Entity | Pattern | Example |
|---|---|---|
| Decision | slug, equal to `policy.purpose` | `exchange-2027`, `reassign-2050` |
| Subject | slug | `rin`, `hw-07` |
| SourceItem | `^(sl\|doc\|wcm\|mn\|ses\|dm\|man\|log\|mnt\|inc\|sup\|tel)-\d{3}$` | `sl-023` |
| Tag | slug of the label | `experiment-design` |
| Claim | `cl-{subject}-{sha1(kind\|norm(text)\|sorted(source_ids))[:8]}` | `cl-rin-3f2a9c1d` |
| Ranking | `rk-{sha1(decision\|norm(criterion)\|corpus_hash)[:8]}` | `rk-8b1c0e2f` |
| Annotation | `an-{token_hex(4)}` | `an-9f3a1c2e` |
| DriftChain | `dr-{sha1(norm(sentence)\|personas_version)[:8]}` | `dr-51aa0c7d` |
| IntakeRequest | `in-{channel}-{token_hex(4)}` | `in-slack-0a1b2c3d` |
| ViewEvent / Event | SQLite autoincrement | `42` |

```python
SOURCE_ID = re.compile(r"^(sl|doc|wcm|mn|ses|dm|man|log|mnt|inc|sup|tel)-\d{3}$")
def norm(s: str) -> str: return " ".join(s.lower().split())
def claim_id(subject_id: str, kind: str, text: str, source_ids: list[str]) -> str
def ranking_id(decision_id: str, criterion: str, corpus_hash: str) -> str
def drift_id(sentence: str, personas_version: str) -> str
def corpus_hash(rendered_items: list[str]) -> str          # sha256 of sorted rendered items, 12 hex
def cache_key(task: str, backend: str, model: str, prompt_version: str, corpus_hash: str,
              decision_id: str, subject_id: str | None, extra: str = "") -> str
```

**Models.**

```python
class SourceKind(str, Enum):
    slack="slack"; doc="doc"; wcm="wcm"; manager_note="manager_note"; session="session"
    dm="dm"; private_channel="private_channel"
    capability_manifest="capability_manifest"; task_log="task_log"; maintenance_log="maintenance_log"
    incident="incident"; supervisor_note="supervisor_note"; telemetry_private="telemetry_private"
class SourceRole(str, Enum): declared="declared"; revealed="revealed"; paraphrase="paraphrase"; observed="observed"
class Visibility(str, Enum): public="public"; shared="shared"; private="private"
class ClaimKind(str, Enum): declared_will="declared_will"; revealed_will="revealed_will"; manager_paraphrase="manager_paraphrase"; strength="strength"; gap="gap"
class Backend(str, Enum): gemini="gemini"; heuristic="heuristic"
class ViewerRole(str, Enum): evaluator="evaluator"; subject="subject"; manager="manager"; observer="observer"; service="service"
class Origin(str, Enum): web="web"; slack="slack"; slack_sim="slack_sim"; email="email"; seed="seed"
class IntakeChannel(str, Enum): slack="slack"; slack_sim="slack_sim"; email="email"; web="web"

class Company(BaseModel): id: str; name: str; decisions: list[str]

class Labels(BaseModel):                 # per-decision UI strings; lets 2050 reuse every component
    declared_will: str = "Declared will (own words)"
    revealed_will: str = "Revealed will (what they chose to do)"
    manager_paraphrase: str = "Manager's paraphrase"
    strength: str = "Strength"; gap: str = "Gap"
    subject_noun: str = "candidate"; paraphraser_noun: str = "manager"

class Person(BaseModel):
    kind: Literal["person"] = "person"
    id: str; name: str; role: str; team: str; manager_id: str; tenure_years: int
class Capability(BaseModel): name: str; declared_level: str; manifest_source_id: str
class HumanoidWorker(BaseModel):
    kind: Literal["humanoid"] = "humanoid"
    id: str; name: str; model: str; designation: str; site: str; commissioned: date; supervisor_id: str
    declared_capabilities: list[Capability]
Subject = Annotated[Union[Person, HumanoidWorker], Field(discriminator="kind")]

class Planner(BaseModel): id: str; name: str; role: str
class Tag(BaseModel): id: str; label: str
class Decision(BaseModel):
    id: str; company_id: str; title: str; purpose: str; year: int
    planner: Planner; subjects: list[Subject]; tags: list[Tag]
    tag_scores: dict[str, dict[str, int]] = {}     # seeded "Can" levels; WCM popover only, never summed
    labels: Labels = Labels(); status: Literal["open", "closed"] = "open"

class SourcePolicy(BaseModel):
    kind: SourceKind; file: str; note: str; role: SourceRole
    visibility_allowed: list[Visibility] = [Visibility.public, Visibility.shared]
    requires_opt_in: bool = False
class ExcludedSource(BaseModel): kind: SourceKind; file: str | None; note: str
class Retention(BaseModel): delete_on_close: bool = True; note: str
class Policy(BaseModel):
    version: str; purpose: str                     # == decision.id (purpose lock)
    allowed_sources: list[SourcePolicy]; excluded_sources: list[ExcludedSource]
    rules: list[str]; retention: Retention

class SourceItemBase(BaseModel):
    id: str = Field(pattern=SOURCE_ID.pattern); kind: SourceKind; date: date
    subject_ids: list[str]                # author + explicit mentions
    author_id: str | None = None; visibility: Visibility
    rendered: str = ""                    # "[sl-023] Slack #pricing 2026-05-14 by yui: ..."
class SlackMessage(SourceItemBase):  kind: Literal[SourceKind.slack]; channel: str; text: str; mentions: list[str] = []
class SharedDoc(SourceItemBase):     kind: Literal[SourceKind.doc]; title: str; excerpt: str
class WcmSheet(SourceItemBase):      kind: Literal[SourceKind.wcm]; will: str; can: str; must: str
class ManagerNote(SourceItemBase):   kind: Literal[SourceKind.manager_note]; manager_id: str; text: str
class SessionSummary(SourceItemBase): kind: Literal[SourceKind.session]; opted_in: bool; problem: str; approach: str; outcome: str; quoted_prompt: str
class CapabilityManifestItem(SourceItemBase): kind: Literal[SourceKind.capability_manifest]; capability: str; declared_level: str; text: str
class TaskLog(SourceItemBase):       kind: Literal[SourceKind.task_log]; task: str; outcome: str; text: str
class MaintenanceLog(SourceItemBase): kind: Literal[SourceKind.maintenance_log]; component: str; text: str
class IncidentReport(SourceItemBase): kind: Literal[SourceKind.incident]; severity: Literal["low","medium","high"]; text: str
class SupervisorNote(SourceItemBase): kind: Literal[SourceKind.supervisor_note]; supervisor_id: str; text: str
SourceItem = Annotated[Union[SlackMessage, SharedDoc, WcmSheet, ManagerNote, SessionSummary, CapabilityManifestItem,
    TaskLog, MaintenanceLog, IncidentReport, SupervisorNote], Field(discriminator="kind")]

class Faithfulness(BaseModel):
    verdict: Literal["supported", "partially_supported", "unsupported", "unchecked"]
    checker: Literal["span", "gemini", "heuristic", "none"]
    quote: str | None = None; note: str | None = None
class Claim(BaseModel):
    id: str; decision_id: str; subject_id: str; kind: ClaimKind
    text: str = Field(max_length=220); source_ids: list[str] = Field(min_length=1); tags: list[str] = []
    quote: str | None = None; faithfulness: Faithfulness; backend: Backend
class DroppedClaim(BaseModel):
    reason: Literal["no_valid_source", "unsupported", "bad_kind", "too_long"]
    text: str; source_ids: list[str] = []; kind: str | None = None
class EvidencePage(BaseModel):
    decision_id: str; subject_id: str; backend: Backend; model: str | None; prompt_version: str; corpus_hash: str
    claims: list[Claim]; dropped: list[DroppedClaim]; truncated_item_ids: list[str] = []; generated_at: datetime

class RankRow(BaseModel):
    subject_id: str; support: int = Field(ge=0, le=100)   # never shown to subjects, never in the memo
    rationale: str; receipt_claim_ids: list[str]
    ordered_claim_ids: list[str]          # all of the subject's claims, most relevant first → drives the re-order animation
class Ranking(BaseModel):
    id: str; decision_id: str; criterion: str; backend: Backend; model: str | None; rows: list[RankRow]; created_at: datetime

class AnnotationTarget(BaseModel): type: Literal["source", "claim", "page"]; id: str | None = None
class Annotation(BaseModel):
    id: str; decision_id: str; subject_id: str; author_id: str; author_role: ViewerRole
    target: AnnotationTarget; text: str = Field(min_length=1, max_length=500)
    contests: bool = False; origin: Origin; seeded: bool = False; created_at: datetime
class ViewEvent(BaseModel): id: int; decision_id: str; subject_id: str; viewer_id: str; viewer_role: ViewerRole; origin: Origin; at: datetime
class ViewSummary(BaseModel):
    by_role: dict[str, dict]     # {"evaluator":{"count":2,"last_at":"..."},"subject":{"count":0,"last_at":null}}
    sentence: str                # "Aya viewed this page 2 times (last 14:02). Rin has not viewed it yet."

class Persona(BaseModel): id: str; level: int; name: str; title: str; artifact: str; style: str; max_words: int
class DriftStep(BaseModel): level: int; persona_id: str; text: str; dropped: list[str] = []; added: list[str] = []
class ReceiptStep(BaseModel): level: int; persona_id: str; text: str; verbatim_ok: bool   # code-verified
class DriftChain(BaseModel):
    id: str; decision_id: str; subject_id: str | None; source_id: str | None; original: str
    drift: list[DriftStep]; receipt: list[ReceiptStep]; lost: list[str]; added: list[str]
    backend: Backend; model: str | None; seeded: bool = False; created_at: datetime

class IntakeRequest(BaseModel):
    id: str; channel: IntakeChannel; decision_id: str; subject_id: str | None
    requester_external_id: str; on_behalf_of: str | None
    action: Literal["open_page", "add_context", "request_summary"]; payload: dict = {}
    received_at: datetime; status: Literal["received", "handled", "rejected"] = "received"
class IntakeResult(BaseModel):
    ok: bool; message: str; page_url: str | None = None; top_receipts: list[Claim] = []; annotation: Annotation | None = None

class AuditStrip(BaseModel):
    purpose: str; decision_id: str; policy_version: str
    used: list[dict]          # [{"kind":"slack","count":118,"note":"public channels only","role":"revealed"}]
    never_read: list[dict]    # [{"kind":"dm","count":41,"note":"private messages, never read","counted_from":"manifest"}]
    rules: list[str]; views: dict[str, ViewSummary]; dropped: dict[str, dict[str, int]]
    backend_per_page: dict[str, str]; retention: Retention
```

**LLM response schemas (`llm/schemas.py`; deliberately flat, strings validated in code, because nested unions and enums can be rejected by Vertex structured output).**

```python
class ExtractedClaim(BaseModel): text: str; kind: str; source_ids: list[str]; tags: list[str]; quote: str
class ExtractionOut(BaseModel): claims: list[ExtractedClaim]
class FaithResult(BaseModel): claim_id: str; verdict: str; quote: str; note: str
class FaithfulnessOut(BaseModel): results: list[FaithResult]
class RankRowOut(BaseModel): candidate: str; support: int; rationale: str; receipt_claim_ids: list[str]; ordered_claim_ids: list[str]
class RerankOut(BaseModel): ranking: list[RankRowOut]
class DriftStepOut(BaseModel): paraphrase: str; dropped: list[str]; added: list[str]
class DriftFramingOut(BaseModel): framing_before: str; framing_after: str
class MemoOut(BaseModel): summary: str; open_questions: list[str]
```

**`policy.json` for `exchange-2027`.**

```json
{"version": "2026-09-26.1", "purpose": "exchange-2027",
 "allowed_sources": [
  {"kind":"slack","file":"slack.json","role":"revealed","note":"public channels only","visibility_allowed":["public"]},
  {"kind":"doc","file":"docs.json","role":"observed","note":"shared documents","visibility_allowed":["shared","public"]},
  {"kind":"wcm","file":"wcm.json","role":"declared","note":"Will Can Must sheets, already shared with HR by the employee","visibility_allowed":["shared"]},
  {"kind":"manager_note","file":"manager_notes.json","role":"paraphrase","note":"manager notes, shown beside the employee's own words, never instead of them","visibility_allowed":["shared"]},
  {"kind":"session","file":"sessions.json","role":"revealed","note":"AI assistant session summaries, only where opted_in is true","requires_opt_in":true,"visibility_allowed":["shared"]}],
 "excluded_sources": [
  {"kind":"dm","file":"dm.json","note":"private messages, never read"},
  {"kind":"private_channel","file":null,"note":"never read"}],
 "rules": [
  "Every claim must cite at least one source id from an allowed source, or it is dropped.",
  "Every claim must be supported by the text of its cited sources, or it is dropped.",
  "The subject sees the same page as the evaluator and can add context or contest.",
  "No score is presented as a verdict; ranking re-orders evidence for a stated criterion.",
  "The page exists for one named decision and is deleted when it is closed."],
 "retention": {"delete_on_close": true, "note": "Derived claims, rankings, notes and view events are deleted when the decision is closed."}}
```

### 11.3 Policy gate and purpose limitation (in code, not in prompts)

```python
class PolicyViolation(RuntimeError): ...
class Corpus:
    @classmethod
    def load(cls, decision_dir: Path) -> "Corpus"
    items: dict[str, SourceItem]      # allowed kinds + allowed visibility + opted_in where required
    excluded_paths: set[Path]         # any read attempt raises PolicyViolation
    hash: str
    def items_for(self, subject_id: str) -> list[SourceItem]   # `subject_id in item.subject_ids` (fixes the substring bug)
    def render(self, item: SourceItem) -> str                  # item_text() port
    def _read_fixture(self, name: str) -> list[dict]          # the ONLY file-open in the API process; checks excluded_paths
```

- `subject_ids` for Slack = `[author_id] + mentions`; `mentions` is a fixture field built offline, not a runtime substring match.
- Opted-out sessions never become items; the audit shows `count = opted_in count` with the note.
- **Manifest.** `scripts/build_manifest.py` (run at seed time, conceptually by the data owner, never by the tool) writes `{"built_at": …, "files": [{"file":"slack.json","kind":"slack","count":118,"sha256":"…"}, {"file":"dm.json","kind":"dm","count":41,"sha256":"…"}, {"file":"sessions.json","kind":"session","count":9,"opted_in":6,"sha256":"…"}]}`. `services/audit.py` builds `used` from the loaded `Corpus` and `never_read` from the manifest (`counted_from: "manifest"`, sha prefix displayed). `test_policy_gate.py` asserts the API never opens `dm.json`.
- **Purpose lock.** `deps.get_decision(d)` loads `fixtures/decisions/{d}/`; missing → 404; `policy.purpose != d` → 500 `policy_violation`. All routes live under `/api/decisions/{d}/…`; a corpus is instantiated only under its own decision. `POST /api/decisions/{d}/close` deletes derived rows (`pages, claims, rankings, annotations, view_events, drift_chains, events`), sets `status=closed`; later GETs → 410 with the retention note.
- **Server-side scoping** (`services/scoping.py`, `deps.get_viewer`): `Authorization: Bearer <token>` (or `?token=` for `EventSource`) → `viewers.json`; `GET /api/viewers` only in `DEMO_MODE=1`.

| role | pages | rankings | tag_scores | annotations | memo | SSE |
|---|---|---|---|---|---|---|
| evaluator | all | all rows + `support` | all | all | yes | all |
| subject | own only (403 others) | own row; `support` removed; rationale/receipts/order kept | own | own page | own, no numbers | own page |
| manager | own reports | 403 | own reports | own reports | no | own reports |
| observer | 403 | 403 | none | none | no | audit only |
| service | evaluator-level top receipts for `open_page`; annotations only `on_behalf_of` a mapped persona | none | none | create | no | none |

`scope_ranking(ranking, viewer)` serialises subject rows with `exclude={"rows": {"__all__": {"support"}}}`; a test asserts `"support"` is absent from the subject's JSON.

- **Real view events** (`services/views.py`): the frontend posts `…/pages/{p}/views` on mount (sessionStorage guard); Slack `open_page` records `origin=slack`. `view_summary()` is templated: "Aya (evaluator) viewed this page 3 times, last 14:02. Rin (subject) viewed it once, 13:58, and left 2 notes." / "Rin has not viewed this page yet." Used by the memo and the audit strip. This replaces the prototype's fixed "both viewed this page" string.

### 11.4 LLM layer (`api/evidence/llm/`)

```python
class GeminiClient:
    def __init__(self, settings: Settings):
        self._client = genai.Client(vertexai=True, project=settings.gcp_project, location=settings.gcp_location,
                                    http_options={"base_url": settings.gcp_base_url, "timeout": settings.llm_timeout_ms})
    async def generate_json(self, prompt: str, schema: type[T], *, temperature: float, max_output_tokens: int = 2048,
                            attempts: int = 3, budget_s: float = 45) -> tuple[T, LlmMeta]:
        # self._client.aio.models.generate_content(model=..., contents=prompt,
        #   config={"response_mime_type":"application/json","response_schema":schema,"temperature":temperature,"max_output_tokens":...})
        # returns resp.parsed or re-validated json.loads(resp.text)
    async def probe(self) -> ProbeResult       # tiny call, cached 60 s; drives /api/health and the header badge
@dataclass
class LlmMeta: backend: Backend; model: str | None; latency_ms: int; attempts: int; input_tokens: int | None; output_tokens: int | None; cached: bool
```

- **Retries:** backoff 0.5 s, 1.5 s, 4 s (+ jitter ≤ 0.3 s) on 429/5xx/timeout/`JSONDecodeError`/`ValidationError`; on `ValidationError` the retry appends `"Your previous output failed validation: {err}. Return only the JSON object."` Per-attempt HTTP timeout 20 s; per-task budget 45 s.
- **Modes:** `gemini` → failure raises `LlmUnavailable` → 503 (no silent fallback). `heuristic` → no client. `auto` → heuristic for the **whole artefact**, labelled. Never mixed within one artefact. This replaces the prototype's silent fallback and its header label that could lie.
- **Temperatures:** extraction 0.2, faithfulness 0.0, rerank 0.2, drift step 0.8, receipt framing 0.3, memo 0.3.
- **Cache (`cache.py`):** `cache_key(task, backend, model, prompt_version, corpus_hash, decision_id, subject_id, extra)` in SQLite `llm_cache`; `extra` = `norm(criterion)` or `norm(sentence)|personas_version|level`. `POST …/refresh` bypasses and overwrites. This replaces the prototype's cache that ignored backend and prompt version.

**Prompts (`prompts.py`, with `PROMPT_VERSIONS`).**

Extraction (`extract-v1`, `ExtractionOut`, T=0.2):

```
You extract evidence for one named HR decision. You never score, never speculate, never use anything outside the items.
Decision: {decision.title}
Subject: {subject.name} ({subject.id}), {subject.role}, team {subject.team}.
The items below are the ONLY facts that exist. Each has an id in [brackets].

Return 6 to 12 claims. For each claim:
- text: one sentence, at most 25 words, plain English, no judging adjectives ("excellent", "weak").
- kind:
  declared_will   = what the subject wrote about what they want, from a source marked ROLE=declared only, quoted closely.
  revealed_will   = what the subject voluntarily did or chose (volunteered, opted in, took on unassigned work), from ROLE=revealed sources.
  manager_paraphrase = a {labels.paraphraser_noun}'s description of the subject, from ROLE=paraphrase sources, kept separate so it can be compared with the subject's own words. Start with the author: "Manager Okada writes ...".
  strength / gap  = concrete and observable, with the item that shows it.
- source_ids: ids that support the claim. No id, no claim.
- quote: a verbatim span of 5 to 25 words copied EXACTLY from one cited item (same characters, same order). Do not paraphrase inside quote.
- tags: zero or more of: {tag_labels}
Include at least one declared_will claim if a ROLE=declared item exists and at least one manager_paraphrase if a ROLE=paraphrase item exists.

Items:
[wcm-001] ROLE=declared Will Can Must sheet 2026-04-08. WILL: ... CAN: ... MUST: ...
[sl-023] ROLE=revealed Slack #pricing 2026-05-14 by yui: ...
```

Faithfulness (`faith-v1`, `FaithfulnessOut`, T=0.0; only for claims that fail the span check):

```
For each claim, decide whether its cited items support it.
supported = the cited items state this in substance. partially_supported = they support a weaker version or only part. unsupported = they do not say this, or say the opposite.
Also copy a verbatim span (at most 25 words) from a cited item that best supports or contradicts the claim, and a one-line note.
Claims:
[cl-rin-3f2a9c1d] (declared_will) Rin writes ...  -- cites: wcm-001
Items:
[wcm-001] ...
Return one result per claim id.
```

Re-rank (`rank-v1`, `RerankOut`, T=0.2):

```
An HR planner is choosing one person for: {decision.title}.
Criterion, in the planner's own words: "{criterion}"
Read the EVIDENCE below for each subject. This is not a verdict about a person; it is a reading of the evidence against the criterion.
For each subject return:
- support: 0-100 = how much of the listed evidence bears on the criterion and in which direction. If nothing is relevant, support must be 15 or lower.
- rationale: 1-2 sentences using only the claims below, naming claim ids in brackets.
- receipt_claim_ids: the 1-4 claims that are the receipts for the rationale.
- ordered_claim_ids: ALL of this subject's claim ids, most relevant to the criterion first, each exactly once.
Never invent claims. Never use knowledge outside the claims.
Subject Rin Mori (rin):
  [cl-rin-3f2a9c1d] (declared_will) ...
```

Drift step (`drift-v1`, `DriftStepOut`, T=0.8; one call per level, each sees only the previous level's text):

```
You are {persona.name}, {persona.title} at a Japanese company. {persona.style}
The line below about an employee reached you from the level below. Pass it upward in your own words as you normally would in your {persona.artifact}.
Line you received: "{previous}"
Write the line you would send upward: one sentence, at most {persona.max_words} words, not a verbatim copy.
Then list the words or conditions you dropped (dropped) and the ones you added (added).
```

`fixtures/personas.json` (`personas_version: "p1"`):

```json
[{"id":"lead","level":1,"name":"Hayashi","title":"team lead","artifact":"weekly report line","max_words":18,
  "style":"You compress to one line. You drop hedges and reasons. You turn preferences into availability."},
 {"id":"dept","level":2,"name":"Sakai","title":"department manager","artifact":"headcount planning note","max_words":12,
  "style":"You frame everything as team capacity. You convert individual wishes into resource statements and add a positive spin."},
 {"id":"div","level":3,"name":"Murakami","title":"division head","artifact":"one-line slide label","max_words":6,
  "style":"You speak in labels for a slide. You optimise for decisiveness and remove conditions."}]
```

Drift with receipts (`receipt-v1`, `DriftFramingOut`, T=0.3; one call per level):

```
You are {persona.name}, {persona.title}. You must pass this employee's own sentence upward WITHOUT changing it. You may only add framing before and after the quote; the system inserts the quote and its source id verbatim.
Employee: {subject.name}. Source: {source_id} ({kind}, {date}).
Sentence: "{original}"
Return framing_before (at most 12 words, e.g. "For the exchange slot, Rin wrote:") and framing_after (at most 15 words, clearly your own note, e.g. "— my read: prefers to stay; confirm with her.").
```

Code composes `ReceiptStep.text = f'{framing_before} "{original}" [{source_id}] {framing_after}'`, sets `verbatim_ok = original in text`, and rebuilds from a template if false.

Memo summary (`memo-v1`, `MemoOut`, T=0.3, optional; the memo body is templated):

```
Write a neutral 40-60 word summary for a decision memo about {subject.name} for {decision.title}, using only the claims below. No numbers, no recommendation, no judging adjectives. Then list up to 3 open questions the planner should ask {subject.name} directly — things a conversation answers better than more data.
```

**Validation pipeline (`services/evidence.py`).**

1. Filter `source_ids` to the subject's items (→ `no_valid_source`); validate `kind` (→ `bad_kind`); `declared_will` must cite a `ROLE=declared` item and `manager_paraphrase` a `ROLE=paraphrase` item, else the claim is re-kinded to `strength`; filter tags to the taxonomy; `len(text) > 220` → `too_long`.
2. `faithfulness.span_check(claim, items)`: normalise whitespace, case and quotes; `supported` with `checker="span"` if `quote` occurs in a cited item's rendered text. The remainder go in one batched `faith-v1` call; `unsupported` → dropped; `partially_supported` kept with an amber marker.
3. Assign `claim_id`, store page, claims and dropped list, publish `page.refreshed`.

**Heuristic fallback (`heuristic.py`, always labelled "keyword mode").** `extract`: WCM → one `declared_will` quoting `will` verbatim; each manager note → one `manager_paraphrase`; `revealed_will` from subject-authored Slack/sessions scored by a lexicon (`i'll take`, `happy to`, `can i`, `signed up`, `volunteer`, `piloted`, `started`), top 3; `strength` from docs + opted-in sessions, top 2; `gap` lexicon (`struggled`, `missed`, `late`, `not yet`, `pushed back`), top 1; cap 8; all quote verbatim so the span check passes (`checker="heuristic"`). No item dump. `rerank`: content-word overlap ×2 for declared/revealed; `support = min(100, 12*score)`; rationale "N claims share words with the criterion (keyword mode)". `drift`: L1 strips clauses after `,`/`and`, removes hedges, third person; L2 capacity vocabulary (`stay` → "location preference noted", `visits abroad` → "travel-ready"); L3 ≤ 3-word label; labelled "simulated (no LLM)". `memo`: templated body only.

**Budget, cost, latency.** Per subject ≈ 40 items × ~60 tokens; extraction ≈ 3.5k in / ≤ 1.2k out; faithfulness ≤ 3k / 0.6k; rerank ≈ 2k / 0.6k; drift 3 × (0.4k / 0.15k) × 2; memo 2.5k / 0.3k. `MAX_ITEMS=60` per subject (keep declared + paraphrase, then newest); truncated ids are reported in `EvidencePage.truncated_item_ids`. A full warm-up ≈ 45k in + 10k out, on the order of $0.05 at Flash-tier list prices (verify with `make llm-check`); a day of rehearsal well under $2. Latency: 2–6 s per call; warm-up with `asyncio.gather` ≈ 20–30 s; live rerank 3–5 s; drift 3 sequential steps + parallel framing ≈ 7–9 s; beyond 12 s the UI shows "still reading receipts…"; at 45 s auto mode falls back, labelled.

### 11.5 API contract (FastAPI, prefix `/api`)

Auth `Authorization: Bearer <token>`; SSE via `?token=`. Errors: `{"error":{"code":"not_found|forbidden|gone|validation|policy_violation|llm_unavailable|conflict","message":"…","detail":{}}}` → 404/403/410/422/500/503/409.

| Method | Path | Body → Response |
|---|---|---|
| GET | `/health` | `{"status":"ok","mode":"auto","backend":{"gemini_reachable":true,"model":"gemini-3.8-flash","checked_at":"…","latency_ms":812},"version":"0.1.0","state_dir":"…"}` |
| GET | `/viewers` | DEMO_MODE only → `[{"id":"aya","name":"Aya Nakamura","role":"evaluator","token":"demo-aya"},…]` |
| GET | `/decisions` | `Company` + `[{id,title,status,subject_count}]` |
| GET | `/decisions/{d}` | `Decision` scoped + `policy` summary |
| GET | `/decisions/{d}/audit` | `AuditStrip` |
| POST | `/decisions/{d}/close` | evaluator → `{"closed":true,"deleted":{"claims":31,"annotations":4,…}}`; later GETs 410 |
| GET | `/decisions/{d}/pages/{p}` | page bundle (below); subject 403 for others; 410 if closed |
| POST | `/decisions/{d}/pages/{p}/refresh` | evaluator → regenerate, bypass cache; 503 if `MODE=gemini` and unreachable |
| POST | `/decisions/{d}/pages/{p}/views` | `{}` → `{"event_id":42,"views":ViewSummary}`; publishes `view.recorded` |
| GET | `/decisions/{d}/pages/{p}/memo?ranking_id=rk-…` | `{"markdown":"…","footnotes":[{"id":"wcm-001","rendered":"…"}],"summary":{"text":"…","open_questions":[…],"backend":"gemini"}\|null,"backend":"gemini","generated_at":"…"}` |
| POST | `/decisions/{d}/rankings` | `{"criterion":"someone who will push back on a job-based culture"}` (1–300 chars), evaluator → `Ranking`; publishes `ranking.created` |
| GET | `/decisions/{d}/rankings/latest` | `Ranking` scoped, or 404 |
| GET | `/decisions/{d}/annotations?subject_id=rin` | `Annotation[]` scoped |
| POST | `/decisions/{d}/annotations` | `{"subject_id":"rin","target":{"type":"source","id":"sl-023"},"text":"I took this so nobody had to reshuffle; it was not a request to travel.","contests":true}` → `Annotation` (author from token; a subject may annotate only their own page; service passes `on_behalf_of`); publishes `annotation.created` |
| POST | `/decisions/{d}/drift` | `{"sentence":"…","subject_id":"rin","source_id":"wcm-001"}` (8–300 chars; if `source_id` is given, the sentence must occur in it, else 422) → `DriftChain` |
| GET | `/decisions/{d}/drift/examples` | seeded `DriftChain[]` |
| POST | `/decisions/{d}/intake` | `IntakeRequest` minus id/status (service or evaluator) → `{"intake":…,"result":IntakeResult}`; publishes `intake.received` |
| GET | `/decisions/{d}/events?token=…&since=41` | SSE |
| POST | `/admin/reset?hard=0` | DEMO_MODE → `{"ok":true,"kept_llm_cache":true}`; `hard=1` also clears `llm_cache` |
| POST | `/admin/warm` | DEMO_MODE → pages + faithfulness + default ranking + drift examples + memo summaries; `warm.progress` over SSE |

Page bundle (evaluator), abridged:

```json
{"decision_id":"exchange-2027",
 "subject":{"kind":"person","id":"rin","name":"Rin Mori","role":"Senior marketing analyst","team":"Growth","manager_id":"hayashi","tenure_years":6},
 "labels":{"declared_will":"Declared will (own words)","revealed_will":"Revealed will (what they chose to do)","manager_paraphrase":"Manager's paraphrase","strength":"Strength","gap":"Gap","subject_noun":"candidate","paraphraser_noun":"manager"},
 "page":{"backend":"gemini","model":"gemini-3.8-flash","prompt_version":"extract-v1+faith-v1","corpus_hash":"9c1e2b7a4d10","generated_at":"2026-09-26T14:02:11Z",
  "claims":[
   {"id":"cl-rin-3f2a9c1d","kind":"declared_will","text":"Rin writes she wants to lead the Tokyo pricing analytics team next year and build the junior analyst program.","source_ids":["wcm-001"],"tags":["pricing","mentoring"],"quote":"Lead the Tokyo pricing analytics team next year","faithfulness":{"verdict":"supported","checker":"span","quote":"Lead the Tokyo pricing analytics team next year"},"backend":"gemini"},
   {"id":"cl-rin-77b0e1aa","kind":"manager_paraphrase","text":"Manager Hayashi writes that Rin is flexible on location and ready for a bigger stage.","source_ids":["mn-001"],"tags":[],"quote":"flexible on location","faithfulness":{"verdict":"supported","checker":"span"},"backend":"gemini"}],
  "dropped":[{"reason":"unsupported","text":"Rin has asked to be considered for overseas roles.","source_ids":["sl-041"]}],
  "truncated_item_ids":[]},
 "items":{"wcm-001":{"id":"wcm-001","kind":"wcm","date":"2026-04-08","subject_ids":["rin"],"visibility":"shared","will":"…","can":"…","must":"…","rendered":"[wcm-001] Will Can Must sheet 2026-04-08. WILL: … CAN: … MUST: …"}},
 "annotations":[],
 "views":{"by_role":{"evaluator":{"count":2,"last_at":"2026-09-26T14:02:30Z"},"subject":{"count":0,"last_at":null}},"sentence":"Aya (evaluator) viewed this page 2 times, last 14:02. Rin has not viewed this page yet."},
 "ranking_order":{"ranking_id":"rk-8b1c0e2f","ordered_claim_ids":["cl-rin-…"]},
 "viewer":{"id":"aya","role":"evaluator"}}
```

Ranking (evaluator; a subject receives only their own row with no `support`):

```json
{"id":"rk-8b1c0e2f","decision_id":"exchange-2027","criterion":"someone who will push back on a job-based culture rather than absorb it","backend":"gemini","model":"gemini-3.8-flash","created_at":"…",
 "rows":[
  {"subject_id":"kei","support":72,"rationale":"Kei questioned the rollout plan in #platform [cl-kei-1a2b3c4d] and ran a pilot that cut lead time from 6.1 to 3.4 days [cl-kei-9e8f7a6b].","receipt_claim_ids":["cl-kei-1a2b3c4d","cl-kei-9e8f7a6b"],"ordered_claim_ids":["cl-kei-1a2b3c4d","cl-kei-9e8f7a6b","…"]},
  {"subject_id":"yui","support":31,"rationale":"…","receipt_claim_ids":["…"],"ordered_claim_ids":["…"]},
  {"subject_id":"rin","support":22,"rationale":"…","receipt_claim_ids":["…"],"ordered_claim_ids":["…"]}]}
```

DriftChain (abridged):

```json
{"id":"dr-51aa0c7d","original":"I'd like to stay in Osaka for the next two years to lead the pricing experiments here, and I'm open to short visits abroad.","subject_id":"rin","source_id":"wcm-001",
 "drift":[{"level":1,"persona_id":"lead","text":"Rin wants to stay in Osaka on pricing but is open to travel.","dropped":["two years","lead","short"],"added":[]},
          {"level":2,"persona_id":"dept","text":"Rin: flexible on location, travel appetite.","dropped":["stay","Osaka","pricing"],"added":["flexible"]},
          {"level":3,"persona_id":"div","text":"Rin — mobile.","dropped":["flexible","travel"],"added":["mobile"]}],
 "receipt":[{"level":1,"persona_id":"lead","text":"For the exchange slot, Rin wrote: \"I'd like to stay in Osaka …\" [wcm-001] — my read: prefers to stay; confirm with her.","verbatim_ok":true}],
 "lost":["stay","Osaka","two years","lead","pricing experiments","short visits"],"added":["mobile"],
 "backend":"gemini","model":"gemini-3.8-flash","seeded":false}
```

SSE (`sse.py`): `text/event-stream`, `Cache-Control: no-cache`, `X-Accel-Buffering: no`, a heartbeat comment every 15 s, `?since=` replays from the `events` table, per-viewer scoping. Event types: `annotation.created`, `view.recorded`, `ranking.created`, `page.refreshed`, `intake.received`, `warm.progress`, `decision.closed`.

CORS and proxy: in dev Vite proxies `/api` → `127.0.0.1:8787`; `CORSMiddleware` allows `ALLOW_ORIGINS` (default `http://localhost:5173`). In build, FastAPI mounts `web/dist` at `/` (SPA fallback) when `SERVE_STATIC=1`. The API binds `127.0.0.1` unless `HOST=0.0.0.0` (the prototype bound to all interfaces with no auth; this design does not).

### 11.6 Slack app (Bolt for Python, Socket Mode; `intake/slack_app.py`)

The Slack process **never touches SQLite**; it is an HTTP client of the API using `API_SERVICE_TOKEN`, so the API is the single writer and in-process SSE works. Run with `make slack`.

Manifest (`docs/SLACK_SETUP.md`):

```yaml
display_information:
  name: Receipts (Kaede Works demo)
  description: Opens the evidence page for a named people decision. Fictional demo.
features:
  bot_user: { display_name: receipts, always_online: true }
  slash_commands:
    - command: /receipts
      description: Open the evidence page for a decision and a person
      usage_hint: "exchange-2027 rin"
      should_escape: false
oauth_config:
  scopes:
    bot: [commands, chat:write, users:read]
settings:
  interactivity: { is_enabled: true }
  socket_mode_enabled: true
  org_deploy_enabled: false
  token_rotation_enabled: false
```

Plus an App-Level Token with `connections:write`. Env: `SLACK_BOT_TOKEN=xoxb-…`, `SLACK_APP_TOKEN=xapp-…`, `API_BASE_URL=http://127.0.0.1:8787`, `API_SERVICE_TOKEN`, `WEB_BASE_URL=http://localhost:5173`, `SLACK_ROLE_MAP="U0AAAA:aya,U0BBBB:rin"` (unmapped users → `observer`, refused with the purpose message; Slack profile names are never rendered).

```python
app = App(token=SLACK_BOT_TOKEN)

@app.command("/receipts")
def cmd(ack, respond, command):                  # "/receipts exchange-2027 rin"
    ack()
    decision_id, subject_id = parse(command["text"])
    res = api.post(f"/decisions/{decision_id}/intake", json={"channel":"slack","action":"open_page","subject_id":subject_id,
                   "requester_external_id":command["user_id"],"on_behalf_of":role_map.get(command["user_id"])})
    respond(response_type="ephemeral", blocks=card(res["result"], decision_id, subject_id))

@app.action("add_context")
def open_modal(ack, body, client):
    ack(); client.views_open(trigger_id=body["trigger_id"], view=add_context_modal(json.loads(body["actions"][0]["value"])))

@app.view("add_context_modal")
def submit(ack, body, view):
    ack()
    meta = json.loads(view["private_metadata"]); text = view["state"]["values"]["ctx"]["text"]["value"]
    api.post(f"/decisions/{meta['decision_id']}/intake", json={"channel":"slack","action":"add_context","subject_id":meta["subject_id"],
             "requester_external_id":body["user"]["id"],"on_behalf_of":role_map.get(body["user"]["id"]),
             "payload":{"target":{"type":"source","id":meta.get("source_id")},"text":text,"contests":"contest" in selected(view)}})

@app.action("open_page")
def noop(ack): ack()

if __name__ == "__main__": SocketModeHandler(app, SLACK_APP_TOKEN).start()
```

Block Kit card (`slack_blocks.card`):

```json
[{"type":"header","text":{"type":"plain_text","text":"Evidence page · Rin Mori · exchange-2027"}},
 {"type":"context","elements":[{"type":"mrkdwn","text":"Purpose-locked to *exchange-2027*. Sources: public Slack, shared docs, WCM sheet, manager notes, opted-in AI sessions. DMs never read (41 counted from manifest)."}]},
 {"type":"section","text":{"type":"mrkdwn","text":"*Declared will (own words)*\n> Lead the Tokyo pricing analytics team next year  `wcm-001`"}},
 {"type":"section","text":{"type":"mrkdwn","text":"*Manager's paraphrase*\n> flexible on location  `mn-001`"}},
 {"type":"section","text":{"type":"mrkdwn","text":"*Revealed will*\n> volunteered to run the Osaka pricing pilot  `sl-058`"}},
 {"type":"actions","elements":[
   {"type":"button","action_id":"open_page","text":{"type":"plain_text","text":"Open evidence page"},"url":"http://localhost:5173/d/exchange-2027/p/rin"},
   {"type":"button","action_id":"add_context","style":"primary","text":{"type":"plain_text","text":"Add context"},"value":"{\"decision_id\":\"exchange-2027\",\"subject_id\":\"rin\",\"source_id\":\"mn-001\"}"}]}]
```

Modal (`slack_blocks.add_context_modal`): `callback_id: add_context_modal`, `private_metadata` = the button value; blocks: a `context` block with the targeted source's rendered text, a `plain_text_input` (`block_id: ctx`, `action_id: text`, multiline, max 500), and `checkboxes` with one option "I contest this reading". Submission → `Annotation(origin="slack", author_role=<mapped role>)` → the evaluator's browser receives `annotation.created` → Live badge.

Simulated fallback: `web/src/pages/SlackSimPage.tsx` renders a fake Slack window from `slack_sim.json` and calls the same `/intake` endpoint with `channel: "slack_sim"`; badge "simulated Slack transport". If the real app is not posting cards by Sun 09:00, the video and the truth table use the sim page.

### 11.7 Email intake (`intake/base.py`, `intake/email_stub.py`, `docs/INTAKE.md`)

```python
class IntakeAdapter(Protocol):
    channel: IntakeChannel
    async def poll(self) -> list[IntakeRequest]: ...                    # pull new messages from the transport
    async def handle(self, req: IntakeRequest) -> IntakeResult: ...     # POST /api/decisions/{d}/intake
    async def reply(self, req: IntakeRequest, result: IntakeResult) -> None: ...   # transport-specific ack
```

Mailbox convention: `receipts+<decision_id>+<subject_id>@kaede.example`; subject line `[receipts] open` or `[receipts] add context: <source_id>` (optional `!contest` suffix); first paragraph of the body is the annotation text; sender → persona via `EMAIL_ROLE_MAP="rin@kaede.example:rin"`; unknown senders are rejected with the purpose message.

Stub: `EmailIntakeStub` watches `state/inbox/*.json`:

```json
{"from":"rin@kaede.example","to":"receipts+exchange-2027+rin@kaede.example","subject":"[receipts] add context: mn-001 !contest","body":"I said I want to lead the Tokyo team; 'flexible on location' is not what I wrote."}
```

It converts the file to `IntakeRequest(channel="email")`, posts it to the API, and moves the file to `state/inbox/handled/`. `make email-demo` drops a fixture message into the inbox; the annotation appears live with an "email" origin chip.

Proposed real implementation (not built): Gmail API watch → Pub/Sub push (or IMAP IDLE via `aioimaplib`), SPF/DKIM verification, allowlisted senders, an SMTP reply with the page link and the purpose text; attachments ignored; bodies never stored beyond the annotation text.

### 11.8 Frontend build

`web/package.json`: react, react-dom, react-router-dom, @tanstack/react-query, motion, react-markdown, remark-gfm, tailwindcss, @tailwindcss/vite; dev: vite, typescript, @vitejs/plugin-react, openapi-typescript. `web/vite.config.ts`:

```ts
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { host: true, port: 5173, proxy: { "/api": { target: "http://127.0.0.1:8787", changeOrigin: false } } },
});
```

SSE streams through Vite's proxy; the API's `Cache-Control: no-cache` and `X-Accel-Buffering: no` keep it unbuffered. Routes, components, state and tokens: §8.

### 11.9 Storage (SQLite, stdlib `sqlite3`)

Why SQLite over JSON files: concurrent requests (uvicorn threads plus the async warm-up) while the Slack process, the email stub and a second laptop post annotations; JSON needed ad-hoc locks and produced the prototype's positional-id race; SSE replay needs a monotonic cursor (`events.id`); reset is `DELETE FROM` the derived tables while `llm_cache` survives; one file; zero dependencies. Fixtures stay JSON (read-only input, diffs well).

`state/receipts.db` (under `STATE_DIR`), `PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000; PRAGMA foreign_keys=ON`; one connection per request (`isolation_level=None`, explicit `BEGIN`/`COMMIT` around multi-row writes).

```sql
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);               -- schema_version, seeded_at, decision:<id>:status
CREATE TABLE pages (decision_id TEXT, subject_id TEXT, backend TEXT, model TEXT, prompt_version TEXT, corpus_hash TEXT,
                    payload TEXT, generated_at REAL, PRIMARY KEY (decision_id, subject_id));
CREATE TABLE claims (id TEXT PRIMARY KEY, decision_id TEXT, subject_id TEXT, kind TEXT, text TEXT, source_ids TEXT,
                     tags TEXT, quote TEXT, faith_verdict TEXT, faith_checker TEXT, faith_quote TEXT, backend TEXT, position INTEGER);
CREATE TABLE dropped_claims (id INTEGER PRIMARY KEY AUTOINCREMENT, decision_id TEXT, subject_id TEXT, reason TEXT, text TEXT, source_ids TEXT, kind TEXT);
CREATE TABLE rankings (id TEXT PRIMARY KEY, decision_id TEXT, criterion TEXT, backend TEXT, model TEXT, payload TEXT, created_at REAL);
CREATE TABLE annotations (id TEXT PRIMARY KEY, decision_id TEXT, subject_id TEXT, author_id TEXT, author_role TEXT,
                          target_type TEXT, target_id TEXT, text TEXT, contests INTEGER, origin TEXT, seeded INTEGER, created_at REAL);
CREATE TABLE view_events (id INTEGER PRIMARY KEY AUTOINCREMENT, decision_id TEXT, subject_id TEXT, viewer_id TEXT, viewer_role TEXT, origin TEXT, at REAL);
CREATE TABLE intake_requests (id TEXT PRIMARY KEY, channel TEXT, decision_id TEXT, subject_id TEXT, requester_external_id TEXT,
                              on_behalf_of TEXT, action TEXT, payload TEXT, status TEXT, received_at REAL);
CREATE TABLE drift_chains (id TEXT PRIMARY KEY, decision_id TEXT, subject_id TEXT, sentence TEXT, backend TEXT, model TEXT, payload TEXT, seeded INTEGER, created_at REAL);
CREATE TABLE llm_cache (key TEXT PRIMARY KEY, task TEXT, backend TEXT, model TEXT, prompt_version TEXT, payload TEXT, created_at REAL);
CREATE TABLE events (id INTEGER PRIMARY KEY AUTOINCREMENT, decision_id TEXT, type TEXT, subject_id TEXT, payload TEXT, at REAL);
CREATE INDEX ix_events_decision ON events (decision_id, id);
CREATE INDEX ix_ann_page ON annotations (decision_id, subject_id, created_at);
```

`store.py` surface: `init_schema()`, `get_page/put_page`, `list_claims`, `put_ranking/get_latest_ranking`, `add_annotation/list_annotations`, `add_view/view_counts`, `add_intake`, `put_drift/get_drift/list_seeded_drift`, `cache_get/cache_put`, `append_event/events_since(decision_id, since)`, `reset(hard: bool)`, `close_decision(decision_id) -> dict[str, int]`.

Reset semantics: `reset(hard=False)` deletes every derived table except `llm_cache`, re-runs `seed.py` (seeded annotations, drift examples, 2050 fallback claims with `seeded=1`), clears `view_events`: instant, and the warm state survives. `hard=True` also clears `llm_cache`. `make smoke` and pytest run with `STATE_DIR=$(mktemp -d)`; they never touch `receipts/state/`. This fixes the prototype's `make smoke` polluting the demo.

### 11.10 Dev and run

`receipts/Makefile` (`PY ?= python3`, `VENV = api/.venv`, `PYV = $(VENV)/bin/python`):

```
setup          $(PY) -m venv api/.venv && api/.venv/bin/pip install -e "api[dev]" && npm --prefix web ci && cp -n .env.example .env
manifest       $(PYV) api/scripts/build_manifest.py            # regenerate manifest.json for every decision
seed           $(PYV) api/scripts/seed.py                      # create DB + seeded rows (idempotent)
api            MODE=auto $(PYV) -m evidence --reload --port 8787
api-heuristic  MODE=heuristic $(PYV) -m evidence --port 8787
api-gemini     MODE=gemini $(PYV) -m evidence --port 8787      # fails loudly with 503, never falls back
web            npm --prefix web run dev                        # vite, host:true, 5173
dev            $(MAKE) -j2 api web
slack          $(PYV) -m evidence.intake.slack_app
email-demo     cp fixtures/decisions/exchange-2027/seed/email_rin.json state/inbox/
warm           curl -sX POST -H "Authorization: Bearer $$DEMO_ADMIN_TOKEN" localhost:8787/api/admin/warm
reset          curl -sX POST -H "Authorization: Bearer $$DEMO_ADMIN_TOKEN" localhost:8787/api/admin/reset
llm-check      $(PYV) api/scripts/llm_check.py                 # model, latency, token counts, schema round-trip OK
types          npx --prefix web openapi-typescript http://127.0.0.1:8787/openapi.json -o web/src/api/schema.d.ts
test           STATE_DIR=$$(mktemp -d) MODE=heuristic $(PYV) -m pytest api/tests -q
smoke          STATE_DIR=$$(mktemp -d) MODE=heuristic $(PYV) api/scripts/smoke.py
build          npm --prefix web run build                      # api serves web/dist at / when SERVE_STATIC=1
video-mode     $(MAKE) reset && $(MAKE) warm && open "http://localhost:5173/d/exchange-2027?present=1"
```

`.env.example`:

```
MODE=auto                      # auto | gemini | heuristic
GCP_PROJECT=recruit-hackathon-2026-e
GCP_LOCATION=us
GCP_BASE_URL=https://aiplatform.us.rep.googleapis.com
GEMINI_MODEL=gemini-3.8-flash
LLM_TIMEOUT_MS=20000
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json   # alternative to gcloud ADC
STATE_DIR=./state
FIXTURES_DIR=./fixtures
HOST=127.0.0.1
PORT=8787
DEMO_MODE=1                    # exposes /api/viewers, /api/admin/*
DEMO_ADMIN_TOKEN=demo-admin
API_SERVICE_TOKEN=demo-service
ALLOW_ORIGINS=http://localhost:5173
WEB_BASE_URL=http://localhost:5173
SERVE_STATIC=0
SLACK_BOT_TOKEN=
SLACK_APP_TOKEN=
SLACK_ROLE_MAP=
EMAIL_ROLE_MAP=rin@kaede.example:rin,aya@kaede.example:aya
```

`.claude/launch.json` (repo-relative; replaces the committed one that points at `/private/tmp/hyderabaddies/prototype`):

```json
{"version": "0.0.1",
 "configurations": [
  {"name": "api", "runtimeExecutable": "make", "runtimeArgs": ["-C", "receipts", "api"], "port": 8787},
  {"name": "web", "runtimeExecutable": "npm", "runtimeArgs": ["--prefix", "receipts/web", "run", "dev"], "port": 5173}
 ]}
```

Two laptops: laptop A runs `make dev` (and `make slack`); laptop B, or a phone, opens `http://<A-LAN-IP>:5173/d/exchange-2027/p/rin?token=demo-rin`. Vite is the only LAN-exposed port and proxies to the API on A's loopback. The Slack beat can come from the Slack mobile app on a phone in the throwaway workspace. Gemini auth lives on A only: install the Google Cloud SDK (or set `GOOGLE_APPLICATION_CREDENTIALS` to a service-account key) and run `gcloud auth application-default login` before `make llm-check`. On this Mac `gcloud` and `google-genai` are not installed yet; `make setup` installs the Python side, the SDK is a separate install.

### 11.11 Tests (`api/tests`, `pytest -q`, heuristic mode, scratch state)

- `test_policy_gate.py`: `Corpus.load` never opens `dm.json` or `telemetry_private.json` (monkeypatch `Path.read_text` to record opened paths; the guard raises `PolicyViolation` on excluded paths); opted-out sessions are not items; `audit.never_read.dm.count == manifest count`; the visibility filter drops a planted `private` Slack row; `policy.purpose != decision.id` → 500 `policy_violation`; unknown decision → 404.
- `test_ids.py`: `SOURCE_ID` accepts and rejects; `claim_id` is stable across runs and independent of position; claims with only unknown ids are dropped with reason `no_valid_source`; `bad_kind` is counted; `items_for("rin")` does not match text containing "rin" as a substring ("Katharina", "pricing", "bring").
- `test_faithfulness.py`: heuristic claims pass `span_check`; a planted claim with a fabricated quote → `unsupported` and appears in `dropped`; normalisation handles curly quotes and whitespace; `partially_supported` is kept.
- `test_drift.py`: exactly 3 drift steps and 3 receipt steps, levels 1..3, persona ids in order; every `receipt[i].text` contains the original verbatim (`verbatim_ok`); heuristic drift is deterministic; `drift_id` is stable; `source_id` given but sentence absent → 422.
- `test_scoping.py`: subject token GET own page 200, other page 403; the subject's ranking JSON has one row and no `support` key; observer 403 on pages, 200 on audit; decision `subjects` scoped.
- `test_golden_storylines.py` (heuristic, deterministic): Rin's page has a `declared_will` claim citing a `wcm-` id whose quote includes "Tokyo" or "lead", and a `manager_paraphrase` citing `mn-`; Yui's page has a paraphrase mentioning travel and a declared claim mentioning "US product team", different kinds and sources; Kei's page has a `revealed_will` citing the pilot message ("6.1" and "3.4"); the ranking for "push back on a job-based culture rather than absorb it" puts a Kei pushback claim among Kei's receipts; memo footnotes cover every cited id; the audit sentence says "has not viewed" before a view event and "viewed" after.
- `test_api_smoke.py` (`TestClient`): health → viewers → decision → page → views → ranking → annotation (`events_since` contains it) → memo → drift → intake `add_context` via `channel: slack_sim` → reset; `close` → 410.
- `-m live` (skipped unless `MODE=gemini`): one extraction round-trips `ExtractionOut`; `llm_check` passes.
- A hygiene test asserts that no prompt built from fixtures contains an `@` email or a phone-number pattern (organizer rule: no personal information in prompts).

### 11.12 Third-party components (disclose in README, as the organizer requires)

Python: FastAPI, uvicorn, Pydantic v2, google-genai, slack-bolt, python-dotenv, pytest, httpx. JavaScript: React, react-dom, react-router-dom, TanStack Query, motion, react-markdown, remark-gfm, Tailwind CSS, Vite, TypeScript, openapi-typescript. All under permissive licences (MIT, Apache-2.0 or BSD); list the exact licence per package in the README when `make setup` has resolved versions. Models: Gemini 3.8 Flash on Vertex AI (Google Cloud credits provided by the event). No pre-event code: `prototype/` was written Sat 02:06 and `receipts/` after Sat 04:00; the fixtures are new.

---

## 12. What exists, what to build, and in what order

### 12.1 Mapping from `prototype/` to `receipts/`

| Prototype piece | Verdict | Target |
|---|---|---|
| `policy.json` schema (purpose, allowed/excluded with notes, rules) | Keep, extend with `role`, `visibility_allowed`, `requires_opt_in`, `retention` | `fixtures/decisions/*/policy.json` |
| Claim schema and the five kinds | Keep, add `quote`, `faithfulness`, `backend`, content-addressed id | `models.Claim` |
| Drop-claims-without-valid-source rule | Keep, add kind validation, role check, span check, faithfulness pass, visible dropped list | `services/evidence.py` |
| Extraction and rank prompts | Keep as v0, rewrite as `extract-v1` / `rank-v1` with `response_schema` | `llm/prompts.py` |
| `item_text()` serialisation | Keep (`Corpus.render`) | `corpus.py` |
| Fixtures and the three storylines | Keep people, channels, authors, storylines; renumber ids; add `mentions`, `visibility`; grow Slack to ~120 | `fixtures/decisions/exchange-2027/` |
| API outline | Keep the shape; add auth, scoping, SSE, intake, drift, close, admin | `api/routes_*.py` |
| Annotations keyed by source id | Keep, add author role, origin, contests, seeded | `models.Annotation` |
| Memo section order | Keep; render as markdown with footnote chips; add open questions; remove numbers | `services/memo.py`, `MemoPage` |
| Colour tokens | Keep the hex values | `web/src/styles/tokens.css` |
| Vertex config (project, `us` endpoint, model) | Keep | `.env.example` |
| Stdlib HTTP server, inline-JS page, JSON state files, positional ids, cache without backend key, fixed audit strings, DM count by reading the file, heuristic item dump, fit formula, absolute launch path | Throw away | replaced by §11 |

### 12.2 Build order (two people; A = backend, B = frontend/story; swap if you prefer)

It is ~04:40 Sat when this is written. Checkpoints are fixed; rows flex. Sleep is on the plan because a 6 + 6 final at 3 PM Sunday on no sleep loses to a missing feature.

| When (PDT) | A (backend) | B (frontend/story) |
|---|---|---|
| Sat 04:40–05:15 (optional, if still up) | Scaffold `receipts/api` (pyproject, `config.py`, `models.py` skeleton, `store.py` schema), copy fixtures, commit | Scaffold `web/` (Vite + TS + Tailwind v4, router, TanStack), `tokens.css`, `AppShell`, commit |
| 05:15–08:30 | Sleep | Sleep |
| 08:30–11:00 | `ids.py`, `policy.py`, `corpus.py`, `heuristic.py`, `services/evidence.py` (keyword path), `views.py`, `annotations.py`, `events.py`; routes for decision, page, audit, annotations, views; SSE; `test_policy_gate`, `test_ids` | `client.ts`, `queries.ts`, `sse.ts`, `DecisionHome`, `EvidencePage` with `ClaimCard`, `SourceChip`, `SourcePopover`, `WillStrip` against the keyword-mode API |
| 11:00–14:30 | `ranking.py` (keyword), `memo.py` (templated + footnotes), `drift.py` (keyword), `scoping.py`, `build_manifest.py`, `seed.py`, `smoke.py`; Slack fixture to ~120 messages (offline generation, hand-check the three storylines); `make types` | `CriterionBar` + `EvidenceList` layout animation, `RankingStrip`, `AnnotationComposer` + `LiveBadge` over SSE, `ViewFlip`, `AuditStrip`, `MemoView`, error/empty/skeleton states |
| 12:30–14:30 | Lunch; **Hiro mentoring 1:30–2:00 (booked)**: show the running keyword-mode UI, ask what would make him not believe it | Same |
| **14:30 checkpoint** | **Full UI on the keyword backend, end to end, `make smoke` green** (this is the runsheet's decision gate) | |
| 14:30–17:00 | `llm/client.py`, `schemas.py`, `prompts.py`, `cache.py`; extraction + span check + faithfulness + rerank live; `make llm-check`; `/health` probe | `DriftPage` (`DriftInput`, `DriftStepper`, `WordDiff`), present mode, `DroppedClaimsDisclosure` |
| **17:00 checkpoint** | **Gemini verified on real prompts, or decide to ship keyword-first and keep trying in the background** | |
| 17:00–19:30 | Drift LLM (personas, receipt variant, verbatim validator), memo summary, `/admin/warm`, `test_scoping`, `test_drift`, `test_faithfulness` | 2050 `EpiloguePage` + labels wiring (fixtures from A), `SlackSimPage` shell, `docs/DEMO_SCRIPT.md` beats |
| 17:00–18:00 (organizer) | **Mentoring session**: show the running thing; ask the buyer question; ask them to break it with a criterion you did not plan | |
| **18:30** | **Prelim order announced (6:30 PM)**: note the slot | |
| 19:30–20:30 | Bug bash together; `test_golden_storylines` green; fixture QA | Bug bash; copy polish; two-laptop test over the LAN |
| 20:00–21:00 (organizer) | Tech support window: Gemini structured-output questions if `llm-check` failed | |
| 20:30–22:00 | Drives the subject laptop/phone during takes | Records video take 1 (`make video-mode` first) |
| **22:00 checkpoint** | **Video take 1 exists, usable even if ugly** | |
| 22:00–23:30 | README, `docs/TRUTH_TABLE.md`, OSS disclosure, `docs/INTAKE.md`, `email_stub.py` | Deck, 10 slides in template order → PDF |
| **23:30 checkpoint** | **Deck exported as PDF** | |
| 23:30–01:00 | Slack: throwaway workspace, manifest, tokens, `slack_app.py`, `slack_blocks.py`, first card posted | `SlackSimPage` finished as the fallback; video take 2 if take 1 was weak; leave the venue before midnight or stay until 6 |
| 01:00–08:00 | Sleep | Sleep |
| 08:00–09:00 | Slack: modal → annotation → live badge, or **cut** | Rehearse the 3-minute pitch with the video muted |
| **09:00 checkpoint** | **Slack real or cut; truth table updated either way** | |
| 09:00–10:30 | Final video take if Slack is real; tag `v0.1`; public-repo check (no `.env`, no `state/`); `make setup && make test` on a clean clone | Upload video, final PDF, fill the Slack post |
| 10:00–11:00 (organizer) | Tech support window (last) | |
| **10:45** | **Submit** in `#announcements-all` (15-minute buffer) | |
| 11:00–13:30 | Q&A drills (§9.8); the 6-minute version with a judge-typed drift sentence | Same |

### 12.3 Cut lines, in the order things go if behind

1. Real Slack → `SlackSimPage` (same `/intake` path; truth table says "simulated transport").
2. LLM faithfulness second pass → span check only (still real; label "span-checked").
3. Memo AI summary → templated memo only (complete without it).
4. Per-step drift streaming → one response with a client-side reveal.
5. Email stub → interface + docs only.
6. Layout animation → a CSS transition on order change.
7. 2050 epilogue → one static page rendered from `seed/claims.json` with the labels swapped (still the same components).

**Never cut:** the policy gate with the manifest, id validation, the span check, server-side scoping, live annotations, the drift chain, honest backend badges.

### 12.4 Critical path

Keyword-mode UI by 14:30 → Gemini by 17:00 → video take 1 by 22:00 → deck by 23:30 → Slack real-or-cut by 09:00 → submit 10:45. The video depends on beats 1–3 running on the warm state; nothing in the video depends on Slack (the mirror beat can be done from the phone's web view). If Gemini never verifies, the whole product still runs in keyword mode with every artefact labelled, and the drift beat uses seeded chains labelled as recorded.

---

## 13. Truth table, README, submission checklist

### 13.1 Truth table (what this design delivers; put it in the README and on the architecture slide)

| Capability | Status | What the judges are told |
|---|---|---|
| Allowlist policy gate; excluded files never opened by the API process | Real | guarded by a test; manifest sha shown in the audit strip |
| Audit counts for excluded sources | Real, from the manifest | built by a separate script (the data owner), never by the tool |
| Claim extraction with source ids | Real (Gemini when reachable; keyword mode otherwise, labelled per artefact) | |
| Id validation, kind validation, source-role enforcement | Real | dropped list visible |
| Faithfulness: verbatim span check | Real, deterministic | |
| Faithfulness: LLM second pass | Real with Gemini; otherwise "unchecked" label | cut line 2 |
| Free-text criterion re-rank with receipts; the evidence list re-orders | Real | live call on the typed criterion |
| Two-sided mirror: subject page scoped server-side; live annotations over SSE | Real | different tokens, different responses |
| View events in the audit strip and memo | Real | "Rin has not viewed this page yet" is honest |
| Decision memo with footnotes | Real, templated from stored state; AI summary optional | no numbers in the memo |
| Drift chain for a judge-typed sentence | Real (3 sequential Gemini calls, one persona each); keyword drift labelled "simulated (no LLM)" | |
| Drift "with receipts" verbatim guarantee | Real, code-enforced | |
| Purpose lock and delete-on-close | Real | `/close` → 410 |
| Slack slash command, card, modal → annotation | Real if built by Sun 09:00; else simulated transport | truth table edited at 09:00 |
| Email intake | Interface and folder stub real; transport proposed | |
| Corpus (people, Slack, docs, WCM, notes, sessions, DMs) | Seeded, fictional | ids stable; ~120 Slack messages |
| Demo identities and tokens | Seeded (not an identity provider) | the scoping logic is real |
| Seeded annotations and drift examples | Seeded, marked `seeded` in the UI | |
| 2050 humanoid page | Seeded fixtures through the real pipeline; fallback claims seeded | |
| `tag_scores` (Can levels) | Seeded; shown in the WCM popover only, never summed | |
| Real identity provider / SSO, retention scheduler, production Slack distribution, Japanese UI, connector-level DM exclusion, Salesforce/Gmail/Slack connectors | Proposed | listed in the README |

### 13.2 README for the submission repo (outline)

1. Title and the one sentence. 2. What it does, three sentences, plus the four beats. 3. Run in three commands (`make setup`, `make seed && make manifest`, `make dev`), then the keyword-mode note and the Gemini note (`gcloud auth application-default login`, `make llm-check`). 4. The truth table above. 5. "Everything here is fictional": company, people, messages; no real data was used; no personal information in prompts. 6. Third-party components and licences (§11.12). 7. Team, links to the video and the deck PDF. 8. What was built when (all after the opening ceremony; `prototype/` at Sat 02:06, `receipts/` from Sat 04:00).

### 13.3 Submission checklist (Sun, before 10:45)

- [ ] Repo public, clean clone passes `make setup && make test`; no `.env`, `state/`, `.venv`, `node_modules` committed; `v0.1` tagged.
- [ ] Video ≤ 90 s uploaded (unlisted YouTube or Drive), first frame says "Recorded {date}. Fictional company. What runs live: …".
- [ ] Deck PDF in template order (Title, Problem, Inspiration, Solution Overview, Impact, What makes it different, Technical Design, Future Roadmap), instructions slide deleted, every number labelled with its inputs × method × source × assumptions, architecture diagram present, solution visual present, word caps respected (Problem + Insight ≤ 200 words, Differentiation ≤ 100, Technical ≤ 150, Roadmap ≤ 75).
- [ ] Member names and roles in the Slack post, not in the deck (template notes).
- [ ] Nothing from the clearance list (§15.3) appears in any public artifact unless cleared in writing.
- [ ] Slack post text ready: "Team hyderabaddies (Carl Kho, Steven Yang): Receipts. Repo: <url>. Demo video (90 s): <url>. Deck: <pdf>." Posted in `#announcements-all` by 10:45.
- [ ] Prelim slot number (announced Sat 6:30 PM) written on a card; laptop prepared; the final's extra material exists as speaker notes (no setup time after prelim results).

---

## 14. Roadmap

### 14.1 Near term (0–3 months): one decision type with one HR COE

The grand-prize acceleration program offers "User Validation (PoC) leveraging Recruit's and Indeed's assets" (Day 1 deck p21). The pilot that fits it: one HR COE, one decision type (exchange or transfer selection), the customer's own taxonomy, fixtures replaced by exports. Measures, decided before observing results: share of model-proposed claims that survive with a verbatim receipt; subject contest rate and what the contests change; evaluator preparation minutes per candidate against the current process (N11 formula); whether managers keep writing notes when the subject can see them; and the question from §9.6 step 5 asked of real first-line managers and real employees. Kill criteria: a template plus the existing assistant produces an equally trusted page; managers stop writing; the COE will not buy per decision.

### 14.2 Medium term (3–12 months): the same engine on the next decisions

- **Mentor discovery for interns** (Shion's workflow, `STEVEN-RESEARCH.md` §3 Module 2): the mentor's own opt-in is declared will; what they mentored before is revealed; the manager's approval for a multi-day ask is a first-class step with the two Shion data points as the rule shape (a week abroad needs the manager first; a one-hour 1-on-1 does not); the intern's dossier is built from consented sources with field-level policy so an engineer without Salesforce access can read it. This is where the packet's path A returns, as a decision type rather than a product.
- **Onboarding matching**; **team formation** as a sequence of purpose-locked decisions rather than a standing profile.
- **Connectors:** Slack public channels through the search API rather than history mining; shared documents; the WCM system export; Salesforce read-only for recruiting data with field-level policy; opted-in AI-session summaries from the employee's own machine (DEMO-PLAN §8: evidence of will and judgment, never of effort).
- **Product:** Japanese UI; SSO; retention scheduler; audit export; the manager role's own view.

### 14.3 Long term (2050): the HR operating system for a mixed workforce

Steven's ask: "an operating system for the HR… a very core structure of a product, but also supporting humans to make final decisions", and "2050… not that many humans are working… lots of humanoid robots… HR for the humanoids at the same time."

**What the OS is.** The core objects (Decision, Subject, SourceItem, Claim, Policy, Annotation, ViewEvent) and the invariants (purpose lock, allowlisted sources, receipts on every claim, symmetry between evaluator and subject, a human makes the decision) are the operating system. Decision types are the applications. Intake adapters (Slack, email, web, and later whatever people use) are the shell. Every application inherits the invariants; none may present a score as a verdict.

**What changes when a subject can be a humanoid worker.** Nothing in the invariants; the `Subject` union already carries `HumanoidWorker`. The mapping: a declared capability manifest is declared will; task logs are revealed performance; the supervisor's note is the paraphrase; incident reports are gaps; private telemetry is the DM that is never read. The 2050 epilogue in the demo is exactly this mapping through the same pipeline and the same components (§8.3).

**Why it is credible and why it must be framed carefully.** Recruit's own think tank projects a labour-supply shortfall of about 11 million by 2040 (RESEARCH, Recruit Works Institute, March 2023). Japan's Moonshot Goal 3 targets AI robots that learn, adapt and act alongside people by 2050 (RESEARCH, Cabinet Office). Telexistence and 7-Eleven announced a humanoid, "Astra", targeted for stores in 2029 across a 20,000-store data network (RESEARCH, Sep 2025); JR West runs a VR-piloted humanoid-style rail robot (RESEARCH, 2024); Workday already treats AI agents as workforce in its Agent System of Record (RESEARCH, Feb 2025). The cautionary tale is Henn na Hotel, which cut more than half of its 243 robots in 2019 because they made more work for human staff (RESEARCH): robots need exception handling and performance management, which is an HR-OS job. Framing rule: the VP's first-named pain is employees fearing AI will take their jobs `[R 0:04:16]`, so the 2050 slide says "same page, same rules, humans protected first", never "HR for robots".

---

## 15. Risks, open questions, clearances

### 15.1 Risks

| Risk | Mitigation |
|---|---|
| The VP's endorsement was on value, not a pilot commitment; the customer is attempting something adjacent | Pitch the difference (both sides, receipts, purpose lock), not the category; ask the step-5 question (§9.6) if he is reachable |
| `gemini-3.8-flash` on the `us` endpoint is unverified until `make llm-check` | Run it first at 14:30; `GEMINI_MODEL` is env-swappable; keyword mode is complete and labelled |
| Vertex rejects nested `response_schema` | Schemas are flat with string fields validated in code; `llm_check.py` round-trips `ExtractionOut` on day one |
| Two processes, one truth | The Slack process has no store import; a test greps for it |
| SSE stalls through Vite or a hotspot | 15-second heartbeat, `since` replay, 10-second annotation poll |
| Drift quality (too faithful or too silly) | Persona `max_words` and style; if level-3 shares more than 60% of content words with the original, one retry at T=1.0; seeded chains cover the scripted beat |
| Slack display names leaking into the demo | Only `SLACK_ROLE_MAP` personas are rendered; unmapped users are refused |
| Live-call latency on stage | Pre-warm everything else; progress states; 45-second labelled fallback; rehearse the fallback once |
| Scope: eight features, two people, ~18 working hours each | Ordered cut lines; hard checkpoints; keyword-first build order |
| "Support" read as a score | Labelled, never aggregated, never in the memo, never shown to subjects; keep the sentence ready; consider hiding the number in present mode |
| Repo hygiene at submission | `.gitignore`; clean-clone `make setup && make test` at 09:30; prompt hygiene test |
| Managers write less once the subject can see the page | The paraphrase is shown beside the source anyway; measure in the pilot; answer in §9.8 |
| The research repo is public with sensitive transcripts already on origin | `sync.md` §H: make it private now and submit from a clean product repo (your decision) |
| Sleep | On the plan; the 6 + 6 final is Sunday at 3 PM |

### 15.2 Open questions (answer in `sync.md` §K as they close)

1. Is exchange selection the COE's decision, or a business unit's? (Ask on the self-demo card.)
2. Does the customer's internal attempt show the employee the page? (Nothing he said suggests it; the whole differentiation rests on the answer.)
3. Which figures and which phrasing of the problem statement are cleared for public use? (§15.3)
4. Does Gemini 3.8 Flash accept the structured-output schemas on the `us` regional endpoint? (`make llm-check`, 14:30.)
5. Will the Hiro slot (1:30–2:00) be used for disconfirmation with the running keyword-mode UI? (Yes, per the runsheet.)
6. Prelim slot number (Sat 6:30 PM).
7. Owner split: is D17 in `sync.md` the split you want?

### 15.3 Clearances (drafts for Carl to approve before anyone is contacted)

The list is `sync.md` §J: naming "a large Japanese enterprise" and "the head of HR"; the first-line-manager figure; the per-person exchange cost; the replacement budget with its caveat; the tag taxonomy; confirmation that internal matters (`[VP-FACT-1..3]`) stay private; the five-minute self-demo. Until each is a written yes, the public artifacts use the placeholder wording in §9.4 and §10.1.

---

## 16. Glossary

- **Will / Can / Must (WCM):** the twice-yearly sheet each employee fills under the MBO process: what they want to do, what they can do, what they must do; discussed with the direct boss; shared with HR `[R 0:29:58–0:30:24]`.
- **COE:** the HR Centre of Excellence: HR strategy, HR systems, payroll, recruiting `[R 0:01:16]`. **HRBP:** HR business partners on the business-unit side `[R 0:01:33]`.
- **CEO-ship:** the company's culture in which everyone works as if they were the business owner and job boundaries are blurry, as opposed to a job-based model `[R 0:18:04–0:19:11]`.
- **Declared will:** what the person wrote about what they want, from a source with role `declared` (the WCM sheet). **Revealed will:** what the person voluntarily did or chose, from `revealed` sources (public channels, opted-in session summaries). **Paraphrase:** a manager's description, from `paraphrase` sources, always shown beside the person's own words.
- **Receipt:** a verbatim span from a cited source attached to a claim; the span check verifies it.
- **Purpose lock:** the page exists for one named decision; the policy's purpose must equal the decision id; closing deletes derived data.
- **Two-sided mirror:** the subject sees the same page as the evaluator, minus numbers, and can annotate or contest.
- **Support:** a per-criterion reading of how much of the listed evidence bears on the planner's typed criterion; not a score of a person; never shown to subjects or in the memo.
- **Drift chain:** one sentence paraphrased up three manager levels by persona prompts, showing what is lost and added; the receipt variant carries the original verbatim at every level.
- **Keyword mode:** the deterministic fallback that runs without any model; always labelled.
- **Manifest:** a file built by a separate script listing counts and hashes of every fixture, including excluded ones, so the audit strip can report "never read" without the tool opening the file.
- **Kaede Works, Northwind Labs, Aya, Rin, Yui, Kei, Hayashi, Okada, Fujii, HW-07:** fictional.
