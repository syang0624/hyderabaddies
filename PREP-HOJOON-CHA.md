# Prep: Steven with Ho Joon Cha (OpenAI)

> **Partly superseded (Sat Sep 26 ~07:45).** The Q&A lines now live in `PRD.md` §9.8 (single source; this table has drifted from it). The lens notes and the "do not" list below still apply.

Written Sat Sep 26 ~02:15 PDT. What the repo knows about him: event title "Applied AI Architect, OpenAI"; one of the four judges (Day 1 deck p16); OpenAI tech support core time 10–11 AM and 8–9 PM in `#ask-mentors-techsupporters`, mention `@hojoon`; a May 2026 OpenAI Academy webinar for ChatGPT Enterprise admins on workspace agents, approvals, safeguards and governance (`codex-packet/work/judges-research.md`, verified). Everything below infers an enterprise-deployment lens from that public record. None of it is his opinion.

He is also a judge on Sunday, so this conversation is a preview of Q&A. Treat it as disconfirmation, not pitching: show the running thing, ask what would make him not believe it.

## The five questions that lens is likely to ask, and the answer to have ready

| Likely question | Our answer | Where it lives |
|---|---|---|
| What does the model decide, and what is deterministic software? | The model extracts claims and writes summaries. Software enforces that every claim carries a source id and drops any that does not; the policy gate decides which sources exist at all; ranking is a re-score over the evidence store, and the human makes the decision. No score is presented as a verdict. | Architecture slide; policy gate config |
| What permissions does this need, and who consented? | Read-only over public channels, shared docs and the Will Can Must sheets the employee already gives HR. DMs and private channels are excluded by config, not by prompt. Opted-in AI session summaries are shared by the employee from their own machine. The subject sees the same page as the evaluator. | Audit strip; two-sided mirror |
| How are harmful errors caught? | The subject can contest any line and the note shows up on the evaluator's side before the decision. A wrong summary is visible to the person it is about. Purpose limitation means the page exists for one named decision, not a standing profile. | Annotation round-trip (live) |
| How do you know it works beyond one polished run? | A judge types a criterion we did not plan; ranking and receipts re-order live on the seeded corpus. Truth table on screen: what is seeded, what runs. | Free-text re-rank (live); truth table |
| What actually works right now? | Say exactly what is in the truth table and nothing more. Fixtures are fictional; extraction, grounding, re-rank, annotation and memo run live. | `DEMO-PLAN.md` §7 |

## The one thing to ask him back

"You've helped enterprises roll out agents with approval and governance layers. When an HR org wants to put evidence in front of first-line managers but is stalled on accountability to employees, what did the deployments that got unstuck do differently?"

That question uses his lens, does not name Recruit or the VP, and the answer becomes either a slide or the reason we change the design.

## Do not

- Quote the VP meeting's internal pilot, cost figures or disclosure status. He is a judge; the repo is public.
- Ask for idea validation. Ask what would break it.
- Present a slide deck. Bring the running spike, even if ugly.

## If it is a tech-support slot rather than mentoring

Bring the one blocker in HANDOFF.md: Claude on Vertex has zero quota on the Recruit project (`global_online_prediction_requests_per_base_model` for `anthropic-claude-fable` returns 429). He is OpenAI, so the useful ask is whether the OpenAI credits for the event cover a grounded-extraction model with structured outputs as a fallback for Gemini, and what the rate limits are.
