PY ?= python3
VENV ?= .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: venv install doctor continue-status continue-preflight continue-select continue-packet continue-finalize validate validate-agentjob validate-agentjobs validate-skills validate-metrics validate-discovery-template bootstrap-memory validate-format-profiles validate-config-sources validate-control-records validate-program-state validate-director-decisions validate-agentjob-registry validate-director-decision-registry validate-handoff-registry validate-completion-receipt-registry validate-memory-preflight-registry validate-handoffs validate-completion-receipts validate-state-snapshots validate-memory-preflight validate-agentjob-boundaries validate-check-diff validate-one-active-agentjob validate-control-loop validate-validation-contract-registry validate-toml-config validate-jsonschema-contracts validate-registry-graph validate-requirement-trace generate-config-control-wiki generate-validation-contracts-catalog validate-generated-derivatives clean-local

venv:
	$(PY) -m venv $(VENV)

install: venv
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

doctor:
	$(PYTHON) -m sys_for_ai.cli doctor

continue-status:
	$(PYTHON) -m sys_for_ai.cli continue-status --json

continue-preflight:
	$(PYTHON) -m sys_for_ai.cli continue-preflight --json

continue-select:
	$(PYTHON) -m sys_for_ai.cli continue-select --json

continue-packet:
	$(PYTHON) -m sys_for_ai.cli continue-packet --json

continue-finalize:
	$(PYTHON) -m sys_for_ai.cli continue-finalize --completion control_records/completions/completion_receipt.example.v0_2.yaml --json

validate-agentjob:
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/examples/phase1_smoke_agentjob.yaml

validate-agentjobs:
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/examples/phase1_smoke_agentjob.yaml
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-SKILL-SYNC-001.yaml
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-CODEX-METRICS-ADAPT-001.yaml
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-SYSTEM-DEFINITION-TEMPLATE-001.yaml
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-SELFHOST-CONTINUE-KERNEL-001.yaml
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-BOUNDARY-VALIDATORS-001.yaml
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-DERIVATIVE-GENERATORS-001.yaml
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-CONTINUE-SKILLS-001.yaml
	$(PYTHON) -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-SELFHOST-ACCEPTANCE-001.yaml

validate-skills:
	$(PYTHON) -m sys_for_ai.cli validate-skills skills/core_skill_manifest.yaml

validate-metrics:
	$(PYTHON) -m sys_for_ai.cli validate-metrics skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py

validate-discovery-template:
	$(PYTHON) -m sys_for_ai.cli validate-discovery-record templates/system_definition/requirements-discovery-record-template.md

bootstrap-memory:
	$(PYTHON) -m sys_for_ai.cli bootstrap-memory registries

validate-format-profiles:
	$(PYTHON) -m sys_for_ai.cli validate-format-profiles registries/format_profile_registry.csv

validate-config-sources:
	$(PYTHON) -m sys_for_ai.cli validate-config-sources registries/config_source_registry.csv

validate-control-records:
	$(PYTHON) -m sys_for_ai.cli validate-control-records registries/control_record_registry.csv

validate-program-state:
	$(PYTHON) -m sys_for_ai.cli validate-program-state control_records/program_state.yaml

validate-director-decisions:
	$(PYTHON) -m sys_for_ai.cli validate-director-decisions control_records/director_decisions

validate-agentjob-registry:
	$(PYTHON) -m sys_for_ai.cli validate-agentjob-registry registries/agentjob_registry.csv

validate-director-decision-registry:
	$(PYTHON) -m sys_for_ai.cli validate-director-decision-registry registries/director_decision_registry.csv

validate-handoff-registry:
	$(PYTHON) -m sys_for_ai.cli validate-handoff-registry registries/handoff_registry.csv

validate-completion-receipt-registry:
	$(PYTHON) -m sys_for_ai.cli validate-completion-receipt-registry registries/completion_receipt_registry.csv

validate-memory-preflight-registry:
	$(PYTHON) -m sys_for_ai.cli validate-memory-preflight-registry registries/memory_preflight_receipt_registry.csv

validate-handoffs:
	$(PYTHON) -m sys_for_ai.cli validate-handoffs control_records/handoffs

validate-completion-receipts:
	$(PYTHON) -m sys_for_ai.cli validate-completion-receipts control_records/completions

validate-state-snapshots:
	$(PYTHON) -m sys_for_ai.cli validate-state-snapshots control_records/state_snapshots

validate-memory-preflight:
	$(PYTHON) -m sys_for_ai.cli validate-memory-preflight control_records/memory_preflights

validate-agentjob-boundaries:
	$(PYTHON) -m sys_for_ai.cli validate-agentjob-boundaries --agentjob AJ-P1-SELFHOST-ACCEPTANCE-001 --git --json

validate-check-diff:
	$(PYTHON) -m sys_for_ai.cli validate-check-diff --agentjob AJ-P1-SELFHOST-ACCEPTANCE-001 --json

validate-one-active-agentjob:
	$(PYTHON) -m sys_for_ai.cli validate-one-active-agentjob

validate-control-loop:
	$(PYTHON) -m sys_for_ai.cli validate-control-loop

validate-validation-contract-registry:
	$(PYTHON) -m sys_for_ai.cli validate-validation-contract-registry registries/validation_contract_registry.csv

validate-toml-config:
	$(PYTHON) -m sys_for_ai.cli validate-toml-config registries/config_source_registry.csv

validate-jsonschema-contracts:
	$(PYTHON) -m sys_for_ai.cli validate-jsonschema-contracts schemas/contracts

validate-registry-graph:
	$(PYTHON) -m sys_for_ai.cli validate-registry-graph registries

validate-requirement-trace:
	$(PYTHON) -m sys_for_ai.cli validate-requirement-trace registries/requirement_trace_registry.csv

generate-config-control-wiki:
	$(PYTHON) -m sys_for_ai.cli generate-config-control-wiki --check

generate-validation-contracts-catalog:
	$(PYTHON) -m sys_for_ai.cli generate-validation-contracts-catalog --check

validate-generated-derivatives:
	$(PYTHON) -m sys_for_ai.cli validate-generated-derivatives docs/generated registries/derivative_registry.csv

validate: doctor validate-agentjobs validate-skills validate-metrics validate-discovery-template bootstrap-memory validate-format-profiles validate-config-sources validate-control-records validate-program-state validate-agentjob-registry validate-director-decision-registry validate-handoff-registry validate-completion-receipt-registry validate-memory-preflight-registry validate-handoffs validate-completion-receipts validate-state-snapshots validate-memory-preflight validate-validation-contract-registry validate-toml-config validate-jsonschema-contracts validate-registry-graph validate-check-diff validate-one-active-agentjob validate-control-loop validate-requirement-trace generate-config-control-wiki generate-validation-contracts-catalog validate-generated-derivatives

clean-local:
	rm -rf .pytest_cache __pycache__ sys_for_ai/__pycache__ .local/receipts
