"""Evaluate three receipt retrievers on data/test.jsonl, English and Japanese asks reported separately:
  keyword   = the demo's keyword engine, imported read-only from prototype/engine.py (keyword mode, no network):
              people come from engine.ask() itself; receipts are scored with ask()'s own receipt rule
              (1.0 + 0.3 x overlapping terms, counted only when at least two terms overlap, ties in corpus order).
  base      = intfloat/multilingual-e5-small, no training ("query: " / "passage: " prefixes, cosine).
  finetuned = the same model after train.py (finetune/model/).
Pool: the receipts of every generated person engine.ask() considers (not on leave); rin, yui and kei are left out
because their fixture items were not made from the generator's templates and carry no intent label.
Metrics, per ask: rank of the first correct receipt (or person). Recall@k = share of asks with a correct item in the
top k (hit rate: most asks have several correct receipts); MRR = mean of 1/rank, 0 when nothing correct is returned.
A person is retrieved at the rank of their best receipt. The keyword engine returns nothing when no receipt shares two
terms with the ask (and no person when no word matches at all); those asks count as misses.

Run: .venv/bin/python eval.py   -> results/metrics.json, results/RESULTS.md, results/per_ask.jsonl (every ask's rank per system)
"""
from __future__ import annotations

import datetime as dt
import json
import platform
import random
import subprocess

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

import common as C

K = (1, 5)
BOOT = 2000


def first_rank(ranked, relevant):
    for i, x in enumerate(ranked, 1):
        if x in relevant:
            return i
    return None


def metrics(ranks):
    n = len(ranks)
    out = {f"R@{k}": round(sum(1 for r in ranks if r and r <= k) / n, 4) for k in K}
    out["MRR"] = round(sum(1 / r for r in ranks if r) / n, 4)
    return out


def rr(r):
    return 1 / r if r else 0.0


def boot_ci(a, b, rng):
    """95% paired bootstrap interval of mean(a) - mean(b) over asks."""
    a, b = np.array(a), np.array(b)
    n = len(a)
    idx = rng.integers(0, n, size=(BOOT, n))
    d = (a[idx] - b[idx]).mean(axis=1)
    return [round(float(np.percentile(d, 2.5)), 4), round(float(np.percentile(d, 97.5)), 4)]


def main():
    eng = C.engine()
    corpus = C.read_jsonl(C.DATA / "corpus.jsonl")
    pool = [r for r in corpus if r["in_pool"]]
    pool_people = sorted({r["person"] for r in pool})
    person_of = {r["id"]: r["person"] for r in pool}
    test = C.read_jsonl(C.DATA / "test.jsonl")
    ranks = {s: {"receipt": [], "person": []} for s in ("keyword", "base", "finetuned")}
    ranks["keyword_no_load"] = {"person": []}

    # ---- keyword engine ----
    pool_terms = [eng._terms(r["text"]) for r in pool]
    for t in test:
        q = set(eng._terms_map(t["ask"]))
        scores = [(1.0 + 0.3 * len(q & ts)) if len(q & ts) >= 2 else 0.0 for ts in pool_terms]
        order = sorted(range(len(pool)), key=lambda i: -scores[i])
        ranked = [pool[i]["id"] for i in order if scores[i] > 0]
        ranks["keyword"]["receipt"].append(first_rank(ranked, set(t["relevant_receipt_ids"])))
        ans = eng.ask(t["ask"], k=len(pool_people), pool=pool_people)
        shown = [p for p in ans["people"] if p["support"] > 0]
        ranks["keyword"]["person"].append(first_rank([p["id"] for p in shown], set(t["relevant_person_ids"])))
        by_support = sorted(shown, key=lambda p: -p["support"])
        ranks["keyword_no_load"]["person"].append(first_rank([p["id"] for p in by_support], set(t["relevant_person_ids"])))

    # ---- dense retrievers ----
    dev = C.device()
    for name, path in (("base", C.BASE_MODEL), ("finetuned", str(C.MODEL_DIR))):
        m = SentenceTransformer(path, device=dev)
        P = m.encode([C.P + r["text"] for r in pool], batch_size=64, normalize_embeddings=True, convert_to_numpy=True)
        Qe = m.encode([C.Q + t["ask"] for t in test], batch_size=64, normalize_embeddings=True, convert_to_numpy=True)
        S = Qe @ P.T
        for t, s in zip(test, S):
            order = np.argsort(-s, kind="stable")
            ranked = [pool[i]["id"] for i in order]
            ranks[name]["receipt"].append(first_rank(ranked, set(t["relevant_receipt_ids"])))
            seen, people = set(), []
            for rid in ranked:
                p = person_of[rid]
                if p not in seen:
                    seen.add(p)
                    people.append(p)
            ranks[name]["person"].append(first_rank(people, set(t["relevant_person_ids"])))

    groups = {
        "en": lambda t: t["lang"] == "en",
        "en_no_shared_keyword": lambda t: t["lang"] == "en" and t["kw_overlap"] == 0,
        "en_heldout_intent": lambda t: t["lang"] == "en" and t["heldout_intent"],
        "en_trained_intent_new_phrasing": lambda t: t["lang"] == "en" and not t["heldout_intent"],
        "ja": lambda t: t["lang"] == "ja",
    }
    rng = np.random.default_rng(C.SEED)
    out_groups = {}
    for g, f in groups.items():
        idx = [i for i, t in enumerate(test) if f(t)]
        sysm = {}
        for s, kinds in ranks.items():
            sysm[s] = {kind: metrics([rs[i] for i in idx]) for kind, rs in kinds.items()}
        ci = {}
        for kind in ("receipt", "person"):
            ft = [rr(ranks["finetuned"][kind][i]) for i in idx]
            for other in ("keyword", "base"):
                ci[f"MRR finetuned - {other} ({kind})"] = boot_ci(ft, [rr(ranks[other][kind][i]) for i in idx], rng)
        out_groups[g] = {"n_asks": len(idx), "systems": sysm, "mrr_diff_95ci_paired_bootstrap": ci}

    chip = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip() or platform.processor()
    mem = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True).stdout.strip()
    res = {
        "date": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "hardware": f"{chip}, {int(mem) // 2**30} GB" if mem.isdigit() else chip, "device": dev,
        "python": platform.python_version(), "torch": torch.__version__, "seed": C.SEED,
        "base_model": C.BASE_MODEL, "finetuned_model": "finetune/model (git-ignored; rebuild with make -C finetune train)",
        "commands": ["make -C finetune all", "= .venv/bin/python build_pairs.py && .venv/bin/python train.py && .venv/bin/python eval.py (after the venv from requirements.txt)"],
        "inputs_sha256_16": {"prototype/engine.py": C.sha(C.PROTO / "engine.py"), "prototype/data/people.json": C.sha(C.DATA_IN / "people.json"),
                             "finetune/data/train.jsonl": C.sha(C.DATA / "train.jsonl"), "finetune/data/test.jsonl": C.sha(C.DATA / "test.jsonl"),
                             "finetune/data/corpus.jsonl": C.sha(C.DATA / "corpus.jsonl")},
        "pool": {"receipts": len(pool), "people": len(pool_people)},
        "definitions": {
            "R@k": "share of asks with at least one correct item in the top k (hit rate)",
            "MRR": "mean over asks of 1/rank of the first correct item; 0 when none is returned",
            "keyword": "prototype/engine.py keyword mode: people from engine.ask() as shipped (evidence score minus its load penalty); receipts by ask()'s receipt rule",
            "keyword_no_load": "engine.ask() people re-sorted by its evidence score alone (no load penalty), people only",
            "person": "a person is retrieved at the rank of their best receipt (keyword: at their place in engine.ask())",
            "correct": "a receipt is correct when its text matches the same generator template and topic as the ask's intent (see build_pairs.py)",
        },
        "groups": out_groups,
    }
    (C.RESULTS / "metrics.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    C.write_jsonl(C.RESULTS / "per_ask.jsonl", [
        {"ask": t["ask"], "lang": t["lang"], "intent": t["intent"], "split": t["split"], "kw_overlap": t["kw_overlap"],
         "rank_receipt": {s: ranks[s]["receipt"][i] for s in ("keyword", "base", "finetuned")},
         "rank_person": {s: ranks[s]["person"][i] for s in ("keyword", "keyword_no_load", "base", "finetuned")}} for i, t in enumerate(test)])

    names = {"keyword": "keyword engine (demo default)", "keyword_no_load": "keyword engine, no load penalty", "base": "e5-small base", "finetuned": "e5-small fine-tuned"}
    titles = {"en": "English asks, all", "en_no_shared_keyword": "English asks that share no keyword with any correct receipt",
              "en_heldout_intent": "English asks on held-out intents", "en_trained_intent_new_phrasing": "English asks on trained intents, unseen phrasing and synonym",
              "ja": "Japanese asks (written for this test, none in training)"}
    md = ["# Results", "", f"Run {res['date']} on {res['hardware']} ({dev}), seed {C.SEED}, torch {torch.__version__}, python {platform.python_version()}.",
          "Pool: %d receipts from %d people (generated fixtures, not on leave)." % (len(pool), len(pool_people)), "",
          "Command: `make -C finetune all` (first run creates finetune/.venv from requirements.txt, then build_pairs.py, train.py, eval.py).", "",
          "Receipt = the right receipt is retrieved. Person = someone whose receipt answers the ask is retrieved. R@k is a hit rate; MRR is mean reciprocal rank (0 when nothing correct comes back).", ""]
    for g, v in out_groups.items():
        md += [f"## {titles[g]} (n = {v['n_asks']})", "", "| system | receipt R@1 | receipt R@5 | receipt MRR | person R@1 | person R@5 | person MRR |", "|---|---|---|---|---|---|---|"]
        for s in ("keyword", "keyword_no_load", "base", "finetuned"):
            m = v["systems"][s]
            rcp = m.get("receipt")
            cells = [f"{rcp['R@1']:.3f}", f"{rcp['R@5']:.3f}", f"{rcp['MRR']:.3f}"] if rcp else ["n/a"] * 3
            p = m["person"]
            md.append(f"| {names[s]} | " + " | ".join(cells + [f"{p['R@1']:.3f}", f"{p['R@5']:.3f}", f"{p['MRR']:.3f}"]) + " |")
        md += ["", "95% paired bootstrap interval of the MRR difference: " + "; ".join(f"{k}: [{a:+.3f}, {b:+.3f}]" for k, (a, b) in v["mrr_diff_95ci_paired_bootstrap"].items()), ""]
    (C.RESULTS / "RESULTS.md").write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
