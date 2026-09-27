# New thread: the 90-second demo video for Pik (Innovation Cup 2026, due Sun Sep 27, 11:00 AM PDT)

Run `date` first. Everything is in `~/CODELocalProjects/hyderabaddies` (public repo `syang0624/hyderabaddies`; pull before every push; commit as Carl Kho <carl@somach.life>, no attribution lines). Read, in this order: `PRD.md` Part A (§0 to §7, it is short), `PRD.md` §9.3a (the shot list and the exact lines that pass the live regression), `deck/JUDGE-MAP.md`, `prototype/README.md`. Do not read Part B of the PRD unless a fact is missing.

## What Pik is, in one breath
It tracks your achievements for you (what you wrote and shipped, with the original attached) and answers "who is the best person for this?" wherever you already work: a Google Meet, a Slack channel, a ticket board. No score. The person named sees the same receipts. Your company keeps its own rubric.

## What runs (all on `main`, all verified)
- `prototype/`: `make run-heuristic` serves the receipts page at `localhost:8787` (`?present=1` for recording, `?before=1` opens on the "Today" view: three manager notes from memory, which flips to receipts when the criterion is heard; `?as=yui` is what the candidate sees; `?q=<question>` prefills a question).
- `make live` (mic → Gemini 3.8 Live on Vertex → tool calls): the page re-sorts on the spoken criterion within a second, asks one follow-up out loud when the ask is vague, prints the conclusion when they agree. `make live-sim` plays a scripted call through it (last runs 6/6, 0 drops); use it to rehearse without a mic.
- `make ask Q="..."`: the engine over a fictional company of 200 people.
- Slack bot and Notion board surfaces: `make slack`, `make notion` (Steven is setting up the workspaces; issue syang0624/hyderabaddies#5). If his 10 to 15 s recordings are not in the repo yet, storyboard those two beats and leave a slot.

## The video
- 90 seconds or less, 1920×1080, submitted as a link or file with the deck (PDF) and the public repo. First frame is a disclosure card: fictional company and people; what is live vs templated.
- Style: Grok Bot's launch page (x.ai/grok-bot): near-white canvas, one calm column, gradient blobs as characters with names, one plain sentence per message, motion that guides the eye. Our palette is earthy, not neon: bone #EFEAE2, sand #E3DCD0, espresso #2B2521, clay #B5654A, olive #6B7048, stone #8C847A. Typeface: Inter Tight (or Geist). No music. No jargon. A manager with a full plate must follow it with the sound off.
- The blobs tell the story (Carl's sketch): a blob looks at a big question ("Who is the best person for this?"); receipts gather for one person, then zoom out to 199 more, always current; then the product in the three tools; then "the person sees the same receipts"; then the future (hiring, skills gaps, any vertical where the wrong person on the job is expensive); end card: "Same page for both sides. A receipt on every line. No score."
- Beats and budget: 0–3 disclosure · 3–12 the question · 12–25 receipts gather, zoom out to 200 · 25–50 Meet (real recording of Carl and Steven; the page re-sorts, the bot asks its one follow-up, the conclusion prints) · 50–62 Slack (the card, one press to loop someone in) · 62–72 Notion board (the ticket fills itself in) · 72–82 the candidate's view and the note · 82–90 end card.
- Captions burned in, one sentence each, from PRD §9.3a. Narration only in gaps, never over a spoken line.

## Your job in this thread
1. Produce a storyboard (one line + one frame description per beat) and confirm it with Carl before rendering anything.
2. Build the animated beats (question, gathering/zoom-out, blobs, end card) as HTML/CSS/SVG or Motion-style compositions Carl can render or screen-record; Carl was a motion designer and will cut in Cap. Keep every asset in `deck/video/`.
3. Capture the product beats from the running prototype in present mode (stills exist in `deck/assets/v5c_*.png`; recapture if the UI changed). Real Gemini Live footage comes from Carl and Steven's take; script and setup are in PRD §9.3a.
4. Keep the deck's four solution slides in sync with the video (Slides artifact: https://claude.ai/artifact/LFhPNTRDq3F5tKCb8wpYWZ).

## Rules
- Nothing about the VP's figures or internal matters (PRD §15, `sync.md` §J). Interviewees unnamed on screen. No real faces.
- Every message to another person is a draft for Carl to send.
- Look at the real render before saying it is done. Cap what you hand Carl at three items.

## Carl's storyboard export (Sat ~20:30): `deck/video/STORYBOARD_v4_figma.pdf`
Read it first for the flow and tone; a few beats have since changed (the product is now called **Pik**; the Meet screen is composed live from primitives; the receipts page is the "why" layer). Its spine: "Who is the best person for X" (three asks: the hackathon, the US-Japan exchange, a construction job board) → "Meet Pik, the company intelligence AI that works wherever you are" → Pik reads Slack and mail and learns who knows what ("Adachi-san is an expert in xyz") → Pik helps the team decide who does the exchange, then who leads the team → "Because the future of your work depends on who you Pik."
