"""Evidence engine: policy gate -> item store -> claims with receipts -> re-rank -> memo.

Two backends:
  - gemini: Gemini on Vertex (needs `gcloud auth application-default login` and GCP_PROJECT).
  - heuristic: deterministic keyword mode, no network. Used when Gemini is unavailable or MODE=heuristic.

Every claim carries source ids. A claim whose ids are not in the allowed item store is dropped.
"""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"
STATE = Path(os.environ.get("STATE") or (HERE / "state"))
STATE.mkdir(exist_ok=True)

MODE = os.environ.get("MODE", "auto")  # auto | gemini | heuristic
RANK_MODE = os.environ.get("RANK_MODE", "heuristic")  # heuristic (instant) | gemini (~45 s per call, too slow for a live demo)
GCP_PROJECT = os.environ.get("GCP_PROJECT", "recruit-hackathon-2026-e")
GCP_LOCATION = os.environ.get("GCP_LOCATION", "us")
GCP_BASE_URL = os.environ.get("GCP_BASE_URL", "https://aiplatform.us.rep.googleapis.com")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")

STOP = set("the a an and or of to in on for with is are was be by at as it this that we our i my you your they their from not but if so than then who what which will can must".split())


def load(name):
    return json.loads((DATA / name).read_text())


# ---------- policy gate ----------

def policy():
    return json.loads((HERE / "policy.json").read_text())


def item_store():
    """Only allowed sources become items. Excluded sources are counted, never read into the store."""
    pol = policy()
    items = {}
    for src, cfg in pol["allowed_sources"].items():
        for row in load(cfg["file"]):
            if src == "sessions" and not row.get("opted_in"):
                continue
            items[row["id"]] = dict(row, source=src)
    return items


def build_manifest():
    """Count and hash every fixture file once (make manifest). The audit reads excluded sources' counts
    from here, so dm.json is never opened by the evidence path."""
    import hashlib
    man = {}
    for f in sorted(DATA.glob("*.json")):
        if f.name == "manifest.json":
            continue
        raw = f.read_bytes()
        try:
            rows = json.loads(raw)
            count = len(rows) if isinstance(rows, list) else None
        except Exception:  # noqa: BLE001
            count = None
        man[f.name] = {"count": count, "sha256": hashlib.sha256(raw).hexdigest()[:16], "bytes": len(raw)}
    (DATA / "manifest.json").write_text(json.dumps(man, indent=1))
    return man


def manifest():
    f = DATA / "manifest.json"
    return json.loads(f.read_text()) if f.exists() else {}


VIEWS = None


def record_view(cid, who):
    f = STATE / "views.json"
    rows = json.loads(f.read_text()) if f.exists() else []
    rows.append({"candidate": cid, "who": who, "t": time.time()})
    f.write_text(json.dumps(rows, indent=1))
    return rows


def views(cid):
    f = STATE / "views.json"
    rows = json.loads(f.read_text()) if f.exists() else []
    rows = [r for r in rows if r["candidate"] == cid]
    return {"evaluator": len([r for r in rows if r["who"] == "evaluator"]), "subject": len([r for r in rows if r["who"] == cid])}


def audit():
    pol = policy()
    man = manifest()
    used = {}
    for src, cfg in pol["allowed_sources"].items():
        rows = load(cfg["file"])
        n = len([r for r in rows if r.get("opted_in", True)]) if src == "sessions" else len(rows)
        used[src] = {"count": n, "note": cfg["note"]}
    never = {}
    for src, cfg in pol["excluded_sources"].items():
        m = man.get(cfg.get("file", ""), {}) if cfg.get("file") else {}
        never[src] = {"count": m.get("count", 0) or 0, "note": cfg["note"], "sha256": m.get("sha256"), "counted_from": "manifest" if m else "none"}
    return {"purpose": pol["purpose"], "used": used, "never_read": never, "rules": pol["rules"], "manifest": bool(man)}


def items_for(cid):
    store = item_store()
    out = []
    for it in store.values():
        if it["source"] in ("wcm", "manager_notes", "docs", "sessions"):
            if it.get("candidate") == cid:
                out.append(it)
        elif it["source"] == "slack":
            if it["author"] == cid or f"@{cid}" in it["text"].lower() or re.search(rf"\b{re.escape(cid)}\b", it["text"], re.I):
                out.append(it)
    return out


def item_text(it):
    s = it["source"]
    if s == "slack":
        return f"[{it['id']}] Slack {it['channel']} {it['date']} by {it['author']}: {it['text']}"
    if s == "docs":
        return f"[{it['id']}] Doc '{it['title']}' {it['date']}: {it['excerpt']}"
    if s == "wcm":
        return f"[{it['id']}] Will Can Must sheet {it['date']}. WILL: {it['will']} CAN: {it['can']} MUST: {it['must']}"
    if s == "manager_notes":
        return f"[{it['id']}] Manager note by {it['manager']} {it['date']}: {it['text']}"
    if s == "sessions":
        return f"[{it['id']}] AI session {it['date']} (opted in). Problem: {it['problem']} Approach: {it['approach']} Outcome: {it['outcome']} Quoted prompt: \"{it['quoted_prompt']}\""
    return json.dumps(it)


# ---------- LLM backend ----------

_client = None


def gemini_client():
    global _client
    if _client is not None:
        return _client
    from google import genai  # type: ignore

    _client = genai.Client(
        vertexai=True,
        project=GCP_PROJECT,
        location=GCP_LOCATION,
        http_options={"base_url": GCP_BASE_URL},
    )
    return _client


def llm_json(prompt: str):
    """Return parsed JSON from Gemini, or None if the backend is unavailable."""
    if MODE == "heuristic":
        return None
    try:
        client = gemini_client()
        resp = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json", "temperature": 0.2},
        )
        return json.loads(resp.text)
    except Exception as e:  # noqa: BLE001
        if MODE == "gemini":
            raise
        print(f"[engine] gemini unavailable ({type(e).__name__}: {e}); using heuristic mode")
        return None


def backend_name():
    if MODE == "heuristic":
        return "heuristic"
    try:
        gemini_client()
        return f"gemini ({GEMINI_MODEL})"
    except Exception:  # noqa: BLE001
        return "heuristic (gemini client unavailable)"


# ---------- claims with receipts ----------

def _tokens(s):
    return {w for w in re.findall(r"[a-z][a-z\-']+", s.lower()) if w not in STOP}


def heuristic_claims(cid, items, tags):
    claims = []
    for it in items:
        if it["source"] == "wcm":
            claims.append({"text": f"Declared will, in their own words: \"{it['will']}\"", "kind": "declared_will", "source_ids": [it["id"]], "tags": []})
        elif it["source"] == "manager_notes":
            claims.append({"text": f"Manager's paraphrase ({it['manager']}): \"{it['text']}\"", "kind": "manager_paraphrase", "source_ids": [it["id"]], "tags": []})
        elif it["source"] == "slack":
            if it["author"] == cid:
                claims.append({"text": f"Volunteered or acted in {it['channel']}: \"{it['text'][:140]}\"", "kind": "revealed_will", "source_ids": [it["id"]], "tags": [t for t in tags if _tokens(t) & _tokens(it["text"])]})
            else:
                claims.append({"text": f"Mentioned by {it['author']} in {it['channel']}: \"{it['text'][:140]}\"", "kind": "strength", "source_ids": [it["id"]], "tags": []})
        elif it["source"] == "docs":
            claims.append({"text": f"Wrote '{it['title']}': {it['excerpt'][:140]}", "kind": "strength", "source_ids": [it["id"]], "tags": [t for t in tags if _tokens(t) & _tokens(it["excerpt"] + " " + it["title"])]})
        elif it["source"] == "sessions":
            claims.append({"text": f"Chose to work on: {it['problem']}. Outcome: {it['outcome']}", "kind": "revealed_will", "source_ids": [it["id"]], "tags": [t for t in tags if _tokens(t) & _tokens(it["problem"] + " " + it["approach"])]})
    return claims


class LLMUnavailable(RuntimeError):
    pass


def _norm(t):
    t = str(t).lower().replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(re.sub(r"[^\w' ]+", " ", t).split())


def _item_text_fields(it):
    return " ".join(str(it.get(k, "")) for k in ("text", "will", "can", "must", "excerpt", "title", "problem", "approach", "outcome"))


def extract_claims(cid, force=False, mode=None):
    global MODE
    if mode in ("gemini", "heuristic") and mode != MODE:
        MODE = mode
    cache = STATE / f"evidence-{cid}-{backend_name()}.json"
    if cache.exists() and not force:
        return json.loads(cache.read_text())
    company = load("company.json")
    tags = list(company["tag_scores"].get(cid, {}).keys())
    items = items_for(cid)
    store_ids = {it["id"] for it in items}
    name = next(c["name"] for c in company["candidates"] if c["id"] == cid)

    prompt = f"""You are an evidence extractor for an HR decision. Decision: {company['decision']['title']}.
Person: {name} ({cid}). Below are the ONLY items you may use, each with an id in [brackets].

Produce JSON: {{"claims": [{{"text": str, "quote": str, "kind": "declared_will|revealed_will|manager_paraphrase|strength|gap", "source_ids": [str], "tags": [str]}}]}}
Rules:
- Every claim must cite one or more ids from the items below. No id, no claim.
- "quote" = 5 to 25 words copied exactly, character for character, from one of the cited items. A claim whose quote is not found in its item is discarded.
- "declared_will" = what the person wrote about what they want, quoted closely from the Will Can Must sheet.
- "revealed_will" = what they voluntarily did or chose to work on, beyond their assigned duties.
- "manager_paraphrase" = the manager's description, kept separate so it can be compared with the person's own words.
- "strength"/"gap" = concrete, with the evidence. Never give a score. Never speculate beyond the items.
- tags must come from this list: {tags}
- 6 to 12 claims. Short sentences.

Items:
""" + "\n".join(item_text(it) for it in items)

    out = llm_json(prompt)
    backend = "gemini"
    if not out or "claims" not in out:
        if MODE == "gemini":
            raise LLMUnavailable("Gemini did not answer (credentials, quota or network). Retry, or use keyword mode.")
        out = {"claims": heuristic_claims(cid, items, tags)}
        backend = "heuristic"

    by_id = {it["id"]: it for it in items}
    kept, dropped, unfaithful = [], 0, 0
    for c in out["claims"]:
        ids = [s for s in c.get("source_ids", []) if s in store_ids]
        if not ids:
            dropped += 1
            continue
        if backend == "gemini":
            q = _norm(c.get("quote", ""))
            if len(q.split()) < 3 or not any(q in _norm(_item_text_fields(by_id[i])) for i in ids):
                unfaithful += 1
                continue
        c["source_ids"] = ids
        c["tags"] = [t for t in c.get("tags", []) if t in tags]
        kept.append(c)
    result = {"candidate": cid, "backend": backend, "claims": kept, "dropped_unsourced": dropped, "dropped_unfaithful": unfaithful, "generated_at": time.time()}
    cache.write_text(json.dumps(result, indent=1, ensure_ascii=False))
    return result


# ---------- re-rank on a free-text criterion ----------

def rank(criterion: str):
    company = load("company.json")
    ev = {c["id"]: extract_claims(c["id"]) for c in company["candidates"]}
    names = {c["id"]: c["name"] for c in company["candidates"]}

    prompt = f"""An HR planner is choosing one person for: {company['decision']['title']}.
Criterion, in the planner's own words: "{criterion}"

For each candidate, judge how strongly the EVIDENCE below supports the criterion. Cite the claim ids (cl-...) that are receipts.
Return JSON: {{"ranking": [{{"candidate": str, "fit": 0-100, "rationale": str, "receipt_claim_ids": [str]}}]}}
Rules: rationale is 1-2 sentences and must only use the claims below. No receipts, fit must be low. Do not invent.

"""
    claim_index = {}
    for cid, e in ev.items():
        prompt += f"\nCandidate {names[cid]} ({cid}):\n"
        for i, c in enumerate(e["claims"]):
            k = f"cl-{cid}-{i}"
            claim_index[k] = c
            prompt += f"  [{k}] ({c['kind']}) {c['text']}\n"

    out = llm_json(prompt) if RANK_MODE == "gemini" else None
    backend = "gemini"
    if not out or "ranking" not in out:
        backend = "heuristic"
        q = _tokens(criterion)
        ranking = []
        for cid, e in ev.items():
            hits = []
            score = 0
            for i, c in enumerate(e["claims"]):
                ov = len(q & _tokens(c["text"]))
                if ov:
                    score += ov * (2 if c["kind"] in ("revealed_will", "declared_will") else 1)
                    hits.append((ov, f"cl-{cid}-{i}"))
            hits.sort(reverse=True)
            ranking.append({"candidate": cid, "fit": min(100, score * 12), "rationale": f"{len(hits)} evidence items overlap the criterion (keyword mode).", "receipt_claim_ids": [h[1] for h in hits[:3]]})
        out = {"ranking": ranking}

    rows = []
    for r in out["ranking"]:
        cid = r.get("candidate")
        if cid not in names:
            continue
        receipts = []
        for k in r.get("receipt_claim_ids", []):
            if k in claim_index and k.startswith(f"cl-{cid}-"):
                c = claim_index[k]
                receipts.append({"claim_id": k, "text": c["text"], "source_ids": c["source_ids"]})
        rows.append({"candidate": cid, "name": names[cid], "fit": int(r.get("fit", 0)), "rationale": r.get("rationale", ""), "receipts": receipts})
    rows.sort(key=lambda r: -r["fit"])
    result = {"criterion": criterion, "backend": backend, "ranking": rows, "at": time.time()}
    (STATE / "last-rank.json").write_text(json.dumps(result, indent=1, ensure_ascii=False))
    return result


# ---------- annotations (the subject's side) ----------

ANN = STATE / "annotations.json"


def annotations():
    return json.loads(ANN.read_text()) if ANN.exists() else []


def annotate(candidate, source_id, author, text):
    rows = annotations()
    rows.append({"id": f"an-{len(rows)+1:03d}", "candidate": candidate, "source_id": source_id, "author": author, "text": text, "at": time.time()})
    ANN.write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    return rows[-1]


# ---------- decision memo ----------

def memo(cid, criterion=None):
    company = load("company.json")
    name = next(c["name"] for c in company["candidates"] if c["id"] == cid)
    e = extract_claims(cid)
    store = item_store()
    anns = [a for a in annotations() if a["candidate"] == cid]
    last = json.loads((STATE / "last-rank.json").read_text()) if (STATE / "last-rank.json").exists() else None
    crit = criterion or (last["criterion"] if last else "(no criterion stated)")

    lines = [f"# Decision memo: {company['decision']['title']}", "", f"Candidate: {name}", f"Criterion: {crit}", f"Purpose: {company['decision']['purpose']}", ""]
    for kind, title in [("declared_will", "In their own words"), ("manager_paraphrase", "Manager's paraphrase (shown beside, not instead)"), ("revealed_will", "What they chose to do"), ("strength", "Strengths"), ("gap", "Gaps")]:
        cs = [c for c in e["claims"] if c["kind"] == kind]
        if not cs:
            continue
        lines.append(f"## {title}")
        for c in cs:
            lines.append(f"- {c['text']}  [{', '.join(c['source_ids'])}]")
        lines.append("")
    if anns:
        lines.append(f"## {name}'s notes on this evidence")
        for a in anns:
            lines.append(f"- On {a['source_id']}: \"{a['text']}\"")
        lines.append("")
    lines.append("## Sources")
    for sid in sorted({s for c in e["claims"] for s in c["source_ids"]}):
        lines.append(f"- {item_text(store[sid])}")
    lines.append("")
    a = audit()
    lines.append("## Audit")
    lines.append("Used: " + "; ".join(f"{k} ({v['count']}, {v['note']})" for k, v in a["used"].items()))
    lines.append("Never read: " + "; ".join(f"{k} ({v['count']}, {v['note']})" for k, v in a["never_read"].items()))
    v = views(cid)
    lines.append(f"Page views recorded: evaluator {v['evaluator']}, {name} {v['subject']}. Claims dropped for lacking a source: {e['dropped_unsourced']}; dropped as unfaithful to their source: {e.get('dropped_unfaithful', 0)}. Backend: {e['backend']}.")
    return "\n".join(lines)


def reset():
    for p in STATE.glob("*.json"):
        p.unlink()


# ---------- ask: who is the best person for this? (the shared engine behind Meet, Slack and Jira) ----------

STOP = set("the a an and or for of to in on with who is best person someone somebody we need want looking this that our their can will should be by at from as it".split())


def people():
    f = DATA / "people.json"
    return json.loads(f.read_text()) if f.exists() else []


def _person_receipts(p):
    """Receipts as (text, source_label, source_id). Fixture people use the validated evidence store."""
    if not p.get("generated"):
        e = extract_claims(p["id"])
        by = {it["id"]: it for it in items_for(p["id"])}
        out = []
        for c in e["claims"]:
            sid = c["source_ids"][0]
            it = by.get(sid, {})
            lab = {"slack": f"Slack {it.get('channel','')}, {it.get('date','')}", "docs": f"Doc: {it.get('title','')}", "wcm": "Will Can Must sheet",
                   "manager_notes": f"{it.get('manager','')}'s note", "sessions": "AI session, opted in"}.get(it.get("source"), sid)
            out.append((c["text"], lab, sid))
        return out
    return [(r["text"], (f"Slack {r['channel']}, {r['date']}" if r["source"] == "slack" else ("Doc, " if r["source"] == "docs" else "AI session, opted in, ") + r["date"]), r["id"]) for r in p["receipts"]]


def _will(p):
    if p.get("will"):
        return p["will"]
    if not p.get("generated"):
        it = next((i for i in items_for(p["id"]) if i["source"] == "wcm"), None)
        return it["will"] if it else ""
    return ""


def ask(question: str, context: str = "", requester: str | None = None, k: int = 3, pool: list | None = None):
    """Rank people on evidence overlap with the question (skills, will, receipts), minus a load penalty.
    Returns people with why + receipts + load, and a follow-up question when the ask is too vague to rank."""
    q = _tokens(question + " " + (context or "")) - STOP
    rows = []
    for p in people():
        if pool and p["id"] not in pool:
            continue
        if str(p.get("availability", "")).startswith("on leave"):
            continue
        score = 0.0
        hits = []
        for t, lvl in (p.get("skills") or {}).items():
            ov = _tokens(t) & q
            if ov:
                score += 2.0 * lvl / 5
                hits.append(("skill", f"{t} ({lvl}/5)", None))
        w = _will(p)
        if w:
            ov = _tokens(w) & q
            if len(ov) >= 2:
                score += 1.5 + 0.2 * len(ov)
                hits.append(("will", w, None))
        recs = _person_receipts(p)
        for text, lab, sid in recs:
            ov = _tokens(text) & q
            if len(ov) >= 2:
                score += 1.0 + 0.3 * len(ov)
                hits.append(("receipt", text, (lab, sid)))
        load = p.get("load", {})
        util = min(1.0, (load.get("hours_booked_this_week", 0) / 40.0 + load.get("open_tickets", 0) / 6.0) / 2)
        adj = score * (1 - 0.35 * util)
        rows.append((adj, score, util, p, hits, recs))
    rows.sort(key=lambda r: (-r[0], r[2]))
    top = rows[:k]
    out = []
    for adj, score, util, p, hits, recs in top:
        rec_hits = [h for h in hits if h[0] == "receipt"][:2]
        why = [h[1] for h in hits if h[0] != "receipt"][:2] + [h[1] for h in rec_hits]
        out.append({
            "id": p["id"], "name": p["name"], "role": p["role"], "team": p["team"], "location": p.get("location"),
            "languages": p.get("languages", []), "why": why[:3],
            "receipts": [{"text": t, "source": lab, "source_id": sid} for t, lab, sid in ([(h[1], h[2][0], h[2][1]) for h in rec_hits] or recs[:2])],
            "load": p.get("load", {}), "availability": p.get("availability"), "support": round(score, 2),
        })
    follow_up = None
    if not top or top[0][1] <= 0:
        out = []  # nothing bears on the words: ask, do not guess
    if not top or top[0][1] < 2.0 or len(q) < 2:
        if "english" in q or "english" in question.lower():
            follow_up = "Do they need to lead meetings in English, or is written English enough?"
        elif not q:
            follow_up = "What would this person actually do in the first month?"
        else:
            follow_up = "Is this for the Tokyo side or the partner side, and by when?"
    return {"question": question, "criterion": " ".join(sorted(q)), "people": out, "follow_up": follow_up,
            "considered": len(rows), "backend": "keyword", "note": "Order is evidence overlap with the words, minus a load penalty. Not a verdict."}
