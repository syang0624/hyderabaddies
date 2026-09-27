# Packet verification

Two passes. The **second pass** (Sat Sep 26, directly below) supersedes the first where they differ. The **first pass** (Fri Sep 25, further down) is left exactly as written.

## Second pass — Sat Sep 26 2026, ~00:10–01:00 PDT

Run by Claude (Fable 5.1) on Steven's machine, in the git checkout at `~/Desktop/code/hyderabaddies` (commit 7e123b5, the packet as Carl committed it at 00:02). Purpose: close the six "unverified / open" items the first pass left, and make the packet usable from this repo instead of from Carl's laptop. Nothing below is claimed that was not run; commands and sources are named. No message was sent to anyone, no Slack was read, and no code, deck, video or submission was made.

### Summary

| Item | First pass said | Second pass result |
|---|---|---|
| Links | 14 local links resolved on Carl's machine | **18 absolute `/Users/carl/…` links and 4 `/private/tmp/…` paths rewritten to relative paths; every local link in the packet now resolves from this repo (0 broken).** Historical mentions in `work/council-brief.md` and first-pass §1 were left as records. |
| 1. Shion DM reply | Not checked | **Still not checked.** No agent has Slack access. Carl reads it. |
| 2. Hiro booking thread | Not checked | **Resolved from local records: the slot is booked, 1:30–2:00 PM.** BRAIN.md "On-Site Hackathon Ops" (added in commit 9cb423f, Fri 19:52) and the floor audio in BRAIN_TRANSCRIBED_RAW.md, segment 19-22-49 at 03:25–03:41 ("Hyderabadis, um, 1:30 p.m. to 2:00 p.m."). Slack itself was not re-read. Runsheet updated. |
| 3. Ebina-san's title | LinkedIn-sourced, not fetched | **Corroborated by a second public listing; still not fetched.** LinkedIn returns HTTP 999 to fetchers. A web search surfaced a ZoomInfo directory entry, "Vice President, COE Human Resources, Recruit", consistent with LinkedIn's "Vice President of Human Resources" and with Shion's "VP of COE / HR". `01` updated. |
| 4. Template order and word caps | From Codex's read, not re-inspected | **Re-inspected: every claim correct.** Slide text and speaker notes extracted from `attachments/hackathon_template.pptx` with Python `zipfile` (no python-pptx here). Two additions below. |
| 5. Rules/schedule PNGs | Not read | **All read. 9 distinct images; `judging.png` is a byte-identical duplicate of `rules-14.png` (same md5).** Every time, rule and title matches `work/event.txt` and the runsheet. No contradiction found. |
| 6. External URLs | 23 counted, none fetched | **22 unique URLs in `01` + `02`. 20 fetched or corroborated, 2 blocked with no substitute (one Medium article, the private Slack DM). 0 claims found wrong. 1 URL now redirects and was updated.** Table in §2.4. |
| Teammate memo | n/a (packet frozen before it existed) | `STEVEN-RESEARCH.md` (committed 23:55, the "Vouch" memo) was not in Codex's source copy. Mapped against the packet in `06-vouch-vs-packet.md`. |
| Repo | n/a | BRAIN.md says `tiger-baddies` was created Friday. `gh search repos tiger-baddies` and `gh repo view` under `CarlKho-Minerva` and `CARLKA-Minerva` at 00:10 found nothing public. It is private, unpushed, or named differently. Runsheet updated. |
| Fixes made | 3 | 10 files edited (§2.6), 1 file added (`06`). Council round files untouched; `04` changed only in its header link. |

### 2.1 Links — what was run

`grep -rnoE '\]\(/[^)]+\)' codex-packet/` found 18 links to `/Users/carl/Documents/Codex/2026-09-25/read/outputs/…`: `00` (5), `03` (11), `04` header (1), `work/council-index-closing.md` (1). All rewritten relative to each file's location. `grep -rnE '/Users/carl|/private/tmp'` found 4 more bare paths (`02` line 148, `05` line 37, `work/judges-research.md` line 7, first-pass §1 line 27). The first three now link to `attachments/…` in this repo; the verification line stays as a record. A Python walk over every markdown link in `codex-packet/**/*.md` then tested each non-http target with `os.path.exists`: **30 local links checked (after `06` was added), 0 broken.**

### 2.2 Template (`attachments/hackathon_template.pptx`)

All 9 slides and their notes were extracted. Confirmed as `02` §Template requirements states: order Title / Problem / Inspiration / Solution Overview / Impact / "What makes it different?" / Technical Design / Future Roadmap; Problem + Insight ≤ 200 words across slides 02–03; Differentiation ≤ 100; Technical ≤ 150 with a required architecture or data-flow diagram; Roadmap ≤ 75 with three horizons; Solution slide "HOW THE SOLUTION WORKS · VISUAL REQUIRED"; at least one impact number labelled VERIFIED / RESEARCH / CALCULATED / ILLUSTRATIVE with "Inputs × method or formula × source × assumptions"; notes say member names and roles belong in the Slack post while the title placeholder still reads "[ Team name + Member ]", so the inconsistency `02` flagged is real.

Two things `02` did not mention: slide 00 says **"Delete this slide before submitting"**, and its notes say **"Keep slides 01–08 in order and address every black content label unless it is marked optional."** Both were added to the runsheet.

### 2.3 Slide screenshots vs `work/event.txt`

Read with the image tool: `schedule-07` (all three days), `schedule-08` (Hiro reservation, walk-in, channel), `rules-14` = `judging` (rubric 40/30/30 with the sub-bullets `02` quotes), `rules-15` (originality, no pre-ceremony code, OSS disclosure in README), `rules-16` (four judges with the titles used in `02`), `rules-17` (11:00 AM PDT Sunday; public repo + "demo or a video of the prototype (Up to 1.5 minutes)" + PDF; `#announcements-all`), `rules-18` (3 + 1.5 minutes; order shared 6:30 PM Day 2), `rules-19` (6 + 6; no setup time after prelim results), `organizers` (Hidetoshi Ebina, no title). Every figure matches the text extraction. Because `judging.png` and `rules-14.png` are identical, the packet holds 9 distinct slides, not 10.

### 2.4 External sources (22 unique URLs in `01` and `02`)

Method: WebFetch with a claim-specific prompt. Where the host blocks fetchers (HTTP 403 or 999), a web search for the same page, using only the search engine's snippet of that exact page. "Verified" means the page exists and supports the specific sentence the packet attaches to it.

| # | Source as cited | Packet claim | Result |
|---|---|---|---|
| 1 | Recruit Holdings blog, 2026-09-04 | Results commentary emphasizes recruiter productivity and hiring outcomes | **Verified.** "From AI promise to real hiring outcomes: What Recruit Holdings' FY2026 Q1 financial results show", Sep 4 2026. Smart Sourcing / Smart Screening remove manual resume review; a client reports "productivity equivalent to several recruiters." For the pitch: Indeed already sells AI candidate screening, so any dossier product will be asked how it differs. |
| 2 | Indeed release, Jim Giles as CTO | Led Google Docs/Sheets/Slides/Drive engineering, founded the Workspace AI platform, interest in improving work and hiring | **Verified.** Feb 16 2026. VP Engineering at Google; founded Workspace AI platform; "how technology can improve the way work gets done." |
| 3 | jp.indeed.com/about/leadership | Corroborates the CTO title | **Verified.** Listed as 最高技術責任者 (Chief Technology Officer). |
| 4 | Glassdoor blog, Hohman mission post | 2015 post on making culture, pay and interview information accessible | **Verified via search snippet** (site returns 403 to fetchers). March 23 2015; content matches. |
| 5 | EDA.gov NACIE 2014–16 biography | Expedia booking engineering, Hotwire leadership | **Verified via search snippet** (403). Hotwire president; original Expedia team; led engineering for the cruise, hotel and package booking systems. An archived copy also exists at eda.gov/archives/2022/oie/nacie/members/2014-16/rhohman.htm. |
| 6 | GitHub GoogleCloudDevRel/next25-retro-tech-revolution | Contreras authored a Godot / Google Cloud AI game demo with published code | **Verified.** Author named. Godot, Gemini, Imagen, Flask, Agent Development Kit, BigQuery, Agones. README: AI that can "enhance our experience proactively." |
| 7 | Medium, "Retro Tech Revolution" | Telemetry and screenshots drive proactive assistance and adaptive difficulty | **Blocked (403), not corroborated.** The repo README links to this exact article, so it exists; the telemetry / screenshot / adaptive-difficulty details rest on Codex's Sep 25 read only. |
| 8 | OpenAI Academy event | Ho Joon Cha listed as Solutions Engineer; May 19 2026 webinar on workspace agents, approvals, governance | **Verified.** Title, date, speakers and topics match. |
| 9 | Granola /chat | In-meeting questions, PRD creation | **Verified.** Real-time questions during meetings; generates product specs and other documents. |
| 10 | Granola MCP help article | Meeting context into coding tools via MCP | **Verified; URL updated.** `help.granola.ai/article/granola-mcp` now 301s to `docs.granola.ai/article/granola-mcp`. Notes and (paid-plan) transcripts are exposed to Claude, ChatGPT and Claude Code. `02` cites the new URL; `round-10.md` keeps the old one, which still redirects. |
| 11 | NBER w31161 | 5,179 agents; +14% average; +34% novice; dissemination of experienced agents' practices | **Verified.** Brynjolfsson, Li and Raymond, April 2023 rev. Nov 2023. All three numbers and the mechanism match. |
| 12 | works-i.com futureofwork project | 2023 simulation projects a 2040 labor shortfall around 11 million | **Verified.** Project page confirms the 2040 simulation. The 1,100万人 figure is in the 2023 report "未来予測2040" (works-i.com/research/report/forecast2040.html) and Recruit's own Sep 26 2023 post. |
| 13 | METI SME White Paper 2025, b1_1_4 | Tayama Studio case: tacit craft knowledge made teachable with AI | **Verified via search snippet** (403). Section 第4節 労働生産性・設備投資. Tayama Studio (Morioka, Nambu ironware) has applied AI to skill transfer since 2023. |
| 14 | MHLW press-release PDF 001742821 | 2025 survey published Aug 31 2026: 46.2% of establishments cite Japanese-proficiency communication difficulty; 3,919 establishments and 14,248 workers responded; frame ≥ 5 insured employees and ≥ 1 foreign worker | **Verified.** The search engine's index of this exact PDF gives 3,919 establishments and 14,248 workers (of 9,016 sampled) and an August 2026 release (the exact day is not visible in the snippet). The string "46.2" is present in the PDF's decompressed content streams (checked with Python zlib; no PDF renderer on this machine). The frame wording matches MHLW's FY2024 results page (mhlw.go.jp/stf/newpage_61317.html). For contrast, FY2024 was 43.9% / 3,623 / 11,568, so do not mix the two years. |
| 15 | Forage /about | Employer-designed simulations, free to learners | **Verified.** "we make money by charging our company partners"; free for students; 300+ simulations. |
| 16 | Forage /simulations | Category adoption; a generic virtual internship is not novel | **Verified, and sharper than the packet says.** Simulations are "a series of tasks guided by pre-recorded videos and example answers", self-paced, with no live interaction. That is the concrete difference a work-rehearsal demo would have to show. |
| 17 | Delphi | Interactive expertise and repeated-question handling | **Verified.** "Digital Minds" answer 24/7 in the expert's voice, grounded in synced sources with citations. |
| 18 | observableintuition.com | Now "Collective Intuition"; state / action / consequence; models private to each customer | **Verified.** Wording matches. The "July 2026 manifesto" date was not visible in the fetch. |
| 19 | Observable Intuition terms | No use of customer data for other customers or third-party models without written consent; customer supplies rights and consents; encryption, screening, subprocessor terms | **Verified.** §3.3, §3.4, §4.2, §4.3 and §7.1 as summarized. |
| 20 | Observable Intuition privacy | Mostly website and demo-contact data | **Verified.** Contact-form data; no mention of model training. |
| 21 | LinkedIn, Hidetoshi Ebina | VP of Human Resources, Recruit | **Blocked (HTTP 999); corroborated** by a ZoomInfo listing found by search: "Vice President, COE Human Resources". |
| 22 | Slack DM permalink | Sent 22:49:33 PDT | **Not fetched (private workspace).** The timestamp was decoded from the permalink in the first pass. |

Net: nothing the packet attributes to a source was found to be wrong. The one place the packet is *weaker* than its source is Forage (row 16), which helps the differentiation slide.

### 2.5 Other checks

- **Koki raw transcript** `interviews/raw/1_koki_20-07-50.json` is still invalid JSON: a trailing comma at line 5, column 601. Not edited (raw source; the first pass also left it). Anyone loading the raw files programmatically needs a lenient parser or to strip that comma.
- **Council files**: `04-full-council-transcripts.md` changed only in its header link (line 5). `council/round-01..10.md` are untouched and still byte-identical to the commit.
- **Pre-event JP PDF vs Day 1 deck**: the Saturday-afternoon discrepancy the first pass flagged stands. Slide 07, read directly, shows the Day 1 deck times used in the runsheet.
- **Current time context**: this pass ran from 00:10 PDT Saturday, so the whole runsheet is still ahead.

### 2.6 Files changed in this pass

`README.md`; `outputs/00-start-here.md` (banner only); `outputs/01-interviews-and-vp.md` (one sentence, VP identity); `outputs/02-research-and-demo-options.md` (PDF path; Granola URL); `outputs/03-council-index.md` (links); `outputs/04-full-council-transcripts.md` (header link); `outputs/05-saturday-runsheet.md` (banner, sync row, repo row, Hiro row, template row, artifact 3); `work/council-index-closing.md` (link); `work/judges-research.md` (PDF path); this file (this section prepended; first-pass text unchanged); and the new `outputs/06-vouch-vs-packet.md`. Nothing was committed; `git status` shows the working tree.

### 2.7 Still open after two passes

1. **Whether Shion replied** to the 22:49 DM. Only Carl can look.
2. **Whether `tiger-baddies` exists and is public.** Carl knows; `gh` could not see it from Steven's account.
3. **The Medium article's specific claims** (row 7) and the **"July 2026" manifesto date** (row 18). Unfetched, low stakes, not used in any pitch line.
4. **The private founder note** in `02` (Observable Intuition capture modalities). Unverifiable by design and already marked not-for-pitch.

---

# First pass — run ~23:20–23:50 PDT, Sep 25 2026 (unchanged record)

Run by a follow-on agent (pi/Claude) after the Codex thread died at the usage limit with "I'm checking the final packet now." This is that check. Nothing below is claimed that was not actually run; commands and sources are named.

## Summary

| Check | Result |
|---|---|
| Internal links / file paths in `00` and `03` | **14 local links, 14 resolve. 0 broken.** (`01` and `02` also scanned: 0 local links, 23 external URLs, not fetched.) |
| Logistics claims in `00` §3 vs `work/event.txt` | **All 7 load-bearing claims grounded** in the Day 1 deck text. 0 rest on a screenshot alone. |
| Ten council rounds present and complete in `04` | **10/10 present, each byte-identical to its `council/round-NN.md`, none truncated, all required sections present.** |
| Fictional-critique labelling | Every round labels itself fictional (14–31 "fiction*" mentions per file); no real judge name is ever used as a speaker. |
| Work-authorization / employment language | 0 hits for work-authoriz*, EAD, OPT, I-765, "employed" across `outputs/`. |
| Messages to humans | One Slack DM was **already sent by Codex at 22:49:33 PDT** (verified from the permalink timestamp), disclosed in `00` §1 and `01`. No other message was sent, drafted-and-sent, or scheduled. Nothing was sent by this pass. |
| Fixes made | 3 (listed below). |
| Unverified / open | 6 items (listed below). |
| Wrong (found and corrected) | 1 factual error: teammate name. |

## 1. Link integrity — what was run

`grep -oE '\]\([^)]+\)'` over `00`, `01`, `02`, `03`; each non-http path tested with `[ -e ]`.

- `00-start-here.md`: 3 local links (`01`, `02`, `03`) — all exist. 1 external (Slack permalink) — not fetched.
- `03-council-index.md`: 11 local links (`council/round-01..10.md`, `04-full-council-transcripts.md`) — all exist.
- `04` header links back to `03` — exists.
- Bare-path mentions (`work/`, `outputs/council/round-10.md`, `outputs/02-research-and-demo-options.md` inside transcripts) all correspond to real files.
- Source PDF path quoted in `02` (`/private/tmp/hyderabaddies/attachments/InnovationCup2026_Day1_Slide.pdf`) — exists (4.6 MB, Sep 25 19:51), alongside `PreEvent_Material_JP.pdf`, `hackathon_template.pptx`, `team_gcp_assignments.tsv`. Note `/private/tmp` does not survive a reboot.

**Count: 14 local links checked, 0 fixed.**

## 2. Logistics fact-check — `00` §3 against `work/event.txt`

`work/event.txt` is the text extraction of the Day 1 deck. The PNGs in `work/` were **not** read (no image lane used); nothing below relies on them.

| Claim in `00` | Source | Status |
|---|---|---|
| Sunday submission 11:00 AM | event.txt p17 "Deadline: 11:00 AM PDT, Sunday, September 27" | Verified |
| Public repo + PDF deck + demo/video ≤ 90 s | p17 items 1–3: public GitHub repo; "demo or a video of the prototype (Up to 1.5 minutes)"; deck ".pdf" | Verified. Note it is "demo **or** video" — a live demo link satisfies item 2. |
| Prelim 3 min + 90 s Q&A | p18 "3 minutes presentation + 1.5 minutes Q&A" | Verified |
| Final 6 + 6 | p19 "6 minutes presentation + 6 minutes Q&A" | Verified |
| Saturday lunch/mentoring 12:30–2:30 PM | p7/p8 "12:30 - 2:30 PM Lunch / Mentoring Session" | Verified |
| Saturday evening session 5–6 PM | p7/p8 "5:00 - 6:00 PM Mentoring Session" | Verified |
| "Not a documented rotation through industries" | p7–9 list only gather / lunch-mentoring / work / mentoring / announcements | Verified (absence of any such item) |
| 40/30/30 rubric | p14 | Verified |
| "Prepare both before submission" | Inference from p19 "No setup time after the prelim results" | Reasonable inference, labelled as such in `05` |
| "Don't reuse AI ideas as-is" | p27 | Verified |
| Slack request "at 10:49 PM" | Permalink `p1790401773440139` → epoch 1790401773 → 2026-09-25 22:49:33 PDT | Verified (timestamp only; message content not re-read) |

Additional facts in `02` cross-checked: prelim order announced 6:30 PM Day 2 (p18) ✓; tech support 10–11 AM and 8–9 PM (p9) ✓; Hiro reservation thread Friday 7 PM, Golden Gates 1F; walk-in at Amazing Grace 1F (p8) ✓; midnight–6 AM hotel-only (p7, p29) ✓; prizes $20k + conditional $30k, two $10k special awards (pp21–22) ✓; submission channel `#announcements-all` (p17) ✓.

**Discrepancy worth knowing:** `work/preevent-jp.txt` (pre-event Japanese PDF) has a *different* Saturday: lunch 12:30–13:30, optional mentoring 13:30–14:30, work 14:30–18:30, announcements 18:30–18:40; and lists the submission as a "working demo" (動作するデモ) rather than "demo or video". The Day 1 deck is the newer document and the packet follows it. Flagged in `05`; a Slack announcement would override both.

## 3. Council transcript completeness

Method: (a) `grep '^# '` on `04` → 10 round headings, ROUND 01…ROUND 10, plus the file header. (b) Python substring test: each `council/round-NN.md` (stripped) appears verbatim inside `04` — **10/10 True**. (c) Sizes: concatenated rounds 334,958 bytes vs `04` 335,521 bytes; the 563-byte difference is `04`'s header + link back to `03`. (d) Each round's last H2 is a closing section (revision/reversal, rehearsal check, or saved-file check), not a mid-body section. (e) One `vertex.py` call (gemini-3.8-flash, tag `recruit-packet`, 69,094 tokens in, $0.024, logged in `~/.local/state/lifeos/vertex_ledger.jsonl` at 23:38:12) audited every round for nine required sections — prelim script, prelim Q&A, final script, final Q&A, 90 s storyboard, four-lens deliberation, score table, truth table, reversal conditions — and returned Y on all 90 cells and "ends cleanly: Y" on all ten. Vertex's negative findings (no real judge as speaker, no employment language) were independently re-checked with grep, below.

The ten rounds, by title and stated direction:

| # | Title | Direction the round itself states |
|---|---|---|
| 01 | baseline comparative council | C, narrowed to one incident |
| 02 | Buyer skepticism, revision 2.0 | C for exploration; A for discovery |
| 03 | Incumbents and disconfirmation | A rehearsed; C concept lead |
| 04 | worker agency, consent and bias | C conditional, learner-owned |
| 05 | No enterprise data, no mentor author, one build day | C as fictional mechanism only |
| 06 | Can the judge actually change the experiment? | B |
| 07 | the magic must survive the missing model | C conditional |
| 08 | Two people, one day | C narrowly, one scene |
| 09 | Who benefits when this crosses an industry boundary? | C-onboarding narrowly; B if no approved case |
| 10 | final head-to-head rehearsal | C, careers-program buyer, exploratory artifact |

This matches the table in `03`. **None truncated.**

Labelling: `grep` for the four real judge names used as a dialogue speaker (`^Name:` / `**Name**`) → 0 hits in `04` and `council/`. The names appear only in evidence-boundary lines citing public backgrounds (lines 1541, 2391 of `04`, and the `02` judges section). Every round file contains "fictional" labelling (counts 14–31 per file).

## 4. Fixes made (3)

1. **`02-research-and-demo-options.md` line 157: "Carl and Stephen" → "Carl and Steven."** Teammate is Steven Yang per the organizer file `team_gcp_assignments.tsv` (team `recruit-hackathon-2026-e`) and every other packet file. Same fix applied to the source line in `work/judges-research.md` line 16.
2. **`00-start-here.md`:** added a 5-line overnight close-out banner at the top pointing to `05` and this file, and naming the one thing only Carl can do (read the Shion DM). No other text in `00` changed.
3. **Created `05-saturday-runsheet.md`** — organizer times only from `event.txt`; suggested rows explicitly labelled; decision gate at 2:30 PM; Saturday-night artifact list.

## 5. Unverified / open (6)

1. **Whether Shion replied to the 22:49 DM.** Not checked. The only local Slack helper (`hackathon-brain/slack_session.py`) scrapes Carl's live browser session; not used while he sleeps. Carl opens the DM.
2. **Whether anyone replied to Hiro's 7:00 PM booking thread** for a Saturday mentoring slot. Not checked, same reason.
3. **Ebina-san's title.** `00` calls him "the VP"; `01` sources this to his LinkedIn page (external URL, not fetched tonight). The Day 1 deck (p4) lists Hidetoshi Ebina under Organizing Team with no title. Treat "VP" as LinkedIn-sourced.
4. **Template section order and word caps** quoted in `02` and repeated in `05` come from Codex's read of `hackathon_template.pptx`. The .pptx exists; its contents were not re-inspected tonight.
5. **The rules/schedule PNGs** in `work/` were not read. Every logistics claim was grounded in `event.txt` text instead, so no claim rests on a screenshot alone. If a PNG contradicts the text extraction, the PNG is the original.
6. **The 23 external URLs** in `01` and `02` (judge bios, MHLW survey, Forage, Delphi, Granola, Observable Intuition terms) were not re-fetched. Their claims stand as Codex's Sep 25 research, not re-verified.

## 6. Wrong (1)

- Teammate name "Stephen" in `02`/`work/judges-research.md`. Corrected (above). No other factual error found in the checked claims.

## 7. Not done, deliberately

- No message drafted, sent, or scheduled to anyone. The 22:49 DM was already out before this pass and is disclosed in `00`, `01` and `05`.
- No code, repo, deck, video, calendar event, or submission created. Those are Carl and Steven's, written after Friday's opening ceremony.
- Council content was not edited. It stays labelled fictional; `04` and `council/` are byte-identical to what Codex left.
- No Vertex call beyond the single audit above.
