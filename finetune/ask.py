"""One ask, two answers side by side: the fine-tuned retriever's top receipts (verbatim, with person and source id)
and the demo's keyword engine (prototype/engine.py ask(), keyword mode, exactly what the demo runs without Gemini).
The retriever prints quotes and where they came from, never a number about a person.

Usage: .venv/bin/python ask.py "Who offered to facilitate the look-back session about the capability map?" [--k 5] [--base]
"""
from __future__ import annotations

import argparse
import textwrap

import numpy as np
from sentence_transformers import SentenceTransformer

import common as C


def corpus(eng):
    """The eval pool (generated people, not on leave) plus the three seeded people's own words
    (Will Can Must line, Slack messages they wrote, their docs, opted-in AI sessions), verbatim."""
    rows = [dict(r, label=f"{r['source']}{' ' + r['channel'] if r.get('channel') else ''}, {r['date']}") for r in C.read_jsonl(C.DATA / "corpus.jsonl") if r["in_pool"]]
    names = {c["id"]: c["name"] for c in eng.load("company.json")["candidates"]}
    for cid, name in names.items():
        for it in eng.items_for(cid):
            own = it["source"] in ("wcm", "docs") or (it["source"] == "slack" and it.get("author") == cid) or (it["source"] == "sessions" and it.get("opted_in"))
            text = eng._verbatim(it)
            if own and text:
                rows.append({"id": it["id"], "person": cid, "name": name, "text": text, "label": eng.source_label(it)})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("question")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--base", action="store_true", help="use the untrained base model instead of finetune/model")
    a = ap.parse_args()
    eng = C.engine()
    rows = corpus(eng)
    path = C.BASE_MODEL if a.base else str(C.MODEL_DIR)
    if not a.base and not (C.MODEL_DIR / "config.json").exists():
        raise SystemExit("finetune/model/ is missing: run `make -C finetune train` first (or pass --base)")
    m = SentenceTransformer(path, device=C.device())
    P = m.encode([C.P + r["text"] for r in rows], batch_size=64, normalize_embeddings=True, convert_to_numpy=True)
    q = m.encode([C.Q + a.question], normalize_embeddings=True, convert_to_numpy=True)[0]
    order = np.argsort(-(P @ q), kind="stable")[: a.k]
    w = lambda s: textwrap.fill(s, 100, initial_indent="     ", subsequent_indent="     ")  # noqa: E731

    print(f"ASK: {a.question}\n")
    print(f"== Retriever ({'e5-small base' if a.base else 'e5-small fine-tuned'}), top {a.k} receipts of {len(rows)} ==")
    for n, i in enumerate(order, 1):
        r = rows[i]
        print(f"{n}. {r['name']} ({r['person']}) | {r['label']} | source id {r['id']}")
        print(w(f'"{r["text"]}"'))
    ans = eng.ask(a.question)
    print("\n== Keyword engine (prototype/engine.py ask(), keyword mode, the demo default) ==")
    if not ans["people"]:
        print("   no one: nothing on file shares the ask's words")
    for n, p in enumerate(ans["people"], 1):
        words = ", ".join(p["covered"]) or "none"
        print(f"{n}. {p['name']} ({p['id']}) | words with a receipt: {words}")
        for r in p["receipts"]:
            print(w(f'"{r["text"]}" ({r["source"]}, source id {r["source_id"]})'))
    if ans.get("follow_up"):
        print(f"   engine asks back: {ans['follow_up']}")


if __name__ == "__main__":
    main()
