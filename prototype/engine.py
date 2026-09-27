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
import threading
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


_VIEWS_LOCK = threading.Lock()


def _read_views():
    f = STATE / "views.json"
    if not f.exists():
        return []
    try:
        return json.loads(f.read_text())
    except ValueError:  # a torn write from before the lock: start over rather than 500 on every view
        return []


def record_view(cid, who):
    """One lock and an atomic replace: two page loads recording a view at once used to tear the file."""
    f = STATE / "views.json"
    with _VIEWS_LOCK:
        rows = _read_views()
        rows.append({"candidate": cid, "who": who, "t": time.time()})
        tmp = f.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(rows, indent=1))
        os.replace(tmp, f)
    return rows


def views(cid):
    rows = _read_views()
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
    out = {"purpose": pol["purpose"], "used": used, "never_read": never, "rules": pol["rules"], "manifest": bool(man)}
    if pol.get("crud_log"):
        f = HERE / pol["crud_log"]["file"]
        n = len([l for l in f.read_text().splitlines() if l.strip()]) if f.exists() else 0
        tomb = STATE / "tombstones.json"
        out["crud_log"] = {"count": n, "removed": len(json.loads(tomb.read_text())) if tomb.exists() else 0, "note": pol["crud_log"]["note"]}
    return out


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
                claims.append({"text": f"Volunteered or acted in {it['channel']}: \"{_clip(it['text'])}\"", "kind": "revealed_will", "source_ids": [it["id"]], "tags": [t for t in tags if _tokens(t) & _tokens(it["text"])]})
            else:
                claims.append({"text": f"Mentioned by {it['author']} in {it['channel']}: \"{_clip(it['text'])}\"", "kind": "strength", "source_ids": [it["id"]], "tags": []})
        elif it["source"] == "docs":
            claims.append({"text": f"Wrote '{it['title']}': {_clip(it['excerpt'])}", "kind": "strength", "source_ids": [it["id"]], "tags": [t for t in tags if _tokens(t) & _tokens(it["excerpt"] + " " + it["title"])]})
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


def _clip(t, n=140):
    """Cut an excerpt at a word boundary (never mid-word) and mark the cut; the trust rule ignores the mark."""
    t = str(t or "")
    if len(t) <= n:
        return t
    cut = t[:n].rsplit(" ", 1)[0].rstrip(" ,;:") or t[:n]
    return cut + "\u2026"


def reset(people_only=False):
    """Clear caches, ranking and annotations; put the people file back to the committed fixture; clear the record logs.
    state/live.jsonl is left alone (a running take keeps its rows). people_only=True (the CRUD take) touches only the
    people file, the record logs (people-log.jsonl, tombstones.json) and the graph cache: annotations, views, evidence
    caches and the filed decision record (asks.jsonl) survive."""
    if not people_only:
        for p in STATE.glob("*.json"):
            p.unlink()
    with PEOPLE_LOCK:
        base = DATA / "people.base.json"
        if base.exists():
            _write_people_locked(json.loads(base.read_text()))
        for name in ("people-log.jsonl",) + (() if people_only else ("asks.jsonl",)):
            f = STATE / name
            if f.exists():
                f.write_text("")
        if TOMBSTONES.exists():
            TOMBSTONES.unlink()
    _GRAPH.clear()


# ---------- ask: who is the best person for this? (the shared engine behind Meet, Slack and Jira) ----------

STOP = set("the a an and or for of to in on with who is best person someone somebody we need want looking this that our their can will should be by at from as it".split())
STOP |= set("own instead hold just have they actually also good really anyone".split())

# Spoken phrases that are one idea: mapped to one token before tokenising, and printed back as the speaker said them.
PHRASES = [("push back", "pushback"), ("pushes back", "pushback"), ("pushed back", "pushback"), ("pushing back", "pushback"),
           ("hold their own", "holdown"), ("holds their own", "holdown"), ("hold her own", "holdown"), ("hold his own", "holdown"), ("holding their own", "holdown")]
PHRASE_SURFACE = {"pushback": "push back", "holdown": "hold their own"}


def _phrase(s):
    s = str(s or "")
    for a, b in PHRASES:
        s = re.sub(r"\b" + re.escape(a) + r"\b", b, s, flags=re.I)
    return s


def _stem(w):
    """Light stemming so 'meeting' meets 'meetings' and 'leading' meets 'lead'. Not linguistics; enough for word forms in a spoken ask."""
    for suf in ("ings", "ing", "ies", "es", "ed", "s"):
        if len(w) > len(suf) + 2 and w.endswith(suf):
            w = w[:-len(suf)] + ("y" if suf == "ies" else "")
            break
    return w


def _terms(s):
    return {_stem(t) for t in _tokens(_phrase(s))} - STOP


def _terms_map(s):
    """stem -> the word as the asker said it (first occurrence, original case), so the UI prints their words.
    Phrases come back as phrases ('pushback' -> 'push back')."""
    out = {}
    for m in re.finditer(r"[A-Za-z][A-Za-z\-']+", _phrase(s)):
        w = m.group(0)
        lw = w.lower()
        if lw in STOP:
            continue
        st = _stem(lw)
        if st in STOP or st in out:
            continue
        out[st] = PHRASE_SURFACE.get(lw, w)
    return out


# ---------- the fictional company's offices: attached to every person at read time; people.json is never regenerated ----------

CITIES = {"Tokyo": (35.69, 139.69, "Asia/Tokyo", "JST"), "Osaka": (34.69, 135.50, "Asia/Tokyo", "JST"), "Fukuoka": (33.59, 130.40, "Asia/Tokyo", "JST"),
          "Singapore": (1.35, 103.82, "Asia/Singapore", "SGT"), "Manila": (14.60, 120.98, "Asia/Manila", "PHT"), "Austin": (30.27, -97.74, "America/Chicago", "CT")}
SLOT = {"label": "Northwind Labs (US partner)", "side": "US", "city": None}  # company.json names no city; none may be invented
REGION_ALIASES = {"us side": ["Austin"], "partner side": ["Austin"], "partner's side": ["Austin"], "us partner": ["Austin"], "in the us": ["Austin"], "stateside": ["Austin"],
                  "japan side": ["Tokyo", "Osaka", "Fukuoka"], "hq": ["Tokyo", "Osaka", "Fukuoka"], "head office": ["Tokyo", "Osaka", "Fukuoka"], "in japan": ["Tokyo", "Osaka", "Fukuoka"],
                  "japanese side": ["Tokyo", "Osaka", "Fukuoka"], "tokyo side": ["Tokyo"]}


def geo(location):
    c = CITIES.get(location or "")
    return {"lat": c[0], "lon": c[1], "tz": c[2], "abbr": c[3]} if c else None


def _people_raw():
    f = DATA / "people.json"
    return json.loads(f.read_text()) if f.exists() else []


def people():
    rows = _people_raw()
    for p in rows:
        p["geo"] = geo(p.get("location"))
    return rows


def cities():
    counts = {}
    for p in _people_raw():
        counts[p.get("location")] = counts.get(p.get("location"), 0) + 1
    return {"cities": {k: {"lat": v[0], "lon": v[1], "tz": v[2], "abbr": v[3], "count": counts.get(k, 0)} for k, v in CITIES.items()}, "slot": dict(SLOT)}


def fixture_ids():
    return [c["id"] for c in load("company.json")["candidates"]]


def is_fixture(p):
    return (p.get("id") if isinstance(p, dict) else p) in fixture_ids()


def _gen_receipt_label(r):
    return f"Slack {r['channel']}, {r['date']}" if r["source"] == "slack" else ("Doc, " if r["source"] == "docs" else "AI session, opted in, ") + r["date"]


def _own_evidence(p):
    """What the person themselves wrote or did, as (text, source_id): their will line and the receipts they authored.
    Manager notes, mentions by others and skill tags are not here: a tag without a receipt is a bare tag, a paraphrase is not their words."""
    out = []
    if is_fixture(p):
        for it in items_for(p["id"]):
            if it["source"] == "wcm":
                out.append((it["will"], it["id"]))
            elif it["source"] == "slack" and it.get("author") == p["id"]:
                out.append((it["text"], it["id"]))
            elif it["source"] == "docs":
                out.append((f"{it['title']} {it['excerpt']}", it["id"]))
            elif it["source"] == "sessions" and it.get("opted_in"):
                out.append((f"{it['problem']} {it['approach']} {it['outcome']}", it["id"]))
        return out
    if p.get("will"):
        out.append((p["will"], f"will-{p['id']}"))
    for r in p.get("receipts") or []:
        out.append((r["text"], r["id"]))
    return out


def coverage(question_terms: dict, p):
    """asked = the ask's words; covered = {word: [source ids where the person's own evidence uses it]}; missing = the rest.
    confidence = round(100 * covered / asked). Coverage of the ask, never a score of the person."""
    asked = list(question_terms.values())
    covered = {}
    for text, sid in _own_evidence(p):
        ts = _terms(text)
        for st, word in question_terms.items():
            if st in ts:
                covered.setdefault(word, [])
                if sid not in covered[word]:
                    covered[word].append(sid)
    missing = [w for w in asked if w not in covered]
    conf = round(100 * len(covered) / len(asked)) if asked else 0
    return {"confidence": conf, "asked": asked, "covered": covered, "missing": missing}


def _person_receipts(p):
    """Receipts as (text, source_label, source_id). Fixture people use the validated evidence store."""
    if is_fixture(p):
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
    return [(r["text"], _gen_receipt_label(r), r["id"]) for r in p.get("receipts") or []]


def _will(p):
    if p.get("will"):
        return p["will"]
    if is_fixture(p):
        it = next((i for i in items_for(p["id"]) if i["source"] == "wcm"), None)
        return it["will"] if it else ""
    return ""


ASK_NOTE = "Confidence is how much of this ask has a receipt for this person. Not a score of the person."


def ask(question: str, context: str = "", requester: str | None = None, k: int = 3, pool: list | None = None):
    """Rank people on evidence overlap with the question (skills, will, receipts), minus a load penalty.
    Returns people with why + receipts + load, and a follow-up question when the ask is too vague to rank."""
    qmap = _terms_map(question + " " + (context or ""))
    q = set(qmap)
    rows = []
    for p in people():
        if pool and p["id"] not in pool:
            continue
        if str(p.get("availability", "")).startswith("on leave"):
            continue
        score = 0.0
        hits = []
        for t, lvl in (p.get("skills") or {}).items():
            ov = _terms(t) & q
            if ov:
                score += 2.0 * lvl / 5
                hits.append(("skill", f"{t} ({lvl}/5)", None))
        w = _will(p)
        if w:
            ov = _terms(w) & q
            if len(ov) >= 2:
                score += 1.5 + 0.2 * len(ov)
                hits.append(("will", w, None))
        recs = _person_receipts(p)
        for text, lab, sid in recs:
            ov = _terms(text) & q
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
        cov = coverage(qmap, p)
        if not rec_hits:  # no receipt overlaps two words: show the ones that covered a word before any other
            lit = {sid for sids in cov["covered"].values() for sid in sids}
            recs = sorted(recs, key=lambda r: (r[2] not in lit))
        out.append({
            "id": p["id"], "name": p["name"], "role": p["role"], "team": p["team"], "location": p.get("location"), "geo": p.get("geo"),
            "languages": p.get("languages", []), "why": why[:3],
            "receipts": [{"text": t, "source": lab, "source_id": sid} for t, lab, sid in ([(h[1], h[2][0], h[2][1]) for h in rec_hits] or recs[:2])],
            "load": p.get("load", {}), "availability": p.get("availability"), "support": round(score, 2),
            "confidence": cov["confidence"], "asked": cov["asked"], "covered": cov["covered"], "missing": cov["missing"],
            "badge": "seeded" if is_fixture(p) else ("simulated" if p.get("generated") else added_badge(p)),
        })
    follow_up = None
    if not top or top[0][1] <= 0:
        out = []  # nothing bears on the words: ask, do not guess
    if not top or top[0][1] < 2.0 or len(q) < 3:
        # under three content words there is nothing to count coverage against (the page prints no number), so Pik asks for more
        if "english" in q or "english" in question.lower():
            follow_up = "Do they need to lead meetings in English, or is written English enough?"
        elif len(q) < 3:
            follow_up = "What would this person actually do in the first month?"
        else:
            words = ", ".join(sorted(q)[:4])
            follow_up = f"Nothing on file mentions {words}. What would this person actually do, and for which team?"
    return {"question": question, "criterion": " ".join(sorted(q)), "asked": list(qmap.values()), "people": out, "follow_up": follow_up,
            "considered": len(rows), "backend": "keyword", "note": ASK_NOTE}


# ---------- the composed screen (Meet): the engine supplies every name, quote and constraint match ----------

SOURCE_LABEL = {"slack": lambda it: f"Slack {it.get('channel','')}, {it.get('date','')}", "docs": lambda it: f"Doc: {it.get('title','')}",
                "wcm": lambda it: f"Will Can Must sheet, {it.get('date','')}", "manager_notes": lambda it: f"{it.get('manager','')}'s note, {it.get('date','')}",
                "sessions": lambda it: f"AI session, opted in, {it.get('date','')}"}


def source_label(it):
    return SOURCE_LABEL.get(it.get("source"), lambda i: i.get("id", ""))(it)


def receipt_for(person: str, kind: str = "claim", about: str = ""):
    """One verbatim quote for a person, with its source id. kind: own_words (the WCM will line), manager (the manager's note),
    or claim (the extracted claim whose quote best overlaps `about`). Returns None if the person or source is unknown."""
    company = load("company.json")
    c = next((x for x in company["candidates"] if x["id"] == person), None)
    if not c:
        return None
    items = {it["id"]: it for it in items_for(person)}
    if kind == "own_words":
        it = next((i for i in items.values() if i["source"] == "wcm"), None)
        return it and {"person": person, "name": c["name"], "text": it["will"], "source": source_label(it), "source_id": it["id"], "stamp": "verbatim", "kind": kind}
    if kind == "manager":
        it = next((i for i in items.values() if i["source"] == "manager_notes"), None)
        return it and {"person": person, "name": c["name"], "text": it["text"], "source": source_label(it), "source_id": it["id"], "stamp": "paraphrase", "kind": kind}
    e = extract_claims(person)
    q = _terms(about or "")
    best, best_ov = None, -1
    for cl in e["claims"]:
        if cl["kind"] in ("declared_will", "manager_paraphrase"):
            continue
        ov = len(q & _terms(cl.get("quote") or cl["text"])) + len(q & _terms(cl["text"]))
        if ov > best_ov:
            best, best_ov = cl, ov
    if not best:
        return None
    sid = best["source_ids"][0]
    it = items.get(sid)
    if not it:
        return None
    # the receipt text must sit verbatim inside the item (the page's trust rule): a Gemini quote passes as is; a
    # keyword-mode claim is a wrapper around the quote ('Volunteered or acted in #ch: "..."'), so the item's own words are used
    text = best.get("quote") or ""
    if not text or _norm(text) not in _norm(item_text(it)):
        text = _verbatim(it)
    return {"person": person, "name": c["name"], "text": text, "source": source_label(it), "source_id": sid,
            "stamp": "verbatim", "kind": "claim", "claim_kind": best["kind"]}


def _verbatim(it):
    """The words the item itself carries (what the person wrote or did), never a wrapper around them."""
    s = it.get("source")
    if s == "slack" or s == "manager_notes":
        return str(it.get("text") or "")
    if s == "docs":
        return str(it.get("excerpt") or "")
    if s == "wcm":
        return str(it.get("will") or "")
    if s == "sessions":
        return str(it.get("problem") or "")
    return str(it.get("text") or "")


def display_name(who):
    """A requester id ('aya') as a name ('Aya Nakamura'): the planner in company.json, a candidate, or a person on file."""
    who = str(who or "")
    company = load("company.json")
    pl = (company.get("decision") or {}).get("planner") or {}
    if pl.get("id") == who:
        return pl.get("name") or who
    for c in company.get("candidates", []):
        if c["id"] == who:
            return c["name"]
    for p in _people_raw():
        if p["id"] == who:
            return p["name"]
    return who


def added_badge(p):
    """'added by <name> · <date>' for a record HR added by conversation (the badge contract; the page prints the same)."""
    by = display_name(p.get("added_by") or "HR")
    at = str(p.get("added_at") or "")[:10]
    return f"added by {by}" + (f" · {at}" if at else "")


def constraint(text: str, pool: list | None = None, named: list | None = None):
    """Which people a stated constraint touches, from facts on file (team, role, location, availability), never from judgement.
    `named` are ids the speakers themselves named; they are kept with the reason 'named on the call'."""
    company = load("company.json")
    ids = pool or [c["id"] for c in company["candidates"]]
    q = _terms(text)
    low = " " + _norm(text) + " "
    alias_cities = set()  # 'US side' / 'partner side' -> Austin; 'Japan side' / 'HQ' -> Tokyo, Osaka, Fukuoka
    for phrase, cs in REGION_ALIASES.items():
        if f" {phrase} " in low:
            alias_cities.update(cs)
    by_id = {p["id"]: p for p in people()}
    affects = []
    for cid in ids:
        p = by_id.get(cid) or next((dict(c) for c in company["candidates"] if c["id"] == cid), None)
        if not p:
            continue
        for field in ("team", "role", "location", "availability"):
            v = str(p.get(field) or "")
            ov = _terms(v) & q
            if field == "location" and v in alias_cities:
                ov = {v}
            if ov:
                reason = {"team": f"on the {v} team", "location": f"based in {v}", "availability": f"availability: {v}"}.get(field, f"{field}: {v}")
                affects.append({"id": cid, "name": p["name"], "reason": reason, "field": field})
                break
    for cid in named or []:
        if cid in ids and not any(a["id"] == cid for a in affects):
            p = by_id.get(cid) or next((c for c in company["candidates"] if c["id"] == cid), {})
            affects.append({"id": cid, "name": p.get("name", cid), "reason": "named on the call", "field": "said"})
    return {"text": text, "affects": affects}


# ---------- people records: read one, add, edit, remove (HR by conversation; every write is logged) ----------


PEOPLE_LOCK = threading.Lock()
PEOPLE_LOG = STATE / "people-log.jsonl"
TOMBSTONES = STATE / "tombstones.json"
LIVE_EVENTS = STATE / "live.jsonl"

# The company's ten teams and their roles (the same list make_people.py generated from; copied so importing this module never regenerates anyone).
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
TEAM_SHORT = {"hr": "People (HR COE)", "people": "People (HR COE)", "people ops": "People (HR COE)", "hr coe": "People (HR COE)", "coe": "People (HR COE)",
              "cs": "Customer Success", "customer success": "Customer Success", "success": "Customer Success",
              "sales ops": "Sales Ops", "sales operations": "Sales Ops", "salesops": "Sales Ops"}
ROLES = sorted({r for rs in TEAMS.values() for r in rs}) + ["Senior marketing analyst"]
LANGS = ["Japanese", "English", "Korean", "Tagalog", "Mandarin", "Spanish", "Portuguese"]
AVAILABILITY = ("available", "at capacity")


def tags():
    return list(load("company.json")["tags"])


def _public(p):
    """A person record as the API returns it: with geo, without nothing else changed."""
    p = dict(p)
    p["geo"] = geo(p.get("location"))
    p["seeded"] = is_fixture(p)
    return p


def get_person(pid: str):
    """The full record (receipts included) plus geo; None when unknown."""
    p = next((x for x in _people_raw() if x["id"] == pid), None)
    return _public(p) if p else None


def _write_people_locked(rows):
    """Atomic rewrite of data/people.json: tmp file next to it, then os.replace. Caller holds PEOPLE_LOCK."""
    f = DATA / "people.json"
    tmp = f.with_suffix(".json.tmp")
    for r in rows:
        r.pop("geo", None)
        r.pop("seeded", None)
    tmp.write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    os.replace(tmp, f)
    _GRAPH.clear()


def _log_row(row):
    with PEOPLE_LOG.open("a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _live_row(**payload):
    row = {"t": time.time(), **payload}
    with LIVE_EVENTS.open("a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def tombstones():
    return json.loads(TOMBSTONES.read_text()) if TOMBSTONES.exists() else []


def _next_id(rows):
    used = [int(r["id"][1:]) for r in rows if re.fullmatch(r"p\d+", r["id"])]
    used += [int(t["id"][1:]) for t in tombstones() if re.fullmatch(r"p\d+", str(t.get("id", "")))]
    return f"p{(max(used) + 1) if used else 1:03d}"


def _validate(fields: dict, rows: list, exclude_id: str | None = None, require: tuple = ()):
    """Returns (clean, problems). problems is the list of field names that are missing or not on the allowed lists."""
    clean, bad = {}, []
    for k in require:
        if not fields.get(k):
            bad.append(k)
    if "name" in fields:
        name = " ".join(str(fields["name"]).split())
        if not name or len(name) > 60:
            bad.append("name")
        elif any(r["name"].lower() == name.lower() and r["id"] != exclude_id for r in rows):
            bad.append("name (already on file)")
        else:
            clean["name"] = name
    if "role" in fields and fields["role"] is not None:
        role = str(fields["role"]).strip()
        if not role or len(role) > 60:
            bad.append("role")
        else:
            clean["role"] = next((r for r in ROLES if r.lower() == role.lower()), role)
    if "team" in fields and fields["team"] is not None:
        t = str(fields["team"]).strip()
        hit = next((k for k in TEAMS if k.lower() == t.lower()), None) or TEAM_SHORT.get(t.lower())
        if hit:
            clean["team"] = hit
        else:
            bad.append("team")
    if "location" in fields and fields["location"] is not None:
        loc = str(fields["location"]).strip()
        hit = next((c for c in CITIES if c.lower() == loc.lower()), None)
        if hit:
            clean["location"] = hit
        else:
            bad.append("location")
    if "languages" in fields and fields["languages"] is not None:
        langs = fields["languages"] if isinstance(fields["languages"], list) else [fields["languages"]]
        out = []
        for l in langs:
            hit = next((x for x in LANGS if x.lower() == str(l).strip().lower()), None)
            if not hit:
                bad.append("languages")
                break
            if hit not in out:
                out.append(hit)
        else:
            clean["languages"] = out
    if "skills" in fields and fields["skills"] is not None:
        sk = fields["skills"]
        if isinstance(sk, list):
            sk = {s: 3 for s in sk}
        ok = isinstance(sk, dict) and all(k in tags() and isinstance(v, int) and 1 <= v <= 5 for k, v in sk.items())
        if ok:
            clean["skills"] = sk
        else:
            bad.append("skills")
    if "availability" in fields and fields["availability"] is not None:
        a = " ".join(str(fields["availability"]).lower().split())
        if a in AVAILABILITY or re.fullmatch(r"on leave until \d{4}-\d{2}-\d{2}", a):
            clean["availability"] = a
        else:
            bad.append("availability")
    if "will" in fields:
        w = fields["will"]
        if w is None or (isinstance(w, str) and len(w) <= 600):
            clean["will"] = (w.strip() or None) if isinstance(w, str) else None
        else:
            bad.append("will")
    return clean, bad


class RecordError(ValueError):
    def __init__(self, msg, code=400, missing=None):
        super().__init__(msg)
        self.code = code
        self.missing = missing or []


def add_person(fields: dict, by: str | None = None, said: str | None = None):
    """POST /api/people. A new record with will:null and receipts:[]: HR never writes someone's will, and receipts arrive as they work."""
    with PEOPLE_LOCK:
        rows = _people_raw()
        clean, bad = _validate({k: fields.get(k) for k in ("name", "role", "team", "location", "languages", "skills", "availability")}, rows,
                               require=("name", "role", "team", "location"))
        if bad:
            raise RecordError("not added: " + ", ".join(bad), 400, bad)
        p = {"id": _next_id(rows), "name": clean["name"], "role": clean["role"], "team": clean["team"], "location": clean["location"],
             "languages": clean.get("languages") or ["English"], "tenure_years": 0, "skills": clean.get("skills") or {}, "will": None,
             "load": {"open_tickets": 0, "hours_booked_this_week": 0}, "availability": clean.get("availability") or "available",
             "receipts": [], "generated": False, "added_by": by or "HR", "added_at": time.strftime("%Y-%m-%d")}
        rows.append(p)
        _write_people_locked(rows)
        pub = _public(p)
        _log_row({"t": time.time(), "op": "add", "person": pub, "by": by or "HR", "said": said})
        _live_row(kind="record", op="add", person=pub, by=by or "HR", said=said)
    return pub


def edit_person(pid: str, fields: dict, by: str | None = None, said: str | None = None):
    """PATCH /api/people/{id}: role, team, location, languages, availability, skills, will."""
    with PEOPLE_LOCK:
        rows = _people_raw()
        p = next((x for x in rows if x["id"] == pid), None)
        if not p:
            raise RecordError("unknown person", 404)
        allowed = ("role", "team", "location", "languages", "availability", "skills", "will")
        want = {k: fields[k] for k in allowed if k in fields}
        if not want:
            raise RecordError("nothing to change", 400, ["one of " + ", ".join(allowed)])
        clean, bad = _validate(want, rows, exclude_id=pid)
        if bad:
            raise RecordError("not changed: " + ", ".join(bad), 400, bad)
        changed = [k for k, v in clean.items() if p.get(k) != v]
        p.update(clean)
        if changed:
            _write_people_locked(rows)
        pub = _public(p)
        _log_row({"t": time.time(), "op": "edit", "person": pub, "changed": changed, "by": by or "HR", "said": said})
        _live_row(kind="record", op="edit", person=pub, changed=changed, by=by or "HR", said=said)
    return pub, changed


def remove_person(pid: str, by: str | None = None, said: str | None = None):
    """DELETE /api/people/{id}. The three seeded people stay (409); everyone else leaves a tombstone for the audit line."""
    with PEOPLE_LOCK:
        rows = _people_raw()
        p = next((x for x in rows if x["id"] == pid), None)
        if not p:
            raise RecordError("unknown person", 404)
        if is_fixture(p):
            raise RecordError("fixture people cannot be removed", 409)
        rows = [x for x in rows if x["id"] != pid]
        _write_people_locked(rows)
        ts = tombstones()
        ts.append({"t": time.time(), "id": p["id"], "name": p["name"], "role": p["role"], "team": p["team"], "location": p.get("location"),
                   "receipts": len(p.get("receipts") or []), "by": by or "HR"})
        TOMBSTONES.write_text(json.dumps(ts, indent=1, ensure_ascii=False))
        pub = _public(p)
        _log_row({"t": time.time(), "op": "remove", "person": pub, "by": by or "HR", "said": said})
        _live_row(kind="record", op="remove", person={"id": p["id"], "name": p["name"], "role": p["role"], "team": p["team"], "location": p.get("location")}, by=by or "HR", said=said)
    return {"id": p["id"], "name": p["name"]}


# ---------- the graph: people and the public channels they posted in; one edge kind, no judgement ----------

_GRAPH: dict = {}


def graph():
    """{nodes, hubs, edges}. Edges are person -> channel hub = 'posted in this public allowlisted channel', weighted by receipt count.
    The three seeded people's channels come from their authored Slack receipts in the evidence store. Cached by people.json mtime."""
    f = DATA / "people.json"
    key = (f.stat().st_mtime_ns if f.exists() else 0, (DATA / "slack.json").stat().st_mtime_ns if (DATA / "slack.json").exists() else 0)
    hit = _GRAPH.get("entry")  # one atomic read: a concurrent _GRAPH.clear() can never split the key from its value
    if hit and hit[0] == key:
        return hit[1]
    rows = _people_raw()
    fix = set(fixture_ids())
    hubs: dict = {}
    edges: dict = {}
    nodes = []
    for p in rows:
        recs = p.get("receipts") or []
        n = len(recs)
        for r in recs:
            ch = r.get("channel")
            if r.get("source") == "slack" and ch:
                hubs[ch] = hubs.get(ch, 0) + 1
                edges[(p["id"], ch)] = edges.get((p["id"], ch), 0) + 1
        nodes.append({"id": p["id"], "name": p["name"], "role": p["role"], "team": p["team"], "location": p.get("location"), "geo": geo(p.get("location")),
                      "availability": p.get("availability"), "generated": bool(p.get("generated")), "seeded": p["id"] in fix,
                      **({"added_by": p["added_by"]} if p.get("added_by") else {}), "receipt_count": n})
    allow = set(hubs)  # the seeded people join the hubs that already exist; no hub is created for them
    for p in rows:
        if p["id"] not in fix:
            continue
        n = 0
        for it in items_for(p["id"]):
            if it["source"] == "slack" and it.get("author") == p["id"]:
                n += 1
                ch = it.get("channel")
                if ch in allow:
                    hubs[ch] += 1
                    edges[(p["id"], ch)] = edges.get((p["id"], ch), 0) + 1
            elif it["source"] in ("docs", "sessions") and it.get("opted_in", True):
                n += 1
        for nd in nodes:
            if nd["id"] == p["id"]:
                nd["receipt_count"] = n
    value = {"nodes": nodes, "hubs": [{"id": k, "count": v} for k, v in sorted(hubs.items(), key=lambda kv: (-kv[1], kv[0]))],
             "edges": [{"source": s, "target": t, "count": c} for (s, t), c in sorted(edges.items())],
             "note": "one edge kind: posted in this public allowlisted channel. No DMs, no reporting lines, no predicted fit."}
    _GRAPH["entry"] = (key, value)
    return value


# ---------- CRUD by conversation: one sentence -> a draft, never a write (the human confirms) ----------

RX_ADD = re.compile(r"\b(add|onboard|new (?:hire|member)|joined)\b", re.I)
RX_EDIT = re.compile(r"\b(move|set|update|change|mark|is now|on leave|back from leave)\b", re.I)
RX_REMOVE = re.compile(r"\b(remove|delete|offboard|left the company)\b", re.I)
RX_NAME = re.compile(r"\b([A-Z][a-z]+(?:-[A-Z][a-z]+)?) ([A-Z][a-z]+(?:-[A-Z][a-z]+)?)\b")
_NAME_SKIP = {w.lower() for w in ["New Hire", "New Member", "Sales Ops", "Customer Success", "Product Operations", "Product Manager", "Hong Kong"]}


def _find_name(text: str, after: int = 0):
    """The first capitalised two-word span after `after` that is not a team, a role or a city."""
    for m in RX_NAME.finditer(text, after):
        span = m.group(0)
        if span.lower() in _NAME_SKIP or m.group(1) in CITIES or m.group(2) in CITIES:
            continue
        if any(span.lower() == r.lower() for r in ROLES) or any(span.lower() == t.lower() for t in TEAMS):
            continue
        return span
    return None


ROLE_ABBREV = {"ops": "operations", "eng": "engineer", "engg": "engineering", "mgr": "manager", "pm": "product manager", "sre": "site reliability engineer",
               "swe": "software engineer", "ml": "machine learning", "cs": "customer success", "csm": "customer success manager", "fp&a": "fp&a", "ux": "ux",
               "analytics": "analytics", "dev": "engineer", "developer": "engineer", "designer": "designer", "recruiting": "recruiter", "l&d": "l&d"}


def _find_role(text: str):
    """Fuzzy: every token of the role appears in the text as a whole word, an abbreviation ('ops' -> operations) or a stem/prefix."""
    words = []
    for w in re.findall(r"[A-Za-z&/'+-]+", text):
        words += ROLE_ABBREV.get(w.lower(), w.lower()).split()
    best, best_len = None, 0
    for role in ROLES:
        toks = [t.lower() for t in re.findall(r"[A-Za-z&/'+-]+", role)]
        ok = all(any(w == t or (len(w) >= 3 and t.startswith(w)) or (len(t) >= 4 and w.startswith(t)) for w in words) for t in toks)
        if ok and len(toks) > best_len:
            best, best_len = role, len(toks)
    return best


def _find_team(text: str):
    low = " " + _norm(text) + " "
    hits = [(low.find(" " + t.lower() + " "), t) for t in TEAMS if " " + t.lower() + " " in low]
    hits += [(low.find(" " + k + " "), v) for k, v in TEAM_SHORT.items() if " " + k + " " in low]
    for m in re.finditer(r"\b(?:on|to|in|into|joins?|joining) (?:the )?([A-Za-z&/ ]+?)(?: team)?\b[,.;]", text):  # 'on Pricing,' 'to the Data team.'
        t = m.group(1).strip()
        hit = next((k for k in TEAMS if k.lower() == t.lower()), None) or TEAM_SHORT.get(t.lower())
        if hit:
            hits.append((m.start(), hit))
    return min(hits)[1] if hits else None


def _find_location(text: str):
    low = " " + _norm(text) + " "
    hits = [(low.find(" " + c.lower() + " "), c) for c in CITIES if " " + c.lower() + " " in low]
    return min(hits)[1] if hits else None


def _find_languages(text: str):
    low = " " + _norm(text) + " "
    return [l for l in LANGS if " " + l.lower() + " " in low]


def _find_availability(text: str):
    low = " ".join(str(text).lower().replace(",", " ").replace(".", " ").split())
    if "back from leave" in low or "back at work" in low:
        return "available"
    m = re.search(r"on leave(?: until| till| through)? (\d{4}-\d{2}-\d{2})", low)
    if m:
        return f"on leave until {m.group(1)}"
    m = re.search(r"on leave(?: until| till| through)? ([a-z]+ \d{1,2})(?:st|nd|rd|th)?", low)
    if m:
        try:
            import datetime as _dt
            d = _dt.datetime.strptime(m.group(1).title() + f" {time.gmtime().tm_year}", "%B %d %Y")
            return f"on leave until {d:%Y-%m-%d}"
        except ValueError:
            pass
    if re.search(r"\bon leave\b", low):
        return None  # said 'on leave' without a date: ask
    if "at capacity" in low or "fully booked" in low:
        return "at capacity"
    if re.search(r"\b(is )?available\b", low):
        return "available"
    return None


def _people_named(name: str):
    n = name.lower()
    rows = _people_raw()
    exact = [p for p in rows if p["name"].lower() == n]
    if exact:
        return exact
    parts = n.split()
    return [p for p in rows if all(part in p["name"].lower().split() for part in parts)]


def _first(name: str):
    return name.split()[0]


def parse_command(text: str, requester: str | None = None):
    """Rules parser for the B2 input. Returns a draft (add/edit/remove) or an ask; it never writes.
    {intent, draft?, target?, missing?, question?, ambiguous?, ask?, backend:'rules'}"""
    text = " ".join(str(text or "").split())
    out = {"intent": "ask", "backend": "rules"}
    m_add, m_edit, m_rem = RX_ADD.search(text), RX_EDIT.search(text), RX_REMOVE.search(text)
    intent = "add" if m_add else "edit" if m_edit else "remove" if m_rem else "ask"
    if intent == "ask":
        out["ask"] = ask(text, "", requester)
        return out
    verb = {"add": m_add, "edit": m_edit, "remove": m_rem}[intent]
    out["intent"] = intent
    name = _find_name(text, verb.end()) or _find_name(text)
    if not name:
        out["missing"] = ["name"]
        out["question"] = {"add": "Who should Pik add? A first and last name.", "edit": "Whose record should change?", "remove": "Whose record should Pik remove?"}[intent]
        return out
    matches = _people_named(name)

    if intent == "add":
        if matches:
            out["ambiguous"] = [p["id"] for p in matches]
            desc = "; ".join(f"{p['name']} ({p['team']}, {p['location']})" for p in matches[:3])
            out["question"] = f"{name} is already on file: {desc}. Update that record, or add a second {name}?"
            return out
        role, team, loc = _find_role(text), _find_team(text), _find_location(text)
        langs = _find_languages(text)
        avail = _find_availability(text) or "available"
        draft = {"name": name, "role": role, "team": team, "location": loc, "languages": langs or ["English"], "availability": avail, "will": None, "receipts": []}
        missing = [k for k in ("role", "team", "location") if not draft[k]]
        out["draft"] = draft
        if missing:
            out["missing"] = missing
            out["question"] = {"team": f"Which team is {_first(name)} on?", "location": f"Where is {_first(name)} based?", "role": f"What is {_first(name)}'s role?"}[missing[0]]
        return out

    if not matches:
        out["missing"] = ["name"]
        out["question"] = f"Pik has nobody called {name} on file. Check the spelling, or add them first."
        return out
    if len(matches) > 1:
        out["ambiguous"] = [p["id"] for p in matches]
        teams = " or ".join(sorted({p["team"] for p in matches}))
        out["question"] = f"{len(matches)} people called {name}: which team, {teams}?"
        return out
    p = matches[0]
    out["target"] = {"id": p["id"], "name": p["name"], "role": p["role"], "team": p["team"], "location": p.get("location")}

    if intent == "remove":
        if is_fixture(p):
            out["question"] = f"{p['name']} is a seeded person in this demo and cannot be removed."
            return out
        out["draft"] = {"id": p["id"], "name": p["name"], "role": p["role"], "team": p["team"], "location": p.get("location"),
                        "receipts": len(p.get("receipts") or [])}
        out["confirm"] = f"This removes {_first(p['name'])}'s record and their receipts from Pik. Continue?"
        return out

    # edit: only the fields the sentence names, matched against the same lists as PATCH
    rest = text[verb.end():] if verb.end() < len(text) else text
    rest_wo_name = rest.replace(name, " ")
    changes = {}
    team = _find_team(rest_wo_name)
    if team and team != p["team"]:
        changes["team"] = team
    loc = _find_location(rest_wo_name)
    if loc and loc != p.get("location"):
        changes["location"] = loc
    role = _find_role(rest_wo_name)
    if role and role.lower() != p["role"].lower():
        changes["role"] = role
    langs = _find_languages(rest_wo_name)
    if langs and re.search(r"\b(speak|speaks|language|languages)\b", rest_wo_name, re.I) and sorted(langs) != sorted(p.get("languages") or []):
        changes["languages"] = langs
    avail = _find_availability(rest_wo_name)
    if avail and avail != p.get("availability"):
        changes["availability"] = avail
    if re.search(r"\bon leave\b", rest_wo_name, re.I) and not avail:
        out["missing"] = ["availability"]
        out["question"] = f"Until when is {_first(p['name'])} on leave? A date, please."
        return out
    if not changes:
        out["missing"] = ["one of role, team, location, languages, availability"]
        out["question"] = f"What should change for {_first(p['name'])}: team, role, location, languages or availability?"
        return out
    draft = {k: p.get(k) for k in ("id", "name", "role", "team", "location", "languages", "availability")}
    draft.update(changes)
    out["draft"] = draft
    out["changed"] = sorted(changes)
    return out


def parse_command_llm(text: str, requester: str | None = None):
    """MODE=gemini: the same schema from Gemini; falls back to the rules when it does not answer."""
    if MODE == "heuristic":
        return parse_command(text, requester)
    prompt = f"""You turn one sentence from an HR admin into a draft record change. Never invent fields the sentence does not state.
Sentence: "{text}"
Teams: {list(TEAMS)}. Roles: {ROLES}. Locations: {list(CITIES)}. Languages: {LANGS}.
Return JSON: {{"intent": "add|edit|remove|ask", "name": str|null, "role": str|null, "team": str|null, "location": str|null, "languages": [str], "availability": "available|at capacity|on leave until YYYY-MM-DD"|null}}"""
    out = llm_json(prompt)
    if not out or out.get("intent") not in ("add", "edit", "remove", "ask"):
        return parse_command(text, requester)
    res = parse_command(text, requester)
    if res.get("draft") and out.get("intent") == res["intent"]:
        for k in ("role", "team", "location", "languages", "availability"):
            if out.get(k) and not res["draft"].get(k):
                clean, bad = _validate({k: out[k]}, _people_raw())
                if not bad:
                    res["draft"][k] = clean[k]
        res["missing"] = [k for k in res.get("missing", []) if not res["draft"].get(k)] or None
        if not res["missing"]:
            res.pop("missing", None)
            res.pop("question", None)
    res["backend"] = "gemini"
    return res


# ---------- the filed record: what a meeting concluded, kept as a row (never a score) ----------

ASKS = STATE / "asks.jsonl"


def file_ask(row: dict):
    """Append the filed conclusion to state/asks.jsonl and return it (ask_id, summary, open_questions, notified)."""
    row = dict(row)
    row.setdefault("ask_id", f"ask-{int(time.time())}")
    row.setdefault("open_questions", [])
    row.setdefault("notified", [])
    row["filed_at"] = time.time()
    with ASKS.open("a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row
