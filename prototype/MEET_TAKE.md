# The Meet take, hard-coded (Sun 01:05 plan, replaces the five-line HR script)

Pik's part is scripted on ONE cue: its four spoken lines and every screen change run on a fixed clock. You two speak between them. Judges are tired: the whole take is one small story in about 42 seconds.

## The story on tape

| tape s | who | what happens |
|---|---|---|
| 0 to 6 | Carl and Steven | Hellos. Steven: "Hey Carl. Let's figure out who should lead the company hackathon this year." Carl: "Yeah, I never know who's actually done this before." |
| 6 | CUE | Carl presses SPACE on the Pik tab (or runs `make take NAME=hackathon`). Pik's clock starts at 0. |
| 6 to 10 | Pik (voice) | "Since you're on that, I can help. What does the person need to have done?" The waveform moves with its voice. |
| 10 to 15.5 | Steven | "Someone who has run a cross-team event, and can present the outcome to the exec team." |
| 15.5 to 23 | Pik | Words drift in from the centre; Rin and Yui appear with their receipts; Pik: "Two people have receipts for that. Rin presented the pricing roadmap to the exec team. Yui ran the Northwind syncs in English. On screen, word for word." |
| 23.5 to 25.5 | Carl | "What did Rin actually do?" |
| 26 to 32.5 | Pik | Rin's receipt flashes on the right with its channel; Pik reads it: "Rin wrote: I'll present the pricing analytics roadmap to the exec team on the ninth. Slack, growth analytics, June." |
| 33 to 35 | Steven | "Great. Let's ask Rin and Yui this week." |
| 35.5 to 39 | Pik | The conclusion card prints, Rin and Yui light up. Pik: "Filed. Rin and Yui can see this same page." |
| 39 to 42 | Carl | "Thanks, Pik." Hold on the card. Stop. |

Pik's clock (from the cue): speaks 0 to 4, screen grows at 9.5, speaks 10.2 to 17, receipt at 20, speaks 20.2 to 26.6, conclusion at 29.5, speaks 30 to 33, filed at 33, end at 36. Your lines sit in the holds: 4 to 9.5, 17.5 to 19.5, 27 to 29. Speak at a normal pace and stop; do not fill silence.

## Setup
1. `prototype/dia_pik.sh` once (Dia relaunches with the Meet flags), then `prototype/meet_dia.sh`: the call is created from your Somach profile, Pik joins as a guest and presents the Pik tab. Steven joins the printed link from his laptop, camera on. Your host tab: camera on, mic off (Pik's voice comes from the presented tab's audio; your own voices go through Steven's mic or the recording's mic).
2. On the presented Pik tab (Dia profile O-Intuition) the page shows a small "ready" dot when armed. Press SPACE there on the cue. If you would rather not touch it, run `cd prototype && make take NAME=hackathon` in a terminal on the cue.
3. Record the host tab with Cap (screen + mic). Three seconds of silence before the first hello. Two takes maximum.
4. Reset between takes: `make reset` and reload the Pik tab (Cmd-R in that tab, or `prototype/meet_dia.sh` again for a fresh call).

## Hand it over
`deck/video/v5/captures/meet_real.mov` (or .mp4), then say "take is in". V5 = tightened front, your take at about 29 to 71 s, Slack, Notion, verticals, end.
