# Deck and demo video

- `final/Pik Pitch Deck/index.html`: the canonical pitch deck, a web page (arrow keys move, each slide builds on a keypress, N shows the speaker notes). Steven's final deck, with the fine-tune slides from `site/` merged in ("The fine-tune, on one ask" and the measured chart, after "Technical design, next").
- `hyderabaddies.pdf`: the submission PDF, the static export of the canonical deck. `Pik_deck.pdf` is the same file, so only one deck PDF is in circulation. Re-render from `deck/`: `pip install playwright pillow`, `playwright install chromium`, `python3 site/render_pdf.py --png-dir /tmp/pik_render --no-notes`. The renderer fails on an overflowing source line, a team member's name on a slide, or the word "receipt" in the final deck.
- `final/Pik Pitch Deck/data/ft_metrics.js`: the numbers on the measured slide, written with `site/data/ft_metrics.js` by `site/sync_metrics.py` from `finetune/results/metrics.json`.
- `site/`: the earlier version of the deck.
- `pik_demo_90s.mp4`: the 90 second demo (1920x1080). Music: "Kosmose Vaikus" by Kevin MacLeod, incompetech.com, CC BY 4.0.
- `assets/`: stills of the running prototype.

Privacy notice from the organisers: the deck carries the team name only, no individual names. The title slide says hyderabaddies, and the name labels in the Meet and Slack stills are blurred.
