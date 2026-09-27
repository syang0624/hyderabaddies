"""Scripted take: replay a meeting script through the live layer's own functions, on a fixed clock.

Every row in the script becomes a call to live.emit / live.compose / live.place / live.filed, so the
rows that land in state/live.jsonl are byte-for-byte the shape Gemini Live writes: the engine fills
every tile, quote and coverage number at replay time (nothing on screen is typed into the script
except the speakers' words and the block ids). The first status row says "scripted take", which is
what the page turns into the "scripted" badge.

Run:  .venv/bin/python live_script.py scripts/meet.json [--speed 1.0] [--fast]
      (the venv: live.py imports sounddevice and google-genai at module load)
      FAST=1 or --fast skips the waits (tests). SPEAK is forced to 0: nothing is ever played.

Script shape: {"name": str, "pool": [ids, optional], "rows": [{"at": seconds, "op": ..., ...}]}
  status   {text}                         -> live.emit("status", text=...)
  heard    {text}                         -> live.emit("heard", text=...)
  said     {text}                         -> live.emit("said", text=...)
  say      {id, text}                     -> live.emit("say", id=..., text=...)   (the page plays ui/vendor/pik_audio.json[id])
  compose  {blocks: [block, ...]}         -> live.compose(blocks)
  place    {op: add|replace|remove, block} -> live.place(op, block)      ("patch" is an alias)
  conclude {args: {summary, candidate_ids, next_steps, open_questions}} -> live.emit("conclude", **args)
  filed    {args: {ask_id, summary, open_questions:[{person,text}], notified}} -> live.filed(**args)
  emit     {kind, payload}                -> live.emit(kind, **payload)   (escape hatch)
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import live  # noqa: E402

OPS = ("status", "heard", "said", "say", "compose", "place", "patch", "conclude", "filed", "emit")


def load_script(path: str) -> dict:
    s = json.loads(Path(path).read_text())
    rows = s.get("rows")
    if not isinstance(rows, list) or not rows:
        raise SystemExit(f"{path}: no rows")
    for i, r in enumerate(rows):
        if r.get("op") not in OPS:
            raise SystemExit(f"{path}: row {i} has unknown op {r.get('op')!r} (one of {OPS})")
        if not isinstance(r.get("at"), (int, float)):
            raise SystemExit(f"{path}: row {i} needs a numeric 'at'")
    s["rows"] = sorted(rows, key=lambda r: r["at"])
    return s


def run_row(r: dict):
    op = r["op"]
    if op in ("status", "heard", "said"):
        return live.emit(op, text=str(r.get("text") or ""))
    if op == "say":  # Pik's pre-rendered line: the page plays vendor/pik_audio.json[id] and shows `text` as Pik's line
        return live.emit("say", id=str(r.get("id") or ""), text=str(r.get("text") or ""))
    if op == "compose":
        return live.compose(list(r.get("blocks") or []), r.get("via"))
    if op in ("place", "patch"):
        return live.place(r.get("op_kind") or r.get("edit") or "add", dict(r.get("block") or {}), r.get("via"))
    if op == "conclude":
        return live.emit("conclude", **dict(r.get("args") or {}))
    if op == "filed":
        return live.filed(**dict(r.get("args") or {}))
    if op == "emit":
        return live.emit(str(r.get("kind") or "status"), **dict(r.get("payload") or {}))
    raise ValueError(op)


def replay(script: dict, speed: float = 1.0, fast: bool = False):
    live.SPEAK = False
    if script.get("pool"):  # the people the engine may answer with for this take (default: the decision's candidates)
        live.POOL = [str(x) for x in script["pool"]]
    live.EVENTS.write_text("")
    live.DOC.clear()
    live._seq["n"] = 0
    t0 = time.monotonic()
    for r in script["rows"]:
        if not fast:
            due = t0 + float(r["at"]) / max(speed, 1e-6)
            while True:
                left = due - time.monotonic()
                if left <= 0:
                    break
                time.sleep(min(left, 0.05))
        try:
            run_row(r)
        except Exception as e:  # noqa: BLE001  one bad row must not end the take
            # not a "scripted take: ..." status: that prefix is the page's session-start marker and would reset the screen
            live.emit("status", text=f"row at {r['at']} failed ({type(e).__name__}: {str(e)[:80]}); the take goes on")
    return [b["type"] for b in live.DOC]


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    path = argv[0]
    speed = 1.0
    fast = os.environ.get("FAST") == "1"
    if "--speed" in argv:
        speed = float(argv[argv.index("--speed") + 1])
    if "--fast" in argv:
        fast = True
    script = load_script(path)
    print(f"[live_script] {script.get('name') or Path(path).stem}: {len(script['rows'])} rows, last at {script['rows'][-1]['at']} s, speed {speed}" + (" (fast)" if fast else ""), flush=True)
    screen = replay(script, speed, fast)
    print(f"[live_script] done; screen at the end: {screen}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
