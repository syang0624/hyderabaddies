# Pik 90-second video, V5: the plan as built (the real Meet take in the middle)

Written Sun Sep 27 2026, ~01:00 PDT. Output `pik_90s_v5.mp4` (1920x1080, 30 fps, H.264 + AAC, ≤ 90.0 s). `TIMING.md` is written by every build and is the authority on starts, speeds, trims and caption windows; this table is the intent. Until the take lands, a 40 s page-coloured slate stands in its slot so the timing can be checked.

Why V5: Carl rejected V4 ("missing its beats, not engaging, the new-hire beat unclear"). The new-hire (08b) and Yui's-page (08c) beats are out. The front is tightened to about 29 s. The Meet beat is the real thing: Carl and Steven inside a Google Meet with Pik as a participant, recorded with Cap (`prototype/MEET_TAKE.md`, the 42 s hackathon story), its own sound kept (their voices, Pik's voice), no narration over it, the music ducked under it, three captions at most.

Brand: one, the screen's (`../v2/html/assets/shared.css`: page #fafafa, white cards with the hairline shadow, ink #171717, one lime accent #D6F25A; the mascot is the screen's Pik mark). Captions: an ink pill with white text on every beat. Music: Kosmose Vaikus by Kevin MacLeod, incompetech.com, CC BY 4.0, -26 dB under any voice, -18 dB in gaps.

Legend: **animated** = a V2 HTML beat rendered on the tokens (`../v2/renders`), played faster to its new length (frames dropped, nothing cut); **real take** = Carl's recordings (the Meet, the Slack workspace, the Notion board); the Slack and Notion takes carry the V2 Pik mascot composited on them. Narration: `vo/` (V5 re-cut lines, Charon 1.35x) with `../v3/vo` as the fallback.

| # | Beat | dur | What is on screen | Kind | Narration | Caption (burned) |
|---|---|---|---|---|---|---|
| 00 | Disclosure | 2.0 s | Page-colour card, ink mono text: recorded date, fictional company, what is live | animated | silent | none |
| 01 | The blur | 3.5 s (x1.57) | `HR · Engineering · Design · Sales · Ops`; the rules dissolve, the words become one blob; the headline mask-reveals | animated | "The line between roles is blurring." | none |
| 02 | We asked | 6.0 s (x1.4) | Three white quote cards typewriter in, roles only; they stack behind "Decided from memory." | animated | "We asked people at Recruit Holdings. Every answer was the same shape: who does what next, decided from memory." | Team formation. Internal mobility. Decided from memory. |
| 03 | The asks | 4.0 s (x1.75) | Three asks stamp in and pile up; three blobs look up | animated | "Who should mentor the interns? Lead the pricing task force? Take the two-year exchange?" | Same question, every week. |
| 04 | Meet Pik | 3.2 s (x1.31) | The Pik mark on its lime disc slides in, antenna springs, blinks; "Meet Pik." then the tagline | animated | "Meet Pik. It knows who's done what, and answers where you ask." | none (the tagline) |
| 05 | Mining | 7.0 s (x1.64) | Slack then Gmail replica; Pik pulls the pieces in, white underneath; the `+ Yui's Slack` / `+ Yui's email` remarks | animated | "Pik reads what Yui already wrote and shipped, where the company allows. Every line keeps its source." | It reads what she already did. / Every line keeps its source. DMs never. |
| 06 | Receipts, zoom out | 3.5 s (x1.29) | Six verbatim stubs settle around her blob, two dropped, zoom out to 200 blobs, one flips as a receipt lands | animated | "Two hundred people, or twenty thousand. Always current." | Any size. Always current. |
| 07 | Meet, the real take | 38 to 42 s | Carl and Steven in a real Google Meet, Pik presenting its screen: hellos; Pik asks what the person needs to have done; Steven's ask; Rin and Yui appear with their receipts, Pik reads them; Rin's receipt with its channel; "Let's ask Rin and Yui this week"; the conclusion card prints, Filed | real take (`captures/meet_real.mov`, own audio) | none (their voices and Pik's) | Pik joined the call. [0.5–4] / Two people with receipts for the ask. Word for word. [when Rin and Yui appear] / Filed. Both of them see the same page. [the conclusion] |
| 08 | Slack | 7.6 s | The real Slack workspace: the question, the real bot card, Loop in Yui; Pik on it | real take (V2) | "Or ask in Slack. One press to loop her in." | Ask where you already are. One press to loop her in. |
| 09 | The ticket | 9.0 s | The real Notion board: a new row, Pik fills Suggested owner, Why and the Receipts link | real take (V2) | "On a ticket, it fills in the owner, and shows why." | A new ticket. Pik fills in the owner, and the why. |
| 10 | Verticals | 4.0 s (x1.75) | Four white cards stamp in around the Pik mark (hospital, airline, construction, any company), a lime receipt ring under each | animated | "Hospitals. Airlines. Construction sites. Anywhere the wrong person is expensive." | Anywhere the wrong person on the job is expensive. |
| 11 | End | 3.6 s (x1.39) | "Because the future of your work depends on who you Pik." (Pik on a lime highlight), the small line, the music credit, the mark blinks | animated | "Because the future of your work depends on who you Pik." | none |

Front 29.2 s, tail 24.2 s, take 38 to 42 s: 91.4 to 95.4 s before the fit rule. **The total must be ≤ 90.0 s**, so `build_v5.py` trims the front in this order, each to a floor: mining 7.0 → 6.0, asked 6.0 → 4.5, blur 3.5 → 3.0, asks 4.0 → 3.5, receipts 3.5 → 3.0, verticals 4.0 → 3.6, and exits if the take still does not fit (shorten it with `--in`/`--out`). With a 40 s take: mining 6.0, asked 4.5, blur 3.0, asks 3.6 (front 26.8 s). Narration lines were re-cut so every one fits its floor.

## When the take lands

```bash
# 1. put it at deck/video/v5/captures/meet_real.mov (or .mp4; git-ignored, any size or aspect)
# 2. look at frames, note: --in = first hello, --out = two seconds after the conclusion card, --marks = when Rin and Yui appear, when the conclusion prints (seconds after --in)
python3 deck/video/v5/build_v5.py --take deck/video/v5/captures/meet_real.mov --in 2.5 --out 44.0 --marks 13.5,33.0
# 3. read TIMING.md (it lists every trim, speed, caption window and any narration overrun), extract stills, look, push
```

Rebuild the front: `deck/video/pw/bin/python deck/video/v2/render.py` (renders on the tokens), `deck/video/pw/bin/python deck/video/v3/render.py 11`; narration for the re-cut lines: `GOOGLE_APPLICATION_CREDENTIALS=... prototype/.venv/bin/python deck/video/v5/narrate_v5.py --takes 2 --keep-shorter`.
