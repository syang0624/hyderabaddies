# Receipt retriever fine-tune. `make -C finetune all` from the repo root: venv (first time), pairs, train, eval.
# Runs locally (MPS if present, else CPU). No LLM calls anywhere.
PY := .venv/bin/python
VENV := .venv/.installed

.PHONY: all setup pairs train eval ask clean

all: $(VENV)
	$(MAKE) pairs
	$(MAKE) train
	$(MAKE) eval

$(VENV): requirements.txt
	python3 -m venv .venv
	$(PY) -m pip install -q --upgrade pip
	$(PY) -m pip install -q -r requirements.txt
	touch $(VENV)

setup: $(VENV)

pairs: $(VENV)
	$(PY) build_pairs.py

train: $(VENV)
	$(PY) train.py

eval: $(VENV)
	$(PY) eval.py

# make -C finetune ask Q="Who offered to facilitate the look-back session about A/B tests on what we charge?"
ask: $(VENV)
	$(PY) ask.py "$(Q)"

clean:
	rm -rf model
