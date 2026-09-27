# Pik 90-second video, V5: the cut as built, around the real Meet take

Built Sun Sep 27 2026, ~02:20 PDT. Output `pik_90s_v5.mp4` (1920x1080, 30 fps, H.264 + AAC, **90.00 s**). `TIMING.md` is written by every build and is the authority on starts, narration offsets and the visual event each line lands on; this table is the intent.

What changed from V4 (Carl's feedback on the V5 slate cut, item by item): no speed-ups (every beat plays at 1.0x; V4's 1.3 to 1.9x are gone); narration re-cut and re-rendered at 1.15x, calm, words cut where a line did not fit; the disclosure card removed; the end card keeps only the headline and the tiny credit; the Recruit wordmark (typography only, Geist) with "Team formation." popping first and alone, then the three quotes, then "Decided from memory." on the words that say it; a "Meet Yui." bridge before the mining; the mining beat rebuilt: "Her Slack" title, the replica at 1.5x so its text reads on a small screen, the vacuum, the surprise line typed large and held 1.2 s, then "Her email" the same way; the receipts gather, pulse once, the two unsourced fade and drop, 2.4 s; a 1 s bridge into the Meet ("Pik joins the call." over the recording's first second) and a 2 s conclusion page after it; the real take in the middle with its own sound; the Slack and Notion takes with slow push-ins; no new-hire or Yui's-page beats; no caption pills anywhere (every word is in the beat's own type); music stays, ducked under any voice.

Brand: one, the screen's (page #fafafa, white cards with the hairline shadow, ink #171717, one lime accent #D6F25A; the Pik mark on a lime disc). Music: Kosmose Vaikus by Kevin MacLeod, incompetech.com, CC BY 4.0, -26 dB under any voice, -18 dB in gaps.

| # | Beat | start | dur | What is on screen | Kind | Narration (1.15x) |
|---|---|---|---|---|---|---|
| 01 | The blur | 0.0 | 3.4 s | `HR · Engineering · Design · Sales · Ops`; the rules dissolve, the words become one blob; the headline mask-reveals at 2.25 s | animated (`html/01_blur.html`) | "The line between roles is blurring." at +1.0 |
| 02 | We asked | 3.4 | 7.6 s | "WE ASKED PEOPLE AT" / **RECRUIT HOLDINGS** (Geist wordmark) → "Team formation." pops alone, big, then rises to a heading → three white quote cards type in (roles only) → they stack behind "Decided from memory." | animated (`html/02_asked.html`) | "We asked people at Recruit Holdings." +0.15 · "Team formation." +2.5 (the pop) · "Every answer: who does what next, decided from memory." +3.9 (the reveal at 6.45 lands on the last words) |
| 04 | Meet Pik | 11.0 | 4.3 s | The Pik mark on its lime disc slides in, antenna springs, blinks; "Meet Pik." then the tagline | animated (V2 render, 1.0x) | "Meet Pik. It knows who's done what, and answers where you ask." +0.1 |
| 04b | Meet Yui | 15.3 | 3.6 s | Yui's disc (lime tint), "Meet Yui.", her role; "Pik lives where she works." at 1.9 s; "her Slack · her email" at 2.6 s | animated (`html/04b_meetyui.html`) | "Pik knows how Yui is doing: it lives where she works." +0.2 |
| 05 | Her Slack, her email | 18.9 | 8.8 s | "Her Slack" title over the replica at 1.5x (message text ≥ 22 px); the antenna reaches in, the pieces are vacuumed, white left behind; "+ Yui's Slack"; typed large and held: **"Oh. She took the partner review herself."** Then "Her email", the Gmail Sent replica at 1.5x, the vacuum, "+ Yui's email", typed and held: **"She proposed the registry fields. Northwind adopted two."** | animated (`html/05_mining.html`, re-timed from the V2 beat) | "It reads what she already wrote, where the company allows." +0.4 |
| 06 | Receipts | 27.7 | 2.4 s | Six verbatim stubs gather around Yui (matched words lime-underlined), one pulse, the two unsourced lines fade and drop | animated (`html/06_receipts.html`) | "Every line keeps its source." +0.3 |
| 07a | Bridge | 30.1 | 1.0 s | The recording's first second (Pik presenting, before the hellos) under a scrim: **"Pik joins the call."** | real take frames + title | none |
| 07 | The Meet | 31.1 | 42.3 s | Carl and Steven in a real Google Meet, Pik presenting its screen: the hellos ("who should lead the company hackathon"), Pik asks what the person needs to have done, Steven's ask, the words drift in and Rin and Yui appear with receipts, Carl asks what Rin actually did, Pik reads Rin's receipt with its channel, "Let's ask Rin and Yui this week", the conclusion card prints, "Filed", "Thanks, Pik." | **real take** (`captures/meet_real.mp4`, own audio: their voices and Pik's) | none |
| 07b | Conclusion | 73.4 | 2.0 s | The presented page itself, scaled up: "What this meeting concluded", Rin and Yui, the next step | still from the take (60.2 s) | none |
| 08 | Slack | 75.4 | 6.2 s | The real Slack workspace, whole window, then a 3 s push-in to the composer where the question is typed; Pik's card lands; Loop in | real take (V2), push-in | "Or ask in Slack. One press to loop her in." +0.3 |
| 09 | The ticket | 81.6 | 5.0 s | The real Notion board, then a 2.5 s push-in to the row Pik fills (owner, why, receipts); held on the filled row | real take (V2), push-in | "On a ticket, it fills in the owner, and shows why." +0.2 |
| 11 | End | 86.6 | 3.4 s | "Because the future of your work depends on who you Pik." (Pik on the lime highlight) and the music credit in tiny mono | animated (`html/11_end.html`) | "Because the future of your work depends on who you Pik." +0.1 |

Front 30.1 s, Meet 45.3 s (bridge + take + conclusion), tail 14.6 s. Total 90.00 s.

## The take, exactly

`captures/meet_real.mp4`: 63.0 s, 1920x1240, a Cap screen recording of the Dia window. Crop: `crop=1920:1080:0:136` (the macOS menu bar and Dia's tab strip are the top 136 px; the Meet fills the rest, the presented Pik page left and the three tiles right, all kept). Kept windows (tape seconds) with 0.3 s cross-dissolves on video and audio between them:

| kept | what | cut before it |
|---|---|---|
| 9.30–25.55 | the hellos, Pik's first line ("Since you're on that, I can help..."), Steven's ask, 0.6 s of air | 0–9.30: the pre-roll (its first second is the bridge) |
| 29.55–39.95 | 0.75 s of air, Pik's second line (the words drift in, Rin and Yui appear), Carl's "what did Rin actually do?", 0.55 s | 25.55–29.55: dead air (nothing changes on screen) |
| 42.45–52.50 | 0.73 s of air, Pik reads Rin's receipt (the receipt flashes on the right at 43.4), Steven's "Great, let's ask Rin and Yui this week", 0.5 s | 39.95–42.45: dead air |
| 54.50–60.85 | 0.7 s of air, Pik's "Filed" (the conclusion card prints at 55.6), "Awesome. Thanks, Pik.", 0.3 s | 52.50–54.50: dead air; 60.85–63.0: the tail |

42.30 s after the dissolves. The take's audio is loudnorm'd on its own (-16 LUFS) and placed at the beat's start; the bed ducks under it like under narration. The conclusion still is the page region `crop=1350:754:34:274` at 60.2 s, scaled to 1920 wide.

## Rebuild

```bash
deck/video/pw/bin/python deck/video/v5/render.py                 # the V5 html beats -> renders/
GOOGLE_APPLICATION_CREDENTIALS=... prototype/.venv/bin/python deck/video/v5/narrate_v5.py --takes 2   # vo/ at 1.15x
python3 deck/video/v5/build_v5.py                                # the cut; --windows "a-b,c-d,..." to re-cut the take
```
