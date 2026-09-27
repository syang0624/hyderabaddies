# Slack and Notion takes: status (2026-09-26, 22:21 PDT)

**Not recorded yet.** The bot and the watcher are running on Carl's Mac; the blocker is browser control, not Pik.

## What is running
- Slack bot `surfaces/slack_bot.py` (posts as "Pik"), Notion watcher `surfaces/notion_board.py`, engine `server.py` on :8787 (keyword backend). Logs: `prototype/state/slack_bot.log`, `prototype/state/notion_board.log`.
- Slack: the seeded channel is **#pricing** (the bot is a member; Carl may need to click Join first). Every seeded channel exists, including #search-relevance.
- Notion: 12 rows. The three "new" seeded rows are already filled (status "Owner suggested"). Two untitled blank rows sit at the top; the watcher skips them.

## Why no take
The Chrome extension could not open its own tab group in Dia ("Tab not found for session ID", seven tries on Browser 1 and Browser 2). Further attempts were then blocked as interfering with the other agent's session in the same browser. The Claude browser pane is signed out of both Slack and Notion. Nothing was posted or added anywhere.

## Two script fixes before anyone records (checked against the engine on this Mac)
1. **Slack line.** `who's best to lead the pricing task force?` returns **Rin Mori**, so the button reads "Loop in Rin". To get "Loop in Yui", type:
   `who's best to run pricing experiments with the US product team?`
   Card: Yui Sato, Product operations, Pricing. Also: Rin Mori, Yuto Murakami. 2 open tickets, 24 h this week.
2. **Notion row.** Title `UI refresh` with description `Rework the receipts page navigation before the Nov launch` makes Pik ask a follow-up instead of naming an owner: Why becomes "Pik asks: Is this for the Tokyo side or the partner side, and by when?" and Suggested owner stays empty. Add one sentence to the description:
   `Rework the receipts page navigation before the Nov launch. Needs a product designer.`
   Fills: Shota Schulz (Product designer, Design), also Gen Haddad, Mei Fukuda.

Exact card blocks and the Notion fill are in `engine_answers_for_surfaces.json`. If Steven runs the engine in Gemini mode, the names can differ.

## Two-minute take, for whoever has the browser
1. Dia window full screen on the main display, Slack open in #pricing.
2. `screencapture -v -V 25 -x _slack_raw.mov` in a terminal, then type the Slack line above, Enter, wait for the card, hover 2 s, click "Loop in Yui".
3. Notion: open the board, `screencapture -v -V 20 -x _notion_raw.mov`, add the row above, wait about 5 s.
4. Crop to 1920x1080: `ffmpeg -i in.mov -vf "crop=2624:1476:0:150,scale=1920:1080:flags=lanczos,fps=30,format=yuv420p" -c:v libx264 -crf 20 -an out.mp4`

DRAFT, not sent. Carl to Steven, only if Steven is the one recording:
> DRAFT: Bot and watcher are live on my Mac. Can you screen-record #pricing: "who's best to run pricing experiments with the US product team?" then Loop in Yui, and add a Notion row "UI refresh" / "Rework the receipts page navigation before the Nov launch. Needs a product designer."?
