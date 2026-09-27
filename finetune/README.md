# Receipt retriever: a fine-tuned model the demo does not use (yet)

This folder holds a real fine-tune with real numbers from one local run. The demo does not use it by default: `prototype/engine.py` ranks with its keyword engine, or with Gemini extraction when a key is set, exactly as before. Only when `PIK_RETRIEVER_URL` is set does `engine.ask()` also ask this retriever, over local HTTP (see "Use it in the engine"). Nothing in `prototype/` imports torch, sentence-transformers or anything from this folder.

## What it is

A retriever over receipts. Given an ask ("Who offered to facilitate the look-back session about A/B tests on what we charge?"), it returns receipts: the verbatim sentence a person wrote or did, whose it is, and its source id. It never outputs a number about a person. It is the first piece of the next pipeline in the deck, a learned employee state that retrieves receipts, never a score.

- Base model: [`intfloat/multilingual-e5-small`](https://huggingface.co/intfloat/multilingual-e5-small) (MIT license, 118M parameters, 384-dim embeddings), used with its `query: ` / `passage: ` prefixes and cosine similarity.
- Training: contrastive, sentence-transformers `MultipleNegativesRankingLoss` on (ask, receipt that answers it, hard negative receipt), in-batch negatives, batches filled so that no two rows in a batch share an intent.
- Hyperparameters, fixed before any evaluation and not tuned on the test split: 3 epochs, batch 32, lr 3e-5, 10% warmup then linear decay, max 64 tokens, seed 2026.
- Run: 798 training pairs, 85 steps, **18.6 s wall** on an Apple M5 Max (MPS). An earlier run of the same script took 24.2 s; the loss curve and every metric were identical across the two runs. Full per-step loss: `results/train_log.txt` (mean loss per epoch 1.7729, 0.2609, 0.1238).
- Weights: `finetune/model/`, 488,220,223 bytes (fp32 safetensors), git-ignored. Rebuild them with the command below.
- No model is called to write or label data: the asks are fixed templates filled with the fixtures' own topics. The templates, the topic synonyms and the 28 Japanese asks were typed into `build_pairs.py` by the coding agent (Claude) that built this folder, once, as plain text.

## Reproduce

```bash
make -C finetune all        # first run: creates finetune/.venv from requirements.txt; then pairs, train, eval (about 1 minute after the install)
make -C finetune ask Q="Who offered to facilitate the look-back session about A/B tests on what we charge?"
```

| step | script | writes |
|---|---|---|
| pairs | `build_pairs.py` | `data/train.jsonl`, `data/test.jsonl`, `data/corpus.jsonl` (every receipt with its recovered label), `data/STATS.md` |
| train | `train.py` | `model/` (git-ignored), `results/train_log.txt` |
| eval | `eval.py` | `results/metrics.json`, `results/RESULTS.md`, `results/per_ask.jsonl` (each ask's rank under each system) |
| ask | `ask.py "question"` | prints the retriever's top receipts next to the keyword engine's answer |
| serve | `serve.py` (`make -C finetune serve`, `PORT=8811`) | nothing; serves the retriever to `prototype/engine.py` when opted in (below) |

`eval.py` and `ask.py` import `prototype/engine.py` read-only: keyword mode forced (no network), its evidence cache pointed at a temp dir, bytecode writing off, so nothing is written into `prototype/`.

## How the labels are made

Every generated person in `prototype/data/people.json` got 2 to 4 receipts from `prototype/make_people.py`, each one of ten sentence templates with an `{area}`, `{skill}` or `{ch}` slot ("Volunteered to run the {area} retro this quarter so the team lead could focus on hiring."). `build_pairs.py` matches each receipt's text back against those same templates. Exactly one template must match and the slot value must be in the generator's own lists; all 587 receipts pass. That gives each receipt an intent, `<template family>:<topic>`, for example `retro:pricing experiments`. A receipt answers an ask when its intent is the ask's intent. A person answers it when any of their receipts does. No model and no person judged relevance; only the ask wording was written (see above).

Split: 38 of the 145 intents (25% per family, seeded) are held out. Their asks are test only, and their receipts never enter training, not even as negatives. For the 107 trained intents, the test asks use an ask template and a topic synonym that appear nowhere in training. All 28 Japanese asks are test only. No test ask text occurs in train (the build fails if one does). Counts: `data/STATS.md`.

"Shares no keyword" is measured, not claimed: an ask is in that group when, after the engine's own tokenizer and stemmer, it has no term in common with any correct receipt (162 of 364 English test asks).

## Results

From the eval run at 2026-09-27 09:37:15 PDT (`results/metrics.json`), on the model trained at 09:35:19 (`results/train_log.txt`); two later eval re-runs reproduced every number exactly. Three systems on the same pool: 553 receipts from the 184 generated people that `engine.ask()` considers (on-leave people are skipped, as the demo does).

- **keyword engine (demo default)**: people come straight from `engine.ask()` as shipped (evidence score minus its load penalty). Receipts are scored with `ask()`'s own receipt rule (1.0 + 0.3 per overlapping term, counted only when two or more terms overlap). Anything the engine does not return counts as a miss.
- **keyword engine, no load penalty**: the same `ask()` people re-sorted by evidence score alone, so the baseline is not handicapped by workload.
- **e5-small base** and **e5-small fine-tuned**: cosine similarity over all receipts; a person ranks where their best receipt ranks.

R@k is a hit rate (share of asks with a correct item in the top k; most asks have several correct receipts). MRR is mean reciprocal rank of the first correct item, 0 when none comes back. Tables copied from `results/RESULTS.md`:

### English asks, all (n = 364)

| system | receipt R@1 | receipt R@5 | receipt MRR | person R@1 | person R@5 | person MRR |
|---|---|---|---|---|---|---|
| keyword engine (demo default) | 0.486 | 0.508 | 0.497 | 0.223 | 0.459 | 0.328 |
| keyword engine, no load penalty | n/a | n/a | n/a | 0.264 | 0.462 | 0.356 |
| e5-small base | 0.544 | 0.596 | 0.578 | 0.549 | 0.648 | 0.609 |
| e5-small fine-tuned | 0.758 | 0.849 | 0.795 | 0.758 | 0.865 | 0.803 |

95% paired bootstrap interval of the MRR difference: MRR finetuned - keyword (receipt): [+0.248, +0.345]; MRR finetuned - base (receipt): [+0.170, +0.264]; MRR finetuned - keyword (person): [+0.432, +0.517]; MRR finetuned - base (person): [+0.150, +0.239]

### English asks that share no keyword with any correct receipt (n = 162)

| system | receipt R@1 | receipt R@5 | receipt MRR | person R@1 | person R@5 | person MRR |
|---|---|---|---|---|---|---|
| keyword engine (demo default) | 0.000 | 0.000 | 0.000 | 0.000 | 0.012 | 0.014 |
| keyword engine, no load penalty | n/a | n/a | n/a | 0.000 | 0.012 | 0.014 |
| e5-small base | 0.080 | 0.185 | 0.150 | 0.093 | 0.296 | 0.216 |
| e5-small fine-tuned | 0.562 | 0.698 | 0.625 | 0.562 | 0.728 | 0.642 |

95% paired bootstrap interval of the MRR difference: MRR finetuned - keyword (receipt): [+0.557, +0.693]; MRR finetuned - base (receipt): [+0.397, +0.543]; MRR finetuned - keyword (person): [+0.561, +0.693]; MRR finetuned - base (person): [+0.348, +0.500]

### English asks on held-out intents (n = 152)

| system | receipt R@1 | receipt R@5 | receipt MRR | person R@1 | person R@5 | person MRR |
|---|---|---|---|---|---|---|
| keyword engine (demo default) | 0.480 | 0.507 | 0.490 | 0.197 | 0.467 | 0.318 |
| keyword engine, no load penalty | n/a | n/a | n/a | 0.230 | 0.474 | 0.337 |
| e5-small base | 0.533 | 0.579 | 0.566 | 0.539 | 0.651 | 0.609 |
| e5-small fine-tuned | 0.770 | 0.842 | 0.803 | 0.770 | 0.862 | 0.812 |

95% paired bootstrap interval of the MRR difference: MRR finetuned - keyword (receipt): [+0.239, +0.386]; MRR finetuned - base (receipt): [+0.167, +0.305]; MRR finetuned - keyword (person): [+0.429, +0.560]; MRR finetuned - base (person): [+0.139, +0.270]

### English asks on trained intents, unseen phrasing and synonym (n = 212)

| system | receipt R@1 | receipt R@5 | receipt MRR | person R@1 | person R@5 | person MRR |
|---|---|---|---|---|---|---|
| keyword engine (demo default) | 0.491 | 0.509 | 0.501 | 0.241 | 0.453 | 0.335 |
| keyword engine, no load penalty | n/a | n/a | n/a | 0.288 | 0.453 | 0.369 |
| e5-small base | 0.552 | 0.609 | 0.587 | 0.557 | 0.646 | 0.610 |
| e5-small fine-tuned | 0.750 | 0.854 | 0.789 | 0.750 | 0.868 | 0.796 |

95% paired bootstrap interval of the MRR difference: MRR finetuned - keyword (receipt): [+0.223, +0.353]; MRR finetuned - base (receipt): [+0.142, +0.264]; MRR finetuned - keyword (person): [+0.406, +0.517]; MRR finetuned - base (person): [+0.125, +0.246]

### Japanese asks (written for this test, none in training) (n = 28)

| system | receipt R@1 | receipt R@5 | receipt MRR | person R@1 | person R@5 | person MRR |
|---|---|---|---|---|---|---|
| keyword engine (demo default) | 0.000 | 0.000 | 0.000 | 0.036 | 0.036 | 0.042 |
| keyword engine, no load penalty | n/a | n/a | n/a | 0.036 | 0.036 | 0.042 |
| e5-small base | 0.679 | 0.821 | 0.754 | 0.714 | 0.929 | 0.797 |
| e5-small fine-tuned | 0.679 | 0.857 | 0.753 | 0.679 | 0.929 | 0.786 |

95% paired bootstrap interval of the MRR difference: MRR finetuned - keyword (receipt): [+0.609, +0.885]; MRR finetuned - base (receipt): [-0.165, +0.176]; MRR finetuned - keyword (person): [+0.620, +0.862]; MRR finetuned - base (person): [-0.160, +0.142]

### Reading it

- English: the fine-tuned model beats both baselines on every metric. Receipt MRR 0.795 against 0.578 for the base model and 0.497 for the keyword engine; the 95% paired bootstrap intervals of those differences exclude zero.
- Where the ask shares no keyword with the right receipt, the keyword engine finds no correct receipt (receipt MRR 0.000, true by construction: these are the asks it cannot match), so the comparison that matters there is base 0.150 against fine-tuned 0.625.
- On held-out intents, which it never trained on, the fine-tuned model scores about the same as on trained intents (receipt MRR 0.803 and 0.789), so it did not just memorise the training receipts.
- **Japanese: the fine-tune does not beat the base model.** Receipt MRR 0.753 fine-tuned against 0.754 base, person MRR 0.786 against 0.797; the interval of the difference spans zero. There was no Japanese in training. Both are far above the keyword engine, whose tokenizer only reads Latin letters.

## One ask, both answers

A held-out intent (`retro:pricing experiments`), phrased so that it shares no keyword with the receipts. In the eval pool the base model ranks the first correct receipt 24th. Output of `ask.py`, verbatim; its corpus also includes Rin's, Yui's and Kei's own words, hence 592 receipts:

```text
ASK: Who offered to facilitate the look-back session about A/B tests on what we charge?

== Retriever (e5-small fine-tuned), top 5 receipts of 592 ==
1. Jun Murakami (p044) | slack #design-crit, 2026-07-04 | source id gr-044-0
     "Volunteered to run the pricing experiments retro this quarter so the team lead could focus on
     hiring."
2. Felix Yamaguchi (p047) | slack #customer-success, 2026-04-15 | source id gr-047-1
     "Volunteered to run the pricing experiments retro this quarter so the team lead could focus on
     hiring."
3. Gen Bianchi (p092) | slack #search, 2026-04-16 | source id gr-092-2
     "Volunteered to run the pricing experiments retro this quarter so the team lead could focus on
     hiring."
4. Felix Kaneko (p161) | slack #growth-analytics, 2026-06-11 | source id gr-161-0
     "Volunteered to run the pricing experiments retro this quarter so the team lead could focus on
     hiring."
5. Lena Takeda (p187) | slack #pricing, 2026-06-05 | source id gr-187-2
     "Volunteered to run the pricing experiments retro this quarter so the team lead could focus on
     hiring."

== Keyword engine (prototype/engine.py ask(), keyword mode, the demo default) ==
1. Yui Sato (yui) | words with a receipt: tests, what
     "Wrote 'Q2 pricing test: results and what I'd change': The 3% increase held SMB retention flat
     (n=4,120 per arm). Enterprise arm was underpowered; next time I'd stratify by contract length
     up…" (Doc: Q2 pricing test: results and what I'd change, source id doc-yui-2)
2. Zara Kobayashi (p088) | words with a receipt: none
     "Office hours Thursday for anyone stuck on pricing; bring your questions." (Slack #design-crit,
     2026-06-24, source id gr-088-0)
     "Took the #growth-analytics incident on a Saturday and wrote the post-mortem by Monday." (Slack
     #growth-analytics, 2026-09-18, source id gr-088-1)
3. Tomas Maeda (p048) | words with a receipt: none
     "Ran the #design-crit sync in English for the first time; notes posted the same day." (Slack
     #design-crit, 2026-09-19, source id gr-048-0)
     "Pushed back on the skills taxonomy timeline in #all-hands-questions with data; the plan
     changed." (Slack #all-hands-questions, 2026-06-07, source id gr-048-1)
   engine asks back: Nothing on file mentions about, charge, facilitate, look-back. What would this person actually do, and for which team?
```

All five retrieved receipts are correct. The keyword engine names Yui on "tests" and "what", then two people with no receipt on any word, and asks a follow-up. Yui's doc is arguably a fair answer too; it is a look-back on a pricing test. It is not in the retriever's top five. The ask is about running a session, and the fixtures' labels treat a retro and a "what I'd change" doc as different intents, which is the boundary the retriever was trained on (see limits).

## Honest limits

- **Fictional, generated data.** The 587 receipts come from 10 templates filled with 14 areas, 25 skills and 11 channels. Real receipts are messier, and these numbers say nothing about real people or real text.
- **Labels come from the generator.** Intent boundaries are the templates' boundaries. A retro and a "what we would do differently" doc on the same topic are different intents by construction, and the model learned that convention.
- **One author wrote every ask.** The coding agent wrote the training and the held-out phrasings and synonyms alike, in one style, so the test is easier than real users' wording.
- **Rin, Yui and Kei are not in train or test.** Their fixture items were not made from the generator's templates, so they have no intent labels. `ask.py` searches their own words too, unlabelled and unevaluated.
- **Small Japanese set.** 28 asks, so the intervals are wide.
- **Duplicates.** Many receipts share the same sentence (the generator reuses templates), so a top five can be five people who wrote the same line.
- **One seed, one configuration.** No dev split, no sweep, no variance across seeds.

## Use it in the engine (opt-in)

```bash
make -C finetune serve                                                           # loads finetune/model once, serves http://127.0.0.1:8811/retrieve
PIK_RETRIEVER_URL=http://127.0.0.1:8811/retrieve make -C prototype run-heuristic   # the demo, with engine.ask() also asking the retriever
```

`serve.py` (stdlib HTTP, the `.venv` here) answers `POST /retrieve {"question", "k"}` with `{"items": [{"id", "person_id", "text", "score"}]}` over the same 553-receipt pool `eval.py` scores; `score` orders receipts and is never shown as a number about a person. With the variable set, `engine.ask()` asks for the top 5 receipts (`PIK_RETRIEVER_K`), 1.5 s timeout, and appends the people behind them who are not already in the keyword result. Each is built by the same row code as a keyword row (the fields the page, the Slack bot and the Notion watcher read) plus `"via": "retriever"`. Its receipt is kept only when the id is one of that person's receipts on file and the text is that receipt verbatim. Any failure (server down, timeout, bad reply) prints one `[engine] RETRIEVER FAILED ...` line on stderr and returns the keyword result unchanged.

Checked on 2026-09-27, by running it, not assumed:

- Variable unset: `engine.ask()` on six asks (English, Japanese, vague, with `context`, with `k=5`) gave byte-identical JSON before and after the engine edit (sha256 `f04cf24d...`, empty diff).
- Variable set, retriever on a test port: "Who offered to facilitate the look-back session about A/B tests on what we charge?" keeps the keyword engine's three people unchanged and adds five via the retriever. All five are the people whose receipts are labelled `retro:pricing experiments`, the only correct ones in the pool. "障害対応のマニュアルを作成したのは誰ですか？", where the keyword engine returns no one, adds three authors of the incident response playbook, all correct.
- Retriever down: one stderr line, result identical to the unset run. Retriever hanging: returns after 1.54 s, same.

Not built yet: the retriever does not search Rin's, Yui's and Kei's items (its pool is the evaluated one). Retrieved people are appended after the keyword people, not ranked with them. A dropped retrieved receipt is reported on stderr, not yet counted on `/stats`. Whether each surface shows the `via` marker is up to that surface; the page's tiles read the same fields as any row.

## License and data

- Base model `intfloat/multilingual-e5-small`: MIT. The fine-tuned weights are a derivative and are not committed.
- Training and test data: the fictional Kaede Works fixtures in `prototype/data/`. No real employee data, no DMs or private channels (the generator never produced any), no hosted model API calls. The base model's weights were downloaded from Hugging Face once; everything else ran on one Mac.

## In production (planned, not built)

Steven's plan for the customer deployment, kept here so the deck and this folder say the same thing:

- **What it learns from:** pairs of an ask and the evidence a filed decision actually used, in Japanese and English; contests and dropped claims as corrections. Per customer, inside that customer's own cloud project, never pooled across customers. Never direct messages, private channels or protected attributes.
- **Where it trains:** `config.example.yaml` is a placeholder for per-customer training on Vertex AI. Nothing has been trained there; the only training so far is the local run above.
- **Output:** retrieved evidence with its source, used to weigh one task. Never a grade of a person; the person named sees the same page.
- **Next layers (not built):** opt-in capture read with OCR and a vision-language model, and connectors for vertical systems such as hospital shift rosters or airline crew logs.

Note on Japanese: the 28 Japanese asks are test only. The model was fine-tuned on English pairs; Japanese asks work through the multilingual base model and score level with it (see the table above).
