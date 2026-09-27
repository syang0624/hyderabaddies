# Future-of-work opportunity research

Prepared September 25, 2026. Exploratory product hypotheses, not validated businesses. Sources read: local BRAIN.md, IDEATION.md, interviews/INTERVIEW_NOTES.md; primary public research and vendor documentation linked below. All demo people/data below are fictional. Private founder conversation is summarized only in the restricted-context note, without personal or fundraising details.

## Recommendation and evidence boundary

Do not let the strongest *interview evidence* automatically dictate the most ambitious *product*. Shion proves a workflow exists and that she actively uses Claude. She has not proved the residual pain is expensive, frequent, or purchasable. Koki describes rapid prototyping as an existing coping mechanism and explicitly downplays frustration. Neither interview establishes willingness to pay.

Take three Odyssey paths into the VP interview: (A) remove a handoff, (B) collapse conversation into a working experiment, (C) make expert experience available to people who cannot access it today. The most promising synthesis for Carl's motivation is **an expert-approved, interactive work rehearsal**: an engineer teaches one real scenario once; candidates or new hires can experience it, ask questions and practice. This connects cloning, a simulated world, career access, and Shion's scarce mentor coordination without claiming that simulated personalities predict employment success. It needs fresh validation.

Recruit judges already know AI hiring automation. Recruit's September 4, 2026 results commentary emphasizes recruiter productivity and hiring outcomes; a generic AI candidate summary will face an obvious substitution question. [Recruit, 2026-09-04](https://recruit-holdings.com/en/blog/post_20260904_0001/). The promising question is what is newly possible, which person benefits, and what evidence would make us stop.

## Three Odyssey paths and six bounded ideas

### A1. The handoff that prepares itself

**One sentence:** When Shion introduces a student to an engineer, a sourced, recipient-appropriate briefing is already drafted in the communication tool she actually uses.

**User/buyer:** Recruiter user; recruiting operations leader possible buyer. Communication channel unverified: email is a hypothesis, not an established interview fact.

**Evidence:** Strongest local workflow evidence: export Salesforce to Excel, combine entry sheets and recordings, use corporate Claude, deliver profiles to engineers excluded from Salesforce. Remaining pain after Claude is unknown. Market context from Recruit is proxy evidence only.

**Substitutes:** Her existing Claude + Excel process, CRM automation, ordinary templates. Win only if collection/checking/sharing takes meaningful effort after summarization.

**75-second demo:** 0–15 show three fictional records and an introduction draft; 15–35 request a briefing for a named engineer; 35–50 inspect a claim's source and flag a conflict; 50–65 switch HR view to mentor view to demonstrate intentional omission of internal-only fields; 65–75 add a new note and update only the affected sentence. Final result is an ordinary draft, not another dashboard.

**Real mechanism / seeded parts:** Real extraction, citations, field-level access filter, draft update. Seeded records and recipient roles. No real Salesforce connector necessary; say explicitly it is an export-based prototype.

**Measurement:** Minutes assembling and checking per candidate/batch, correction rate, recipient preparedness. Count review time; do not claim time saved until timed comparison.

**Kill criterion:** Shion says existing Claude is quick enough, packet work is infrequent, or approved data cannot reach the intended recipient. Do not bypass the access boundary.

### A2. Find the available mentor without exposing the HR file

**One sentence:** Ask for a mentor with a specific experience and language; the system finds an opted-in person and prepares the manager approval handoff.

**User/buyer:** Global TA / early-career programs; potential recruiting or learning budget owner.

**Evidence:** Shion coordinates 10–20 employees annually and relies on colleagues' knowledge and repeat lists. The scale of unresolved work is small until demonstrated across teams. Performance records are not necessary to solve this version.

**Substitutes:** Slack DMs, spreadsheet of volunteers, existing talent directory. The product must reduce coordination and uncover a useful person outside the existing list.

**75-second demo:** Ask in plain language for a Japanese/English-speaking engineer who has mentored first-time interns; reveal three fictional opted-in profiles with reasons; choose one; show calendar availability and a draft manager request; change the requirement and show a newly relevant mentor. Candidate information is not broadcast to all matches.

**Real / seeded:** Real matching and rationale over consented profile fields; synthetic directory and calendar; approval simulation marked as such.

**Measurement:** Time to confirmed suitable mentor, number of coordination messages, acceptance rate. **Kill:** existing list handles nearly all cases or managers, not discovery, are the bottleneck. Do not convert hidden performance evaluations into a ranking.

### B1. Meeting-to-experiment: the room leaves with something testable

**One sentence:** During a product discovery meeting, spoken constraints become two working alternatives that the customer can try before the call ends.

**User/buyer:** Product agency or enterprise innovation team that repeatedly turns customer discovery into prototypes; agency lead or product head buyer. Narrow customer is crucial.

**Evidence:** Koki's search-versus-recommendation debate is a concrete episode, but he already prototypes rapidly and reports little frustration. Generic meeting context is crowded: Granola supports in-meeting questions, PRD creation, and sharing meeting context into coding tools via MCP. [Granola product](https://www.granola.ai/chat), [MCP documentation](https://help.granola.ai/article/granola-mcp), accessed 2026-09-25.

**Differentiator to test:** Explicit uncertainty → controlled alternatives → observed user interaction. Merely generating UI from a transcript is weak against a note-taker plus coding assistant.

**90-second demo:** 0–15 customer says construction workers need work near home; 15–35 two functioning experiences appear (search and recommendation); 35–55 judge adds an unplanned constraint, e.g. no car, only evenings; 55–75 both adapt and the judge performs the same task; 75–90 show which assumptions remain untested and save a concrete next experiment. Do not claim the judge's one interaction validates a market.

**Real / seeded:** Real speech/transcript extraction and bounded generation/configuration, real filtering and interactive UI; synthetic job inventory and prebuilt component grammar. Disclose the grammar. This delivers responsive magic without pretending an arbitrary production app appeared from nothing.

**Measurement:** Time from disputed requirement to usable comparison, number of mismatches identified before handoff. **Kill:** customer says the limiting factor is authority or access to users, not making alternatives; existing tools are equally quick; live agent interrupts enough to harm the discussion.

### B2. Teach it once: a visible rehearsal before invisible execution

**One sentence:** An operations expert demonstrates a repetitive exception, explains the judgment, and sees the assistant rehearse it on a new case before authorizing use.

**User/buyer:** Service operations team with recurring exceptions; operations manager. Start with harmless sandbox cases such as a missing field in an internal request, not payments or hiring decisions.

**Evidence:** External evidence supports knowledge transfer as a mechanism, not this product. NBER's 2023 study of 5,179 support agents reported 14% average productivity improvement and 34% among novice/lower-skilled agents; it suggested dissemination of experienced agents' practices. Do not apply those percentages to the demo or recruiting. [NBER, April 2023; revised November 2023](https://www.nber.org/papers/w31161).

**Substitutes:** Written SOP, workflow automation, human training, general computer-use agents. Differentiation is eliciting the exception rule and testing it rather than replaying clicks.

**90-second demo:** Expert handles fictional request A; system asks “what would make you escalate instead?”; expert states a condition; request B has changed layout but same rule; assistant completes sandbox steps; request C violates the rule and pauses with the reason. End with a trace comparing novice behavior, expert rule, and assistant behavior.

**Real / seeded:** Real rule extraction, state transition and task execution in controlled UI; seeded requests. No claim of general employee cloning from one example.

**Measurement:** Correct novel-case completion, escalation precision, expert review time. **Kill:** rule is already fully captured in a simple form, demonstrations cannot capture needed context, or no measurable frequent exception exists.

### C1. Borrow an expert's judgment: an interactive apprenticeship

**One sentence:** A senior worker turns approved real decisions into practice situations that teach newcomers what to notice, when to act, and when to ask for help.

**User/buyer:** New hires/trainees; learning or operations leader. For Shion, engineer mentors could author a small preview of engineering work that students explore before a live meeting. That application is unvalidated.

**Why now / social impact:** Japan's challenge is also transferring capability when experienced labor is scarce. Recruit Works Institute's 2023 simulation projects a 2040 labor shortfall around 11 million; this is a modeled scenario, not a current vacancy count or product TAM. [Research project](https://www.works-i.com/research/project/futureofwork/). Japan's 2025 SME White Paper includes AI-assisted transfer of tacit craft knowledge; its page describes turning experience and intuition into explicit knowledge. [METI SME White Paper, 2025](https://www.chusho.meti.go.jp/pamflet/hakusyo/2025/chusho/b1_1_4.html). This is evidence of relevance, not purchase intent for our product.

**Substitutes:** Delphi Digital Minds, internal knowledge search, training videos, mentor office hours. Delphi already offers interactive expertise and repeated-question handling. [Delphi product](https://www.delphi.ai/), accessed 2026-09-25. Differentiate by decisions with consequences and expert-approved feedback on attempted work.

**90-second demo:** A fictional senior engineer teaches a support incident with two subtle clues; trainee enters a small simulated office and receives a task; they choose an action and see consequences; ask the expert model “why not restart it?”; it retrieves the specific approved example; change one clue and the recommended action changes; ask an out-of-scope question and it escalates. The magic is transferable judgment, not face/voice mimicry.

**Real / seeded:** Real retrieval from approved scenario records, grounded explanation, stateful branching, scope checks; seeded environment, expert notes and visual world. Label model as AI representation; no claim that it is the actual person.

**Measurement:** Transfer to a held-out scenario, expert interruptions avoided, time to competent completion. **Kill:** answers cannot beat documents on held-out scenarios, expert authoring/review is too costly, or the worker does not want this use of their knowledge.

### C2. Try the job before choosing the job

**One sentence:** A student spends ten minutes inside a realistic workday, collaborating with fictional colleagues, and leaves knowing whether the work interests them and what they need to learn.

**User/buyer:** Students/career changers; employer early-career marketing or university careers buyer. Free-to-learner is a plausible model, not a pricing conclusion.

**Evidence/substitute:** Forage already sells employer-designed simulations and offers them free to learners; its catalog demonstrates category adoption. Vendor outcome claims are observational/marketing, not proof that simulations cause employment gains. [Forage about](https://www.theforage.com/about), [simulation catalog](https://www.theforage.com/simulations), accessed 2026-09-25. A generic virtual internship is not novel; dynamic coworkers, changed constraints and learner-controlled questioning must add value.

**90-second demo:** Student enters a Habbo-like office for a fictional engineering role; a colleague requests help prioritizing a bug; student inspects evidence and asks questions; another colleague changes the deadline; consequences become visible; learner receives an artifact of what they tried and a comparison of two role styles. Finish by showing the student can reset, learn, and choose what to share.

**Real / seeded:** Real agent dialogue anchored to scenario rules, persistent task state, actual work artifact; seeded fictional coworkers and tasks. Do not show a magical compatibility percentage or infer employability from simulated agents chatting with each other.

**Measurement:** Role understanding before/after, voluntary completion, learner preference clarity, employer willingness to sponsor, authoring cost. **Kill:** fun does not improve role understanding, employers only want automated ranking, or scenario accuracy requires too much expert labor. Do not claim bias-free assessment; keep this exploratory/training unless assessment validity is separately established.

## Observable Intuition: what can and cannot be concluded

Public homepage now identifies itself as **Collective Intuition**, with a July 2026 manifesto. It describes making organizational state/action/consequence learnable, deploying in large enterprises, and models private to each customer. It does not publicly demonstrate a validated full cognitive clone of an employee or name the financial company in Carl's question. [Homepage](https://observableintuition.com/), accessed 2026-09-25.

The public enterprise terms, version 1.0 (effective at first Order Form; no fixed publication date shown), prohibit using customer data to benefit other customers or third-party models without written consent; assign lawful rights/consents to the customer; provide for role-based controls, encryption, a data-processing addendum, specified-region storage and human review. They expressly do not establish that a particular security certification already exists. These are public contractual commitments, not evidence of a named bank's consent process or successful implementation. [Enterprise terms](https://www.observableintuition.com/terms-of-service), accessed 2026-09-25.

The May 28, 2026 public privacy policy primarily concerns website/demo-contact data. Do not cite it as though it explains employee observation deployments. [Privacy](https://www.observableintuition.com/privacy).

Restricted-context note, not for a public pitch: Carl's September 9 conversation reported limited capture modalities, including screen/UI state, click coordinates and keystroke timing rather than key contents, with faces blurred and audio excluded by policy. This is an unverified founder account of design choices, **not** proof of enterprise or individual consent, regulator approval, or anonymization. Screenshots can still contain sensitive information. We do not have the private agreement and cannot answer how that particular customer approved deployment.

Useful design inference for our demo: use an explicitly approved set of professional examples, show scope and deletion controls, preserve recipient permissions, and distinguish “expert-inspired answer” from the person's actual decision. Data minimization makes review easier; it does not itself supply permission.

## Questions that select among directions

1. VP: “Where does a capable employee still need to wait for another person's experience or judgment? Tell us the last actual case.” Follow with frequency, consequence, current workaround and budget owner. This can distinguish knowledge transfer from mere paperwork.
2. Shion tomorrow: “After Claude creates the profile, what work is still left before an engineer can use it?” Then ask for an example packet/process, with redacted or fictional content.
3. Engineer/mentor: “What do students or new colleagues repeatedly need to experience or try before your advice makes sense?” Ask whether a practice scenario would reduce repetition or just create more review work.

## What not to claim in the pitch

- A workaround equals a painful business; a macro labor forecast equals our TAM; a competitor's customer count equals our demand.
- A seeded showcase is live integration; a prebuilt world is generated from nothing; a simulated council predicts the judges; one demo proves time savings.
- A model speaking like someone can predict their work performance or chemistry with another person. For now, role-play the environment and observe actual learner choices.

## Practical prioritization

Best fit for **Carl's energy + future-of-work magic:** C1, with C2's playful interface and B2's demonstration of a changed-condition test. Most defensible near-term interview evidence: A1. Fastest Astra-style wow: B1, but weakest differentiation unless tied to a specific repeated customer problem. Do not combine all six in one hackathon build. Interview evidence tomorrow should choose one narrow entry point and one measurable result.
