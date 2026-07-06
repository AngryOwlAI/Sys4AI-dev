PY ?= python3
VENV ?= .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: venv install doctor validate validate-agentjob validate-agentjobs validate-skills validate-metrics validate-discovery-template bootstrap-memory clean-local

venv:
	$(PY) -m venv $(VENV)

install: venv
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

doctor:
	$(PYTHON) -m sys_for_ai.cli doctor

validate-agentjob:
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/examples/phase1_smoke_agentjob.yaml

validate-agentjobs:
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/examples/phase1_smoke_agentjob.yaml
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-SKILL-SYNC-001.yaml
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-CODEX-METRICS-ADAPT-001.yaml
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-SYSTEM-DEFINITION-TEMPLATE-001.yaml

validate-skills:
	$(PYTHON) -m sys_for_ai.cli validate-skills skills/core_skill_manifest.yaml

validate-metrics:
	$(PYTHON) -m sys_for_ai.cli validate-metrics skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py

validate-discovery-template:
	$(PYTHON) -m sys_for_ai.cli validate-discovery-record templates/system_definition/requirements-discovery-record-template.md

bootstrap-memory:
	$(PYTHON) -m sys_for_ai.cli bootstrap-memory registries

validate: doctor validate-agentjobs validate-skills validate-metrics validate-discovery-template bootstrap-memory

clean-local:
	rm -rf .pytest_cache __pycache__ sys_for_ai/__pycache__ .local/receipts
