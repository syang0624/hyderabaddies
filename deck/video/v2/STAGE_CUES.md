# Stage cues: the Meet demo video (`meet_stage_demo.mp4`)

**Share this video as a Dia tab with audio; press play at the moment you say "Pik, are you there?" or just start it and begin beat 1 at 3 s.**

Video: `deck/video/v2/meet_stage_demo.mp4`, 78.0 s, 1920x1080, 30 fps, H.264 + AAC. The only sound in it is Pik's follow-up question at 36.8 s. Everything else is said live by Carl and Steven; the screen reacts on the marks below. Second marks are measured from the recording (when each block actually became visible), not the plan.

| t | who | says | what appears |
|---|---|---|---|
|   0.0 s | screen | (press play) | The "today" page: three people, three notes from memory. Idle. |
|   3.0 s | Steven | Sure. So for the Northwind exchange slot. Honestly I need someone who will push back on the job-based culture over there instead of just absorbing it. And they have to hold their own in English in meetings. | Nothing yet. Say it at speaking pace, about 9 s. |
|  13.8 s | screen |  | The question block, then three tiles re-sorted on the words, Yui first, one why line each with its source. |
|  20.0 s | Carl | Got it. One constraint from my side: the posting starts April 2027, and we cannot lose anyone from pricing before the Q1 close. | Nothing yet, about 6 s. |
|  27.1 s | screen |  | Two constraint chips. Yui's tile dims: "on the Pricing team". |
|  32.0 s | Carl | Actually, we also need someone good for this. Just someone good. | Nothing yet, about 3 s. |
|  36.8 s | Pik (audio in the video) | Is this for the Tokyo side or the partner side, and by when? | The ask block appears and the same sentence plays from the tab share. Let it finish, do not talk over it. |
|  43.0 s | Steven | I keep coming back to Yui. What did she actually write about this herself, and what did her manager write about her? | Nothing yet, about 5 s. |
|  49.6 s | screen |  | Yui comes forward. Her own words (verbatim, Will Can Must sheet) beside Okada's note (paraphrase), both with sources. |
|  56.0 s | Steven | Okay. Looking at this, Yui's own words say she wants exactly that, and she has been running the Northwind sync in English. Let's set up calls with Yui and Kei this week, and ask Yui whether her manager's note about being flexible on location is actually true. That's it for today, thanks. | Nothing yet, about 13 s. |
|  70.3 s | screen |  | The conclusion prints: people to talk to, next steps, what to ask them before deciding. |
|  78.0 s | end |  | Final frame held until here; the video ends. |

## What the speakers must know

- Holds are generous on purpose: finish the line, then wait for the screen. If you finish early, keep looking at the screen, not the camera.
- Beat 2 dims **Yui** ("on the Pricing team"). That is the real behaviour; Steven's "I keep coming back to Yui" in beat 4 brings her forward again.
- Beat 3: the spoken follow-up is exactly the on-screen text: "Is this for the Tokyo side or the partner side, and by when?". Nobody answers it; Steven moves to beat 4 at 43 s.
- Beat 5 is the longest line (13 s). The conclusion prints only at the mark, so do not rush it.
- Rebuild: `deck/video/pw/bin/python deck/video/v2/record_stage.py` (server on :8787), then `python3 deck/video/v2/build_stage.py`. The follow-up wav comes from `narrate_vertex.py --only stage_followup`.
