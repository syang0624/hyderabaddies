"""Shared helpers for finetune/: paths, a read-only import of the demo engine, and the receipt corpus with its labels.

Nothing here writes into prototype/: bytecode writing is off, and the engine's STATE dir (where it caches evidence)
is pointed at a fresh temp dir. MODE is forced to heuristic, so importing the engine can never call Gemini.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # importing prototype/*.py must not drop a __pycache__ into prototype/

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROTO = ROOT / "prototype"
DATA_IN = PROTO / "data"
DATA = HERE / "data"
RESULTS = HERE / "results"
MODEL_DIR = HERE / "model"
BASE_MODEL = "intfloat/multilingual-e5-small"
SEED = 2026
Q, P = "query: ", "passage: "  # e5 prefixes

_engine = None
_engine_state = None  # a TemporaryDirectory: the engine's evidence cache lives here and is removed at exit
_make_people = None


def engine():
    """prototype/engine.py, imported read-only: keyword mode, state in a temp dir."""
    global _engine, _engine_state
    if _engine is None:
        os.environ["MODE"] = "heuristic"
        _engine_state = tempfile.TemporaryDirectory(prefix="pik-finetune-engine-state-")
        os.environ["STATE"] = _engine_state.name
        sys.path.insert(0, str(PROTO))
        import engine as eng  # noqa: E402
        _engine = eng
    return _engine


def make_people():
    """prototype/make_people.py, imported read-only for its template lists (its main() is never called)."""
    global _make_people
    if _make_people is None:
        sys.path.insert(0, str(PROTO))
        import make_people as mp  # noqa: E402
        _make_people = mp
    return _make_people


# Which slot names the topic of each generator template (make_people.RECEIPT, by index).
FAMILY = ["writeup", "retro", "office_hours", "lessons_doc", "incident", "playbook", "pushback", "session", "english_sync", "onboarding_guide"]
SLOT = ["area", "area", "skill", "area", "ch", "skill", "area", "area", "ch", "area"]


def template_regexes():
    mp = make_people()
    out = []
    for i, (src, tpl) in enumerate(mp.RECEIPT):
        rx = re.escape(tpl)
        rx = rx.replace(re.escape("{area}"), "(?P<area>.+?)").replace(re.escape("{skill}"), "(?P<skill>.+?)").replace(re.escape("{ch}"), r"(?P<ch>#[a-z\-]+)")
        out.append((i, src, re.compile("^" + rx + "$")))
    return out


def label(receipt, rxs):
    """The receipt's own label, recovered by matching its text against the generator's templates: (template index, slot values).
    Exactly one template must match, and the slot values must come from the generator's own lists; anything else raises."""
    mp = make_people()
    hits = [(i, m.groupdict()) for i, src, rx in rxs if src == receipt["source"] and (m := rx.match(receipt["text"]))]
    if len(hits) != 1:
        raise ValueError(f"receipt {receipt['id']} matches {len(hits)} templates: {receipt['text']!r}")
    i, d = hits[0]
    if d.get("area") is not None and d["area"] not in mp.AREAS:
        raise ValueError(f"unknown area in {receipt['id']}: {d['area']!r}")
    if d.get("skill") is not None and d["skill"] not in mp.TAGS:
        raise ValueError(f"unknown skill in {receipt['id']}: {d['skill']!r}")
    if d.get("ch") is not None and d["ch"] not in mp.CHANNELS:
        raise ValueError(f"unknown channel in {receipt['id']}: {d['ch']!r}")
    return i, d


def intent_of(i, d):
    return f"{FAMILY[i]}:{d[SLOT[i]]}"


def people_rows():
    return json.loads((DATA_IN / "people.json").read_text())


def on_leave(p):
    return str(p.get("availability", "")).startswith("on leave")


def corpus(rows=None):
    """Every receipt of every generated person, with its label. in_pool = the person is someone engine.ask() considers
    (not on leave). The three hand-written fixture people (rin, yui, kei) are left out: their items carry no intent label."""
    rows = rows or people_rows()
    rxs = template_regexes()
    out = []
    for p in rows:
        if not p.get("generated"):
            continue
        for r in p.get("receipts") or []:
            i, d = label(r, rxs)
            out.append({"id": r["id"], "person": p["id"], "name": p["name"], "source": r["source"], "channel": r.get("channel"),
                        "date": r["date"], "text": r["text"], "template": i, "intent": intent_of(i, d), "slots": d,
                        "in_pool": not on_leave(p)})
    return out


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


def read_jsonl(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def write_jsonl(path, rows):
    Path(path).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def device():
    import torch
    return "mps" if torch.backends.mps.is_available() else "cpu"
