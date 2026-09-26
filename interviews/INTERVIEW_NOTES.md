# Interview Notes

## Koki — Software Engineer, Recruit

### 1 — Who are you
* Role: Software Engineer at Recruit, based in Japan.
* Works on Japanese job boards; currently on a small internal team spinning up a niche vertical job board for construction workers.
* "I'm a software engineer."
* "I work on Japanese job boards like building"
* "We're trying out like building a vertical job board that's going like into niche market... like construction."
* Team size: Small team recruited internally after a PM pitched the concept to leadership; team kept lean by using AI for rapid prototyping.

### 2 — Tell me the last time
* Deciding MVP scope and which core feature to launch first for the construction job board.
* "when you actually try and do it, it's very challenging to example, figure out which feature you're going to build out first, right?"
* "For example, is it going to be search, or is it going to be recommendation?"

### 3 — Where'd it get annoying
* Aligning team members who hold differing views on core product hypotheses.
* "challenging when you're a small team, and uh people have different ideas... aligning within your team always."
* "technically and things like that, I don't have any frustrations."
* Also noted earlier that bureaucratic alignment and single-approver responsibilities are undesirable: "It's tedious and that's not, that's- that's something that I'm not interested in doing."

### 4 — How do you cope today
* Meeting in person rather than online to speed up debates.
* "culture of like prototyping over debating" — building quick prototypes before or during meetings instead of endlessly arguing.
* Default rule: Defer final call to PM intuition based on domain background.
* "we have a rule that, you know, the product manager, product owner gets to decide. Cuz you can debate all all all day and get nowhere... while you're debating, you can try both ideas."
* "he's the one who has experience doing construction working. So, he has the most domain knowledge... we trust his intuition."

### 5 — Magic wand
* —

### 6 — Reveal reaction
* — (Interviewers did not pitch their agent concept).

### 7 — Close / next intro
* —

---

## Shion Kuroda — Recruiter, New Grad Hiring Team (Global Talent Acquisition)

### 1 — Who are you
* Role: "Recruiter, actually... in the new grad uh hiring team, especially uh global talent acquisition."
* Organization: "COE" (covers new grad hiring, mid-career recruiting).
* Team size: 3–4 people in global talent acquisition; "new grad team itself has 30."
* Day-to-day: Manages sourcing (campus events, career forums), selection, and attraction; coordinates 10–20 internal engineers/employees per year for internships, mentorships, and 1-on-1s.

### 2 — Tell me the last time
* Sourcing engineer mentors (e.g., Hiro) for international events/hackathons: Had a candidate list, checked with manager first because mentorship is "outside of their official... mission," sent an explanatory document, then arranged flights and lodging.
* Preparing candidate data for internship mentors: Evaluated ~40 student candidates across sourcing events (e.g., 30 attendees at a Minerva event) and selection interviews (20 candidates), needing to assemble overview dossiers for engineer mentors.

### 3 — Where'd it get annoying
* Performance data silos: "The first time... We don't have information about like how his performance, or like... how the other managers eval- evaluate him."
* Organizational walls: "New grad like recruiting team and uh HRBP... is separated. And the data is separated."
* Siloed talent pools: Global TA recruits global engineers but lacks familiarity with internal engineers, while the engineering TA team holds those relationships.
* Rigid internal tooling: "Recruit's version of Salesforce is very customized and very complicated. So we cannot like arrange by ourselves, but like sales Salesforce uh engineer... it takes long time."
* Access controls: Salesforce is restricted to HR; sharing candidate data directly with engineering mentors runs into heavy security authorization barriers.
* Travel logistics: Multi-layered administrative chain: "My boss ask assistant to arrange it, like, then that assistant ask travel agency to do that arrangement."

### 4 — How do you cope today
* Mentor matching: Relies on "human knowledge," personal networks, asking peer HR reps directly ("Do you know this person?"), and maintaining an approved list of repeat/famous employees for 1-on-1s.
* Data consolidation: Exports data out of Salesforce into Excel.
* AI dossiers: Uses enterprise AI: "Very recently, we started using Claude, actually. Like we are allowed to use corporate like version of Claude... I use very often, very, very often." Uses Claude to synthesize meeting recordings, interview transcripts, and entry sheets into detailed candidate profiles ("his life history, um what we talk in the meeting") in Excel for mentors.
* Travel booking: Relies on assistants and outside travel agencies despite lengthy lead times.

### 5 — Magic wand
—

### 6 — Reveal reaction
—

### 7 — Close / next intro
* Introduced the Vice President of COE / HR arriving around midnight (24:00 / 12:00 AM).
* Clarified the VP does not speak English and offered to interpret: "Well, I can, like, translate... I can be there, so I can listen, too."
* Mentioned team members are coordinating an upcoming campus visit to Minerva on October 30/31.

### Pain points ranked (by how concrete the story + workaround is)
1. Candidate profile synthesis and cross-system data assembly: Concrete workflow (exporting Salesforce data to Excel, feeding meeting transcripts and entry sheets into enterprise Claude to compile detailed candidate packets for engineers locked out of Salesforce).
2. Internal mentor discovery and evaluation opacity: Concrete workflow hurdles (HRBP evaluation records and engineering rosters are siloed from Global TA; workaround relies entirely on informal Slack DMs, word-of-mouth HR vetting, and pre-negotiated lists).
3. Corporate travel scheduling bureaucracy: Concrete chain of handoffs (employee -> manager -> assistant -> travel agency), but treated as standard background reality with no active personal workaround attempted.

### Signal strength (one line + why)
Strong signal on recruiting data silos and automated candidate dossier generation (demonstrated an elaborate, active workaround using Excel and Claude); weak signal on travel management (interviewers pushed the topic, while Shion voiced no active friction).

### Follow-ups owed (anything promised, e.g. people to intro, the VP arriving at midnight)
* Interview with the Japanese-speaking VP of HR / COE arriving at midnight (around 12:00 AM / 24:00).
* Shion promised to join and translate/interpret the interview with the VP.

---

## Cross-interview patterns
* Note: Only one customer interview was conducted in this recording window (Koki).
* **0-to-1 product creation inside large enterprise:** Recruit employees pitch ideas to product heads and recruit their own internal teams to build new vertical job boards.
* **Rapid prototyping with AI:** Small teams utilize AI to handle grunt work and MVP prototyping without worrying about early production quality ("most of the work we can just use AI").
* **Decision resolution via domain hierarchy:** Feature disputes (search vs. recommendation) are resolved through rapid code prototypes and relying on the PM's direct industry domain experience rather than prolonged debate.
* **Heavy Slack usage and approvals:** Bureaucracy is being expedited from multi-week legal reviews down to single Slack approvals, though engineers actively avoid holding that approval responsibility.

---

## Signal strength
* **Koki: Moderate**
  * Concrete story shared: Prioritizing search vs. recommendation for the new construction job board.
  * Workaround exists: Fast prototyping in meetings + hard rule deferring to the PM’s construction domain intuition to avoid debating all day.
  * Why not strong: Explicitly downplayed pain ("I wouldn't call it frustrating, but like challenging", "technically... I don't have any frustrations"). The team did not test a pitch or ask for a magic wand fix.

---

## 7. Ryo (Recruit, product org mentor), Sat Sep 26, ~11:42 to ~12:30 PDT

Source: Mentra glasses, `interviews/raw/7_ryo_11-40-00.json`, `7_ryo_11-50-00.json`, `7_ryo_12-00-00.json`, `7_ryo_12-20-00.json` (the last two local only; Gemini 3.8 Flash). Timestamps are `segment+offset`. The 12-10 segment and the back half of 12-00 are social chat (Cebu, Minerva, a mutual friend joining his team, visas) and are not distilled. Consent: Carl asked Ryo after the interview and he said yes (Carl, 12:40 Sat); the ask itself is not on tape. Raw `12-00` and `12-20` stay local and untracked: past the interview they are personal talk, including a third party joining Ryo's team.

**Focus: how he is evaluated, from the evaluated side.**

### 1. Who
- Manages product managers ("product managers' manager"): 5 to 6 PMs, 30 to 40 people including engineers and designers (11-40 03:38).
- Evaluated by his boss, the VP of product (11-40 03:38).
- Product owner of Indeed Plus AI Assistant, an AI recruiter for Japanese SMBs, launched last August (11-40 04:00 to 05:04).

### 2. The last time
- Senior PMs are judged on results, not process: adoption and outcome per client, the product's KGI, with targets set early in the period (11-40 08:47 to 09:34).
- As a junior PM he was judged on whether he delivered, regardless of the result (11-50 00:00).

### 3. Where it gets hard
- His boss does not see all his work (11-50 00:26).
- What he really wants his boss to know is how his colleagues' view of him changed over the half year, as he changes his management style. His self-report can't show that (11-50 02:47 to 03:08).
- The 360 survey is "useless": answering is mandatory but the free-text part is optional, and "almost nobody answers the optional part, which is the most important part." He got his results last month (11-50 03:38 to 04:00).

### 4. Workaround today
- **Every cycle he builds his own presentation deck** of the past year, "put out all the things that even my boss didn't see", including PR and product impact (11-50 00:26 to 00:44). A deliberate, recurring manual workaround: real pain.
- Nothing automates it. Asked if he'd built one: "No, that I haven't, but that's a good idea." (11-50 01:21)
- He sees the route himself: "if we gather all the Slack conversation, I think it's really easy to actually put out the outputs... all the Google Docs and stuff are linked to your Slack messages" (11-50 01:49). Product org runs on Slack + Google Docs, not Microsoft (11-50 02:26).
- For peer perception he has no workaround: "I haven't figured out a way at all." Spoken feedback is polite, so it has to be written (11-50 04:52).

### 5. Magic wand
Not asked directly. The nearest answer is step 3: honest peer perception over time, in a form his boss would believe.

### 6. Reveal (evidence dashboard shared by employee and evaluator, evidence tags, no AI score, used for team matching)
- Did not land at first: "in the beginning... I wasn't sure what is the problem you guys are trying to solve" (12-00 00:47).
- **Team formation is what landed**: "that is a very specific, easy to understand problem... very big, but very difficult" and he asked what the product plan is (12-00 00:47 to 01:26). "Team formation is very intuitive... maybe we can actually prove from data instead" (12-00 00:06).
- He added his own example: HR needs an engineer with deep HR domain knowledge rather than two more HR hires, and internal search can't find one today (11-50 09:23 to 09:47).
- Chain-of-communication drift (the VP's second gap) did **not** land: "it could happen... I'm not clear on what is actually the scenarios", since there is no formal meeting where a boss discusses a member's member (11-50 06:33).

### 7. Close and leads
- **Business hook, his words:** Recruit is only in hiring now but "we have to get into talent enablement". If internal mobility finds nobody inside, "you can hire this person in Indeed and... make them pay more for our product" (12-00 02:25 to 03:14). This ties the idea to Recruit's revenue.
- **Competition:** "I heard one of the other teams were also considering a similar idea" (12-00 02:25).
- **Lead:** Hironebito-san (name as transcribed), a mentor and former Meta engineering lead (12-20 02:40).
- He agreed to think about figures to quantify internal mobility; nothing promised (12-20 06:48 to 07:29).
- Coaching: spend most time on problem definition; judges expect an idea plus MVP, "very niche and sharp" (12-20 01:34 to 01:58).

### Signal strength
**Strong on the self-evidence pain** (a recurring hand-built deck, a 360 he calls useless, and he named the Slack + Docs route himself). **Strong on team formation as the problem framing.** **Weak on chain-of-command drift**; drop it from the pitch unless someone else confirms it.
