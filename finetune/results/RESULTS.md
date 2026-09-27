# Results

Run 2026-09-27T09:37:15-07:00 (the run in metrics.json; re-runs at 09:39 and 09:40 reproduced every number exactly) on Apple M5 Max, 128 GB (mps), seed 2026, torch 2.14.0, python 3.14.7.
Pool: 553 receipts from 184 people (generated fixtures, not on leave).

Command: `make -C finetune all` (first run creates finetune/.venv from requirements.txt, then build_pairs.py, train.py, eval.py).

Receipt = the right receipt is retrieved. Person = someone whose receipt answers the ask is retrieved. R@k is a hit rate; MRR is mean reciprocal rank (0 when nothing correct comes back).

## English asks, all (n = 364)

| system | receipt R@1 | receipt R@5 | receipt MRR | person R@1 | person R@5 | person MRR |
|---|---|---|---|---|---|---|
| keyword engine (demo default) | 0.486 | 0.508 | 0.497 | 0.223 | 0.459 | 0.328 |
| keyword engine, no load penalty | n/a | n/a | n/a | 0.264 | 0.462 | 0.356 |
| e5-small base | 0.544 | 0.596 | 0.578 | 0.549 | 0.648 | 0.609 |
| e5-small fine-tuned | 0.758 | 0.849 | 0.795 | 0.758 | 0.865 | 0.803 |

95% paired bootstrap interval of the MRR difference: MRR finetuned - keyword (receipt): [+0.248, +0.345]; MRR finetuned - base (receipt): [+0.170, +0.264]; MRR finetuned - keyword (person): [+0.432, +0.517]; MRR finetuned - base (person): [+0.150, +0.239]

## English asks that share no keyword with any correct receipt (n = 162)

| system | receipt R@1 | receipt R@5 | receipt MRR | person R@1 | person R@5 | person MRR |
|---|---|---|---|---|---|---|
| keyword engine (demo default) | 0.000 | 0.000 | 0.000 | 0.000 | 0.012 | 0.014 |
| keyword engine, no load penalty | n/a | n/a | n/a | 0.000 | 0.012 | 0.014 |
| e5-small base | 0.080 | 0.185 | 0.150 | 0.093 | 0.296 | 0.216 |
| e5-small fine-tuned | 0.562 | 0.698 | 0.625 | 0.562 | 0.728 | 0.642 |

95% paired bootstrap interval of the MRR difference: MRR finetuned - keyword (receipt): [+0.557, +0.693]; MRR finetuned - base (receipt): [+0.397, +0.543]; MRR finetuned - keyword (person): [+0.561, +0.693]; MRR finetuned - base (person): [+0.348, +0.500]

## English asks on held-out intents (n = 152)

| system | receipt R@1 | receipt R@5 | receipt MRR | person R@1 | person R@5 | person MRR |
|---|---|---|---|---|---|---|
| keyword engine (demo default) | 0.480 | 0.507 | 0.490 | 0.197 | 0.467 | 0.318 |
| keyword engine, no load penalty | n/a | n/a | n/a | 0.230 | 0.474 | 0.337 |
| e5-small base | 0.533 | 0.579 | 0.566 | 0.539 | 0.651 | 0.609 |
| e5-small fine-tuned | 0.770 | 0.842 | 0.803 | 0.770 | 0.862 | 0.812 |

95% paired bootstrap interval of the MRR difference: MRR finetuned - keyword (receipt): [+0.239, +0.386]; MRR finetuned - base (receipt): [+0.167, +0.305]; MRR finetuned - keyword (person): [+0.429, +0.560]; MRR finetuned - base (person): [+0.139, +0.270]

## English asks on trained intents, unseen phrasing and synonym (n = 212)

| system | receipt R@1 | receipt R@5 | receipt MRR | person R@1 | person R@5 | person MRR |
|---|---|---|---|---|---|---|
| keyword engine (demo default) | 0.491 | 0.509 | 0.501 | 0.241 | 0.453 | 0.335 |
| keyword engine, no load penalty | n/a | n/a | n/a | 0.288 | 0.453 | 0.369 |
| e5-small base | 0.552 | 0.609 | 0.587 | 0.557 | 0.646 | 0.610 |
| e5-small fine-tuned | 0.750 | 0.854 | 0.789 | 0.750 | 0.868 | 0.796 |

95% paired bootstrap interval of the MRR difference: MRR finetuned - keyword (receipt): [+0.223, +0.353]; MRR finetuned - base (receipt): [+0.142, +0.264]; MRR finetuned - keyword (person): [+0.406, +0.517]; MRR finetuned - base (person): [+0.125, +0.246]

## Japanese asks (written for this test, none in training) (n = 28)

| system | receipt R@1 | receipt R@5 | receipt MRR | person R@1 | person R@5 | person MRR |
|---|---|---|---|---|---|---|
| keyword engine (demo default) | 0.000 | 0.000 | 0.000 | 0.036 | 0.036 | 0.042 |
| keyword engine, no load penalty | n/a | n/a | n/a | 0.036 | 0.036 | 0.042 |
| e5-small base | 0.679 | 0.821 | 0.754 | 0.714 | 0.929 | 0.797 |
| e5-small fine-tuned | 0.679 | 0.857 | 0.753 | 0.679 | 0.929 | 0.786 |

95% paired bootstrap interval of the MRR difference: MRR finetuned - keyword (receipt): [+0.609, +0.885]; MRR finetuned - base (receipt): [-0.165, +0.176]; MRR finetuned - keyword (person): [+0.620, +0.862]; MRR finetuned - base (person): [-0.160, +0.142]
