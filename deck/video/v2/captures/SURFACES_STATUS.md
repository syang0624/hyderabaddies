# Real surface takes (Sat Sep 26, 22:40–22:45 PDT)

Both takes are real: the Slack bot and the Notion watcher ran on Carl's Mac against the engine on :8787, and the takes were driven in Carl's own Dia (AppleScript + JavaScript; Dia relaunched once with `--enable-applescript-javascript`). Nothing is overlaid.

| File | What happens | Length |
|---|---|---|
| `slack_real.mp4` | #growth-analytics. The question "who's best to run pricing experiments with the US product team?" is typed and sent; Pik answers in under a second with Yui Sato (tags without levels, two verbatim receipts, load, two alternates, the no-score footer); "Loop in Yui" is pressed and Pik posts the loop-in. Recorded from the screen, cropped to the page. | 20 s |
| `notion_real.mp4` | Tickets board. A new ticket "Pricing page A/B test with the Northwind team" is created (API, as a teammate would) and appears at ~3.3 s; the Pik watcher fills Suggested owner (Yui Sato, alternates), Why (tags, one verbatim receipt with source, load) and Receipts within ~2 s. Recorded from Dia's window only. | 18 s |
| `*_still.png` | One frame of each, after the answer lands. | |

Changes that made the takes read right (committed with them): the Slack card and the Notion Why no longer print skill levels like "(5/5)", which read as a score; "Loop in" now carries the question instead of a tag line; `PIK_SLACK_INLINE=1` makes the bot answer a top-level ask in the channel instead of a thread (demo setting; default unchanged).

Left in the workspace from rehearsal: in #pricing one earlier take, in #northwind-sync a question sent half-typed (Pik answered it with Rin Mori). Messages were not deleted.
