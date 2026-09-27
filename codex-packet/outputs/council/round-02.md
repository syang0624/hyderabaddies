# Round 02 — Buyer skepticism, revision 2.0

**FICTIONAL SIMULATION.** Fictional critique generated for preparation. These are not statements by the actual judges, and scores do not predict judging. **All presenter speech below is DRAFTED FOR CARL/STEVEN.** It is not a record of anything they said.

## Evidence boundary

Frozen evidence: `work/opportunity-research.md`, `work/judges-research.md`, and `work/interview-audit.md`, prepared September 25, 2026. This round does not inspect private personal data, claim a working implementation, or invent pilot results. It evaluates proposed mechanisms rather than current PoC scores. Buyer, pricing and adoption remain hypotheses. Neither Shion nor Koki has validated willingness to pay. Their interviews establish workflows; Shion already uses Claude and Koki already prototypes rapidly. The interviewer audit explicitly cautions against upgrading friendly agreement into pain.

The fictional lenses are inspired only by public professional background: Workflow & Scale ([Indeed announcement](https://www.indeed.com/news/releases/indeed-appoints-jim-giles-as-chief-technology-officer?co=US)); Worker Value & Business ([historical Glassdoor mission article](https://www.glassdoor.com/blog/ceo-robert-hohman-talks-about-the-glassdoor-mission/)); Real-time Systems ([published demo repository](https://github.com/GoogleCloudDevRel/next25-retro-tech-revolution)); Enterprise AI Reliability ([OpenAI Academy event](https://academy.openai.com/public/events/workspace-agents-guidance-for-chatgpt-enterprise-admins-zs4dny9yey)). No personal preference or actual judging position is attributed to anyone.

## All-three comparison before selection

| Candidate | Recurring pain and buyer hypothesis | One-hour generic alternative | Smallest pilot and buyer-skeptic verdict |
|---|---|---|---|
| A — Handoff | Recruiting operations leader might pay for less assembly/checking per handoff. Actual sequence is observed; residual effort and frequency are not. | Export a fictional spreadsheet, prompt existing Claude with a source-linked template, manually review and share. | Observe one batch, then compare total assembly plus review time. Strongest route to a real operator, weakest reason yet to buy another product. |
| B — Live Experiment | Agency/product lead might pay to resolve repeated disputed requirements before implementation. Koki downplayed frustration. | Feed meeting notes into a coding agent; generate two component-based alternatives and test them. | One real disputed decision, two alternatives, same participant task, count useful mismatches and cleanup. Best immediate spectacle; weakest urgency. |
| C — Work Rehearsal | Support/onboarding manager might pay when repeated coaching of the same judgment consumes expert time across cohorts. This precise pain has not been interviewed. | Expert writes a case and answer key in a document; ordinary chatbot role-plays it with a trainee. | One expert-approved scenario, one altered transfer case, a handful of consenting trainees, document/chatbot comparison. Best ambitious hypothesis only if it improves transfer enough to repay authoring. |

**Provisional choice: C, narrowed to repeated new-hire incident judgment.** The world is an optional interface; the economic unit is one approved scenario reused across a cohort. Do not also sell recruitment screening in the initial pilot. C wins the creative future-of-work brief, not customer validation. A overtakes it immediately if observation reveals a large costly residual handoff step and a credible buyer. B wins only if an actual buyer demonstrates expensive decision delay that generic tools fail to remove.

## Preliminary rehearsal — 3 minutes, approximately 330 spoken words

[0:00–0:15 — Title: “Work Rehearsal.” On-screen badge: PROPOSED PROTOTYPE / FICTIONAL SCENARIO.]

**Presenter:** “The hardest part of a new job is often knowing what to notice before you act. We propose Work Rehearsal: a place to practice consequential decisions with fictional coworkers, using explanations an experienced worker has explicitly approved.”

[0:15–0:43 — Show a new hire facing a fictional support incident.]

“Our first buyer hypothesis is a support onboarding manager whose experts repeatedly explain the same incident decisions. We have not validated that buyer. Our interviews found working AI workarounds, not proof of an expensive unsolved problem. So this is a hypothesis we want to test, not a claim that customers asked us to build it.”

[0:43–1:28 — Conditional demonstration; do not imply screens exist.]

“In the proposed demo, you would receive a service alert. A coworker asks you to restart everything. You can inspect evidence, ask questions, or act. The simulation would respond to your actual choice. If you restart, a deterministic rule would show the consequence. If you investigate, you would discover a dependency that changes the decision.

“Then you would ask why. The AI explanation would cite the approved scenario rule. Change one clue, and the correct action would change. That is our core test: does the system teach judgment, or merely repeat a script?”

[1:28–2:02 — Baseline alongside scenario.]

“A document and a generic chatbot could already teach this case. We would compare against both. The business only works if trainees handle a fresh case better, while expert review and authoring cost less than the coaching they replace. We have no savings or learning results yet.”

[2:02–2:36 — Architecture and control.]

“The model would handle conversation. A rule engine would own state and consequences. Approved examples would ground explanations; unsupported questions would escalate. Learners could retry and choose what to share. We would not generate an employability or personality score.”

[2:36–3:00 — Pilot ask.]

“Our smallest pilot is one willing manager, one expert, one repeated incident and a small trainee group. The manager would agree on the baseline and success threshold first. If the chatbot is just as effective, or authoring costs too much, we stop. The ambition is access to practice; the first proof is one useful decision learned.”

### Preliminary Q&A — 90 seconds, fictional dialogue

[0:00–0:12]
**Worker Value & Business:** “People enjoy games. Why would a manager pay for this one?”

[0:12–0:43]
**Presenter:** “Enjoyment is a usability signal, not the purchasing case. The manager would need repeated expert coaching or slow readiness that already costs them something. We would ask for the last incident, its frequency, and who owns onboarding spending. Then we would count authoring, review and ongoing maintenance against avoided coaching. If we cannot establish that recurring cost, we do not have a buyer, regardless of how delightful the world looks.”

[0:43–0:53]
**Real-time Systems:** “Could I build your alternative with a chatbot in an hour?”

[0:53–1:30]
**Presenter:** “You could build the main baseline, and we should. Our proposed additional value is enforceable scenario state, actual consequences and feedback tied to the action the trainee took. That only matters if it improves a fresh decision rather than making the same lesson look better. We would keep the baseline's content and learning time comparable. If our benefit disappears when those are equal, we should use the generic tool instead. A polished scene alone is not a reason to buy.”

## Final rehearsal — 6 minutes, approximately 708 spoken words

[0:00–0:25 — Title, explicit proposal badge.]

**Presenter:** “Imagine starting a new role and getting to make your first consequential mistake somewhere safe. A fictional colleague pushes you to act. You ask a question, examine evidence, make the decision and see what follows. Work Rehearsal would make that experience available using scenarios and explanations approved by an experienced worker.”

[0:25–1:05 — Show recurring incident hypothesis; keep evidence label visible.]

“Our first business hypothesis is deliberately narrow: support onboarding managers whose senior people repeatedly coach the same incident decisions. We have not interviewed that buyer yet. Our existing conversations showed something valuable but different: people already combine AI with spreadsheets or rapid prototypes. That means a new product must beat a working alternative. It does not mean every workaround deserves a startup.

“We would first establish whether repeated coaching is frequent, expensive and important enough to change. Without that, the rest is theater.”

[1:05–2:25 — Proposed scenario, with pauses for learner action.]

“Here is the demonstration we propose to build. You enter a small fictional workplace. An alert arrives. Your coworker says, ‘Restart the service; we're running out of time.’ You can obey, investigate, or ask for help. Nobody has assigned you a personality type or decided what you should do.

“Behind the scene is an approved case: a dependency is still processing work, so restarting immediately would interrupt it. The environment would change only when you take an action that changes the scenario state. Conversation alone would not secretly mark the task complete.

“After your decision, you would ask, ‘Why was that a problem?’ The explanation would point to the approved rule and the clue you could have inspected. Now a judge changes the clue: the dependency has finished. The rule engine would recompute the consequence; the explanation should change with it.

“We would also ask something outside the case. The system should say that the expert material does not establish the answer. It would not invent the expert's opinion.”

[2:25–3:20 — Baseline and impact.]

“The outcome we care about is a better decision on a different case. Repeating the demo answer proves little. Our pilot would compare this rehearsal with the same material in a document and a generic chatbot, followed by a fresh case the learner has not practiced.

“We would track whether the trainee identifies the decisive clue and acts appropriately. We would also count the expert's authoring and review time, and later coaching requests. We have no results today. Any pilot size or threshold would be an agreed test design, never a claimed customer outcome.

“The learner would get another try and control sharing. We would not turn practice mistakes into a hidden hiring score.”

[3:20–4:05 — Competition and purchase.]

“Existing products already offer employer-designed simulations and interactive expertise. Our proposed difference is neither a virtual office nor a talking copy of a person. It is the connection between the learner's action, a changed world and an explanation tied to approved evidence.

“The manager would pay only if that connection produces enough useful learning or reduced repeat coaching to justify its full cost. We would sell one supported scenario pilot before proposing a subscription library. Procurement authority and willingness to spend are open questions.”

[4:05–5:10 — Architecture, failure and scope.]

“The implementation would separate three responsibilities. A versioned scenario contains clues, legal actions and consequence rules. Deterministic code maintains state. A language model interprets questions and explains only from approved scenario material.

“The model would propose a structured action; validation would accept or reject it. Unsupported answers would escalate. If inference fails, the interface would preserve state and allow inspection, rather than fabricate success. The visual world would reflect those events; it would not be the source of truth.

“We would use fictional coworkers and synthetic incidents for the prototype. Moving to company material would require the expert's approval, a defined audience and a way to withdraw outdated content. This is scoped knowledge transfer, not a cognitive clone.”

[5:10–6:00 — Pilot and reversal.]

“Our smallest pilot needs one manager who owns the problem, one willing expert and one recurring incident. We would agree on the comparison and decision threshold before observing results. If authoring overwhelms the benefit, the generic chatbot matches transfer, or the manager wants only automated screening, this version should stop.

“The larger ambition is for more people to experience work before its consequences become real. The first step is much smaller: prove that one approved rehearsal helps someone make one fresh decision, at a cost a real buyer accepts.”

**Source note accompanying the differentiation slide:** Forage documents employer-designed simulations ([Forage](https://www.theforage.com/about)); Delphi offers interactive expertise ([Delphi](https://www.delphi.ai/)). These demonstrate substitutes/category presence, not demand for this proposal. No competitor marketing outcome is repeated as causal evidence.

### Final Q&A — 6 minutes, fictional dialogue with deliberate pauses

[0:00–0:20]
**Worker Value & Business:** “Name the buyer. ‘Companies’ is not a buyer. Who approves the spending, and what existing line item loses money when they buy you?”

[0:20–1:00]
**Presenter:** “The hypothesis is the support onboarding manager, with a support operations director potentially controlling spend. We have not verified either person's authority. The initial budget could be training or operations improvement; we cannot claim a line item yet. We would ask who approved their most recent training purchase, its process, and whether this pilot can be funded. The displaced cost is repeated expert coaching and readiness delays only if their records show those costs exist. If a manager loves the idea but cannot identify a decision maker or a funded problem, that is not a sale.”

[1:00–1:15]
**Workflow & Scale:** “One scenario sounds like a consulting project. Where is recurring revenue?”

[1:15–1:55]
**Presenter:** “Initially it may be a service-heavy pilot. Recurrence would come from new cohorts using approved cases and from maintaining a useful scenario library. Neither is established. We would record marginal expert effort per new case and maintenance effort when policy changes. If every cohort requires rebuilding the world, recurring revenue could conceal recurring labor with poor economics. We would favor reusable task mechanics and versioned content, but those are design intentions. We should not declare a scalable subscription business before measuring reuse.”

[1:55–2:10]
**Real-time Systems:** “The generic chatbot knows the rules too. Why does your deterministic world justify a product?”

[2:10–2:50]
**Presenter:** “It might not. The proposed reason is that a learner must act on evidence while multiple events continue, and consequences remain consistent across attempts. A chatbot can approximate this, so we should put that approximation into the baseline. We would use the same case facts and comparable session time, then test a changed case. If stable state adds no learning value, we lose. If the only gain is visual appeal, we might have a content experience rather than an onboarding tool, and should not sell an unproved operational outcome.”

[2:50–3:05]
**Enterprise AI Reliability:** “If the expert's rule is wrong, your reliable engine teaches the wrong thing perfectly.”

[3:05–3:45]
**Presenter:** “Correct. Determinism makes a rule inspectable; it does not make it true. The expert would review cases, allowed variation and explanations, and another qualified reviewer should check consequential material before deployment. A case would show its version, scope and owner. A changed procedure should retire the old case from active practice. The prototype would use a fictional incident with explicit rules so we can test system behavior without claiming operational expertise. Expert disagreement would be recorded as a boundary or alternative, not averaged into certainty.”

[3:45–4:00]
**Worker Value & Business:** “Why narrow to onboarding? The student world was more ambitious and socially valuable.”

[4:00–4:40]
**Presenter:** “A student exploration product could be valuable, but it introduces a different buyer, distribution channel and outcome. It would compete with existing free-to-learner simulations. The onboarding hypothesis gives us a potentially observable repeated cost and access to a transfer test. It also risks privileging employers who can afford training. We would preserve learner access and agency in the design, and later test sponsored career exploration separately. We should not treat that expansion as evidence for today's business or make students pay before establishing useful learning.”

[4:40–4:55]
**Workflow & Scale:** “What exactly happens in the smallest pilot, and what evidence makes you abandon it?”

[4:55–5:40]
**Presenter:** “First, reconstruct one repeated coaching incident with a manager and consenting expert. Then build one approved scenario and a separate transfer case. A small consenting trainee group would try the rehearsal or baseline; assignment should reduce obvious selection differences. A reviewer who does not know the condition would judge the fresh-case actions against a pre-agreed rubric where practical. We would collect expert time and learner feedback as well. The small pilot is feasibility evidence, not causal proof at scale. We abandon or redesign if no repeated cost exists, the expert rejects the use, transfer is no better, or authoring cost makes reuse unattractive.”

[5:40–6:00]
**Real-time Systems:** “What can you honestly claim now?”
**Presenter:** “A clearly scoped proposal, known alternatives and a falsifiable experiment. We cannot claim an implemented engine, customer approval, a paid pilot, saved hours or better learning until those things actually happen.”

## Standalone 90-second demo storyboard — conditional build specification

This is a script for a future live run or clearly labeled recording. No screen below is claimed to exist. A presenter must replace conditional language with factual language only after verifying the corresponding behavior.

| Time | Viewer sees | Presenter/learner action and observable proof |
|---|---|---|
| 0–12 | Small fictional office; badge “Synthetic support incident; proposed prototype.” Alert and coworker request visible. | “You are new here. Your colleague wants an immediate restart. What do you need to know?” |
| 12–25 | Inspectable incident record, dependency status, approved-case version. | Learner opens evidence. The crucial dependency field is a real state variable, not explanatory decoration. |
| 25–45 | Actions: inspect, ask, restart, wait/escalate. Event log next to scene. | Learner chooses restart in the seeded unsafe condition. Rule engine produces the defined consequence; event log records the actual transition. No production infrastructure is touched. |
| 45–60 | Explanation with clickable approved rule, plus the learner's action. | Ask “Why?” Retrieval supplies the approved reason. Claim only retrieval actually executed, not a cognitive model of an expert. |
| 60–75 | Judge-editable dependency status and visible rerun. | Judge changes completion state. Same action now causes a different rule-defined consequence. Unsupported variation should be rejected rather than narrated as supported. |
| 75–90 | Attempt artifact: evidence inspected, choice, consequence, cited rule; reset and sharing controls. | Ask an out-of-scope question; show uncertainty. End: “This would demonstrate a scoped rehearsal, not learning improvement or hiring validity.” |

Fallback if not built: use a clearly labeled clickable concept and say it does not prove the engine. A prerecorded successful run cannot stand in for a live novel-input claim.

## Full council deliberation — FICTIONAL SIMULATION

**Worker Value & Business:** “I oppose choosing C on evidence. You moved from two people we actually met to an imagined support manager because the game is attractive. Who told you repeated incident coaching is the problem?”

**Presenter:** “Nobody in the frozen interviews. C is a new product hypothesis. We should place that sentence early in the pitch.”

**Workflow & Scale:** “Then A leads customer discovery. It has an operator and an existing handoff. We can observe remaining work tomorrow. It is irresponsible to downgrade proximity to a user.”

**Real-time Systems:** “Proximity does not prove value. A sourced briefing is technically straightforward, but Claude is already in the loop. We should not mistake certainty about a spreadsheet for certainty about a business.”

**Enterprise AI Reliability:** “C also has a tractable narrow mechanism: fixed state, approved rules, limited explanations. That is more defensible than pretending a person was cloned. But there is no implemented evidence. Architecture earns plausibility, not PoC points.”

**Worker Value & Business:** “The initial version says student, candidate, employee, university and employer. That is five customer stories hiding the absence of one. Choose a person with a budget and a repeated loss.”

**Presenter:** “Revision: one support onboarding manager, one expert, one recurring incident. No hiring rank or employer marketing promise.”

**Workflow & Scale:** “Better, but now authoring is your integration problem. An expert can write a document today. How many cohorts reuse it before your effort pays back?”

**Presenter:** “Unknown. We would measure total authoring plus review plus maintenance. Break-even reuse is total content cost divided by incremental benefit per learner, where benefit must be observed rather than assumed.”

**Worker Value & Business:** “And do not convert that equation into dollars using invented salaries. Ask the buyer for their actual costing convention. Faster completion could also mean worse learning.”

**Real-time Systems:** “B could generate an experiment live and wow the room. I would rank it above A creatively. But its one-hour substitute is dangerously good: transcript, coding assistant, component library. The special behavior must expose an uncertainty that changes a decision.”

**Enterprise AI Reliability:** “And a generated alternative can look functional while ignoring the constraint. In C the judge can change a state variable and inspect an explicit rule. That is a sharper verification target for a weekend.”

**Workflow & Scale:** “Only if the scene is doing useful work. Otherwise a form plus chatbot is simpler. Put that in the baseline rather than claim the office is inherently superior.”

**Presenter:** “Agreed. The architecture can support both a plain interface and the world. We should not spend the whole weekend decorating before proving the state transition.”

**Worker Value & Business:** “I still rank A first for commercial discovery. C needs a new buyer interview and may end up as custom learning content. The best business might look less magical.”

**Real-time Systems:** “I still rank C first for this brief. A paid pain is not established for any candidate. Given equal absence of buying evidence, the differentiated interaction is a reasonable exploration, provided we say what would kill it.”

**Enterprise AI Reliability:** “My condition is explicit boundaries: approved case, synthetic data, scope refusal, learner agency. No compatibility percentage and no secret inference that mistakes predict employment performance.”

**Workflow & Scale:** “My condition is tomorrow's observation can reverse us. We cannot make C the favorite and reinterpret every interview as support.”

**Presenter:** “Then the decision is provisional C for the rehearsal, A for the closest existing evidence path, B only with a demonstrated decision bottleneck. Our next fact is not whether someone likes the demo. It is whether a manager can show the recurring coaching cost and commit their own expert time to testing it.”

**Worker Value & Business:** “That is finally a purchase-shaped hypothesis. It is still not a purchase.”

## Internal scoring — not organizer scores, not measured PoC points

Illustrative rubric judgments of the proposed directions using frozen evidence. Technical points represent feasibility and proposed verifiability only; **none demonstrate current implementation**. Bands show disagreement, not confidence intervals. Official top-level weights are 40/30/30; no organizer subcategory weights are invented.

| Idea | Impact /40 | Creativity /30 | Technical /30 | Total /100 | Dissent / rank instability |
|---|---:|---:|---:|---:|---|
| A Handoff | 22 | 13 | 19 | 54 | Buyer lens ranks first because a reachable operator exists. Plausible range 47–65 after residual-work observation. |
| B Live Experiment | 17 | 21 | 16 | 54 | Systems lens sees spectacle; buyer lens sees low urgency and cheap substitute. Range 43–65. |
| C Work Rehearsal | 21 | 25 | 19 | 65 | Creative lead, speculative buyer. Buyer lens could rank it below A. Range 46–72. |

Prelim assessment: C's changed-clue action is memorable, but saying “manager pays” without uncertainty would overstate evidence. Final assessment: extra time should make economics and baseline explicit, not add more fictional departments. Technical scores should be recalculated after observing a real run, including failure behavior.

## Real / seeded / proposed truth table

| Element | Status | Honest claim |
|---|---|---|
| Shion workflow and existing Claude use | Interview evidence, audited with limitations | A workflow exists; remaining cost and willingness to pay unknown. |
| Koki debate and rapid prototyping | Interview evidence, audited with limitations | A decision occurred; severe frustration and unmet tooling need were not established. |
| Forage / Delphi alternatives | Public vendor product descriptions | Relevant alternatives exist; their claims do not validate this proposal. |
| New-hire coaching buyer | Proposed hypothesis | No interview, approval or budget established by this packet. |
| Expert, coworkers, incident, dependency clue | To be seeded and labeled fictional | No actual employee clone, customer incident or production access. |
| Scenario engine, retrieval, state transition, edited-clue behavior | Proposed, unverified here | Must run and be inspected before called implemented. |
| Learner choice | Intended real interaction | Only actual actions taken in a run qualify; a scripted video must be labeled. |
| Pilot cohort, transfer results, saved time, revenue | Not obtained | No invented quantities or success statements. |
| Small pilot sizes or decision thresholds | Future agreed design | Any numbers supplied later must be labeled test design, not results. |

## Critique-driven revision and reversal conditions

Revision 1 would have pitched a broadly useful virtual workplace for candidates and employees. Revision 2 chooses one training buyer, moves the unvalidated-pain disclosure into the first minute, puts the generic chatbot into the baseline, and evaluates total expert effort. It retains the playful interface but makes the world justify itself through action and consequence. The final Q&A now explicitly answers spending authority and recurring revenue without pretending either is known.

Reverse to A if observation identifies significant recurring assembly/checking work after Claude, an allowed data path, a recipient who uses the output and a budget owner prepared to test replacement of that work. Reverse to B if a team provides repeated expensive requirement disputes, can bring actual users into comparison, and shows generic note-taking plus coding tools fail on the relevant speed or experiment quality. Stop C if buyers cannot show recurring coaching demand, experts will not approve cases, authoring fails reuse economics, fresh-case performance matches the generic baseline, or the purchase depends on unvalidated automated screening. Continue C only with a concrete incident, willing expert and buyer-owned pilot decision.
