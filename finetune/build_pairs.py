"""Build (ask, positive receipt, hard negative) pairs from the prototype's fixtures. No model is called to write or label
data: every ask is a fixed template filled with the fixtures' own topics. The templates, the topic synonyms and the
Japanese asks below were typed into this file as plain text by the coding agent (Claude) that built finetune/.

Labels. Every generated receipt in prototype/data/people.json was made by prototype/make_people.py from one of ten
templates (RECEIPT) with an {area}, {skill} or {ch} slot. We match each receipt's text back against those templates
(common.label: exactly one must match, and the slot value must come from the generator's own lists; all 587 do).
An intent is "<template family>:<topic>", e.g. "retro:pricing experiments" for "Volunteered to run the pricing
experiments retro ...". A receipt answers an ask exactly when its recovered intent equals the ask's intent; a person
answers it when any of their receipts does. Nothing is judged by a model or by hand except the ask wording.

Split. 25% of intents per family are held out (seeded): their asks are test only, and their receipts never enter
training, not even as negatives. Each ask template list and each topic-synonym list ends with a test-only entry, so
test asks for trained intents use a phrasing and a synonym never seen in training. All Japanese asks are test only.

Run: .venv/bin/python build_pairs.py   -> data/train.jsonl, data/test.jsonl, data/corpus.jsonl, data/STATS.md
"""
from __future__ import annotations

import collections
import random
import re

import common as C

# ---------- ask templates per family: the last entry of each list is test only ----------
# "kw" asks reuse the receipt's own words; "para" asks are written to avoid them (the overlap is measured, not assumed).
ASKS = {
    "writeup": {"kw": ["Who posted the {t} write-up?", "Who wrote up {t} and flagged the open questions?", "Is there a write-up on {t}, and who posted it?"],
                "para": ["Who shared a summary of {t} with the unresolved points marked?", "Who circulated notes on {t} that call out what is still undecided?",
                         "Who put out a recap of {t} listing the loose ends?"]},
    "retro": {"kw": ["Who ran the {t} retro?", "Who volunteered to run a retro on {t}?", "Who has run the {t} retro this quarter?"],
              "para": ["Who offered to facilitate the look-back session about {t}?", "Who stepped up to host the post-project reflection on {t}?",
                       "Who chaired the reflection meeting on {t} so their boss could recruit?"]},
    "office_hours": {"kw": ["Who holds office hours on {t}?", "Who helps people stuck on {t}?", "Who runs {t} office hours on Thursday?"],
                     "para": ["Who makes themselves available to colleagues needing help with {t}?", "Who does a weekly drop-in clinic about {t}?",
                              "Where can a junior go to get unblocked on {t}?"]},
    "lessons_doc": {"kw": ["Who wrote what we would do differently on {t}?", "Who has a decision log for {t}?", "Is there a doc on {t} with the numbers and the decision log?"],
                    "para": ["Who documented lessons learned from {t}?", "Who authored the post-project review of {t}, including metrics and choices made?",
                             "Who put in writing the takeaways from {t}?"]},
    "incident": {"kw": ["Who took the {t} incident and wrote the post-mortem?", "Who wrote the post-mortem for the {t} incident?", "Who took a Saturday incident in {t}?"],
                 "para": ["Who dealt with a weekend outage for {t} and documented the root cause?", "Who was on call when {t} had a production problem, and filed the analysis afterwards?",
                          "Who fixed a breakage affecting {t} outside working hours?"]},
    "playbook": {"kw": ["Who drafted the {t} playbook?", "Is there a {t} playbook used by other teams?", "Who wrote the playbook for {t}?"],
                 "para": ["Who authored the how-to on {t} that other departments follow?", "Who created the reference manual for {t}?",
                          "Whose handbook on {t} got picked up across the company?"]},
    "pushback": {"kw": ["Who pushed back on the {t} timeline?", "Who pushed back with data on {t}?", "Who changed the {t} plan with data?"],
                 "para": ["Who challenged the schedule for {t} using evidence and got it revised?", "Who disagreed with the {t} deadlines, backed by figures, and won?",
                          "Who argued, with metrics, that the {t} dates were unrealistic?"]},
    "session": {"kw": ["Who chose to work on {t}?", "Whose work on {t} was adopted by the team?", "Who worked on {t} and got it adopted?"],
                "para": ["Who picked {t} as a side project and saw colleagues take it up?", "Who built something for {t} unprompted that people now use?",
                         "Who self-selected into {t} and delivered something others rely on?"]},
    "english_sync": {"kw": ["Who ran the {t} sync in English?", "Who has run a sync in English in {t}?", "Who posted notes the same day after the {t} sync?"],
                     "para": ["Who hosted the {t} meeting without using Japanese?", "Who chaired the {t} check-in in a non-native language and circulated minutes promptly?",
                              "Who facilitated the {t} call for the overseas side?"]},
    "onboarding_guide": {"kw": ["Who wrote the onboarding guide for {t}?", "Is there an onboarding guide on {t} for new joiners?", "Who wrote {t} onboarding for the new joiners?"],
                         "para": ["Who prepared ramp-up material on {t} for recent hires?", "Who made the starter docs that teach newcomers {t}?",
                                  "Who helps people who just started get up to speed on {t}?"]},
}

# ---------- topic synonyms, written into this file: the last one is test only ----------
TOPIC = {
    # areas
    "pricing experiments": ["price tests", "trials of different price points", "A/B tests on what we charge"],
    "cohort retention": ["whether customers stick around", "churn by signup month", "keeping users from leaving"],
    "search relevance": ["result ranking quality", "how well results match queries", "ordering of hits for a query"],
    "partner onboarding": ["getting new resellers set up", "bringing alliance firms up to speed", "the first weeks with a new reseller"],
    "FY26 dashboard": ["the annual metrics board", "this fiscal year's KPI report", "the yearly KPI screen"],
    "exchange program": ["the overseas secondment", "the two-year posting abroad", "staff rotation with the US partner"],
    "incident response": ["handling outages", "firefighting production breakages", "on-call emergencies"],
    "skills taxonomy": ["the competency framework", "how we classify abilities", "the capability map"],
    "customer interviews": ["user research calls", "talking with clients one on one", "sitting down with buyers"],
    "Northwind integration": ["connecting to the US partner's systems", "the API hookup with our American partner", "linking up with the Austin partner"],
    "SQL training": ["teaching database queries", "a course on writing queries", "helping people get fluent with database tables"],
    "design system": ["the shared UI component library", "our reusable interface kit", "the common widget catalogue"],
    "hiring loops": ["the interview process for candidates", "recruiting panels", "how we assess applicants"],
    "LMS migration": ["moving to a new course platform", "switching training software vendors", "porting courses to a new e-teaching tool"],
    # skills (the engine's tag vocabulary, company.json "tags")
    "data analysis": ["crunching numbers", "digging into datasets", "making sense of metrics"],
    "experiment design": ["setting up A/B tests", "planning controlled trials", "structuring split tests"],
    "pricing": ["what we charge", "price points", "setting rates"],
    "stakeholder management": ["keeping executives aligned", "handling what senior leaders expect", "bringing department heads along"],
    "written communication (EN)": ["clear English prose", "drafting emails and docs in English", "English writing"],
    "spoken communication (EN)": ["speaking English in meetings", "presenting aloud in English", "English conversation"],
    "cross-team coordination": ["aligning several departments", "getting groups to move together", "keeping many squads in step"],
    "mentoring": ["coaching juniors", "growing less experienced colleagues", "guiding new analysts"],
    "product thinking": ["judging what users need built", "feature prioritisation instinct", "deciding what to build next"],
    "system design": ["service architecture", "how the backend is structured", "scalable infrastructure layout"],
    "documentation": ["writing things down for others", "keeping the wiki current", "technical reference writing"],
    "negotiation": ["bargaining with vendors", "haggling over contracts", "reaching deals"],
    "org design": ["reporting lines", "how departments are arranged", "restructuring the company chart"],
    "ambiguity tolerance": ["comfort with unclear goals", "working without a clear brief", "staying calm when things are vague"],
    "initiative": ["self-starting", "acting without being told", "doing things before being asked"],
    "feedback culture": ["giving honest critiques", "candid reviews between peers", "saying hard things kindly"],
    "project management": ["keeping deliverables on schedule", "running milestones", "tracking deadlines"],
    "SQL": ["database queries", "writing queries against tables", "relational databases"],
    "python": ["scripting", "writing scripts for analysis", "pandas notebooks"],
    "marketing analytics": ["campaign measurement", "attribution reports", "measuring promotion results"],
    "onboarding others": ["ramping up new hires", "welcoming new colleagues", "getting newcomers productive"],
    "public speaking": ["presenting on stage", "giving talks", "addressing large audiences"],
    "learning agility": ["picking up unfamiliar tools fast", "adapting quickly to new domains", "getting good at new things quickly"],
    # channels
    "#growth-analytics": ["the growth analysts", "the acquisition metrics team", "the user-growth data group"],
    "#pricing": ["the price-setting team", "the monetisation group", "the rate-card folks"],
    "#platform": ["the infrastructure group", "the core backend team", "the internal tooling engineers"],
    "#search": ["the discovery team", "the ranking engineers", "the query-results group"],
    "#people-ops": ["HR operations", "the personnel team", "the HR admin group"],
    "#customer-success": ["the client support team", "the account care group", "the retention support folks"],
    "#design-crit": ["the UI review forum", "the mockup feedback circle", "the visual critique group"],
    "#data": ["the analytics team", "the BI group", "the numbers people"],
    "#learning": ["the training channel", "the L&D group", "the upskilling forum"],
    "#all-hands-questions": ["the company-wide Q&A", "the town hall thread", "the all-staff ask-me-anything"],
    "#northwind-sync": ["the US partner call", "the Austin partner meeting", "the weekly call with the American partner"],
}

# ---------- Japanese asks, written into this file for existing intents (test only) ----------
JA = [
    ("retro:pricing experiments", "価格実験のふりかえりを進行したのは誰？"),
    ("retro:SQL training", "SQL研修のレトロを担当したのは誰ですか？"),
    ("retro:incident response", "障害対応のふりかえり会を買って出たのは誰？"),
    ("office_hours:mentoring", "後輩の育成について相談できるオフィスアワーを開いている人は？"),
    ("office_hours:pricing", "価格設定で困ったときに質問できる時間を設けているのは誰？"),
    ("office_hours:feedback culture", "フィードバックの文化について気軽に相談できる場を持っている人は？"),
    ("playbook:SQL", "SQLのプレイブックを書いた人は誰？"),
    ("playbook:negotiation", "交渉の手引きをまとめて、他のチームでも使われている人は？"),
    ("playbook:incident response", "障害対応のマニュアルを作成したのは誰ですか？"),
    ("playbook:marketing analytics", "マーケティング分析のガイドを書いて、複数のチームで使われている人を探しています。"),
    ("incident:#growth-analytics", "グロース分析チームで週末に障害対応をして、事後レポートを書いた人は？"),
    ("incident:#design-crit", "デザインレビューのチャンネルで起きた障害を土曜日に引き受けたのは誰？"),
    ("english_sync:#people-ops", "人事オペレーションの定例を英語で回したのは誰？"),
    ("english_sync:#northwind-sync", "Northwindとの定例ミーティングを英語で進行した人は？"),
    ("english_sync:#platform", "プラットフォームチームの定例を初めて英語で仕切ったのは誰？"),
    ("onboarding_guide:SQL training", "SQL研修について、新しく入った人向けのオンボーディング資料を書いたのは誰？"),
    ("onboarding_guide:exchange program", "交換プログラムについて、新メンバー向けのガイドを書いた人は？"),
    ("onboarding_guide:cohort retention", "コホート継続率について新人向けの資料を作ったのは誰？"),
    ("lessons_doc:Northwind integration", "Northwind連携で次は何を変えるべきか、数字付きでまとめた人は？"),
    ("lessons_doc:exchange program", "交換プログラムの反省点をドキュメントにまとめたのは誰ですか？"),
    ("pushback:LMS migration", "LMS移行のスケジュールに、データを示して異を唱えた人は？"),
    ("pushback:cohort retention", "コホート継続率の計画に、根拠を示して反対した人は？"),
    ("pushback:partner onboarding", "パートナー企業の受け入れスケジュールを、データで押し戻した人は？"),
    ("session:skills taxonomy", "スキル体系づくりに自分から取り組んで、チームに採用された人は？"),
    ("session:design system", "デザインシステムに自主的に取り組み、チームで使われるようになった人は？"),
    ("session:pricing experiments", "価格実験を自分で選んで取り組み、成果がチームに採用された人は？"),
    ("writeup:partner onboarding", "パートナーのオンボーディングについてまとめを投稿し、未解決の論点を示した人は？"),
    ("writeup:LMS migration", "LMS移行についてのまとめを投稿したのは誰？"),
]

HOLDOUT_SHARE = 0.25
POS_PER_ASK = 2


def norm(s):
    return " ".join(re.sub(r"\s+", " ", s.strip().lower()).split())


def main():
    rng = random.Random(C.SEED)
    eng = C.engine()
    rows = C.corpus()
    C.write_jsonl(C.DATA / "corpus.jsonl", rows)
    by_intent = collections.defaultdict(list)
    for r in rows:
        by_intent[r["intent"]].append(r)
    missing = [t for t in {r["slots"][C.SLOT[r["template"]]] for r in rows} if t not in TOPIC]
    if missing:
        raise SystemExit(f"no hand-written synonyms for topics: {missing}")

    # ---- hold out intents, per family ----
    held = set()
    for fam in C.FAMILY:
        its = sorted(i for i in by_intent if i.startswith(fam + ":"))
        rng.shuffle(its)
        held |= set(its[: max(1, round(HOLDOUT_SHARE * len(its)))])
    for intent, _ in JA:
        if intent not in by_intent:
            raise SystemExit(f"Japanese ask names an intent that does not exist: {intent}")

    def fill(tpl, topic):
        return re.sub(r"\bthe the\b", "the", tpl.format(t=topic))

    def topic_of(intent):
        return intent.split(":", 1)[1]

    def kw_overlap(ask, intent):
        q = set(eng._terms_map(ask))
        return max((len(q & eng._terms(r["text"])) for r in by_intent[intent] if r["in_pool"]), default=0)

    # ---- train ----
    train_receipts = [r for r in rows if r["intent"] not in held]
    train, train_asks = [], set()
    for intent in sorted(by_intent):
        if intent in held:
            continue
        fam, topic = intent.split(":", 1)
        asks = [(f"kw{k}", fill(ASKS[fam]["kw"][k], topic)) for k in (0, 1)]
        asks += [(f"para{k}/syn{s}", fill(ASKS[fam]["para"][k], TOPIC[topic][s])) for k in (0, 1) for s in (0, 1)]
        pos_texts = sorted({r["text"]: r for r in by_intent[intent]}.values(), key=lambda r: r["id"])
        same_topic = [r for r in train_receipts if r["intent"] != intent and topic in r["slots"].values()]
        same_family = [r for r in train_receipts if r["intent"] != intent and r["intent"].startswith(fam + ":")]
        for tid, ask in asks:
            train_asks.add(norm(ask))
            for pos in rng.sample(pos_texts, min(POS_PER_ASK, len(pos_texts))):
                pool = same_topic if (same_topic and (rng.random() < 0.5 or not same_family)) else (same_family or train_receipts)
                neg = rng.choice(pool)
                train.append({"ask": ask, "positive": pos["text"], "positive_id": pos["id"], "negative": neg["text"], "negative_id": neg["id"],
                              "intent": intent, "negative_intent": neg["intent"], "ask_template": f"{fam}/{tid}", "lang": "en"})
    rng.shuffle(train)

    # ---- test ----
    test = []

    def add_test(ask, intent, tid, reason, lang):
        rel = [r for r in by_intent[intent] if r["in_pool"]]
        if not rel:
            return False
        if norm(ask) in train_asks:
            raise SystemExit(f"test ask also in train: {ask!r}")
        test.append({"ask": ask, "intent": intent, "relevant_receipt_ids": sorted(r["id"] for r in rel),
                     "relevant_person_ids": sorted({r["person"] for r in rel}), "lang": lang, "split": reason,
                     "heldout_intent": intent in held, "ask_template": tid, "kw_overlap": kw_overlap(ask, intent)})
        return True

    skipped = 0
    for intent in sorted(by_intent):
        fam, topic = intent.split(":", 1)
        if intent in held:
            items = [(f"{fam}/kw0", fill(ASKS[fam]["kw"][0], topic)), (f"{fam}/kw2", fill(ASKS[fam]["kw"][2], topic)),
                     (f"{fam}/para0/syn2", fill(ASKS[fam]["para"][0], TOPIC[topic][2])), (f"{fam}/para2/syn2", fill(ASKS[fam]["para"][2], TOPIC[topic][2]))]
            reason = "held_out_intent"
        else:
            items = [(f"{fam}/kw2", fill(ASKS[fam]["kw"][2], topic)), (f"{fam}/para2/syn2", fill(ASKS[fam]["para"][2], TOPIC[topic][2]))]
            reason = "held_out_template"
        for tid, ask in items:
            skipped += not add_test(ask, intent, tid, reason, "en")
    ja_dropped = [intent for intent, ask in JA if not add_test(ask, intent, "ja/hand", "japanese", "ja")]
    if ja_dropped:
        raise SystemExit(f"Japanese asks whose intent has no receipt in the pool: {ja_dropped}")

    C.write_jsonl(C.DATA / "train.jsonl", train)
    C.write_jsonl(C.DATA / "test.jsonl", test)

    # ---- stats ----
    en = [t for t in test if t["lang"] == "en"]
    ja = [t for t in test if t["lang"] == "ja"]
    pool_people = {r["person"] for r in rows if r["in_pool"]}
    lines = [
        "# Pair statistics", "",
        "Generated by `build_pairs.py` (seed %d). Counts only; every number below is computed from the files in this folder." % C.SEED, "",
        "| what | count |", "|---|---|",
        f"| receipts in prototype/data/people.json (generated people) | {len(rows)} |",
        f"| receipts whose text matched exactly one generator template | {len(rows)} |",
        f"| receipts in the retrieval pool (people engine.ask() considers: not on leave) | {sum(r['in_pool'] for r in rows)} |",
        f"| people in the pool | {len(pool_people)} |",
        f"| intents (template family x topic) | {len(by_intent)} |",
        f"| intents held out (test only; receipts never in training) | {len(held)} |",
        f"| intents trained | {len(by_intent) - len(held)} |",
        f"| train pairs (ask, positive, hard negative) | {len(train)} |",
        f"| distinct train asks | {len(train_asks)} |",
        f"| test asks, English | {len(en)} |",
        f"| - on held-out intents | {sum(t['split'] == 'held_out_intent' for t in en)} |",
        f"| - on trained intents, held-out phrasing and synonym | {sum(t['split'] == 'held_out_template' for t in en)} |",
        f"| - sharing no keyword with any correct receipt (engine tokenizer) | {sum(t['kw_overlap'] == 0 for t in en)} |",
        f"| test asks, Japanese (written into build_pairs.py) | {len(ja)} |",
        f"| - on held-out intents | {sum(t['heldout_intent'] for t in ja)} |",
        f"| test asks skipped (intent has no receipt in the pool) | {skipped} |",
        f"| test ask texts that also occur in train | 0 (checked; the build fails otherwise) |",
        "", "Train pairs per family:", "",
        "| family | pairs |", "|---|---|",
    ] + [f"| {fam} | {sum(p['ask_template'].startswith(fam + '/') for p in train)} |" for fam in C.FAMILY]
    (C.DATA / "STATS.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
