# Judges, audience, competition, and rehearsal design

Research date: September 25, 2026. Read-only source review. This is preparation, not a prediction of judges' preferences or scores. Council roles below are fictional expertise lenses, not impersonations.

## Verified event requirements

Source: [attachments/InnovationCup2026_Day1_Slide.pdf](../../attachments/InnovationCup2026_Day1_Slide.pdf), pages 7–19, 21, 27. Extracted full text and visually inspected schedule, rubric, submission, preliminary and final slides. Also extracted all slides and speaker notes from `hackathon_template.pptx`.

- Theme (pp11–12): envision a product driving innovation in the future of work. Work includes individuals, teams, organizations, labor systems, society. No requirement to fit Recruit's businesses. AI optional. Clear problem, target user, approach matter more than stack.
- Rubric (p14): Potential Impact 40% covers BOTH social impact (problem importance/scale, meaningful user/society benefit) and business potential (demand, market opportunity, sustainable growth). Creativity & Innovation 30%: original insight, novel approach/combination, clear differentiation. Technical Architecture 30%: appropriate technology, realistic design, PoC demonstrating the key idea, credible practical path. No official numerical split inside the 40% category.
- Sunday September 27 11:00 AM PDT submission: public GitHub repository, link to demo or prototype video up to 1.5 minutes, PDF deck. Submit via Recruit Community Workspace Slack `#announcements-all`. No changes after deadline; lateness disqualifies (p17).
- Prelim: Sunday 1:30–2:45 PM, all teams; 3-minute presentation + 1.5-minute Q&A. Laptop ready beforehand. Order announced Saturday 6:30 PM (p18).
- Final: Sunday 3:10–3:55 PM, 3 teams; 6-minute presentation + 6-minute Q&A. Same slides/demos allowed with more detail; prepare final beforehand because there is no setup time after results (p19). Interpretation: include needed final detail before submission rather than assume post-deadline edits allowed.
- Grand prize $20,000 plus conditional $30,000 if project becomes a business, with 3-month acceleration. Two special awards $10,000 each (pp21–22). Do not call the conditional amount guaranteed.
- Original, previously unpublished output made during hackathon. No pre-opening code or existing self-authored libraries; public OSS allowed with licenses and substantial components disclosed. Pre-event discussion/ideas allowed (p15). Revisit Astra's concept if useful, but rebuild rather than reuse pre-event personal code.
- p27: no personal information in prompts; do not reuse AI-suggested ideas as-is. Treat this research as inputs for Carl and Steven to synthesize and validate. Fictional demo data helps comply with the specific event restriction.

### Saturday is mentoring and work, not documented industry rotations

All times PDT, September 26 (pp7–9):

| Time | Published schedule |
|---|---|
| 6:00 AM–12:30 PM | Free time, technical support 10–11 AM |
| 12:30 PM | Gather |
| 12:30–2:30 PM | Lunch and mentoring |
| 2:30–5 PM | Work |
| 5–6 PM | Mentoring |
| 6–6:40 PM | Work / announcements |
| 6:40 PM–midnight | Work / free time, technical support 8–9 PM |
| Midnight–6 AM | Restricted entry/exit, direct hotel travel only |

Hiro: reserve 30-minute spot via thread posted Friday 7 PM, Golden Gates (1F). Walk-in mentoring: in front of Amazing Grace (1F), preferences can be requested. Channel `#ask-mentors-techsupporters`. No published guarantee of external-industry interviewees. No VP midnight appointment is in this schedule; Carl's interview information is separate and appointment remains unconfirmed.

### Template requirements

Eight sections in this order: Title; Problem; Inspiration; Solution Overview; Impact; Differentiation; Technical Design; Future Roadmap. Layout can change; required labels must be addressed. Problem + insight max 200 words, differentiation max100, technical max150, roadmap max75. Solution needs a visual; architecture needs diagram. At least one supported impact number, labeled VERIFIED / RESEARCH / CALCULATED / ILLUSTRATIVE, with inputs, method, source, sample/conditions, assumptions. Speaker notes say member names/roles belong in Slack submission, although title placeholder includes members: minor source inconsistency, prioritize notes or clarify if relevant. No need to cram names in pitch.

## Actual people and evidence-based relevance

### Jim Giles — CTO, Indeed

Event deck p16 identifies him. Indeed's February 16, 2026 appointment announcement says he previously led engineering for Google Docs/Sheets/Slides/Drive and founded Workspace AI platform. He describes a career interest in improving work and simplifying hiring. This makes real workflow value and integration credible rehearsal lenses, but does not establish how he will judge.

Primary source: [Indeed appointment announcement](https://www.indeed.com/news/releases/indeed-appoints-jim-giles-as-chief-technology-officer?co=US). Japanese corroboration: [Indeed leadership, Japanese](https://jp.indeed.com/about/leadership).

Inferred rehearsal questions: Which recurring task disappears? Why will a user adopt this inside current tools? Does a hiring product improve opportunity for the candidate as well as throughput for the employer? Where does unreliable output make the process worse?

### Robert Hohman — Glassdoor co-founder and former CEO

Event deck's title is the appropriate event label; do not call him current CEO. His authored 2015 Glassdoor mission post describes making employer culture, pay and interview information accessible so people can make better workplace decisions. His earlier career includes Expedia booking engineering and Hotwire leadership. Those are public facts, not a license to infer private investment preferences.

Primary sources: [Hohman's Glassdoor mission post](https://www.glassdoor.com/blog/ceo-robert-hohman-talks-about-the-glassdoor-mission/); [US Economic Development Administration historical biography](https://www.eda.gov/strategic-initiatives/national-advisory-council-on-innovation-and-entrepreneurship/board/2014-16/Robert-Hohman).

Inferred rehearsal questions: What information imbalance does this remove? Who pays and who benefits? Does the worker gain agency? Why would either side trust the information? What differentiated value survives once incumbents add similar model features?

### Damien Contreras — Data Cloud Specialist, Strategic AI, Google Cloud

Event deck p16 gives title. Particularly relevant primary artifact: he authored a live Godot/Google Cloud AI gaming demo. It uses telemetry and screenshots for proactive contextual assistance and adaptive game difficulty, with an accompanying published codebase. Thus a playful live world is plausibly legible to this audience; it is not novel simply because it is a game or changes live. The article is personal, not official Google policy.

Sources: [Contreras, Retro Tech Revolution](https://medium.com/google-cloud/next25-retro-tech-revolution-04d260746cf3), [GoogleCloudDevRel repository](https://github.com/GoogleCloudDevRel/next25-retro-tech-revolution). Public profile search also matches Google, but no need to infer views from liked posts.

Inferred rehearsal questions: What event triggers an intervention? What happens during inference delay? Is data collection necessary and proportionate? Can you demonstrate a novel input altering output? Why is a simulated world the right interface for this work outcome?

### Ho Joon Cha — Applied AI Architect, OpenAI (event title)

OpenAI Academy lists him as Solutions Engineer in a May 19, 2026 enterprise workspace-agent webinar discussing deployment, approvals, safeguards and governance. Titles differ by source/date; use event title for event materials. Public evidence supports an enterprise implementation lens, not attributing particular opinions to him.

Primary source: [OpenAI Academy enterprise agent event](https://academy.openai.com/public/events/workspace-agents-guidance-for-chatgpt-enterprise-admins-zs4dny9yey).

Inferred rehearsal questions: What does the model decide vs deterministic software? What permissions does execution require? How are harmful errors caught? How do evaluations distinguish useful behavior from a polished single run? What can you show actually working now?

## Fictional council rubric

Every rehearsal must begin: “Fictional critique generated for preparation. These are not statements by the actual judges, and scores do not predict judging.” Use role names, not judge names in dialogue: Workflow & Scale; Worker Value & Business; Real-time Systems; Enterprise AI Reliability.

Use actual 40/30/30 category weights. Proposed internal anchors (not organizer-issued subcriteria scores):

- Impact /40: 0–10 clear target and observed problem; 0–10 measurable benefit with credible baseline; 0–10 buyer/demand/adoption; 0–10 social benefit and foreseeable exclusion addressed.
- Creativity /30: 0–10 non-obvious insight; 0–10 differentiated mechanism against real alternatives; 0–10 useful new interaction/outcome.
- Technical /30: 0–10 demonstrated core mechanism; 0–10 feasible architecture/data access; 0–10 reliability, human control and path beyond fixture data.

Rate evidence separately: observed interview, external research, tested PoC, assumption. A beautiful rendering does not promote assumptions into evidence. Reviewer disagreement should remain visible. At least one critic should argue why an apparently winning idea loses. Report score ranges or rank instability, not “winning probability.”

For ten independent passes, vary the stress test rather than repeating a friendly panel: 1 baseline; 2 buyer skeptical; 3 incumbent comparison; 4 worker downside; 5 data access unavailable; 6 novel input; 7 latency/outage; 8 small-team feasibility; 9 social scale; 10 final head-to-head using the same frozen evidence packet. Keep a full transcript with pitch, stage directions, questions, answers, critique and revised recommendation. Each includes prelim and final assessment, and explicit demo truth table.

## Three idea families through four expertise lenses

| Idea | Workflow & Scale | Worker Value & Business | Real-time Systems | Enterprise AI Reliability |
|---|---|---|---|---|
| Employee expertise clone | Which expert interruptions or blocked decisions recur? | Who controls likeness/knowledge? Is worker helped or merely replaced? What does buyer pay for? | How does new evidence update advice without full retraining? | Access boundaries, revoked permission, uncertainty, no pretending to be the person |
| Work-trial universe | Which real task does simulation represent? | Does candidate learn about employer too? Who gets excluded by games/language/time? | Can changing a scenario produce meaningful behavior rather than cosmetic animation? | No unvalidated personality/hiring scores; show task evidence and human judgment |
| Live meeting-to-prototype agent | Which decision currently waits days for a shared artifact? | Is saved time real vs simply moving work to cleanup? Who buys? | Interruption, latency and novel constraint handling live | Requirements vs suggestions distinguished; safe execution and undo; trace decision to artifact |

### Demo truth table, applied to every idea

Label fictional people/data. State which inputs are fixed, which outputs are prerecorded, which transformations execute live, and what remains proposed. Fixtures are useful for reproducibility; hardcoding the claimed key technical behavior cannot demonstrate that behavior. Submitted video may be prerecorded, clearly presented as a recording. A valid narrow PoC can be compelling: prove one surprising transformation on a judge-supplied variation. Do not imply production integration or customer approval from a local mock.

## Time-boxed presentation design

Prelim 180 seconds: title 10; problem25; observed insight20; solution/demo55; measured impact25; differentiation15; architecture20; roadmap10. This preserves section order by placing live demo inside solution. Q&A90: two substantive answers with supporting evidence ready. Technical diagram remains visible long enough to understand, not decorative.

Final360 seconds: title10; problem40; insight30; solution/demo100; impact55; differentiation35; architecture60; roadmap30. Q&A360: expect buyer/demand, comparison, evidence quality, privacy/data access, failed-input behavior and long-term roadmap. All durations are suggestions, not rules.

Standalone90-second demo: 0–12 specific person and stuck moment; 12–25 input and baseline; 25–60 core transformation; 60–75 new constraint or failure handled; 75–90 resulting usable artifact and boundary of what actually works. Avoid a tour of settings. The audience should be able to describe the before-and-after without saying “AI dashboard.”
