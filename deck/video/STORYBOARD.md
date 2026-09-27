# Pik, 90-second video: storyboard v1 (Sat Sep 26, 19:50 PDT, for Carl's review)

Premise change from the PDF: drop "Tokyo, Jul 30 2026". Open on the blur, not a date.
One demo only: the Meet take. Slack is one shot. Jira/Notion is cut (slot kept if Steven's clip lands).
Palette: bone / sand / espresso / clay / olive / stone. Inter Tight. No music. Followable with sound off.
Pikbot = the spring-antenna mascot from the Figma file. Blobs stay as the people (circle, rounded square, arch).

| t | Beat | Line (caption, burned in) | Frame |
|---|---|---|---|
| 0–3 | Disclosure | Recorded Sep 27. Fictional company and people. Live: listener tool calls, extraction, re-ranking. Templated: memo. | Bone card, espresso mono text, nothing else. |
| 3–9 | The blur | The line between jobs is blurring. | Big Inter Tight headline; the word "jobs" splits into three faint tags (HR, engineering, ops) that drift apart and overlap. |
| 9–15 | The pile | Who is the best person for… organizing the Recruit hackathon / a US–Japan work exchange / a job board for construction | Three asks stamp in one after another, each on a sand card, tilting and stacking into a pile. The pile gets tall. |
| 15–19 | Meet Pik | Meet Pik. | Pikbot slides in from the right, antenna bobbing, looks up at the pile, a squiggle appears over its head (confused). Beat. Lightbulb. Antenna springs straight. |
| 19–31 | The mining | It reads what she already wrote and shipped. Every line keeps its source. | Pikbot grabs a magnifying glass and darts into a Slack logo, then Gmail, then a Doc, then a ticket. Each visit pulls one line out as a white receipt stub with a mono source line ("#pricing, Mar 12") and a "verbatim" stamp. Two stubs turn grey and drop off the bottom: "2 dropped, no source." |
| 31–36 | The pie | One person, from what they did. | The stubs slot around Adachi's blob like slices of a pie until it is whole. Three slices are labelled in her own words (pushes back, writes in English, ran the offsite). |
| 36–41 | Zoom out | Two hundred people. Always current. | Adachi shrinks; 199 more pies tile the canvas. One slice on a far pie flips as a new receipt lands. A small Slack ping on the corner = the reason. |
| 41–60 | Meet (real take) | Heard the criterion. Re-sorted on their words. No score. → Every line is a receipt. → What the meeting concluded. | Screen recording of the page in present mode. Steven says the Northwind line; the cards settle into a new order; matched receipts light up; Pik asks one follow-up out loud (caption: "Lead meetings in English, or write?"); the conclusion prints from the top. Narration in gaps only. |
| 60–67 | Slack | Ask where you already are. One press to loop her in. | Slack window (Steven's clip, or a still with a cursor): "who's best for the pricing write-up?" → ephemeral card: best person, two receipts, load this week, two alternates. Press "Loop in" → "@Yui, looping you in: …". |
| 67–75 | The other side | She sees the same page. She answers first. | Yui's blob at a phone. The same receipts, no rank, no other names. She adds a yellow sticky: "I'd rather build the team here first." The sticky lands on the manager's page. |
| 75–82 | Beyond | The next intern. The next pilot. Anyone the wrong pick is expensive for. | The pile from beat 3 returns, and new asks join it: "the intern for this pilot", "who mentors the new hire", "who is retiring from this team". Pikbot points at each; a pie appears under every one. |
| 82–90 | End card | Because the future of your work depends on who you Pik. | Headline, then small: Same page for both sides. A receipt on every line. No score. Your rubric. |

Narration slots (gaps only, ≤150 wpm): 3–9, 19–36, 67–75, 75–82. Silent: 0–3, 41–60 while Steven or Carl speaks, 82–90.

---

# v2, as built (Sat Sep 26, ~20:15 PDT) — see TIMING.md for exact starts

Changes from v1 after Carl's notes: Yui is the one name; Jira/Notion cut; the three asks are now hackathon / one-on-one evaluation / construction job board (distinct flavours, not two exchange-shaped asks); the mining beat is the polished one (Pik sucks verbatim Slack and Gmail lines Kirby-style, skips the DM stub, jumps between sources, then the receipts settle around Yui and two unsourced lines drop out). Built in Figma Motion (frames V1-00 … V1-10), stitched by build.py, narrated by Gemini TTS so timing is replicable.

| start | beat | source |
|---|---|---|
| 0.0 | Disclosure | Figma V1-00 |
| 3.0 | The blur (over Shibuya b-roll, multiply) | Figma V1-01 |
| 7.0 | Three asks (over office / portrait b-roll) | Figma V1-02 |
| 15.0 | Meet Pik (slide in, blink, antenna, eyes) | Figma V1-03 |
| 19.5 | Mining: Slack → Gmail | Figma V1-04a |
| 30.5 | Receipts ring, two dropped | Figma V1-04b |
| 37.0 | Zoom out to 200 | Figma V1-05 |
| 42.5 | Meet (stand-in replay; real take goes here) | captures/meet_replay.webm |
| 61.5 | Slack card, loop in | Figma V1-07 |
| 68.5 | Candidate's page, Yui's note | captures/candidate.webm |
| 75.0 | Beyond: mentor / one-on-one / intern | Figma V1-09 |
| 81.5 | End card | Figma V1-10 |
| 88.0 | end | |
