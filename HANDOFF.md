# Handoff for Steven's Claude session (Sat Sep 26, 00:15 PDT)

Carl's Codex thread hit its usage limit around 23:14 on Fri. This file is where it stopped and what's in the repo now.

## UPDATE ~02:30 Sat: for the Fable session
- **Best VP source now:** `interviews/5_VP_MEETING_TRANSCRIPT_RECONCILED.md`. It merges phone and glasses audio (aligned at 00:09:40), labels speakers, translates all 243 Japanese lines, and lists 24 unresolved spots per chunk. Prefer it over `5_VP_MEETING_TRANSCRIPT.md` (single source, no translation). Per-chunk raw output and the script are in `interviews/raw/vp-reconcile-chunks/`.
- Detailed summary: `interviews/5_VP_MEETING_SUMMARY.md` (written from the single-source transcript; check quotes against the reconciled one).
- Steven's "define innovation" riff (glasses, 01:30): `interviews/6_STEVEN_INNOVATION_FRAME.md`.
- Prototype: `prototype/` (`make run-heuristic`, then open http://localhost:8787; `make smoke` checks every endpoint). The pitch scripts are in `DEMO-PLAN.md` section 9.
- Open before Sunday: run `make run-gemini` once; get the VP or Shion to clear which figures and quotes can go in the public deck.

## UPDATE 01:30 Sat: VP meeting happened (72 min, ~00:14-01:26)
- Summary: `interviews/5_VP_MEETING_SUMMARY.md` (timestamped, read this first)
- Full transcript: `interviews/5_VP_MEETING_TRANSCRIPT.md`, raw JSON `interviews/raw/5_vp-meeting_full.json`
- The "Still open" items below about the VP meeting are superseded.

## Read in this order
1. `codex-packet/outputs/00-start-here.md`: the decision brief
2. `codex-packet/outputs/03-council-index.md`, section "What the rehearsals actually resolved"
3. `codex-packet/outputs/05-saturday-runsheet.md`: Saturday hour by hour
4. `codex-packet/outputs/01-interviews-and-vp.md`: interview feedback, the Ebina-san guide, the Shion observation plan
5. `interviews/INTERVIEW_NOTES.md` + `interviews/raw/`: the evidence

## Where Codex stopped
- It finished. All 10 councils are complete, and the packet was fact-checked afterwards (`codex-packet/outputs/PACKET-VERIFICATION.md`).
- Three directions are still open, and none has a paying customer yet:
  - **A. Shion's candidate-handoff workflow.** Closest to something we actually observed.
  - **B. Live experimentation.** A judge adds a constraint and working alternatives adapt. This is the cleanest demo.
  - **C. Work rehearsal / career preview.** The biggest ambition. Pick ONE buyer: employer onboarding or career preview, not both.
- Council stopping rule: get the one missing operator fact, get a real core mechanism running, and compare it against the best current workaround. Do not run more councils in place of customer evidence.

## Still open, as of 00:15
- **Ebina-san (Hidetoshi Ebina, organizing team; LinkedIn says VP HR, Recruit Co.).** No meeting has happened. A request went to Shion over Slack DM at 22:49, and no reply has been confirmed. Only Carl or Steven can check that DM.
- **Shion 15-min workflow observation.** Not booked yet. The script is in `01-interviews-and-vp.md`.
- **Submission deadline: Sun 11:00 AM.**

## New in `interviews/raw/` (Gemini 3.8 Flash, transcribed 00:05 Sat)
| File | What it is |
|---|---|
| `x_floor_21-20-00` to `x_floor_22-00-00` | Floor and team chatter. 21:20 includes Carl dictating pitch-question ideas. 22:00 includes meeting Risa (Cambridge, from Tokyo). |
| `3_carl-reflection_22-40-00` | Carl, solo: he doesn't have conviction in an idea yet. It's the boring-but-viable idea versus a cool demo with solid data, and the pressure to win is blocking his creativity. **Read this before pushing a direction on him.** |
| `3_carl-demo-plan_22-42-32` | Carl, solo: demo plan (agent structure, simulated parts, separate walkthrough paths for different audiences including the VP) |
| `4_gcp-credits_23-10-00`, `4_gcp-credits_23-20-00` | Using the Recruit GCP credits (project `recruit-hackathon-2026-e`) instead of personal credits |
| `x_floor_23-50-00` | Carl and Steven meeting up at about 00:00 about the overnight simulation runs |

Summaries are model-written. Speaker names in these files are guesses; the model hears "Karl/Stephen/Stiven" for the same two people.

Glasses and phone audio from 22:10 to 23:50 that isn't listed here is personal (calls, a workout) or background media. It was deliberately left out.

## Compute
- Gemini 3.8 Flash on Vertex, project `recruit-hackathon-2026-e`: **works.**
- Claude Fable on the same project is offered at the global endpoint, but the quota is 0 (429). A project admin (Recruit or the Google SE) has to raise `global_online_prediction_requests_per_base_model` for `anthropic-claude-fable`. Carl can't raise it himself.

## Ground rules from Carl
- **Every message to another person is a draft.** That includes Slack to Shion, organizers and judges. Show it to Carl, and send only after he explicitly approves that exact text.
- Councils are fictional rehearsal. Never quote them as something a real judge said.
- Don't state anything about Carl's own career or internship next steps. Leave that to him.
