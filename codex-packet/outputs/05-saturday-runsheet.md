# Saturday runsheet — Sep 26, 2026 (Day 2)

**Read this first:** the deadline is **Sunday 11:00 AM PDT**, no changes after, late = disqualified (`work/event.txt` p17). Everything below exists to make that submission possible with a working core and a recorded video already in hand by Saturday night.

_Second pass, Sat Sep 26 ~00:10 PDT: the Hiro slot, repo status and template rows below were updated from local records (BRAIN.md, floor audio, the .pptx itself). Details in [PACKET-VERIFICATION.md](PACKET-VERIFICATION.md). Steven's overnight memo is mapped against this packet in [06-vouch-vs-packet.md](06-vouch-vs-packet.md)._

Two kinds of rows. **Organizer** rows are verbatim from the Day 1 deck (`work/event.txt`, pp7–9, 17–19) and are the only times you can rely on. **Suggested** rows are a plan, not a schedule; move them, don't miss the organizer rows.

Where the pre-event Japanese PDF (`work/preevent-jp.txt`) disagrees with the Day 1 deck — it does for Saturday afternoon (JP: lunch 12:30–13:30, optional mentoring 13:30–14:30, work 14:30–18:30, announcements 18:30–18:40) — the Day 1 deck is newer and wins. If a Slack announcement says otherwise, Slack wins over both.

## The one decision gate

**By 2:30 PM (end of lunch/mentoring): one path, one task, one user, one observable benefit. Written down in the repo README.** Not three paths. Not a grand vision with a demo TBD. If you leave lunch without this, everything after is at risk, because the video, deck and repo all depend on it and there are only ~20 usable hours to 11:00 Sunday, minus sleep.

The three candidates and what would earn each one are in `00-start-here.md` §2. The test is the same as council round 10's artifact gate: *one real action changes state; one changed condition changes the consequence; the explanation matches what actually happened or fails honestly.*

## Hour by hour

| Time (PDT) | Kind | What | Why / source |
|---|---|---|---|
| 0:00–6:00 AM | Organizer | Venue restricted entry/exit; venue ⇄ hotel only. If you're at the venue past midnight you can't go home until 6. | event.txt p7, p29; preevent-jp.txt |
| When you wake | Suggested | Open the Shion DM. Did she reply to the 22:49 request? If yes, that sets your morning. If no, do not treat any slot as booked. | 00-start-here §1 |
| Wake → 10:00 | Suggested | Sync with Steven: what did each of you try overnight? (Steven's is `STEVEN-RESEARCH.md`, the Vouch memo; the side-by-side with this packet is `06-vouch-vs-packet.md`.) Pick the *one* path you'd both bet on if forced to choose now (you can still reverse at lunch). BRAIN.md says a GitHub repo `tiger-baddies` was created Friday evening, but a `gh` search at 00:10 Saturday found no *public* repo by that name under either of Carl's handles, so it is private or not yet pushed: confirm it exists, make it public, and give it the README skeleton (team + one-paragraph problem, license notes section with the required disclosure of substantial third-party components — p15/p27). Every line of code must be written after Friday's opening ceremony. | event.txt p15, p27 |
| 6:00 AM–12:30 PM | Organizer | "Free time." Venue open 24h. | event.txt p7 |
| 10:00–11:00 AM | Organizer | **Tech Support core time** (OpenAI). `#ask-mentors-techsupporters`, mention `@hojoon @nkhurana @evanroberts`. Use it for anything blocking Gemini API / GCP project / Codex credits — not for idea feedback. | event.txt p9 |
| 10:00–12:15 | Suggested | Spike the *core transformation* only, not the UI: input → action → consequence → changed condition → different consequence. Ugly is fine. Goal: by 12:15 you can say which of the three paths actually runs end-to-end in a terminal. | 00 §3; round 08 "build the decision before the world" |
| 12:15–12:30 | Suggested | Write the mentoring question on a card. One sentence per path: "what would make this not worth building?" Bring the running spike, not slides. | |
| 12:30 PM | Organizer | **Gather.** | event.txt p7 |
| 12:30–2:30 PM | Organizer | **Lunch / Mentoring Session.** "Hiro" (the deck's only listed mentor is Hirotaka Moriguchi, p5; the match is an inference): reservation required, Golden Gates (1F), 30-min slots; **your 30-min slot is already booked for 1:30–2:00 PM** (BRAIN.md "On-Site Hackathon Ops", committed Fri 19:52; the floor audio in BRAIN_TRANSCRIBED_RAW.md, segment 19-22-49 at 03:25–03:41, has Carl replying to the Friday 7 PM booking thread with that slot). Slack itself was not re-read; if the thread shows otherwise, Slack wins. Walk-in mentoring: in front of Amazing Grace (1F), no reservation, you can state a mentor preference. | event.txt p8 |
| 12:30–2:30 | Suggested | Spend the mentoring slot on **disconfirmation**, not pitching. If Shion is available and still willing, this is the window for the 15-minute observation in `01-interviews-and-vp.md` (observe her actual residual work after Claude; that's the fact that decides path A). | 01 §observation guide; round 10 reversal fact |
| **2:30 PM** | **Gate** | **Path chosen. Task, user and benefit written in the README. Both of you agree. Kill the other two paths out loud.** | |
| 2:30–5:00 PM | Organizer | **Work.** | event.txt p7 |
| 2:30–5:00 | Suggested | Make the chosen core mechanism run reliably on the seeded case *and* on one changed condition. Log what is real vs seeded vs proposed as you go (the truth table the deck needs). No art, no world-building yet. | 02 "Demo truth table" |
| 5:00–6:00 PM | Organizer | **Mentoring Session.** | event.txt p7 |
| 5:00–6:00 | Suggested | Show the running thing to one mentor and ask the buyer question: who pays, what do they stop doing? Then ask them to break the demo with a condition you didn't plan. If it survives, that's your video's 60–75s beat. | 02 "Standalone 90-second demo" |
| 6:00–6:40 PM | Organizer | **Work / Announcements.** | event.txt p7 |
| **6:30 PM** | Organizer | **Preliminary presentation order is randomly selected and shared.** Note your slot; if you're early Sunday, your Sunday-morning fix window shrinks. | event.txt p18 |
| 6:40 PM–0:00 | Organizer | Work / free time. Venue access available. | event.txt p7 |
| 6:40–8:00 | Suggested | Deck v1 in the template's section order (Title, Problem, Inspiration, Solution Overview, Impact, Differentiation, Technical Design, Future Roadmap — per `02` §Template requirements; the .pptx is [attachments/hackathon_template.pptx](../../attachments/hackathon_template.pptx), re-inspected Sat 00:10 — order and caps confirmed: Problem + Insight ≤ 200 words across slides 02–03, Differentiation ≤ 100, Technical ≤ 150, Roadmap ≤ 75; solution visual and architecture diagram required; **delete the instructions slide 00 before exporting**; member names go in the Slack post, not the deck). Every impact number labelled VERIFIED / RESEARCH / CALCULATED / ILLUSTRATIVE. Export a PDF to prove the pipeline works. | 02 |
| 8:00–9:00 PM | Organizer | **Tech Support core time** (second and last window before Sunday 10–11). Last chance for infra help before submission morning. | event.txt p9 |
| 8:00–10:00 | Suggested | **Record the ≤90-second video, take 1.** Screen-record the real build. Prerecorded is allowed; say so in the video. Even a rough take is the safety copy that makes Sunday survivable. Then draft the 3-minute prelim script (≈300–330 spoken words; the council drafts in `04` are starting material, not lines to read). | event.txt p17; round 10 word counts |
| 10:00–11:30 | Suggested | Second recording if take 1 is unusable. Write the Slack submission post text (repo link, video link, PDF) into the README so Sunday morning is copy-paste. Push everything. Sleep decision: leave before midnight or you're in the venue until 6. | event.txt p29 |
| 0:00–6:00 AM Sun | Organizer | Restricted entry/exit again. | event.txt p7 |

## What must exist by Saturday night for 11:00 Sunday to be possible

All three submission items are required (event.txt p17). "Possible" means each has at least a v1 that could be submitted as-is if Sunday morning goes wrong.

1. **Public GitHub repo**, pushed, containing: the running core mechanism; a README with problem/user/benefit, how to run it, a truth table (real / seeded / proposed), and disclosure of substantial third-party components. No pre-Friday code, no personal information in prompts or fixtures (p27).
2. **A ≤ 90-second video (or a demo link) you would be willing to submit as-is.** Uploaded somewhere with a link (unlisted YouTube, Drive, etc.). The spine from `00` §3: real-looking task → action → consequence → unplanned condition → different grounded response → usable result.
3. **A PDF deck v1** already exported once, in template order, with the architecture diagram at least sketched, the instructions slide deleted, and at least one impact number shown with its label and its inputs × method × source × assumptions line (template slide 05).
4. **A prelim script** you have read aloud once with a timer. The final (6 + 6) reuses the same slides with more detail (p19) and there is **no setup time after prelim results** — so the final's extra material should exist before 11:00 Sunday too, at least as speaker notes.
5. **Your prelim slot number** (announced 6:30 PM Saturday).

If (1) or (2) does not exist by midnight Saturday, Sunday 6:00–11:00 is five hours with one tech-support window (10–11), and one recording failure eats it.

## Sunday, for reference (organizer times, event.txt p7, pp17–19)

6:00–11:00 free time · 10:00–11:00 tech support · **11:00 submission deadline, post in `#announcements-all`** · 11:00–12:00 presentation prep · 12:00–1:10 lunch · 1:10–1:25 pitch opening · **1:30–2:45 preliminary judging (3 min + 1.5 min Q&A, all teams, bring your PC, wait behind the judges during the prior team)** · 2:45–3:00 break · 3:00–3:10 prelim results & prep · **3:10–3:55 final (3 teams, 6 min + 6 min Q&A, mic and clicker, own PC)** · 3:55–4:20 break · 4:20–4:35 results · 4:35–5:00 judges' remarks · 5:00–6:30 reception · 6:30–7:20 closing.

## Boundaries that hold all day

- Every message to Shion, Hiro, mentors or organizers is **yours to send**. Nothing in this packet has been or will be sent by an agent; the one 22:49 Slack message is the disclosed exception and it is already out.
- Carl posts the submission. No agent submits.
- The ten council rounds are **fictional rehearsal**, not judge feedback. Don't quote a lens as if a judge said it.
- Don't reuse an AI-suggested idea as-is (p27). The research and rehearsals are inputs; the idea and the code are yours and Steven's, written after Friday 5 PM.
