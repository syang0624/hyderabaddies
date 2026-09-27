# Evidence-layer demo. All targets work on macOS with system python3.
PY ?= python3
VENV = .venv
PIP = $(VENV)/bin/pip
PYV = $(VENV)/bin/python
PORT ?= 8787
ADC ?= $(firstword $(wildcard $(HOME)/.config/carl-life-os/gcloud-tmuc/application_default_credentials.json $(HOME)/.config/gcloud/application_default_credentials.json))
export GOOGLE_APPLICATION_CREDENTIALS ?= $(ADC)

.PHONY: setup run run-heuristic run-gemini test reset open smoke live live-sim video-mode warm manifest people ask

setup:            ## one-time: venv + google-genai + sounddevice (Gemini mode and the live layer)
	$(PY) -m venv $(VENV) && $(PIP) -q install --upgrade pip google-genai sounddevice

live:             ## meeting listener: mic -> Gemini 3.8 Live -> tool calls -> the UI (MIC="MacBook" to pick a device)
	MODE=heuristic $(PYV) live.py

people:           ## generate the fictional company (200 people) -> data/people.json
	$(PY) make_people.py && $(MAKE) manifest

ask:              ## who is best for Q? e.g. make ask Q="someone who can run the Northwind sync in English"
	curl -sf -X POST localhost:$(PORT)/api/ask -H 'Content-Type: application/json' -d "{\"question\": \"$(Q)\"}" | $(PY) -c 'import sys,json;d=json.load(sys.stdin);print("follow_up:",d["follow_up"]);[print(f"{i+1}. {p[chr(110)+chr(97)+chr(109)+chr(101)]} ({p[chr(114)+chr(111)+chr(108)+chr(101)]}, {p[chr(116)+chr(101)+chr(97)+chr(109)]}) load={p[chr(108)+chr(111)+chr(97)+chr(100)]} why={p[chr(119)+chr(104)+chr(121)]}") for i,p in enumerate(d["people"])]'

manifest:         ## count + hash every fixture file; the audit counts never-read sources from this, without opening them
	$(PY) -c 'import engine,json;m=engine.build_manifest();print(json.dumps({k:v["count"] for k,v in m.items()}))'

warm:             ## before a demo: extract all three people with Gemini once, so pages load instantly
	for c in rin yui kei; do curl -sf "localhost:$(PORT)/api/evidence/$$c?force=1&mode=gemini" | $(PY) -c 'import sys,json;d=json.load(sys.stdin)["evidence"];print(d["candidate"],d["backend"],len(d["claims"]),"claims,",d.get("dropped_unfaithful",0),"unfaithful")'; done

run:              ## start the demo (auto: Gemini if credentials work, else heuristic)
	PORT=$(PORT) MODE=auto $(PYV) server.py

run-heuristic:    ## no network, no credentials, deterministic
	PORT=$(PORT) MODE=heuristic $(PY) server.py

run-gemini:       ## force Gemini on Vertex; fails loudly if creds/quota are missing
	PORT=$(PORT) MODE=gemini $(PYV) server.py

reset:            ## clear cached evidence, ranking and annotations
	rm -f state/*.json

open:
	open http://localhost:$(PORT)

live-sim:         ## scripted PM/HR call (macOS say) through Gemini Live; reports which tools fired
	$(PYV) live_sim.py

video-mode:       ## clean state, then open the page in present mode
	rm -f state/*.json state/live.jsonl && open 'http://localhost:$(PORT)/?present=1'

smoke:            ## end-to-end API check against a running server
	curl -sf localhost:$(PORT)/api/company | $(PY) -c 'import sys,json;d=json.load(sys.stdin);print("backend:",d["backend"],"| candidates:",[c["id"] for c in d["candidates"]])'
	curl -sf localhost:$(PORT)/api/evidence/yui | $(PY) -c 'import sys,json;d=json.load(sys.stdin)["evidence"];print("yui claims:",len(d["claims"]),"dropped:",d["dropped_unsourced"],"backend:",d["backend"])'
	curl -sf -X POST localhost:$(PORT)/api/rank -H 'Content-Type: application/json' -d '{"criterion":"someone who will push back on a job-based culture rather than absorb it"}' | $(PY) -c 'import sys,json;d=json.load(sys.stdin);print("rank:",[(r["name"],r["fit"]) for r in d["ranking"]])'
	curl -sf -X POST localhost:$(PORT)/api/annotate -H 'Content-Type: application/json' -d '{"candidate":"yui","source_id":"sl-023","author":"yui","text":"I took this so nobody had to reshuffle; it was not a request to travel."}' >/dev/null && echo "annotation stored"
	curl -sf "localhost:$(PORT)/api/memo/yui" | head -12
	curl -sf localhost:$(PORT)/api/audit | $(PY) -c 'import sys,json;d=json.load(sys.stdin);print("never read:",{k:v["count"] for k,v in d["never_read"].items()})'
	@$(PY) -c 'import json,pathlib;p=pathlib.Path("state/annotations.json");r=[a for a in json.loads(p.read_text()) if a.get("author")!="smoke"] if p.exists() else [];p.write_text(json.dumps(r,indent=1))' && echo "smoke annotation removed"
