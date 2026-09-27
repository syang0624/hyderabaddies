# Evidence-layer demo. All targets work on macOS with system python3.
PY ?= python3
VENV = .venv
PIP = $(VENV)/bin/pip
PYV = $(VENV)/bin/python
PORT ?= 8787
ADC ?= $(firstword $(wildcard $(HOME)/.config/carl-life-os/gcloud-tmuc/application_default_credentials.json $(HOME)/.config/gcloud/application_default_credentials.json))
export GOOGLE_APPLICATION_CREDENTIALS ?= $(ADC)

.PHONY: setup run run-heuristic run-gemini run-auth stats test reset open smoke live live-sim video-mode warm manifest people ask slack notion take take-meet take-crud live-script people-reset people-log graph

setup:            ## one-time: venv + google-genai + sounddevice (Gemini mode and the live layer)
	$(PY) -m venv $(VENV) && $(PIP) -q install --upgrade pip google-genai sounddevice slack_bolt notion-client

live:             ## meeting listener: mic -> Gemini 3.8 Live -> tool calls -> the UI (MIC="MacBook" to pick a device)
	MODE=heuristic $(PYV) live.py

people:           ## once: the fictional company, 200 people -> data/people.json. The committed file is the demo fixture; FORCE=1 regenerates it
	@if [ -s data/people.json ] && [ -z "$(FORCE)" ]; then echo "data/people.json exists (the demo fixture, shared with the video); make people FORCE=1 to regenerate"; else $(PY) make_people.py && $(MAKE) manifest; fi

ask:              ## who is best for Q? e.g. make ask Q="someone who can run the Northwind sync in English"
	curl -sf -X POST localhost:$(PORT)/api/ask -H 'Content-Type: application/json' -d "{\"question\": \"$(Q)\"}" | $(PY) -c 'import sys,json;d=json.load(sys.stdin);print("follow_up:",d["follow_up"]);[print(f"{i+1}. {p[chr(110)+chr(97)+chr(109)+chr(101)]} ({p[chr(114)+chr(111)+chr(108)+chr(101)]}, {p[chr(116)+chr(101)+chr(97)+chr(109)]}) load={p[chr(108)+chr(111)+chr(97)+chr(100)]} why={p[chr(119)+chr(104)+chr(121)]}") for i,p in enumerate(d["people"])]'

slack:            ## Slack surface (Socket Mode); tokens in ~/.config/carl-life-os/.env
	$(PYV) surfaces/slack_bot.py

notion:           ## Notion board surface; token + database id in ~/.config/carl-life-os/.env
	$(PYV) surfaces/notion_board.py

seed-slack:       ## fill the demo Slack workspace with fictional history from the fixtures (needs chat:write.customize, channels:manage, channels:join); DRY=1 previews
	$(PYV) surfaces/seed_slack.py

seed-notion:      ## fill the Notion board with fictional tickets (Done / In progress / new); DRY=1 previews
	$(PYV) surfaces/seed_notion.py

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

run-auth:         ## the judge walkthrough: sign-in required (PIK_AUTH=1), bring your own key on /settings, /stats; auto backend (Gemini via your key or ADC, else keyword)
	PIK_AUTH=1 PORT=$(PORT) MODE=auto $(if $(wildcard $(PYV)),$(PYV),$(PY)) server.py

stats:            ## the numbers behind /stats, from the state files (against a running server; with PIK_AUTH=1 pass COOKIE=<cookie file from curl -c>)
	curl -sf $(if $(COOKIE),-b $(COOKIE)) localhost:$(PORT)/api/stats | $(PY) -c 'import sys,json;d=json.load(sys.stdin);c=d["claims"];t=d["contest"];print("backend:",d["backend"],"|",d["extraction"]);print("receipts per source:",d["receipts_per_source"]);print("dropped share:",c["dropped_share"],"=",c["dropped_unsourced"],"+",c["dropped_unfaithful"],"/",c["proposed"]);print("contest rate:",t["rate"],"=",t["annotations"],"/",t["receipts_shown"]);print("asks per surface:",{k:v["asks"] for k,v in d["asks"]["by_surface"].items()});print("never read:",{k:v["count"] for k,v in d["never_read"].items()})' || echo "make stats: /api/stats did not answer (server down, or PIK_AUTH=1 without COOKIE=)"

reset:            ## clear cached evidence, ranking and annotations
	rm -f state/*.json

open:
	open http://localhost:$(PORT)

live-sim:         ## scripted PM/HR call (macOS say) through Gemini Live; grades which blocks landed per line (never plays audio)
	SPEAK=0 $(PYV) live_sim.py

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

take:             ## replay a transcript (scripts/<name>.json) through the running server's live layer: make take NAME=meet
	curl -sf -X POST localhost:$(PORT)/api/take -H 'Content-Type: application/json' -d '{"name": "$(NAME)"}'; echo

live-script:      ## replay a transcript directly, no server needed: make live-script SCRIPT=scripts/meet.json (FAST=1 skips the waits)
	SPEAK=0 MODE=heuristic $(PYV) live_script.py $(or $(SCRIPT),scripts/meet.json)

people-reset:     ## put data/people.json back to the committed fixture (data/people.base.json) and clear the record logs; annotations and caches survive (make reset clears those)
	curl -sf -X POST localhost:$(PORT)/api/reset -H 'Content-Type: application/json' -d '{"people": true}'; echo

people-log:       ## the record log: every confirmed add / edit / remove
	@test -s state/people-log.jsonl && cat state/people-log.jsonl | $(PY) -c 'import sys,json;[print(r["op"], r["person"]["id"], r["person"]["name"], "by", r["by"], r.get("changed","")) for r in map(json.loads, sys.stdin)]' || echo "no record changes"

graph:            ## shape and size of GET /api/graph
	curl -sf localhost:$(PORT)/api/graph | $(PY) -c 'import sys,json;g=json.load(sys.stdin);print(len(g["nodes"]),"nodes",len(g["hubs"]),"hubs",len(g["edges"]),"edges")'
