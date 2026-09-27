# Brain — Innovation Cup 2026 (live team brain & sync)

_Last synced: 2026-09-25 ~8:00 PM PT (incorporates Recruit Slack snapshot + local Vertex Gemini 3.8 Flash audio transcript from DG717 floor)_

Team: **hyderabaddies** — Carl Kho + Steven Yang  
GitHub repo: `tiger-baddies`

---

## 🚨 PIVOT NOTICE (Sept 25, ~7:33 PM)
The original pitch — **B2B AI Travel Desk Agent for Japanese SMBs** (Navan / TravelPerk competitor, Jalan integration, policy-generator) — has been **deprioritized / effectively dropped**.

- **Direct quote from floor audio (Carl, 19:33):** *"It doesn't have to be travel honestly."*
- **Context:** While the SMB market need was validated earlier by mentor Ryo Tomiki ("ask the boss" manual travel booking), on-site testing and energy shifted immediately upon arriving at DG717 toward hardware/wearables and novel agentic interaction models.

---

## New Direction Candidates (from live discussion)

Ideas explicitly discussed on the floor tonight (verbatim from transcript, no final lock yet):

1. **Smart Glasses / Wearable Real-Time HUD Agent**
   - Live demoed on-site using prescription/AR display smart glasses (tested live English-to-Japanese speech transcription and translation on-screen).
   - Use cases raised:
     - Meeting navigation assistant for back-to-back founders to retain context and avoid losing track.
     - Stepping stone toward long-term personal cognitive cloning.
     - Continuous inference / facial recognition lookup (referenced Harvard Meta-glasses project pulling up dossiers upon looking at people).
     - *Hardware caveats observed:* Display-integrated glasses caused slight motion sickness / eye fatigue when using both eyes.
2. **Simulated Agent Matchmaking / Lifetime Simulation ("Work Trial")**
   - Idea raised: Agent-based simulation inspired by dating platforms where AI agents representing two people simulate an entire lifetime together to predict compatibility.
   - Adaptation mentioned: Applying that simulation loop to a professional "work trial" context.
3. **Low-Latency Agent State Machines (Jev-style)**
   - Mentioned low-latency classification agents (referencing Jev running state machines to play Mario).

---


## Retro after interview 1 (Koki), 8:13–8:24 PM

- **Idea on the table:** a real-time meeting agent. When a meeting hits a crossroads, it spins up a whiteboard and prototypes as the conversation goes, like an interpreter. Carl demoed Gemini Live on the glasses, including live Tagalog/Korean translation.
  - Problems seen live: it talks over you, and nobody has named a customer yet ("who are going to be our customers?").
  - Steven: "I think the travel agent idea is like better than that one." Carl: this one "optimizes for wow moments during the judging."
- **Interview 1 follow-up:** skipped "how do you cope today" and the magic wand. Ask both next time.
- **Next:** interview Shion after she finishes eating. Agreed on general discovery first, not a travel pitch; take a concrete idea back to people later.

## On-Site Hackathon Ops & Setup
- **Mentorship booking:** Booked Hyderabaddies slot for **1:30 PM – 2:00 PM** (mentorship window is 12:30–2:30 PM).
- **Repo:** GitHub repo `tiger-baddies` created (Carl handle: `CARLKA-Minerva`).
- **Tooling:** Carl running Claude Code Max + setting up shared brain scraping scripts; targeting GCP Model Garden (investigating Feble/models) alongside Vertex.
- **GCP & Codex status:** GCP org invites sent out ($200 event credit); Codex redemption promo still throwing errors ("We couldn't prepare this promotion").

---

## Slack & Mentor Logistics (Retained from Pre-Pivot)

### #announcements-all
- Welcome message from organizers (Shion Kuroda). Pre-event material sent as PDF.
- Travel expense policy: Round-trip residence↔venue only, flights booked by organizer's travel agency (self-booked flights NOT reimbursable), ground transport reimbursed after event (standard tier only — UberX/Lyft Standard). Reimbursement process differs for JP vs overseas bank accounts.

### DM — Yuriko Wada (organizer)
- Hotel: Hyatt Regency SF Downtown SOMA, Fri Sept 25 – Sun Sept 27. Check out before venue on the 27th, luggage OK to bring to venue.
- Carl asked about extending/changing hotel — **denied**, outside policy, too late to change.

### #ask-mentors
- Mentor/supporter roster: OpenAI (Ho Joon Cha, Nick Khurana, Evan Roberts — core hours 10-11am, 8-9pm), Hiro (by appointment), walk-in supporters (Jun Sato, Koki Makino, Ryo Tomiki, Keisei Okegawa, ykanai) at DG717.
- **Open issue:** Codex credit promo link broken for multiple participants (Carl, Chika, Rafael Pradillo Lopez-Ortum). Escalated to Chika in #ask-organizers. Confirmed still broken during setup tonight.

### #ask-organizers
- Dress code question asked (Kaartik), no answer on record yet.
- Judging format confirmed: Prelims = 3 min + 1.5 min Q&A; Finals (top 3) = 6 min + 6 min Q&A. Bring own laptop. Time limits strictly enforced.

### #intro-and-teaming
- Team finalized: **hyderabaddies = Steven Yang + Carl Kho**.

### #mentors-judges-intro
- Ryo Tomiki — PM at Recruit/Indeed, Product Owner of Indeed PLUS AI Assistant.
- Ho Joon Cha — OpenAI Applied AI Architect.
- Jim Giles — CTO, Indeed.

### DM — Koki Makino (Codex credits)
- $150 OpenAI Codex credit, personal redemption link DM'd. Redeem by **Sept 28, 8:00 PM PT**, valid 4 days after redemption. Carl's link failed.

### #times-ryo-tomiki (DM/times channel) — Research archive
- *Note:* Kept for context if SMB workflow elements are reused. Ryo confirmed Japanese SMBs (20-50 people) lack travel desks or full-time ops admins; policies are unwritten ("ask the boss"), making behavior easy to modify since there is no rigid enterprise tool to replace.

---

## Open items / tripwires
- [ ] **Lock new project concept:** Decide between smart glasses HUD/translation/context agent vs simulated work trial agent before morning hacking.
- [ ] **Codex promo error:** Known failure across teams ("We couldn't prepare this promotion") — awaiting organizer/OpenAI mentor fix.
- [ ] **GCP org setup:** Verify project permissions under the official event organization.
- [ ] **Dress code:** Unanswered in Slack.

---

## Note on freshness
This file combines:
1. Manual Slack snapshots from the Recruit Community workspace.
2. On-site audio captured via Mentra smart glasses and transcribed via **local Vertex Gemini 3.8 Flash** (not Whisper, not Claude, per GCP Vertex processing rules). Updates will continue via fresh transcript injections and manual Slack pastes.