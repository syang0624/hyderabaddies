# Round 06 — Can the judge actually change the experiment?

**FICTIONAL SIMULATION.** Fictional critique generated for preparation. These are not statements by the actual judges, and scores do not predict judging. Every presenter line is **DRAFTED FOR CARL/STEVEN**, not their speech. Revision **06.1, explicitly descended from 03.1**. Frozen evidence: September 25, 2026. Preparation only; no implementation, run, customer approval, expert validation, latency, savings, or purchasing commitment is asserted.

## Evidence boundary and revision lineage

Read the three frozen reports (`work/opportunity-research.md`, `work/judges-research.md`, `work/interview-audit.md`) and `outputs/council/round-03.md`. No source repository, personal corpus, external service, or other output was modified. Local interview evidence has no public URL: Koki 20-00-00, 03:08–03:59 downplays frustration; 05:39–07:05 describes existing rapid prototyping and a domain-expert PM making final decisions. Shion's observed Claude/Excel process establishes a workflow, not expensive residual pain.

Round 03 provisionally rehearsed A as a cheap investigation, while C led its concept scores and incumbents remained the adoption default. Round 06 **changes the rehearsal vehicle to B**, giving its strongest plausible mechanism an adversarial test. This does not turn Koki into a dissatisfied customer. Round 03's objections remain load-bearing: templates can beat A; a competent coding agent can beat B; simpler practice can beat C; vendor procurement and authoring costs count; a controlled fixture is not production evidence.

**Selection for this round:** B is the strongest live-input experiment to attempt in one day. It earns a competition demonstration only if the core comparison survives a judge-authored, previously unseen constraint. C remains the more direct learner-value hypothesis. None has earned an adoption recommendation.

## Three-way comparison and one-day scope

| Candidate | Honest one-day build hypothesis | Real variation worth demonstrating | Incumbent objection preserved |
|---|---|---|---|
| A Handoff | Reviewed structured fictional records, claim links, recipient policy, editable draft | A judge changes a permitted fact or recipient; correct claims and omissions change | Claude + Excel + a good template may cover the whole residual task. Field filtering does not solve arbitrary free-text privacy |
| B Live Experiment | Two prebuilt job-discovery interfaces, shared fictional inventory, natural-language-to-typed predicate, validated shared execution, task trace | Judge authors a compound constraint in free text; both alternatives change through one verified interpretation; neither screen has a matching canned button | Granola can supply meeting context to coding tools. A generic coding agent can build this. Value must be a repeatable, inspectable comparison during a decision, not code generation |
| C Work Rehearsal | One fictional scenario, explicit state/rule engine, grounded coworker dialogue, learner artifact | Learner's actual action changes consequences; changed evidence changes the explanation | Delphi and Forage already establish adjacent products. Expert approval, transfer benefit, authoring economics, and buyer remain unknown |

Existing product capabilities are vendor descriptions, not our effectiveness findings: [Granola meeting chat](https://www.granola.ai/chat), [Granola MCP](https://help.granola.ai/article/granola-mcp), [Delphi](https://www.delphi.ai/), [Forage](https://www.theforage.com/about). We do not claim these products lack the proposed features.

### What “unseen” must mean

B's supported grammar is disclosed: Boolean combinations of comparisons over fictional job fields, plus interval overlap and elementary arithmetic using fields already present. The inventory includes hourly pay, shift start/end, travel minutes by transit, and explicit missing values. This is **new semantic composition over a known schema**, not arbitrary software generation or arbitrary real-world understanding.

The judge types a request after the fixture, grammar, and initial comparison have been frozen. No suggested prompts, constraint chips, or presenter-provided values appear. The exact string is logged. The presenter may explain supported fields before the judge chooses; they cannot quietly rewrite the request into an easier one afterward. A clarification is acceptable if visible and answered by the judge. Both views must use the same accepted predicate version.

An **illustrative adversarial rehearsal input, excluded from any claim of unseen success**, is: “Only shifts I can finish before 8 pm, but allow later endings if the journey is under fifteen minutes; after travel time I need at least eighteen dollars per hour.” This combines a conditional exception with arithmetic. The “before 8 pm” phrase needs clarification: shift end or arrival home? The effective-pay calculation also needs agreement on whether travel is round trip. A canned “evening + no car” filter would not satisfy it.

A truly unseen constraint is selected at presentation time; it might differ entirely. “Only employers who reliably accommodate childcare emergencies” requires unavailable information. The correct result is an explicit unsupported condition, not invented employer attributes. That is an honest reliability demonstration, but **does not count as a successful adaptation demonstration**. A different supported attempt, if offered, is recorded as a second attempt; the first stays visible.

### Build budget: one day, two people, conditional

Use approximately 20 combined engineering hours as a planning allowance, not an observed estimate: 3 for fixtures and the shared data contract; 5 for two usable views and task logging; 5 for typed parsing/validation and the review surface; 4 for independent oracle checks and adversarial runs; 3 for integration and honest demo recording. Existing public OSS may be used under event rules; do not reuse pre-event personal code. If core correctness consumes the allowance, cut voice, animated generation, integrations, general app creation, accounts, and visual polish first. Plain text is sufficient for the live input.

Build the common predicate interpreter and reference evaluator before adding model parsing. Restrict arithmetic and operators; never execute model-supplied arbitrary code. An independent reference check on a tiny reviewed fixture should not call the same evaluator as its supposed test oracle. Show expected eligible IDs on hand-reviewed cases, including missing data and boundary times. A browser sandbox here is a local application using synthetic jobs, not proof of secure execution of arbitrary applications.

## Preliminary presentation — three minutes

**DRAFTED FOR CARL/STEVEN. 324 spoken words; pauses and live viewing fit the remaining time. Every action is conditional on implementation. Required deck topics are addressed in sequence across the speech: title, problem, inspiration, solution, impact, differentiation, technical design, roadmap.**

**0:00–0:30 — Carl; title, problem, inspiration.**
“Live Experiment is a proposal for making a disagreement usable. In one interview, a team described debating search versus recommendations. They already prototype quickly and did not describe a major technical frustration. So our question is narrower: can people try a fair comparison while the disagreement is still in the room?”

**0:30–1:35 — Steven; proposed solution. Show PROPOSED until built.**
“We would build two ways to explore the same fictional jobs. One lets you search; one recommends a starting point. The task, inventory, and eligibility rules would stay shared. Only the discovery experience would differ.

“Now the judge would type a constraint we have not seen. There are no prepared constraint buttons. The system would show its interpretation before applying it. If a phrase is ambiguous, it would ask. If a fact is missing, it would say so.

“After confirmation, both alternatives would change together. You would try the task and inspect which jobs were eligible, which were excluded, and why. We would preserve your exact input and the rule version behind each view. A surprising response is useful only if it is also correct.”

**1:35–2:00 — Carl; impact.**
“Our intended customer is a product team repeatedly testing discovery decisions. The hoped-for benefit is finding requirement mistakes before handoff. We have no measured savings. One judge trying both views would reveal problems in this demonstration; it would not establish which design customers prefer.”

**2:00–2:30 — Steven; differentiation.**
“A coding agent can generate these screens. Meeting tools already share context with coding tools. Our proposed contribution is preserving a comparable experiment as requirements change: one accepted constraint, two working alternatives, and visible evidence about what changed. If existing tools do that just as well, they win.”

**2:30–3:00 — Carl; technical design and roadmap.**
“The one-day prototype would use a small component library and a typed rule interpreter. A model proposes rules; deterministic code validates and runs them. It would not generate arbitrary production applications. Next we would compare the full task against a capable operator using existing tools. If faster prototypes do not unblock a recurring decision, we stop.”

### Preliminary Q&A — 90 seconds

**0:00–0:12 — Real-time Systems, FICTIONAL SIMULATION:** “You disclosed a grammar. Is this just a form with natural-language input?”

**0:12–0:45 — Presenter, DRAFTED:** “The components and operators are prebuilt. That is a limitation we would show. The live claim is that an unseen combination becomes one inspectable rule that changes both working alternatives consistently. A form may be the better input if it is equally convenient. Our hypothesis concerns the comparison, not the magic of language. We would fail this demonstration if the natural-language request quietly became a different, easier constraint.”

**0:45–0:56 — Worker Value & Business, FICTIONAL SIMULATION:** “You still haven't shown that somebody needs this.”

**0:56–1:30 — Presenter, DRAFTED:** “Correct. Koki's existing process is counterevidence to a broad productivity claim. We need a team with recurring decisions that stall because participants cannot experience alternatives together. We would observe the whole decision, including setup and cleanup, and let their current tools improve. If authority or access to customers is the actual bottleneck, this product does not solve it. Today's proposed demo can establish technical feasibility; demand requires a separate test.”

## Final presentation — six minutes

**DRAFTED FOR CARL/STEVEN. 671 spoken words, leaving time to inspect the live state. Do not claim a behavior exists until the artifact has been implemented and inspected.**

**0:00–0:45 — Carl; title and problem.**
“Live Experiment asks whether a conversation can leave behind a decision people have actually tried. Imagine a team discussing how workers should discover jobs: search for exactly what they want, or start from recommendations. A slide can explain either idea. A working comparison could reveal that the disagreement depends on a requirement nobody has made explicit.

“This is a product hypothesis, not an established customer problem. The person who described this debate already prototypes rapidly. He did not tell us that generating software was a major frustration.”

**0:45–1:15 — Steven; inspiration.**
“That correction shaped our proposal. We should not compete on producing another attractive screen. We should investigate whether keeping alternatives comparable, while people change their requirements, makes a discussion more informative. The useful output would be an inspectable experiment: what varied, what stayed shared, what someone tried, and what remains unknown.”

**1:15–2:50 — Carl; solution and demonstration.**
“The proposed prototype has two prebuilt job-discovery experiences and one fictional inventory. Search begins with controls. Recommendations begin with suggestions. Both must obey the same eligibility rule, and both offer the same task: find a job you could realistically take.

“We would invite a judge to type a new constraint. We would show the supported data fields first, but supply no example answer or menu of constraint buttons. The exact sentence would stay visible.

“The system would propose a structured interpretation and explain it in plain language. Ambiguity would pause the update. Missing information would remain missing. Only after the interpretation is accepted would both experiences receive the same rule version.

“Then the judge would try the task. We would open the evidence panel: eligible jobs, exclusions, and the calculation behind an edge case. If one interface shows a forbidden job, that is a failed comparison. If the parser invents a requirement, that is a failed interpretation. A fluent explanation does not repair either error.

“The two views are designed in advance. Their behavior would change live. That is the demonstration we intend to build.”

**2:50–3:40 — Steven; impact and business.**
“The buyer hypothesis is an agency or product lead whose teams repeatedly need customers to experience competing ideas. The intended benefit is fewer misunderstood requirements reaching implementation. We have not established frequency, willingness to pay, or time saved.

“Our first comparison would measure the full route from disagreement to usable alternatives, including verification and cleanup. It would also record whether a previously hidden requirement emerged. One live judge cannot establish customer preference, accessibility, or a causal improvement in decision quality. Those need representative participants and a separate study.

“The social ambition is to let people affected by a product shape it through use, including people who cannot express their needs as specifications.”

**3:40–4:25 — Carl; differentiation.**
“Meeting assistants can already hand context to coding tools. A capable coding agent can build both interfaces. Our proposed difference is a reusable contract around the comparison: a shared task and inventory, a reviewed constraint, synchronized execution, and an evidence trace. That could become a feature of an existing tool. It does not automatically justify a new company.

“We also considered candidate handoffs and expert-guided work rehearsal. Handoffs have clearer workflow evidence; rehearsal has compelling learner agency. Both still need to beat simpler alternatives.”

**4:25–5:30 — Steven; technical design.**
“The one-day architecture is intentionally bounded. A model maps language into a typed expression. A validator rejects unknown fields and unsafe operations. A deterministic interpreter computes the common eligible set. Two components render it differently. Event logs connect the user's input, accepted rule, visible alternatives, and attempted task.

“We would check the interpreter against independently reviewed small cases. Both screens agreeing is insufficient if they share the same wrong rule. We would retain the last valid comparison during an unsuccessful update and label it stale. No live integration, arbitrary application generation, or production security claim is implied.”

**5:30–6:00 — Carl; roadmap.**
“First, make one unseen supported constraint work honestly. Then compare against a competent incumbent workflow with equal starting materials. Finally, investigate one repeated buying situation. If the comparison does not help a real decision, we should keep the useful technique and stop the product claim.”

Source beside the incumbent claim: [Granola MCP documentation](https://help.granola.ai/article/granola-mcp). Interview qualifications: local audit, Koki 20-00-00 timestamps above. No invented quantitative customer outcome or macro market figure is included. For a required impact slide number, use only a labeled **ILLUSTRATIVE** scenario, such as “4 sessions × 15 minutes hypothetical reduction = 60 minutes”; explicitly label every input assumed and the calculation not a result. Prefer replacing it with an actually measured full-task observation if obtained; do not present this placeholder as evidence of benefit.

### Final Q&A — substantive six-minute rehearsal

**All roles are FICTIONAL SIMULATION; all presenter answers DRAFTED FOR CARL/STEVEN. Timing reserves pauses for the evidence panel.**

**0:00–1:00 — Workflow & Scale:** “A coding agent with a good system prompt can maintain shared state. Why is this a product?”

**Presenter:** “It may not be a standalone product. The strongest proposed version is a repeatable meeting workflow where comparability is explicit and checked every time, instead of reconstructed by an operator. We would give a capable incumbent operator the same components, dataset, task, and time to prepare. We would compare interpretation corrections, divergent behavior across alternatives, total operator effort, and whether the customer can actually complete the task. Our implementation receives no credit merely for having a specialized interface. If the incumbent matches it, the mechanism may belong in a prompt or reusable project template. A business needs a recurrent advantage substantial enough to justify adoption.”

**1:00–2:00 — Real-time Systems:** “I'll ask for union membership, childcare compatibility, and emotional fit. What happens?”

**Presenter:** “The inventory does not establish those facts. The system must identify the unsupported conditions and avoid claiming it has applied them. It can still show the last accepted comparison with an explicit stale label. That would be a correct refusal, but it would not prove the central adaptation claim. We would log that attempt as unsupported. If you choose another constraint using available fields, we can attempt it and label it a second run. We will not silently map emotional fit to pay or invent employer characteristics. The supported boundary is known before your input, while your combination and values are genuinely your choice.”

**2:00–3:00 — Enterprise AI Reliability:** “The model writes a plausible formula and both views agree. How do I know the answer is correct?”

**Presenter:** “Agreement only shows consistency. We need three separate checks: your accepted meaning, the interpreter's calculation, and the rendered behavior. The meaning panel should expose terms such as one-way versus round-trip travel. Small hand-reviewed cases provide expected eligible IDs independently of the implementation. We would also inspect boundary examples live: a job exactly at the pay threshold or missing travel data. Finally, both interfaces must operate on the accepted set and identify its rule version. A visible trace is an inspection aid, not proof by itself. We should report failed cases alongside passed ones, including any correction the presenter had to make.”

**3:00–4:00 — Worker Value & Business:** “Are you going to call the recommendation screen better because I clicked it faster?”

**Presenter:** “No. Your interaction is one inspection of a seeded example. Order effects, prior familiarity, content choices, and the recommendation ranking could all influence it. In the prototype we would hold eligibility fixed and label ranking as a separate designed difference. We would not report a causal winner or a preference percentage. A later comparison would require representative participants, counterbalanced order or another appropriate design, and a clear outcome. The immediate artifact should say what you attempted and where you struggled, not proclaim what all workers prefer. The people affected by the product should gain a way to express their constraints, not become a decorative audience for an automated conclusion.”

**4:00–5:00 — Workflow & Scale:** “You have one day. Is the real novelty too small after you cut everything?”

**Presenter:** “The achievable claim is small: an unseen compound constraint becomes an accepted typed rule, both working alternatives update consistently, and a person can inspect the result. We would not build general meeting intelligence, generate arbitrary apps, or integrate customer systems. If we cannot make that narrow transformation correct, adding voice or animation would hide the failure. The creativity claim is the interaction pattern: disagreement becomes an experiment that remains inspectable as requirements move. Whether that is sufficiently original is uncertain, especially against existing coding tools. We would prefer a narrow working mechanism with a clear limit over an expansive story whose essential behavior is prerecorded.”

**5:00–6:00 — Enterprise AI Reliability:** “What would you conclude if the live run works, but your customer says it is unnecessary?”

**Presenter:** “Technical feasibility would improve, but the demand hypothesis would fail for that customer. Koki already gives us reason to expect this. We would ask for the last actual decision and where it waited. If it waited for authority or access to users, making the sandbox faster has little value. We would not keep changing the interview language until he agreed that it hurt. We could investigate another clearly defined team, but we should preserve the negative evidence. If neither frequency nor consequence justifies repeated use, our next step is not a bigger platform. A successful hackathon demonstration and a justified company are different conclusions.”

## Standalone 90-second demo storyboard

**Proposed recording/run, not an existing result.** A submitted recording must be called a recording. Keep visible labels: SYNTHETIC JOBS, PREBUILT VIEWS, LIVE RULE EXECUTION only when true. No timing figure below is an achieved latency.

| Time | Viewer sees | Required actual behavior / narration |
|---|---|---|
| 0–12s | Shared task, two working interfaces, fictional inventory; compact list of available fields | “Same task and jobs, two discovery approaches. The interfaces are prebuilt.” |
| 12–24s | Judge freely types an unseen sentence into an empty input; exact input captured | “Choose your own requirement using these available facts.” No examples or suggested chips |
| 24–40s | Pending state; proposed rule and plain-language meaning; ambiguity highlighted if present | Judge confirms or clarifies. No hidden presenter correction; latency is visible. If unresolved, the run cannot proceed as though accepted |
| 40–57s | Both interfaces update; shared rule-version ID and eligible count | Real interpretation, validation, computation and render. Open one exclusion and inspect actual field values |
| 57–73s | Judge performs the same task in both interfaces; visible selectable items and resulting job detail | Actual interaction, not two screenshots. Record what happened, not an A/B winner |
| 73–90s | Input → accepted meaning → rule version → excluded/eligible evidence → task trace | “This run tests adaptation and consistency. It does not validate a market or decide which design workers prefer.” Show unsupported assumptions explicitly |

If inference or clarification consumes the window, end with the actual state and failed/unfinished status. A fallback recording may illustrate a **previous** completed run but cannot replace the failed attempt without disclosure. Freeze and timestamp input log before any recording edit; keep failed attempts in the development evidence. The 90-second artifact can choose one completed run if clearly labeled selected and recorded; do not call it representative performance.

## Council deliberation — four lenses, full disagreement

**FICTIONAL SIMULATION throughout, not actual individuals' statements or predicted judging.** Lens background sources: [Workflow & Scale](https://www.indeed.com/news/releases/indeed-appoints-jim-giles-as-chief-technology-officer?co=US), [Worker Value & Business](https://www.glassdoor.com/blog/ceo-robert-hohman-talks-about-the-glassdoor-mission/), [Real-time Systems](https://github.com/GoogleCloudDevRel/next25-retro-tech-revolution), [Enterprise AI Reliability](https://academy.openai.com/public/events/workspace-agents-guidance-for-chatgpt-enterprise-admins-zs4dny9yey).

**Presenter:** “Round 03 put A on stage while allowing C to lead concept scores. For the unseen-input round, I want B to receive its strongest case. What is that case?”

**Real-time Systems:** “An input arrives after the demonstration has been prepared and changes functioning software in a way the audience can interrogate. B can show that directly. More importantly, the same constraint must alter both alternatives while preserving the experiment. That is more interesting than generating an app from a meeting transcript.”

**Workflow & Scale:** “It is also something a coding agent can build quickly. You have strengthened the demo without strengthening the customer evidence. Koki said he already prototypes and the PM decides. You must not revise that fact away.”

**Presenter:** “Agreed. Our new hypothesis is repeated comparison maintenance, not insufficient coding speed.”

**Worker Value & Business:** “That sounds like a designer inventing a new task to make the software useful. What does the customer stop doing? And why does the worker benefit instead of simply helping an agency sell a concept?”

**Real-time Systems:** “The plausible benefit is discovering a requirement while affected people can still correct it. A customer saying ‘I cannot get home from that shift’ can change the experience immediately. The mechanism lets concrete experience challenge the specification.”

**Worker Value & Business:** “Plausible. But the affected person must actually be present, and one articulate judge is not representative. C more directly gives a learner agency over experiencing a role. I still prefer its social-benefit route.”

**Enterprise AI Reliability:** “C needs an approved professional scenario and grounded consequences. A fictional expert label does not supply that. B has a comparatively crisp correctness target: the shared eligible set. That makes it attractive for one day, even though its business case is weak.”

**Workflow & Scale:** “A also has a crisp target if the records are reviewed. Why abandon it?”

**Real-time Systems:** “We are changing the stress test, not retroactively disproving A. A's recipient change demonstrates a useful rule. B allows a more expressive composition to be authored at the microphone or keyboard. Under this round's criterion, the technical learning is larger.”

**Enterprise AI Reliability:** “Only if expression means semantics. If you invite ‘no car’ and match it to a prepared flag, you have disguised a button. Show the grammar, leave the input blank, accept a judge's composition, and expose ambiguity before applying it.”

**Presenter:** “Could we claim arbitrary constraints by letting a coding agent rewrite the application?”

**Enterprise AI Reliability:** “That exceeds the one-day reliability budget. Generated code may invalidate the shared comparison, add a feature to only one side, or invent missing data. A typed rule interpreter sacrifices scope for inspectability. Say that explicitly.”

**Real-time Systems:** “I support that cut. But do not call a refusal a full success. If the judge asks about an unavailable field and the system refuses, the boundary worked; the central adaptation was not demonstrated. Those deserve separate checkboxes in the evidence.”

**Worker Value & Business:** “And do not score the recommendation design as better because the judge follows its first suggestion. Different content ordering is already a confound. Preserve the task trace without fabricating a scientific winner.”

**Workflow & Scale:** “I want the incumbent objection to survive in the final slide. Granola hands context to coding tools. A competent operator with this very schema can reproduce the mechanism. Give the baseline your components. Otherwise your preparation advantage becomes your alleged product advantage.”

**Presenter:** “That could erase the differentiation.”

**Workflow & Scale:** “Then the differentiation was preparation. A reusable template could be valuable. It need not be a startup.”

**Real-time Systems:** “I still choose B for the next build attempt. A successful unseen composition, an actual task, and a visible trace would make the proposed mechanism legible in ninety seconds. C risks spending that window on a world tour; A risks being another summary.”

**Worker Value & Business:** “I dissent on product choice, not the narrow experiment. If an expert and learner identify a consequential practice gap tomorrow, C could be worth much more. Do not let B's demo clarity become a claim of impact.”

**Enterprise AI Reliability:** “My final condition: build an independent oracle for a tiny inventory. Shared code can make both views identically wrong. If you cannot distinguish consistent from correct, the experiment's central promise fails.”

**Presenter:** “The revision is therefore B for the live-input rehearsal, not B as validated business. Existing tools remain the adoption default; we preserve the right for the actual constraint, expert conversation, or customer observation to reverse us.”

## Internal scoring experiment

**Subjective FICTIONAL SIMULATION only.** Official category weights, not organizer-issued subcriteria or predicted judge scores. No currently demonstrated PoC points are claimed; architecture scores express feasibility and quality of the proposed narrowed design. Impact includes social benefit and business plausibility, both uncertain. Ranges indicate disagreement rather than statistical confidence.

| Candidate | Impact /40 | Creativity /30 | Technical architecture /30 | Total /100 | Plausible range | This round's decisive weakness |
|---|---:|---:|---:|---:|---:|---|
| A Handoff | 20 | 10 | 19 | 49 | 40–57 | Unseen fact changes are credible, but existing Claude/template may solve the residual task |
| B Live Experiment | 17 | 22 | 22 | 61 | 43–66 | Strongest bounded live mechanism; generic-agent substitution and absent demand remain serious |
| C Work Rehearsal | 19 | 23 | 17 | 59 | 42–67 | Strong worker agency; approved content and accurate novel consequences are a larger one-day burden |

B's change from Round 03's 48 reflects a **newly specified hypothetical architecture and live-test emphasis**, not newly discovered demand or a working prototype. Its impact increase is speculative upside from a more precise participation mechanism, not evidence promotion. Worker Value & Business still ranks C first; Workflow & Scale prefers incumbent use over adopting any. If B cannot pass its unseen supported case, its technical rationale falls and its nominal two-point lead over C has no decision value.

## Real / seeded / proposed truth table

| Element | Real evidence available | Seeded or fixed in proposed demo | Proposed, unknown, or prohibited inference |
|---|---|---|---|
| A workflow | Shion describes exports, Claude, restricted access | Fictional records and reviewed policies | Residual burden, production authorization and savings unmeasured |
| B motivating incident | Koki's search/recommendation debate; fast prototyping already exists; frustration downplayed | Presenter framing of the fictional job task | No assertion that Koki wants or would buy B |
| B data and interface | No inspected implementation in this round | Invented jobs, known schema, prebuilt search/recommendation components, disclosed ordering | No real vacancies, live employer data or generated-from-scratch UI claim |
| B new input | Nothing yet executed | Grammar and initial task fixed before judge input | Exact judge sentence must actually be new; rehearsed illustrative constraint never counts |
| B transformation | Proposed architecture only | Allowed operator set | Parsing, clarification, validation, shared execution and trace must run; no precomputed answer substitution |
| B comparison | Existing alternatives documented in cited vendor sources | Common task/inventory and rule-version display | No causal A/B result, user preference, decision-quality gain or representative usability finding |
| C world | Related external categories exist | Fictional coworkers, scenario, rules and expert notes | Expert approval and learner transfer not established; no cognitive clone or personality fit score |
| Commercial/social claims | No customer outcome measured for these concepts | Optional impact arithmetic explicitly illustrative | Demand, willingness to pay, time saved, broader inclusion and sustainable business remain hypotheses |
| Council | Authored fictional preparation | All dialogue, scores and timings | Not actual judges' words, advice, forecasts or measured performance |

## Critique-driven revision and reversal conditions

**03.1 → 06.0:** Move from A's evidence-led investigation to B's strongest bounded live-input case; preserve every incumbent objection. Replace “conversation generates apps” with “a reviewed constraint keeps a working comparison synchronized.” Do not transfer Shion's workflow evidence to B or C.

**06.0 → 06.1, after fictional council critique:** Require free-text judge input after a freeze; distinguish successful adaptation from unsupported-input handling; add clarification for ambiguous arithmetic/time semantics; independent reference cases rather than shared-code agreement; retain failed attempts; make incumbent starting components equal; remove preference-winner language; cut voice/general generation to protect the one-day core.

Three decision gates, none assumed passed:

1. **Technical:** An independently authored, unseen supported combination must alter both actual views correctly, with accepted meaning and inspectable evidence. If only canned values work, stop calling this a live experiment engine. A correct refusal earns boundary evidence only.
2. **Customer and incumbent:** Observe a repeated comparison bottleneck and compare the complete task against an empowered incumbent operator. If the team waits for authority or user access, or the baseline matches the result at similar effort, keep the simpler tool. This preserves Round 03's adoption default.
3. **Direction reversal:** Choose A if a meaningful, authorized residual handoff burden appears that a template cannot cheaply resolve. Choose C if an expert approves a narrow case, a buyer names a repeated learner need, and dynamic practice has a credible advantage over a static case. If none emerges, the honest outcome is a technical experiment without a validated product.

**Recommendation:** Give B the one-day live-input attempt under these gates. Its strongest honest promise is a small, auditable transformation of a comparison—not general software generation, demonstrated market demand, or a validated winner between designs.
