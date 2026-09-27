# Pik 90-second video, V2: the cut as built

Built Sat Sep 26 2026, ~22:50 PDT. Output `pik_90s_v2.mp4` (1920x1080, 30 fps, H.264 + AAC, 90.0 s). `TIMING.md` is written by every build and is the authority on starts and offsets; this table is the intent.

Legend: **animated** = an HTML beat in `html/`, rendered frame by frame by `render.py` (deterministic, `window.seek(ms)`); **replayed** = the real product page driven by a scripted event log (`record_meet.py` writes `prototype/state/live.jsonl` while Playwright records `localhost:8787/?present=1&before=1`); **replica** = a sibling-built HTML replica of a third-party app (Slack, Gmail, a Linear-style ticket) with the real bot's card layout. Narration: Gemini 3.8 Live on Vertex (`narrate_vertex.py`), Charon for the narrator at 1.22x, Puck for the manager at 1.15x.

| # | Beat | dur | What is on screen | Kind | Narration | Caption (burned) |
|---|---|---|---|---|---|---|
| 00 | Disclosure | 2.2 s | Bone card, mono text: recorded date, fictional company, what is live | animated | silent | none (on screen) |
| 01 | The blur | 5.2 s | `HR · Engineering · Design · Sales · Ops` with rules; the rules blur and dissolve, the words drift into one blob character; the blob rises and the headline mask-reveals | animated | "In a post-LLM world, the line between what one person can do is blurring." | none (the headline is the line) |
| 02 | We asked | 8.2 s | Three quote cards typewriter in, roles only, no names or company; they stack behind "Decided from memory." | animated | "We asked people at Recruit Holdings what their hardest problem in HR is. Every answer was the same shape: who does what next, decided from memory." | Team formation. Internal mobility. Decided from memory. |
| 03 | The asks | 6.8 s | Three asks stamp in and pile up (interns, pricing task force, two-year exchange); three blobs look up at the pile | animated | "Who is the best person to mentor the interns? To lead the pricing task force? For the two-year exchange? Same question, every week." | Same question, every week. |
| 04 | Meet Pik | 4.0 s | Pikbot slides in, antenna springs, blinks; "Meet Pik." then the tagline | animated | "Meet Pik. It knows who's done what, and answers where you ask." | none (the tagline is on screen) |
| 05 | Mining | 11.5 s | Slack then Gmail replica; Pik pulls the pieces in, white underneath; `+ Yui's Slack` / `+ Yui's email` typewriter remarks; one hop | replica (sibling) | "Pik reads what Yui already wrote and shipped, where the company allows. Every line keeps its source." | It reads what she already did. / Every line keeps its source. DMs never. |
| 06 | Receipts, zoom out | 4.3 s | Six verbatim stubs (Yui's real Slack lines from `company.json`'s fixtures) settle around her blob; two unsourced lines drop; the stubs fold into her and the frame zooms out to 200 blobs; one far blob flips as a clay receipt lands | animated | "Two hundred people. Always current." | Two hundred people. Always current. |
| 07 | Meet | 18.9 s | The real page. The "today" view (three notes from memory) while the manager speaks; the stage composes on the criterion: the heard line, three tiles re-sorted, Yui's own words (verbatim) and Okada's note (paraphrase) open, then the meeting's conclusion | replayed | Manager (Puck) starts 1.8 s before the cut; narrator "It hears the criterion and re-sorts on their words. No score."; Manager (Puck) "Okay, let's set up calls with Yui and Kei this week..." | Heard the criterion. Re-sorted on their words. No score. / Her own words, and what her manager wrote. Both attached. / What the meeting concluded. Receipts attached. |
| 08 | Slack | 8.0 s | Full Slack replica, `#pricing-team`; "who's best to lead the pricing task force?"; the real bot card; Loop in Yui pressed | replica (sibling) | "Or ask in Slack. One press to loop her in." | Ask where you already are. One press to loop her in. |
| 09 | The ticket | 9.5 s | Linear-style dark issue "UI refresh"; lines type in; Assignee opens itself and picks Yui Sato; the ? shows two receipt stubs | replica (sibling) | "On a ticket, it fills in the owner, and shows why." | One click to assign. The why is attached. |
| 10 | Verticals | 6.8 s | Four asks stamp in around Pikbot (hospital, airline, construction, any company), a receipt ring draws under each blob; Pik looks at each | animated | "The same map answers hospitals, airlines, construction sites. Anywhere the wrong person on the job is expensive." | Anywhere the wrong person on the job is expensive. |
| 11 | End | 4.6 s | "Because the future of your work depends on who you Pik." (Pik in clay), the small line, Pikbot blinks | animated | "Because the future of your work depends on who you Pik." | none (the headline is the line) |

Total 90.0 s. No stock footage, no faces, no overlaid stills. Captions are burned by `build_v2.py` (PIL, Geist Medium, bottom-centre pill; espresso on light beats, bone on the dark product beats), so their timing is re-tuned without re-rendering.

## Rebuild

```bash
deck/video/pw/bin/python deck/video/v2/render.py            # every html/ beat -> renders/
deck/video/pw/bin/python deck/video/v2/record_meet.py       # needs `cd prototype && make run-heuristic` on :8787
GOOGLE_APPLICATION_CREDENTIALS=... prototype/.venv/bin/python deck/video/v2/narrate_vertex.py --only 02   # one line
python3 deck/video/v2/build_v2.py                            # the stitch; writes TIMING.md
deck/video/pw/bin/python deck/video/v2/preview.py 06 1200 3000   # contact sheet of one beat at chosen ms
```

## Open questions only Carl can answer
1. The tagline in beat 04 (this cut uses "Meet Pik. It knows who's done what, and answers where you ask.").
2. Yui vs Adachi (the fixtures, the Meet page, the Slack card and the ticket all say Yui Sato; this cut says Yui everywhere).
3. Whether Steven records the two manager lines himself or Puck stays.
