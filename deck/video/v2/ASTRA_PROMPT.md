# Pik demo video, V2: the brief for GPT-6 Astra (run by Steven)

Written Sat Sep 26 2026, 21:05 PDT, by Claude in Carl's session, from Carl's dictated brief (`CARL_BRIEF_RAW.md`, audio and re-transcription beside it), the V1 build (`../README.md`, `../STORYBOARD.md`, `../build.py`), the interviews, and the PRD. Everything Carl decided is marked **Carl**. Everything I decided for him is marked **decided**; he said "you figure it out" and "take over", so treat those as the brief unless he overrides them in person.

Run `date` first. Deadline: **Sun Sep 27, 11:00 AM PDT**, posted in Slack `#announcements-all`: public repo + video ≤ 90 s + PDF deck. Prelim pitch Sun 13:30 (3 min + 1.5 Q&A). Carl posts the submission; you do not.

## 0. What you are making (two files, plus the pieces)

1. `deck/video/v2/pik_90s_v2.mp4`: 1920x1080, 30 fps, H.264 + AAC, **≤ 90.0 s**, captions burned in, narration by TTS on the shared GCP project (section 6). Followable with the sound off.
2. `deck/video/v2/meet_stage_demo.mp4`: the "live demo" for the stage. **Carl**: on stage the Meet demo is hard-coded. Carl screen-shares a video that plays; he and Steven time their lines to what pops up so it looks like magic. This file is that video: the Meet beat only, slower, with silent gaps where they speak, and a cue sheet `STAGE_CUES.md` (t → what appears → who speaks what). It is separate from the 90-second submission.

Plus: Figma frames `V2-00` … `V2-11` (new frames; do not edit `V1-*`), renders in `v2/renders/`, captures in `v2/captures/`, narration in `v2/vo/`, `v2/build_v2.py` (copy `../build.py`, new `SEGMENTS`), `v2/STORYBOARD_v2.md` and `v2/TIMING.md` written by the build.

## 1. Read, in this order, nothing else first

1. `deck/video/v2/CARL_BRIEF_RAW.md` (his words) and `CARL_BRIEF_TRANSCRIPT.md` (the audio, re-transcribed; trust it where the raw text is garbled).
2. `deck/video/README.md`, `STORYBOARD.md`, `TIMING.md`, `build.py`, `narrate.py`: how V1 was built. V2 is built the same way (Figma Motion exports + prototype captures + TTS + ffmpeg stitch). Watch `_assets/pik_90s_v1.mp4` once.
3. `deck/video/STORYBOARD_v4_figma.pdf`: Carl's storyboard. V2 follows its flow; section 3 below is that flow with the revisions.
4. `PRD.md` Part A only (§0 to §7). Then `interviews/INTERVIEW_NOTES.md` §2 (Shion), §7 (Ryo), §9 (Hiro) and `interviews/5_VP_MEETING_SUMMARY.md` §2 and §4. These are the people the "we asked Recruit" beat quotes.
5. `deck/JUDGE-MAP.md`: who judges and what each one listens for.
6. `prototype/README.md` and `prototype/surfaces/slack_bot.py` (the real Slack card's blocks) and `prototype/surfaces/notion_board.py` (the real board fields).

Figma file: `Pik - Recruit Holdings Hack`, key `1md8EyJXD30RKXXYb1pAoo` (Carl shares it with Steven as editor; the MCP refuses writes on view-only). Read it with the Figma MCP, never web-fetch it. Nodes Carl made for you tonight:
- **Gmail chops**: https://www.figma.com/design/1md8EyJXD30RKXXYb1pAoo/Pik---Recruit-Holdings-Hack?node-id=26-190 (node `26:190`). **Carl**: he manually cropped the Gmail UI into pieces (header, sender name, body text) so that when Pik sucks a piece in, a white background is revealed underneath.
- **Slack UI**: https://www.figma.com/design/1md8EyJXD30RKXXYb1pAoo/Pik---Recruit-Holdings-Hack?node-id=26-211 (node `26:211`). Same treatment: the message table, reactions, name, avatar and channel are separate pieces over white.
- V1 frames `V1-00` … `V1-10` on Page 1 at y=17000 and y=18400: the Pikbot mascot (black body, spring antenna, two eyes), the blob characters, the receipt stub component, the mask-reveal text animation. Reuse the components; make the V2 frames at y=20000.

## 2. The thesis (every beat must serve it)

**Carl (restated on tape by Steven):** AI is removing the boundaries between roles. An engineer can do work outside engineering; HR can ship software; one person now does what a team of specialists did. So a company stops being fixed teams doing fixed jobs and becomes **a task force per task**. That makes one question the most frequent decision in the company: **who is the best person for this?** Today it is answered from memory and a paraphrase (the head of HR, a product leader and a former engineering leader all told us so this week, each unprompted). Pik answers it from what people actually did, with the receipt attached, wherever the question is asked (a Meet, a Slack channel, a ticket), and the person named sees the same receipts. No score.

Test for every example, ask, quote and screen: *does it show a task looking for a person, answered from what people did?* If it shows a job title, a resume, a score, or a dashboard for its own sake, cut it.

## 3. The 90 seconds, beat by beat

Timing budget sums to 90.0. Narration is faster than V1: **Carl** wants it to "speak a bit faster" (target ~165 wpm; `narrate_vertex.py --rate 1.12` does it). Narration only in gaps, never over the Meet lines. One caption per beat, one sentence, burned in (PIL, as in `build.py`; this ffmpeg has no drawtext).

| t | Beat | On screen | Narration (TTS unless marked) | Caption |
|---|---|---|---|---|
| 0.0–2.5 | Disclosure | V1-00 shortened: bone card, mono text. Required first frame. | silent | Recorded Sep 27. Fictional company and people. Live in the product: listener tool calls, extraction, re-ranking. |
| 2.5–8.0 | The blur | **Carl** liked V1's mask-reveal text; keep the animation, change the content. **decided**: no stock people under this beat (he doubts the b-roll). Typographic: the words `HR · Engineering · Design · Sales · Ops` in one row with rules between them; the rules blur and dissolve; the words drift and overlap into one blob character. Then the headline. | "In a post-LLM world, the line between what one person can do is blurring." | The line between roles is blurring. |
| 8.0–16.0 | We asked Recruit | **Carl**: "we asked people around Recruit Holdings what their biggest problems in HR is." Three quote cards, **typewriter** in, roles only, no names, no company on screen (`sync.md` §J is uncleared; PRD public-repo rule). Cards: (1) *"Team formation, as AI dissolves the roles. That is what we're most troubled by."* — a head of HR. (2) *"Every cycle I build my own deck of everything my boss didn't see."* — a product leader who manages 40. (3) *"Managers pitch people from memory. Four or five days a quarter."* — a former engineering leader of 150. Then the three cards stack behind one line. | "We asked people at Recruit Holdings what their hardest problem in HR is. Every answer was the same shape: who does what next, decided from memory." | Team formation. Internal mobility. Decided from memory. |
| 16.0–23.0 | The asks | Keep V1's stamp-and-stack animation (V1-02). **Carl**: the three V1 asks were made up on a whim; replace them with asks that advance the thesis, and talent acquisition is on theme for the judges. **decided**, escalating, each a task not a title: (1) *Who is the best person to mentor this year's interns?* (2) *Who is the best person to lead a pricing task force with the US partner?* (3) *Who is the best person for the two-year exchange?* (3 is what the Meet beat answers.) B-roll under: **decided** none; blob characters look up at the pile instead. If you keep any, greyscale and lifted as V1 did, and only the office clip. | "Who is the best person to mentor the interns? To lead the pricing task force? For the two-year exchange? Same question, every week." | Who is the best person for this? |
| 23.0–26.5 | Meet Pik | V1-03 unchanged (slide in, blink, antenna springs). **Carl**: "company intelligence AI that works wherever you are" is not the line. **decided** tagline: **"Meet Pik. It knows who's done what, and answers where you ask."** Alternates if Carl vetoes it: "Meet Pik. Who's best for this, with the receipts, in the tools you already use." / "Meet Pik. Ask anywhere. Answered with receipts." Rules: ≤ 12 words, no "intelligence", no "AI-powered". | "Meet Pik. It knows who's done what, and answers where you ask." | (the tagline, as the headline) |
| 26.5–38.0 | Mining: Slack, then Gmail | **Carl's mechanism, exact:** Pikbot extends its antenna into the Slack UI (node `26:211`). Piece by piece the table, the reactions, the name, the avatar and the channel get sucked into Pik and each is **replaced by plain white** (Carl cut the pieces so white is underneath). A "+" card: `+ Yui's Slack` → typewriter: *"I see. Yui runs the English study channel and reviews every pricing doc."* A little **jump** (Pikbot hops once). Typewriter: *"What else can I learn about Yui?"* Scene changes to Gmail (node `26:190`; **Carl**: show sent mail, simulated). Same suck: header, sender name, body text go into Pik, white revealed. `+ Yui's email` → typewriter remark. **decided** remark, on theme for talent acquisition: *"She onboarded the last three hires and ran the mentor intake herself."* Then *"I see. She also does that."* Rule from the product: every line Pik states must be something a receipt could carry (a verbatim line with a source); the sucked-in pieces ARE the receipts. Never show a DM. | "Pik reads what Yui already wrote and shipped, where the company allows. Every line keeps its source." | It reads what she already did. Every line keeps its source. DMs never. |
| 38.0–43.0 | Receipts settle, zoom out | V1-04b + V1-05 tightened: the pulled lines settle around Yui's blob as receipt stubs; two unsourced lines drop; zoom out to 200 blobs, one far slice flips as a new receipt lands. | "Two hundred people. Always current." | Two hundred people. Always current. |
| 43.0–58.0 | Meet | **Carl**: the Meet integration UI is now a dense **network-graph** view; Steven is pushing it (not on `main` at 21:05 Sat; `git pull` until it lands, then read its README/commit). For the 90-second cut **Carl** will freeze-frame the new UI: use a Playwright or screen capture of it, and animate over the still (the graph re-sorts, three tiles come forward, a receipt opens, the conclusion prints). Two manager lines by TTS voice Puck (or Steven's real take if he records one). Narration only in the gaps. Exact lines (they pass the live regression): Manager: *"For the Northwind slot I need someone who will push back on the job-based culture instead of just absorbing it, and they have to hold their own in English in meetings."* … Manager: *"Okay, let's set up calls with Yui and Kei this week, and ask Yui whether that location note is actually true."* | Manager (Puck) ×2; narrator in the gap: "In the meeting, it hears the criterion and re-sorts on their words. No score." | Heard the criterion. Re-sorted on their words. No score. → What the meeting concluded. Receipts attached. |
| 58.0–66.0 | Slack: who leads the team | **Carl**: "we can do better; add more Slack UI elements." Build a fuller Slack replica in Figma (sidebar with channels, `#pricing-team` header, message list, composer) using the pieces in node `26:211`. Someone types *"who's best to lead the pricing task force?"*; Pik's ephemeral card appears with the real bot's layout from `slack_bot.py`: name + role + team, one why line, two receipts quoted with sources, load line, "Also:" two alternates, buttons **Loop in Yui** and **Why? See the receipts**, footer *"Order is evidence overlap with your words, minus load. Not a score."* Cursor presses Loop in → *"@Yui, looping you in: …"*. | "Or ask in Slack. One press to loop her in." | Ask where you already are. One press to loop her in. |
| 66.0–76.0 | The ticket | **Carl, exact:** build in Figma a replica of a Linear/Jira/Notion issue page (**decided**: Linear-style, dark, because it is the cleanest and matches the product's palette; fields named as the real Notion watcher has them: Suggested owner, Why, Receipts). The brief title *"UI refresh"* and the task lines are **typed in**; then the AI feature highlights itself: on the properties/labels panel the **Assignee** dropdown opens by itself and selects **Yui Sato**; next to it a **?** button; hover/press shows a tooltip that explains why with a **mini receipts UI** (two stubs, source lines, "verbatim" stamp). | "On a ticket, it fills in the owner, and shows why." | One click to assign. The why is attached. |
| 76.0–84.0 | Other verticals | **Carl**: the "second dashboard" beat becomes how this extends to other industries. **decided**: the ask pile from beat 3 returns with new asks stamping in, each with a small icon and a blob, no dashboards: *Which surgeon for this case?* (hospital) · *Which crew for this route?* (airline) · *Which foreman for this site?* (construction) · *Which mentor for the new hire?* Pikbot points at each; a receipt ring appears under every one. | "The same map answers hospitals, airlines, construction sites. Anywhere the wrong person on the job is expensive." | Anywhere the wrong person on the job is expensive. |
| 84.0–90.0 | End card | V1-10: headline, then the small line. | "Because the future of your work depends on who you Pik." | Because the future of your work depends on who you Pik. |

Narration total ≈ 175 words at ~165 wpm ≈ 64 s of speech inside 90 s; the Meet beat's two manager lines are on top of that, in their own gaps. If a line does not fit its beat, cut words from the line, not seconds from the beat.

**One name.** Carl's brief says "Adachi-san" because his storyboard did. The product's fixtures, the Slack card, the ticket and the Meet screen all render **Yui Sato** (`prototype/data/company.json`). **decided**: Yui Sato everywhere in the video; she/her. If Carl wants Adachi, the fixture rename touches `company.json`, `people.json`, the seeded Slack and Notion histories and the live prompt; tell him that cost before doing it.

## 4. Style rules (unchanged from V1 unless noted)

- Animated beats: bone `#EFEAE2` canvas, espresso `#2B2521` ink, sand `#E3DCD0` cards, clay `#B5654A` for one accent only, the black Pikbot. Inter Tight or Geist. Product beats: the product's own dark UI (`#0A0A0A` paper, `#EDEDED` ink, Geist) as captured. Slack and Gmail replicas: their real light UIs, over white, so the suck-in reveals white.
- No music. No jargon. No real faces (the storyboard's stock portraits are placeholders; do not ship them). No zooms except the two written above. Cursor moves slowly and once per beat.
- Typewriter for every text change Pik "thinks" (Carl's instruction), mask-reveal for headlines, a single hop for Pikbot's jump.
- Nothing from the VP meeting that is a figure or an internal matter (PRD §0.1 public-repo rule; the self-check grep in that section must stay clean). Interviewees are roles, never names. Fictional company (Kaede Works), fictional people.
- The disclosure is the first frame, always.

## 5. How to build it (the V1 pipeline, reused)

1. `git pull` on `main` (Steven's UI push, Carl's Figma nodes). Put the AirDropped folder at `deck/video/_assets/` (git-ignored; see its `MANIFEST.md`). Never commit it.
2. Figma: make frames `V2-00` … `V2-11` at 1920x1080 on Page 1 at y=20000, reusing the V1 components. Motion keyframes per beat. `export_video` each top-level frame (1920 wide, 30 fps, high) into `deck/video/v2/renders/<beat>.mp4` with the ids in the table (`00_disclosure`, `01_blur`, `02_asked`, `03_asks`, `04_meetpik`, `05_mining`, `06_receipts`, `07_meet`, `08_slack`, `09_ticket`, `10_verticals`, `11_end`).
3. Product captures: `cd prototype && make run-heuristic` (port 8787), then Playwright (`../record_meet.py` and `record_candidate.py` show the pattern; the venv recipe is in `../README.md`). Capture the new network-graph UI in `?present=1` for the Meet beat and the stage file.
4. Narration: section 6. Ids stable so the build rows map.
5. Stitch: `python3 deck/video/v2/build_v2.py` (copy of `../build.py` with the new `SEGMENTS`, `OUT = pik_90s_v2.mp4`, `V = v2/vo`, `R = v2/renders`). It writes `TIMING.md`.
6. Stage file: a second `SEGMENTS` table in the same script, `OUT = meet_stage_demo.mp4`, Meet beat only, with 4–6 s silent holds before each pop so Carl and Steven can speak; write `STAGE_CUES.md` from it.
7. Look at both renders end to end before saying done (play them; check the ffprobe duration ≤ 90.0; check the captions are inside the safe area). Commit as yourself with no attribution lines; `git pull` before every push, Carl pushes too.

## 6. TTS on the shared GCP project (no API key)

**Carl**: use TTS on the project Recruit allocated to us so nobody records at 3 a.m. Project id: **`recruit-hackathon-2026-e`**. Verified Sat 20:52 PDT: `gemini-3.8-flash-tts` is **not** offered on Vertex in this project (404 in `us`, `us-central1`, `global`) and Cloud Text-to-Speech is 403 for our accounts. What works is **Gemini 3.8 Live on Vertex** (`gemini-3.8-live`, `us-central1`), the same model the Meet bot uses: send a text turn, get 24 kHz PCM back. `deck/video/v2/narrate_vertex.py` does exactly that and is tested (two lines rendered from this machine, `v2/vo/01_blur.wav` and `03_meet.wav`).

```bash
cd prototype && make setup                     # google-genai into prototype/.venv
gcloud auth application-default login          # the account Recruit added to the hackathon group
prototype/.venv/bin/python deck/video/v2/narrate_vertex.py            # all LINES, --rate 1.12
prototype/.venv/bin/python deck/video/v2/narrate_vertex.py --only 05  # one id
```

Edit `LINES` in that file to the section 3 narration (voice Charon for the narrator, Puck for the manager). The style string is a system instruction; the text is read verbatim. If a Live session returns nothing, the script exits non-zero; rerun that id. Fallback only if Vertex is down: `../narrate.py` with a `GEMINI_API_KEY` from AI Studio created on the same project.

## 7. What is not yours to decide, and what to hand Carl

- Do not send anything to anyone. Do not touch `PRD.md`, the deck, or `prototype/` logic. If the engine lacks something the video needs, say so in the commit, do not fake it in the fixtures.
- Hand Carl at most three items when you stop, each with the path. He reads fast; lead with the file.
- Open questions only he can answer, listed once: (1) the tagline pick in beat 5; (2) Yui vs Adachi; (3) whether Steven records the two manager lines himself or Puck stays.
