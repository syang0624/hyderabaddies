"""The fine-tuned receipt retriever as a tiny local HTTP service (stdlib http.server). Loads finetune/model once.

POST /retrieve {"question": str, "k": int}  ->  {"items": [{"id", "person_id", "text", "score"}]}
GET  /health                                ->  {"ok": true, "model": ..., "receipts": n}
Pool: the same receipts eval.py scores (generated people engine.ask() considers, from data/corpus.jsonl).
"score" is the cosine similarity between the ask and that receipt; it orders receipts, it is not a score of a person.

Run: make -C finetune serve   (PORT=8811 by default; binds 127.0.0.1 only)
Then: PIK_RETRIEVER_URL=http://127.0.0.1:8811/retrieve make -C prototype run-heuristic
"""
from __future__ import annotations

import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import numpy as np
from sentence_transformers import SentenceTransformer

import common as C

MAX_K = 50


def load():
    if not (C.MODEL_DIR / "config.json").exists():
        sys.exit("finetune/model/ is missing: run `make -C finetune train` first")
    pool = [r for r in C.read_jsonl(C.DATA / "corpus.jsonl") if r["in_pool"]]
    model = SentenceTransformer(str(C.MODEL_DIR), device=C.device())
    emb = model.encode([C.P + r["text"] for r in pool], batch_size=64, normalize_embeddings=True, convert_to_numpy=True)
    return model, pool, emb


MODEL, POOL, EMB = None, None, None


def retrieve(question: str, k: int):
    q = MODEL.encode([C.Q + question], normalize_embeddings=True, convert_to_numpy=True)[0]
    s = EMB @ q
    order = np.argsort(-s, kind="stable")[:k]
    return [{"id": POOL[i]["id"], "person_id": POOL[i]["person"], "text": POOL[i]["text"], "score": round(float(s[i]), 4)} for i in order]


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        raw = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, {"ok": True, "model": "finetune/model (e5-small fine-tuned)", "receipts": len(POOL)})
        self._send(404, {"error": "GET /health or POST /retrieve"})

    def do_POST(self):
        if self.path != "/retrieve":
            return self._send(404, {"error": "POST /retrieve"})
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
            question = str(body.get("question") or "").strip()
            k = max(1, min(MAX_K, int(body.get("k") or 5)))
        except (ValueError, TypeError) as e:
            return self._send(400, {"error": f"bad request: {e}"})
        if not question:
            return self._send(400, {"error": "question is empty"})
        t0 = time.time()
        items = retrieve(question, k)
        sys.stderr.write(f"[serve] {int((time.time() - t0) * 1000)} ms k={k} {question[:80]!r}\n")
        self._send(200, {"items": items})

    def log_message(self, fmt, *args):  # one line per request is printed by do_POST
        pass


def main():
    global MODEL, POOL, EMB
    port = int(os.environ.get("PORT", "8811"))
    MODEL, POOL, EMB = load()
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"retriever: {len(POOL)} receipts, listening on http://127.0.0.1:{port}/retrieve", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
