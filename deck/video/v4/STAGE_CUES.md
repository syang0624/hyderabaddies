# Stage cues: the Meet demo video on the new Pik screen (`meet_stage_demo.mp4`)

**Share this video as a tab with audio; press play at the moment you say "Pik, are you there?" or just start it and begin beat 1 at 3 s.**

Video: `deck/video/v4/meet_stage_demo.mp4`, 78.0 s, 1920x1080, 30 fps, H.264 + AAC. The only sound in it is Pik's follow-up question at 36.1 s. Everything else is said live by Carl and Steven; the screen reacts on the marks below. Second marks are measured from the recording (when each block actually became visible), not the plan. Same holds as V2 (speakers at 3, 20, 32, 43, 56 s).

| t | who | says | what appears |
|---|---|---|---|
|   0.0 s | screen | (press play) | The Pik screen at rest: the graph of 200 people and 11 channel hubs, what Pik reads and never reads, the ground strip. Idle, "At rest". |
|   3.0 s | Steven | Sure. So for the Northwind exchange slot. Honestly I need someone who will push back on the job-based culture over there instead of just absorbing it. And they have to hold their own in English in meetings. | Nothing yet. Say it at speaking pace, about 9 s. |
|  13.9 s | screen |  | Status Heard; the line typed in; three tiles A–Z (Rin: nothing on file; Yui 29; Kei 29: "2 of 7 words you asked for have a receipt. Not a score"); the graph dims and lights the receipts behind each number. |
|  20.0 s | Carl | Got it. One constraint from my side: the posting starts April 2027, and we cannot lose anyone from pricing before the Q1 close. | Nothing yet, about 6 s. |
|  27.3 s | screen |  | Two constraint chips in your words. Yui's tile dims: "on the Pricing team". |
|  32.0 s | Carl | Actually, we also need someone good for this. Just someone good. | Nothing yet, about 3 s. |
|  36.1 s | Pik (audio in the video) | What would this person actually do in the first month? | The ask bar appears and the same sentence plays from the tab share. Let it finish, do not talk over it. |
|  43.0 s | Steven | I keep coming back to Yui. What did she actually write about this herself, and what did her manager write about her? | Nothing yet, about 5 s. |
|  49.7 s | screen |  | Yui comes forward. Her own words (verbatim, Will Can Must sheet) and under them Okada's note (paraphrase, grey), both with sources. |
|  56.0 s | Steven | Okay. Looking at this, Yui's own words say she wants exactly that, and she has been running the Northwind sync in English. Let's set up calls with Yui and Kei this week, and ask Yui whether her manager's note about being flexible on location is actually true. That's it for today, thanks. | Nothing yet, about 13 s. |
|  70.6 s | screen |  | The conclusion card: what this meeting concluded, Yui and Kei, next steps, "ask them before deciding". |
|  73.0 s | screen |  | "Filed · 1 question to Yui · Yui and Kei can see this page". Read count unchanged: nothing new was read. |
|  78.0 s | end |  | Final frame held until here; the video ends. |

## What the speakers must know

- Holds are generous on purpose: finish the line, then wait for the screen. If you finish early, keep looking at the screen, not the camera.
- Beat 2 dims **Yui** ("on the Pricing team"). That is the real behaviour; Steven's "I keep coming back to Yui" in beat 4 brings her forward again.
- Beat 3: the spoken follow-up is exactly the on-screen text: "What would this person actually do in the first month?" (engine.ask on the vague line; it changed since V2). Nobody answers it; Steven moves to beat 4 at 43 s.
- Beat 5 is the longest line (13 s). The conclusion prints only at the mark, so do not rush it; the Filed line follows about 3 s later.
- The numbers on the tiles are coverage ("2 of 7 words you asked for have a receipt"), not a score; if a judge asks, that is the answer.
- Rebuild: `deck/video/pw/bin/python deck/video/v3/capture_ui.py --beats stage` (starts or reuses the worktree server), then `python3 deck/video/v4/build_stage_v4.py`. The follow-up wav comes from `narrate_v3.py --only stage_followup`; if engine.ask's follow-up text changes, update scripts/stage_v3.json and re-render it.
