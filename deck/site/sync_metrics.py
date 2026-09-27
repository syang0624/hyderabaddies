#!/usr/bin/env python3
"""Copy the fine-tune metrics into the deck, as a script file that works from file:// (no fetch).

    cd /Users/carl/CODELocalProjects/hyderabaddies/deck
    video/pw/bin/python site/sync_metrics.py        # or plain python3; stdlib only

Reads   ../finetune/results/metrics.json   (read-only; written by the fine-tune run)
Writes  site/data/ft_metrics.js            window.FT_METRICS = {run_date, source, sizes, rows, raw}

The layout of metrics.json is not fixed, so every numeric leaf is classified by the words on its path
(and by the string fields of the record it sits in): system (keyword | base | finetuned), language
(en | ja | all), task (receipt | person), metric (R@1 | R@5 | MRR). Values above 1 are read as percents.
Prints the table it understood, so a wrong reading is visible before the deck is rendered.
Exits 1, loudly, if the file is missing, unreadable, or yields no rows: never a silent success.
"""
import datetime as dt
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent.parent / "finetune" / "results" / "metrics.json"
OUT = HERE / "data" / "ft_metrics.js"

SYSTEM = [("finetuned", re.compile(r"fine[-_ ]?tun|^ft$|^tuned$|^trained$|^ours$|contrastive")),
          ("keyword", re.compile(r"keyword|heuristic|bm25|lexical|^engine$|^demo$|^kw$")),
          ("base", re.compile(r"^base$|base[-_ ]?model|zero[-_ ]?shot|pretrained|^e5$|^baseline$|^untuned$|^off[-_ ]?the[-_ ]?shelf$"))]
LANG = [("en", re.compile(r"^(en|eng|english)$")), ("ja", re.compile(r"^(ja|jp|jpn|japanese)$")),
        ("all", re.compile(r"^(all|overall|both|total|combined)$"))]
TASK = [("receipt", re.compile(r"receipt|evidence|claim|passage|doc")), ("person", re.compile(r"person|people|candidate|who|employee"))]
SIZE_KEYS = re.compile(r"^(n|n_?queries|num_?queries|n_?asks|num_?asks|asks|queries|n_?test|test_?size|size|count|n_?eval|eval_?size)$")
DATE_KEYS = re.compile(r"date|time|created|finished|run_?at|started")


def metric_of(key):
    k = re.sub(r"[^a-z0-9@]", "", key.lower())
    if k in ("mrr", "meanreciprocalrank") or k.startswith("mrr"):
        return "MRR"
    m = re.fullmatch(r"(recall|r|hit|hits|top|acc|accuracy|success)(@|at)?([0-9]+)", k)
    if m and m.group(3) in ("1", "5"):
        return "R@" + m.group(3)
    return None


def classify(tokens, table):
    for name, rx in table:
        if any(rx.search(t) for t in tokens):
            return name
    return None


def tokens_of(parts):
    out = []
    for p in parts:
        out.append(p.lower())
        out.extend(t for t in re.split(r"[^a-z0-9@]+", p.lower()) if t)
    return out


def walk(node, path, ctx, rows, sizes, dates):
    if isinstance(node, dict):
        strings = [str(v) for v in node.values() if isinstance(v, str)]
        for k, v in node.items():
            if isinstance(v, str) and DATE_KEYS.search(k.lower()):
                dates.append(v)
            walk(v, path + [str(k)], ctx + strings, rows, sizes, dates)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, path + [str(i)], ctx, rows, sizes, dates)
    elif isinstance(node, (int, float)) and not isinstance(node, bool):
        key = path[-1] if path else ""
        toks = tokens_of(path[:-1] + ctx)
        if SIZE_KEYS.match(key.lower()):
            sizes.append({"lang": classify(toks, LANG) or "all", "task": classify(toks, TASK) or "any", "n": int(node), "path": "/".join(path)})
            return
        metric = metric_of(key)
        if not metric:
            return
        value = float(node)
        if 1.0 < value <= 100.0:
            value /= 100.0
        rows.append({"system": classify(toks, SYSTEM), "lang": classify(toks, LANG) or "all",
                     "task": classify(toks, TASK) or "receipt", "metric": metric, "value": round(value, 4),
                     "path": "/".join(path)})


def main():
    global SRC, OUT
    args = sys.argv[1:]
    if "--src" in args:
        SRC = pathlib.Path(args[args.index("--src") + 1])
    if "--out" in args:
        OUT = pathlib.Path(args[args.index("--out") + 1])
    if not SRC.exists():
        print(f"FAIL: {SRC} does not exist yet; nothing written. The deck must not show the measured slide without it.", file=sys.stderr)
        sys.exit(1)
    try:
        raw = json.loads(SRC.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001 - report and stop
        print(f"FAIL: {SRC} is not readable JSON: {e}", file=sys.stderr)
        sys.exit(1)
    rows, sizes, dates = [], [], []
    unknown = []
    if isinstance(raw, dict) and isinstance(raw.get("groups"), dict):
        # the fine-tune's own layout: groups -> {n_asks, systems -> system -> task -> metric -> value}; the group key
        # is kept exactly (en, ja, en_no_shared_keyword, ...), so a subset name never leaks into the system field
        for group, g in raw["groups"].items():
            if isinstance(g.get("n_asks"), (int, float)):
                sizes.append({"lang": group, "task": "any", "n": int(g["n_asks"]), "path": f"groups/{group}/n_asks"})
            for system, tasks in (g.get("systems") or {}).items():
                for task, metrics in (tasks or {}).items():
                    for key, value in (metrics or {}).items():
                        metric = metric_of(key)
                        if metric and isinstance(value, (int, float)):
                            rows.append({"system": system, "lang": group, "task": task, "metric": metric,
                                         "value": round(float(value), 4), "path": f"groups/{group}/systems/{system}/{task}/{key}"})
        if isinstance(raw.get("date"), str):
            dates.append(raw["date"])
    else:
        walk(raw, [], [], rows, sizes, dates)
        unknown = [r for r in rows if not r["system"]]
        rows = [r for r in rows if r["system"]]
    if not rows:
        print(f"FAIL: no (system, metric) values understood in {SRC}; paths seen: {[r['path'] for r in unknown][:20]}", file=sys.stderr)
        sys.exit(1)
    run_date = None
    for d in dates:
        m = re.search(r"20\d\d-\d\d-\d\d", d)
        if m:
            run_date = m.group(0)
            break
    if not run_date:
        run_date = dt.datetime.fromtimestamp(SRC.stat().st_mtime).strftime("%Y-%m-%d")
    data = {"source": "finetune/results/metrics.json", "run_date": run_date,
            "synced_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "sizes": sizes, "rows": rows, "raw": raw}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("/* written by site/sync_metrics.py from finetune/results/metrics.json; do not edit by hand */\n"
                   "window.FT_METRICS = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    print(f"wrote {OUT}  run_date {run_date}  rows {len(rows)}  unclassified {len(unknown)}")
    for r in sorted(rows, key=lambda r: (r["task"], r["metric"], r["lang"], r["system"])):
        print(f"  {r['task']:<8} {r['metric']:<4} {r['lang']:<4} {r['system']:<10} {r['value']:.4f}   <- {r['path']}")
    for s in sizes:
        print(f"  size  {s['task']:<8} {s['lang']:<4} n={s['n']}   <- {s['path']}")
    for r in unknown:
        print(f"  UNCLASSIFIED {r['metric']} {r['value']} <- {r['path']}")


if __name__ == "__main__":
    main()
