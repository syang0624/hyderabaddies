# STEVEN-RESEARCH.md — "Vouch": An AI Rolodex + Approval Router for Large, Siloed Orgs

_Deep-dive research memo synthesizing the Koki and Shion interviews into one connected business idea, with market sizing, problem validation, and a concrete product spec. Written 2026-09-25 for hyderabaddies (Carl Kho + Steven Yang), Innovation Cup 2026._

Sources: [`interviews/INTERVIEW_NOTES.md`](interviews/INTERVIEW_NOTES.md), raw transcripts in [`interviews/raw/`](interviews/raw/), [`BRAIN.md`](BRAIN.md), [`BRAIN_TRANSCRIBED_RAW.md`](BRAIN_TRANSCRIBED_RAW.md), [`IDEATION.md`](IDEATION.md), [`INTERVIEW_GUIDE.md`](INTERVIEW_GUIDE.md). External market figures are web-sourced and cited inline; see the [Sources](#sources) section for full links.

---

## TL;DR

Two interviews that look unrelated on the surface — a **software engineer** (Koki) building a niche job board, and a **campus recruiter** (Shion) staffing mentors for hackathons — are actually reporting the **same missing piece of infrastructure** inside Recruit: there is no fast, trustworthy, permissioned way to answer *"who inside this company knows X / can do Y / is allowed to say yes to Z"* — so people route around it with tribal knowledge, hard-coded social rules, and manual re-typing of the same data into spreadsheets and chat windows.

**The idea:** *Vouch* — an AI agent that (1) auto-builds live, permissioned "who is this person" dossiers from data people have already consented to share (meeting transcripts, entry sheets, past project/mentor history), and (2) answers "who's a good fit for X, are they available, and what's the correct approval path" in one shot, then executes that approval path instead of a human manually pinging a manager and waiting.

This is not a new pitch invented from nothing — it is the literal, unautomated workflow Shion already runs by hand today with a general-purpose Claude chat window, generalized into a product, with Koki's team independently validating the surrounding cultural pattern (rigid decision-rights rules substituting for real data, and reluctance to be a manual gatekeeper).

---

## 1. What each interview actually found

### 1.1 Koki — Software Engineer, Recruit (construction vertical job board team) — **Moderate signal**

- Small internal team, spun up after a PM with construction-industry experience pitched a niche vertical job board (construction workers) to a product head and had to recruit his own team — Recruit's internal 0-to-1 / "intrapreneur" pattern.
- Team stays lean because "most of the work we can just use AI," especially for rapid prototyping.
- **Concrete pain, told as a real story:** deciding whether to build *search* or *recommendation* first for the MVP. *"It's very challenging to figure out which feature you're going to build out first... What is the core hypothesis you have that's going to attract the user?"*
- **Coping mechanism — a hard social rule, not a tool:** *"We have a rule that... the product manager, product owner gets to decide. Cuz you can debate all day and get nowhere... it's a culture of prototyping over debating... we trust his intuition"* because the PM has real construction-industry domain experience.
- **Separate but related datapoint:** legal/compliance review at Recruit has been compressed from multi-week, multi-team review down to a single Slack message to one accountable approver — but Koki explicitly does **not** want to be that approver: *"It's tedious... that's not something I'm not interested in doing."* Concentrating a decision in one person removes debate-paralysis, but nobody wants to hold the resulting responsibility.
- Signal graded "moderate" in the notes: he downplayed the pain twice ("I wouldn't call it frustrating, but challenging"; "technically, I don't have any frustrations"), and the team never tested a concrete pitch with him.

### 1.2 Shion — Recruiter, Global Talent Acquisition / COE, Recruit — **Strong signal**

Shion is on a 3–4 person global team inside a 30-person new-grad recruiting org, inside a larger "COE" HR org (new grad + mid-career recruiting). Three concrete, ranked pains, each with an active workaround already built:

**Pain #1 — Candidate/data assembly across silos (strongest, most concrete workaround).**
- Numbers from the interview: ~40 student candidates evaluated per hiring cycle, sourced from events like a 30-person Minerva campus event, of whom ~20 advance to selection interviews.
- Recruit's Salesforce instance is "very customized and very complicated" — she can't self-serve changes; a dedicated Salesforce engineer/ops team has to make edits, on a **weekly meeting cadence**, so *"it takes long time."*
- The candidate data engineers-as-mentors need to see lives partly inside Salesforce and partly outside it, and Salesforce access is HR-only for security reasons — so sharing it with engineering mentors requires a formal access grant that itself is slow. *"Ironically, using Salesforce takes much longer"* than just working around it.
- **Workaround, told in detail:** she exports data to Excel and uses Recruit's corporate Claude instance — *"we started using Claude... I use it very, very often"* — to synthesize meeting recordings, interview transcripts, and entry sheets into a detailed narrative profile ("his life history, what we talked about in the meeting") for each candidate, then hands that off to engineer mentors as an Excel dossier. This is a fully manual, one-candidate-at-a-time, copy-paste-into-Claude ritual, repeated ~40+ times per cycle, multiple cycles a year.

**Pain #2 — Internal mentor/expert discovery is tribal knowledge, not a system.**
- Global TA recruits engineers globally but doesn't have relationships with *internal* engineers; a separate Engineering TA team does, and the data is siloed from Global TA by design (a real "data council" governs any cross-use proposal).
- Performance-evaluation data lives with HRBP, walled off from the recruiting org: *"We don't have information about how the other managers evaluate him... we just have to ask other HR, 'do you know this person, do you have performance information?'"*
- Vetting a first-time mentor candidate is 100% word-of-mouth. Repeat/trusted mentors get onto an informal, internally-maintained "approved list" (e.g., "this person can be asked ~10 times this year") — a manually curated cache that exists *because* there's no queryable source of truth.
- **Approval-routing is a fuzzy, memorized rule, not a system:** asking someone for a >1-day "official mission" (e.g., flying someone to a hackathon) requires messaging their manager first, waiting for sign-off, then messaging the person directly with a written justification document. A casual 1-hour 1:1 skips the manager entirely and runs on personal relationships. The line between the two paths is judgment, held in her head, not documented — the same shape of problem Koki's team solved for feature-prioritization by hard-coding "PM decides."
- Volume: 10–20 employees/year require this formal request flow for mentorship alone; casual 1:1s are additional and higher-frequency.

**Pain #3 — Corporate travel booking (real, but weak signal — voluntarily reported as "standard background reality," not an active gripe).**
- Chain of custody: employee → manager → assistant → outside travel agency. A meeting date moving 2 days out means restarting the entire booking chain from scratch.
- The team's own hackathon travel took **over a month** to arrange after the invite went out.
- Employees and the company both frequently fail to claim miles/points they're entitled to, because bookings route through an agency instead of direct channels.
- Note: this is the pain the original pre-pivot "AI Travel Desk" pitch was built around (see [`BRAIN.md`](BRAIN.md) pivot notice and [`IDEATION.md`](IDEATION.md)). Shion's account, and the interviewers' own live experience booking hackathon travel, is more evidence *for* the underlying mechanic (see §3) but is the weakest of her three pains as a standalone product bet — she offered no personal workaround, and the interviewers had to push the topic rather than her volunteering it.

### 1.3 Cross-interview pattern already flagged in the clean notes

> *"Bureaucracy is being expedited from multi-week legal reviews down to single Slack approvals, though engineers actively avoid holding that approval responsibility."* — [`interviews/INTERVIEW_NOTES.md`](interviews/INTERVIEW_NOTES.md)

This is the exact same tension Shion lives with structurally (a human has to be the approval bottleneck, and everyone treats it as a chore) but from the opposite side of the desk: Koki resents *being* the approver; Shion resents *needing* one, repeatedly, with no shortcut.

---

## 2. Why Koki + Shion are the same problem, not two problems

Strip away the job titles and both interviews describe an organization that is large, fast, AI-friendly, and **deliberately decentralized** — but has no shared, permissioned layer answering "who knows this, who owns this, who can say yes to this." In its absence, every team invents its own manual substitute:

| | Missing infrastructure | Manual substitute in use today | Cost of the substitute |
|---|---|---|---|
| **Koki** | A live signal for "who has the right domain expertise/data to make this call" | A hard social rule ("PM always decides") + rebuild-it-twice prototyping instead of debating | Fast, but brittle — works only because the team is small enough that everyone remembers the rule, and doesn't scale past one person's bandwidth |
| **Shion** | A live, permissioned index of "who is this candidate / who is this internal expert / what's their approval status" | Excel + copy-paste into Claude one candidate at a time; word-of-mouth Slack pings to other HR reps; a manually-maintained "approved mentor" list; memorized approval-tier judgment calls | ~40 candidates × multiple cycles/year of manual dossier-building; 10–20+ manager-approval round-trips/year; data that's stale the moment the spreadsheet is exported |

Both are, functionally, **ad hoc replacements for the same missing product**: a system that (a) knows what people inside the org actually know/have done, (b) can be queried in natural language, (c) respects the access-control boundaries that exist for good reasons (security, HR privacy), and (d) can execute the correct next step (an approval ping, a document draft, a rebooking) without a human having to remember the rule or manually re-key the data every time.

Recruit has *already* proven, on its own, that (1) it will adopt an AI tool for exactly this synthesis work the moment it's available (corporate Claude, used "very, very often" by Shion) and (2) it is comfortable codifying human judgment into a hard rule when debate is too slow (Koki's "PM decides," the single-Slack-approval pattern). The product below just takes both instincts and turns them into shared infrastructure instead of two teams reinventing them independently.

---

## 3. The product: Vouch

**One-liner:** *An AI layer that turns "who inside this company can help with X, and how do I get to yes" from a multi-day manual scavenger hunt into a single request the agent resolves itself — using only data people already agreed to share, respecting the exact access walls that exist today.*

### Module 1 — Auto-Dossier (directly automates Shion's Pain #1)
- Input: meeting recordings/transcripts, entry sheets, and any other source a person has already consented to (the same sources Shion feeds into Claude by hand today).
- Output: a structured, permissioned candidate/employee profile — skills, background narrative, prior interactions — generated once and kept live, instead of re-assembled from scratch by a human every time someone new needs to see it.
- Key design constraint pulled straight from the interview: it must **not** require ripping out or waiting on Salesforce. It reads from whatever sources are authorized and writes a lightweight, role-scoped profile a mentor/engineer can see *without* needing raw Salesforce access — sidestepping the exact bottleneck ("it takes long time," "only HR has access") Shion described.

### Module 2 — Expert Finder + Approval Router (directly automates Shion's Pain #2, generalizes Koki's "PM decides" instinct)
- Natural-language query in: *"I need an engineer mentor for a campus hackathon, Nov 1, comfortable traveling, has hiring/product experience, hasn't been over-asked this year."*
- The agent ranks candidates using the profiles from Module 1 plus lightweight signals recruiters already track informally today (times asked this year, domain area, past mentor feedback) — replacing the word-of-mouth "do you know this person, do you have performance info?" loop.
- It then classifies the request against org policy (>1 day / official mission → route to manager first; casual 1-hour ask → go direct) and **executes** the routing — drafting and sending the manager-approval message and the request document Shion currently writes by hand each time — instead of a person having to remember which threshold applies.
- This is the same move Koki's team made when they got tired of debating feature priority: turn a fuzzy judgment call into an explicit, applied rule. The difference is Vouch applies it consistently and automatically instead of it living in one recruiter's head.

### Module 3 (Phase 2 / stretch) — Generalized policy-triggered rebooking
- The underlying mechanism in Modules 1–2 — *natural-language request → look up the (usually undocumented) policy → auto-execute or auto-route to the one human who must sign off → re-resolve automatically when circumstances change* — is exactly the mechanism the original pre-pivot travel-desk pitch needed (Ryo Tomiki's SMB validation: "ask the boss," no written policy; Shion's account: a moved meeting means re-doing the entire booking chain by hand). Framed this way, corporate travel becomes a second application of the same core engine rather than a separate product, and lets the team credibly reuse the earlier research (see [`IDEATION.md`](IDEATION.md)) if the judges ask "didn't you pivot away from travel?" — the answer is: travel is now a downstream feature of a more general internal-request-routing agent, not the whole company.

### Demo shape for judging (3 min prelim, 1.5 min Q&A per [`LOGISTICS.md`](LOGISTICS.md))
1. **Hook:** play back Shion's own words — "40 students," "Claude, very very often," "ironically, using Salesforce takes much longer."
2. **Live demo, Module 1:** paste a mock interview transcript + entry sheet → structured dossier appears in seconds (the exact task she does by hand today).
3. **Live demo, Module 2:** type the campus-hackathon mentor request → ranked candidate list + auto-drafted manager-approval Slack message, with the approval tier correctly classified.
4. **Wow moment:** change one variable (event moves from 1 day to 3 days) → the agent re-classifies the approval path live, from "no approval needed" to "manager sign-off required," and re-drafts the message — visually proving the "re-resolve when the world changes" engine, without ever using the word "travel."

---

## 4. Market sizing (numbers, shown bottoms-up, not asserted)

There's no single market category for "internal expert-finder + approval router," so size it as the intersection of three adjacent, well-measured categories it draws revenue from, plus a bottoms-up estimate anchored on Recruit's own numbers.

**Top-down, adjacent categories:**
- Talent acquisition software: **$11.4B in 2026 → $16.2B by 2034** at ~6% CAGR (Research and Markets); a more optimistic vendor estimate has the talent-acquisition *platform* segment at $8.5B in 2026 growing to $18.4B by 2033 at 14.1% CAGR.
- Knowledge management software (the "who knows what, retrieve it via AI" side of the product): **$15.9–17.2B in 2026 → $62–70B by 2034–35** at ~18.5% CAGR — the fastest-growing adjacent category, driven explicitly by AI-based enterprise search and "expertise graph" tooling.
- Internal talent marketplaces (the "match people to internal opportunities" side): no clean dollar TAM found, but adoption proof-points are strong — orgs using AI-driven internal talent marketplaces get 66% of hires from internal candidates despite only 6% of applications being internal, 33% higher retention intent, and up to 65% faster fills on critical roles (Phenom/Deloitte-cited data).

Blended, conservative **TAM ≈ $25–30B in 2026**, growing toward the $80–90B range by early-2030s across the two priced categories alone — before counting the unpriced internal-mobility layer.

**Bottoms-up, anchored on Recruit itself (the pilot customer):**
- Recruit Holdings: ~47,000–49,500 employees globally, ~$24.5B trailing-twelve-month revenue.
- At the SHRM 2025 benchmark for *large* organizations (1.03 HR staff per 100 employees, notably lower than the 1.98 all-size median — large orgs already under-hire HR relative to smaller ones, i.e., they're the most short-staffed and most in need of leverage), Recruit's HR/TA function is on the order of **~480–500 people** company-wide, of which Shion's specific 3–4 person Global TA sub-team is a small slice.
- External recruiter-productivity benchmarks corroborate the scale of the pain her sub-team is absorbing manually: recruiters lose ~17.7 admin hours per vacancy (>2 working days), 70–80% of a typical recruiter's week goes to admin/repetitive work rather than candidate/mentor relationship-building, and manual data entry alone is cited by 61% of recruiters as something that actively delays hiring decisions. One UK benchmarking study puts the fully-loaded cost of that lost time at ~£17k (~$21k) per recruiter per year.
- Applying even a fraction of that recovered time (say, 20–30%, since Vouch targets the dossier-assembly and approval-routing slice specifically, not all admin work) across a ~500-person HR/TA org implies **on the order of 100+ FTE-equivalent hours/week** returned to relationship-building and sourcing inside Recruit alone — before counting the identical Salesforce-silo and mentor-discovery pattern that almost certainly recurs across Recruit's Engineering TA, mid-career recruiting, and HRBP-adjacent teams, none of which were interviewed but were explicitly named as separate, similarly-siloed teams in Shion's own account.

**SAM/SOM framing for the pitch:** the wedge customer is any organization structurally like Recruit — large enough to have split TA/HRBP/Engineering-TA teams with formal data-access walls between them (roughly the same population as "large organization" in the SHRM benchmark above, i.e., orgs where HR is proportionally *most* short-staffed and where Salesforce-style customization lock-in is common). Recruit itself is both the design partner and, notably, a company whose core *business* is selling HR technology (Indeed, Glassdoor, HR Technology segment) to exactly this population — making Recruit a plausible **channel partner**, not just a customer, for reselling this into its own enterprise client base. That's a meaningful pitch angle in front of judges who include Indeed's own CTO and PM leadership.

**AI-adoption tailwind (why now, quantified):** 88% of organizations already use AI in at least one function, and Global-2000 companies with an AI workload in production jumped from 41% (Q1 2024) to 78% (Q1 2026). Anthropic (Claude) already holds ~40% of enterprise LLM spend vs. 27% for OpenAI — directly consistent with Recruit having already standardized on corporate Claude, which is the exact substrate Vouch would sit on top of rather than fight. The one soft spot in the data: HR/recruiting use cases currently show the *lowest* AI ROI of any enterprise function measured (1.9x, vs. 3.4x for customer support), which is itself the opportunity — it's low not because AI can't help HR, but because, per this research, HR teams are still doing the AI-assisted work by hand, one Claude conversation at a time, with no product wrapping the workflow.

---

## 5. Competitive landscape (why this gap is still open)

- **Talent marketplace incumbents** (Gloat, Eightfold AI, Workday) solve *internal mobility* (matching employees to open internal roles) — adjacent but not the same job. They assume the employee is job-hunting; Vouch's use case is a recruiter or PM hunting for a *person*, one-off, for a bounded ask (mentor, reviewer, decision input), not a role change.
- **Enterprise search / knowledge management tools** (ServiceNow's expanding KM platform, generic "expertise graph" tools) solve *find the document / find the person who wrote it* — they stop at retrieval. None of the reviewed tools execute the approval workflow that follows ("now route this to the right manager and draft the ask").
- **HRIS/CRM incumbents** (Salesforce itself) are the *cause* of the pain in this research, not a competitor to it — Shion's team already pays for Salesforce and still built a shadow Excel+Claude workflow around it because the officially-provisioned tool is too slow and too locked-down to use for this job.
- **Net:** the closest existing products solve either "find the person" or "find the role," but nothing found in this research closes the loop from natural-language ask → ranked, policy-aware candidate → auto-routed approval → auto-executed re-route on change, especially not one built to sit *on top of* existing access-controlled systems rather than replace them.

---

## 6. Risks & open questions

- **Data governance is the real product risk, not a footnote.** Shion's own account makes clear Recruit has a formal "data council" process for any new cross-team data use — Vouch's core value proposition (cross-silo visibility) is also its biggest adoption risk. The pitch and the build should lead with *role-scoped, need-to-know profile fields* and an explicit consent/audit trail, not a single merged database — this is a feature to demo, not just a disclaimer.
- **Signal graded "moderate," not "strong," for Koki.** His pain (feature-prioritization alignment) is real but he twice downplayed it and the team never pressure-tested a pitch with him. Treat Koki's interview as *corroborating evidence for the organizational pattern* (rule-based decision shortcuts, aversion to being the bottleneck), not as an independent second customer for Module 2 — the primary paying-pain customer in hand is Shion's persona, not Koki's.
- **Unresolved interview owed:** Shion committed to introducing the (Japanese-speaking, translation-needed) VP of COE/HR arriving around midnight — that conversation, if it happened, is the highest-value next validation point for whether this problem exists at a level above an individual recruiter (i.e., is it a COE-wide/company-wide priority, or just Shion's team's workaround?). Check whether that interview was captured before finalizing the pitch's "how big is this, really" framing.
- **Travel (Module 3) should stay a stretch/roadmap slide, not the opening pitch** — Shion's own signal on travel was explicitly weak (interviewers pushed the topic; she offered no personal workaround), consistent with the team's decision to deprioritize it as a standalone product on 09/25.

---

## 7. Recommended next steps before the pitch

1. If a transcript of the midnight VP interview exists, fold it in — it's the single most valuable missing data point for company-wide (vs. team-level) validation.
2. Turn the fuzzy "manager-approval vs. casual 1:1" threshold Shion described from memory into an explicit rule set for the demo (mirror Koki's team's instinct to hard-code a rule rather than debate it).
3. Build the live demo around the two moments in §3's "Demo shape," since both are dramatizations of things Shion already described doing manually on camera — the demo should feel like *automating a thing she just told you she does by hand*, not introducing a new concept.
4. Lead the pitch with the quote *"ironically, using Salesforce takes much longer"* — it's the single line that best captures the whole thesis in the fewest words.

---

## Sources

Interview & internal sources:
- [`interviews/INTERVIEW_NOTES.md`](interviews/INTERVIEW_NOTES.md) — clean interview notes, Koki and Shion
- [`interviews/raw/`](interviews/raw/) — verbatim Gemini 3.8 Flash transcripts, both interviews
- [`BRAIN.md`](BRAIN.md), [`BRAIN_TRANSCRIBED_RAW.md`](BRAIN_TRANSCRIBED_RAW.md) — floor context, pivot notice
- [`IDEATION.md`](IDEATION.md) — original travel-desk pitch and Ryo Tomiki SMB validation
- [`LOGISTICS.md`](LOGISTICS.md), [`INTERVIEW_GUIDE.md`](INTERVIEW_GUIDE.md) — judging format and interview methodology

External market data (web-sourced 2026-09-25):
- [Talent Acquisition Software Market Outlook 2026-2034](https://www.researchandmarkets.com/reports/6257102/talent-acquisition-software-market-outlook)
- [Talent Acquisition Software Market — Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/talent-acquisition-software-market)
- [Global Talent Acquisition Platform Market — Verified Market Reports](https://www.verifiedmarketreports.com/product/talent-acquisition-platform-market/)
- [Knowledge Management Software Market — Straits Research](https://straitsresearch.com/report/knowledge-management-software-market)
- [Knowledge Management Software Market — Market Research Future](https://www.marketresearchfuture.com/reports/knowledge-management-software-market-4193)
- [33 Statistics That Prove You Need a Talent Marketplace — Phenom](https://www.phenom.com/blog/talent-marketplace-statistics)
- [Activating the internal talent marketplace — Deloitte Insights](https://www.deloitte.com/us/en/insights/topics/talent/internal-talent-marketplace.html)
- [Recruit Holdings company profile — PitchBook](https://pitchbook.com/profiles/company/57356-74)
- [Recruit Holdings Q3 earnings — Staffing Industry](https://www.staffingindustry.com/news/global-daily-news/recruit-holdings-q3-revenue-boosted-by-hr-technology-business)
- [Recruit Holdings FY earnings release](https://recruit-holdings.com/en/ir/library/upload/recruit_202603Q3_earnings_en/)
- [UK recruiters lose two days per hire to admin — People Management](https://www.peoplemanagement.co.uk/article/1929340/uk-recruiters-lose-two-days-per-hire-admin-report-finds)
- [Recruiters lose £17k annually to admin tasks — Staffing Industry](https://www.staffingindustry.com/news/global-daily-news/recruiters-lose-ps17k-annually-to-admin-tasks-study-finds)
- [Why Recruiters Spend 80% of Their Time on Admin](https://www.shortlistd.io/blog/why-recruiters-spend-80-of-time-on-admin-work-(and-how-to-fix-it))
- [How Many HR Staff Members Is Best? — SHRM](https://www.shrm.org/topics-tools/news/talent-acquisition/how-many-hr-staff-members-is-best-shrm)
- [SHRM Releases 2025 Benchmarking Reports](https://www.shrm.org/about/press-room/shrm-releases-2025-benchmarking-reports--how-does-your-organizat)
- [The state of AI adoption in large orgs (76k companies) — Bloomberry](https://bloomberry.com/blog/the-state-of-enterprise-ai-adoption/)
- [Claude / Gemini Enterprise Adoption Statistics 2026 — Thunderbit](https://thunderbit.com/blog/claude-gemini-enterprise-adoption-statistics)
- [Corporate Travel Management Software Market Report 2026-2030](https://finance.yahoo.com/markets/stocks/articles/corporate-travel-management-software-market-112800709.html)
