"""Generate the fictional company: ~200 employees with skills, a will line, load, availability and
generated receipts of the same shape as the real fixtures. Deterministic (seeded), no LLM, no real names
(surnames and given names are drawn from small fictional-safe lists and combined at random).

Run:  python3 make_people.py   -> data/people.json
The three fixture people (rin, yui, kei) keep their ids; their receipts come from the evidence store.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"
rng = random.Random(2026)

company = json.loads((DATA / "company.json").read_text())
TAGS = company["tags"]

GIVEN = ["Aoi", "Haruto", "Mio", "Ren", "Sora", "Yuna", "Kaito", "Hina", "Riku", "Sakura", "Daichi", "Emi", "Itsuki", "Nao", "Kenta", "Rio",
         "Mina", "Takumi", "Ayaka", "Shota", "Noa", "Yuto", "Hana", "Souta", "Mei", "Kota", "Rina", "Asahi", "Yui", "Ryo",
         "Jun", "Mai", "Leo", "Nana", "Kai", "Sana", "Taro", "Eri", "Gen", "Miku",
         "Priya", "Marcus", "Lena", "Diego", "Amara", "Felix", "Nadia", "Tomas", "Ines", "Jonah", "Wei", "Sofia", "Arun", "Chloe", "Mateo", "Zara"]
FAMILY = ["Aoyama", "Fujimoto", "Hasegawa", "Ikeda", "Kato", "Kimura", "Kobayashi", "Matsuda", "Miura", "Nakagawa", "Nishimura", "Ogawa", "Okamoto",
          "Sakai", "Shimizu", "Sugimoto", "Takeda", "Ueda", "Wada", "Yamaguchi", "Yokoyama", "Endo", "Fukuda", "Goto", "Hara", "Ishii", "Kaneko",
          "Maeda", "Murakami", "Noguchi", "Ono", "Saito", "Taniguchi", "Uchida", "Watanabe",
          "Novak", "Reyes", "Okafor", "Lindqvist", "Haddad", "Moreau", "Bianchi", "Iyer", "Costa", "Schulz"]
TEAMS = {
    "Growth": ["Marketing analyst", "Growth manager", "Content lead", "Lifecycle marketer"],
    "Pricing": ["Product operations", "Pricing analyst", "Product manager"],
    "Platform": ["Software engineer", "Site reliability engineer", "Staff engineer", "Engineering manager"],
    "Search": ["Software engineer", "Machine learning engineer", "Product manager"],
    "Sales Ops": ["Sales operations analyst", "Account manager", "Solutions consultant"],
    "People (HR COE)": ["HR planner", "Recruiter", "L&D partner", "HR systems analyst"],
    "Customer Success": ["Customer success manager", "Onboarding specialist", "Support lead"],
    "Finance": ["FP&A analyst", "Controller", "Procurement lead"],
    "Design": ["Product designer", "UX researcher", "Design manager"],
    "Data": ["Data analyst", "Analytics engineer", "Data scientist"],
}
LOCATIONS = ["Tokyo", "Tokyo", "Tokyo", "Osaka", "Fukuoka", "Austin", "Singapore", "Manila"]
LANGS = ["Japanese", "English", "Korean", "Tagalog", "Mandarin", "Spanish", "Portuguese"]
CHANNELS = ["#growth-analytics", "#pricing", "#platform", "#search", "#people-ops", "#customer-success", "#design-crit", "#data", "#learning", "#all-hands-questions", "#northwind-sync"]

WILL = [
    "I want to lead a small team on {area} next year and stop being the only person who can do {skill}.",
    "I want to spend a year closer to customers, ideally on {area}, and come back with a clearer product sense.",
    "I would like to stay on the Japan side and build the {area} practice here; I am not looking to relocate.",
    "I want to work with the US partner on {area}; my written English is strong and I want to fix the speaking part.",
    "I want to move from {skill} execution to owning outcomes on {area}, even if the title stays the same.",
    "I want to mentor two juniors on {skill} and be measured on how they do, not on my own output.",
    "I want to try a job-based team for a year to see if I work better with clear ownership.",
    "I want to do more {skill} and less coordination; the coordination is what burns me out.",
]
RECEIPT = [
    ("slack", "Posted the {area} write-up in {ch}; two open questions flagged inline."),
    ("slack", "Volunteered to run the {area} retro this quarter so the team lead could focus on hiring."),
    ("slack", "Office hours Thursday for anyone stuck on {skill}; bring your questions."),
    ("docs", "Wrote '{area}: what we would do differently', with the numbers and the decision log."),
    ("slack", "Took the {ch} incident on a Saturday and wrote the post-mortem by Monday."),
    ("docs", "Drafted the {skill} playbook now used by three teams."),
    ("slack", "Pushed back on the {area} timeline in {ch} with data; the plan changed."),
    ("sessions", "Chose to work on: {area} with {skill}. Outcome: adopted by the team."),
    ("slack", "Ran the {ch} sync in English for the first time; notes posted the same day."),
    ("docs", "Onboarding guide for {area}, written for the two new joiners."),
]
AREAS = ["pricing experiments", "cohort retention", "search relevance", "partner onboarding", "FY26 dashboard", "exchange program", "incident response",
         "skills taxonomy", "customer interviews", "Northwind integration", "SQL training", "design system", "hiring loops", "LMS migration"]


def pick_tags(role, n):
    weights = []
    for t in TAGS:
        w = 1.0
        if any(k in role.lower() for k in ("engineer", "sre", "staff")) and t in ("system design", "incident response", "python", "SQL", "documentation"):
            w = 4
        if "analyst" in role.lower() and t in ("data analysis", "SQL", "marketing analytics", "experiment design"):
            w = 4
        if any(k in role.lower() for k in ("manager", "lead", "planner", "partner")) and t in ("stakeholder management", "cross-team coordination", "mentoring", "project management", "org design"):
            w = 4
        if "design" in role.lower() and t in ("customer interviews", "product thinking", "documentation"):
            w = 4
        weights.append(w)
    chosen = set()
    while len(chosen) < n:
        chosen.add(rng.choices(TAGS, weights)[0])
    return {t: rng.choice([3, 3, 4, 4, 5]) for t in sorted(chosen)}  # sorted: set order follows hash randomization, which would make each run differ


def person(i):
    team = rng.choice(list(TEAMS))
    role = rng.choice(TEAMS[team])
    given, fam = rng.choice(GIVEN), rng.choice(FAMILY)
    loc = rng.choice(LOCATIONS)
    langs = ["Japanese", "English"] if loc in ("Tokyo", "Osaka", "Fukuoka") else ["English", rng.choice(LANGS)]
    if rng.random() < 0.3:
        langs.append(rng.choice(LANGS))
    langs = list(dict.fromkeys(langs))
    skills = pick_tags(role, rng.randint(4, 7))
    skill = rng.choice(list(skills))
    area = rng.choice(AREAS)
    tickets = rng.choice([0, 1, 1, 2, 2, 3, 4, 5, 6])
    hours = rng.randint(8, 46)
    avail = "available"
    if hours >= 40 or tickets >= 5:
        avail = "at capacity"
    if rng.random() < 0.06:
        avail = "on leave until " + rng.choice(["2026-10-06", "2026-10-13", "2026-10-20"])
    receipts = []
    for k in range(rng.randint(2, 4)):
        src, tpl = rng.choice(RECEIPT)
        ch = rng.choice(CHANNELS)
        receipts.append({"id": f"gr-{i:03d}-{k}", "source": src, "channel": ch if src == "slack" else None,
                         "date": f"2026-{rng.randint(4, 9):02d}-{rng.randint(1, 28):02d}",
                         "text": tpl.format(area=area, skill=skill, ch=ch)})
    return {
        "id": f"p{i:03d}", "name": f"{given} {fam}", "role": role, "team": team, "location": loc, "languages": langs,
        "tenure_years": rng.randint(1, 12), "skills": skills,
        "will": rng.choice(WILL).format(area=area, skill=skill),
        "load": {"open_tickets": tickets, "hours_booked_this_week": hours},
        "availability": avail, "receipts": receipts, "generated": True,
    }


def main():
    people = [person(i) for i in range(1, 198)]
    # the three fixture people, by id; their receipts come from the evidence store
    for c in company["candidates"]:
        people.append({"id": c["id"], "name": c["name"], "role": c["role"], "team": c["team"], "location": "Tokyo",
                       "languages": ["Japanese", "English"], "tenure_years": c["tenure_years"],
                       "skills": company["tag_scores"].get(c["id"], {}), "will": None,
                       "load": {"open_tickets": {"rin": 4, "yui": 2, "kei": 3}[c["id"]], "hours_booked_this_week": {"rin": 38, "yui": 24, "kei": 31}[c["id"]]},
                       "availability": "available", "receipts": [], "generated": False})
    (DATA / "people.json").write_text(json.dumps(people, indent=1, ensure_ascii=False))
    print(f"wrote {len(people)} people to data/people.json ({sum(1 for p in people if p['availability']=='available')} available)")


if __name__ == "__main__":
    main()
