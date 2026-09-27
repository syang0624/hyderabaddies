"""Fine-tune intfloat/multilingual-e5-small (MIT) as a receipt retriever: MultipleNegativesRankingLoss over
(query: ask, passage: positive receipt, passage: hard negative), locally (MPS if present, else CPU). No LLM calls.

Hyperparameters are fixed up front and were not tuned on the test split.
Run: .venv/bin/python train.py   -> model/ (git-ignored), results/train_log.txt
"""
from __future__ import annotations

import datetime as dt
import platform
import random
import subprocess
import time

import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer.losses import MultipleNegativesRankingLoss

import common as C

EPOCHS, BATCH, LR, WARMUP, MAX_LEN = 3, 32, 3e-5, 0.1, 64


def batches(rows, rng):
    """Shuffle, then fill each batch greedily so no two rows share an intent and no row's hard negative answers another
    row's ask: in-batch negatives must really be negatives."""
    pending = rows[:]
    rng.shuffle(pending)
    out = []
    while pending:
        batch, pos, neg, rest = [], set(), set(), []
        for r in pending:
            if len(batch) < BATCH and r["intent"] not in pos and r["intent"] not in neg and r["negative_intent"] not in pos:
                batch.append(r)
                pos.add(r["intent"])
                neg.add(r["negative_intent"])
            else:
                rest.append(r)
        out.append(batch)
        pending = rest
    return out


def main():
    random.seed(C.SEED)
    np.random.seed(C.SEED)
    torch.manual_seed(C.SEED)
    rng = random.Random(C.SEED)
    dev = C.device()
    rows = C.read_jsonl(C.DATA / "train.jsonl")
    model = SentenceTransformer(C.BASE_MODEL, device=dev)
    model.max_seq_length = MAX_LEN
    loss_fn = MultipleNegativesRankingLoss(model)
    plan = [batches(rows, rng) for _ in range(EPOCHS)]
    total = sum(len(p) for p in plan)
    opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01)
    warm = max(1, int(WARMUP * total))
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: (s + 1) / warm if s < warm else max(0.0, (total - s) / max(1, total - warm)))

    chip = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip() or platform.processor()
    log = [f"# train.py run {dt.datetime.now().astimezone().isoformat(timespec='seconds')}",
           f"base_model={C.BASE_MODEL} device={dev} hardware={chip} python={platform.python_version()} torch={torch.__version__}",
           f"seed={C.SEED} epochs={EPOCHS} batch={BATCH} lr={LR} warmup={WARMUP} max_seq_length={MAX_LEN} loss=MultipleNegativesRankingLoss(scale=20, cos_sim) + 1 hard negative per pair",
           f"train_pairs={len(rows)} steps={total} (batches filled without intent collisions)", "", "epoch\tstep\tbatch_size\tloss\tlr"]
    print("\n".join(log), flush=True)
    t0 = time.time()
    step = 0
    model.train()
    epoch_means = []
    for ep, plan_ep in enumerate(plan, 1):
        losses = []
        for b in plan_ep:
            feats = []
            for texts in ([C.Q + r["ask"] for r in b], [C.P + r["positive"] for r in b], [C.P + r["negative"] for r in b]):
                f = model.preprocess(texts)
                feats.append({k: (v.to(dev) if torch.is_tensor(v) else v) for k, v in f.items()})
            loss = loss_fn(feats, None)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            sched.step()
            opt.zero_grad()
            step += 1
            losses.append(loss.item())
            line = f"{ep}\t{step}\t{len(b)}\t{loss.item():.4f}\t{sched.get_last_lr()[0]:.2e}"
            log.append(line)
            print(line, flush=True)
        epoch_means.append(sum(losses) / len(losses))
        log.append(f"# epoch {ep} mean loss {epoch_means[-1]:.4f}")
        print(log[-1], flush=True)
    wall = time.time() - t0
    model.eval()
    C.MODEL_DIR.mkdir(exist_ok=True)
    model.save(str(C.MODEL_DIR))
    size = sum(f.stat().st_size for f in C.MODEL_DIR.rglob("*") if f.is_file())
    log += ["", f"train_wall_seconds={wall:.1f}", f"epoch_mean_loss={[round(x, 4) for x in epoch_means]}",
            f"saved={C.MODEL_DIR.relative_to(C.ROOT)} bytes_on_disk={size}"]
    C.RESULTS.mkdir(exist_ok=True)
    (C.RESULTS / "train_log.txt").write_text("\n".join(log) + "\n")
    print("\n".join(log[-4:]))


if __name__ == "__main__":
    main()
