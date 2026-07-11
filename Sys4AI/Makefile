PY ?= python3
VENV ?= .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
SYNC_REMOTE ?= origin
SYNC_BRANCH ?= main
SYNC_CHECK_HASHES ?= 0

.PHONY: venv install doctor sync-check validate validate-skills validate-dev-skills validate-metrics validate-discovery-template bootstrap-memory validate-format-profiles validate-config-sources validate-control-records validate-system-layers validate-discovery-records validate-roles validate-artifact-contracts validate-core-skill-proposals validate-skill-lifecycle validate-program-state validate-director-decisions validate-director-decision-registry validate-handoff-registry validate-completion-receipt-registry validate-memory-preflight-registry validate-handoffs validate-completion-receipts validate-state-snapshots validate-memory-preflight validate-validation-contract-registry validate-strategic-intent validate-prd-semantics validate-host-capability-profiles validate-lifecycle-and-patterns validate-safety-evaluation validate-capability-migration validate-toml-config validate-jsonschema-contracts validate-registry-graph validate-requirement-trace validate-requirement-trace-migration validate-evidence-closure-plan validate-local-evidence-execution validate-python-package-surface validate-yaml-control-surface validate-format-governance-surface validate-plan-interpretation validate-prd-modules validate-walking-skeleton validate-target-package-smoke generate-evidence-closure-ledger generate-plan-interpretation generate-config-control-wiki generate-validation-contracts-catalog generate-governance-docs validate-generated-derivatives clean-local

venv:
	$(PY) -m venv $(VENV)

install: venv
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

doctor:
	$(PYTHON) -m sys_for_ai.cli doctor

sync-check:
	@set -eu; \
	target_ref="$(SYNC_REMOTE)/$(SYNC_BRANCH)"; \
	echo "Fetching $(SYNC_REMOTE)"; \
	git fetch "$(SYNC_REMOTE)"; \
	head_sha="$$(git rev-parse HEAD)"; \
	upstream_sha="$$(git rev-parse --verify "$$target_ref")"; \
	echo "HEAD: $$head_sha"; \
	echo "$$target_ref: $$upstream_sha"; \
	if [ "$$head_sha" != "$$upstream_sha" ]; then \
		echo "Sync check failed: HEAD does not match $$target_ref"; \
		exit 1; \
	fi; \
	echo "Git sync check passed: HEAD matches $$target_ref"
	$(PYTHON) -m sys_for_ai.cli memory status --json
	@if [ "$(SYNC_CHECK_HASHES)" = "1" ]; then \
		$(PYTHON) -m sys_for_ai.cli memory validate-hashes --json; \
	else \
		echo "Hash validation skipped. Run: make sync-check SYNC_CHECK_HASHES=1"; \
	fi

validate-skills:
	$(PYTHON) -m sys_for_ai.cli validate-skills skills/core_skill_manifest.yaml

validate-dev-skills:
	$(PY) ../scripts/skills/validate_skill_manifest.py --root ..

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

validate-system-layers:
	$(PYTHON) -m sys_for_ai.cli validate-system-layers registries/system_layer_registry.csv

validate-discovery-records:
	$(PYTHON) -m sys_for_ai.cli validate-discovery-records registries/discovery_record_registry.csv

validate-roles:
	$(PYTHON) -m sys_for_ai.cli validate-roles

validate-artifact-contracts:
	$(PYTHON) -m sys_for_ai.cli validate-artifact-contracts registries/artifact_contract_registry.csv

validate-core-skill-proposals:
	$(PYTHON) -m sys_for_ai.cli validate-core-skill-proposals registries/core_skill_proposal_registry.csv

validate-skill-lifecycle:
	$(PYTHON) -m sys_for_ai.cli validate-skill-lifecycle registries/skill_lifecycle_status_registry.csv

validate-program-state:
	$(PYTHON) -m sys_for_ai.cli validate-program-state control_records/program_state.yaml

validate-director-decisions:
	$(PYTHON) -m sys_for_ai.cli validate-director-decisions control_records/director_decisions

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

validate-validation-contract-registry:
	$(PYTHON) -m sys_for_ai.cli validate-validation-contract-registry registries/validation_contract_registry.csv

validate-strategic-intent:
	$(PYTHON) -m sys_for_ai.cli validate-strategic-intent

validate-prd-semantics:
	$(PYTHON) -m sys_for_ai.cli validate-prd-semantics

validate-host-capability-profiles:
	$(PYTHON) -m sys_for_ai.cli validate-host-capability-profiles configs/host_profiles --schema schemas/contracts/host_capability_profile.schema.json

validate-lifecycle-and-patterns:
	$(PYTHON) -m sys_for_ai.cli validate-lifecycle-and-patterns ../PRDs/Sys4AI_phase-0_product_system_design_prd.md

validate-safety-evaluation:
	$(PYTHON) -m sys_for_ai.cli validate-safety-evaluation assurance/meta_agent_self_change_safety_evaluation.yaml --schema schemas/contracts/self_change_safety_evaluation.schema.json --holdout-schema schemas/contracts/self_change_holdout_suite.schema.json

validate-capability-migration:
	$(PYTHON) -m sys_for_ai.cli validate-capability-migration configs/capability_migration.toml

validate-toml-config:
	$(PYTHON) -m sys_for_ai.cli validate-toml-config registries/config_source_registry.csv

validate-jsonschema-contracts:
	$(PYTHON) -m sys_for_ai.cli validate-jsonschema-contracts schemas/contracts

validate-registry-graph:
	$(PYTHON) -m sys_for_ai.cli validate-registry-graph registries

validate-requirement-trace:
	$(PYTHON) -m sys_for_ai.cli validate-requirement-trace registries/requirement_trace_registry.csv

validate-requirement-trace-migration:
	$(PYTHON) -m sys_for_ai.cli validate-requirement-trace-migration registries/requirement_trace_registry.csv --schema schemas/contracts/requirement_trace_registry_row.schema.json

validate-evidence-closure-plan:
	$(PYTHON) -m sys_for_ai.cli validate-evidence-closure-plan registries/evidence_closure_plan_registry.csv --trace registries/requirement_trace_registry.csv --execution-registry registries/local_evidence_execution_registry.csv

validate-local-evidence-execution:
	$(PYTHON) -m sys_for_ai.cli validate-local-evidence-execution registries/local_evidence_execution_registry.csv --trace registries/requirement_trace_registry.csv --ledger registries/evidence_closure_plan_registry.csv

validate-python-package-surface:
	$(PYTHON) -m sys_for_ai.cli validate-python-package-surface --pyproject pyproject.toml --requirements requirements.txt

validate-yaml-control-surface:
	$(PYTHON) -m sys_for_ai.cli validate-yaml-control-surface --pyproject pyproject.toml --format-profiles registries/format_profile_registry.csv --control-records registries/control_record_registry.csv --policy docs/configuration_control_wiki_policy.md --python-root sys_for_ai

validate-format-governance-surface:
	$(PYTHON) -m sys_for_ai.cli validate-format-governance-surface --format-profiles registries/format_profile_registry.csv --policy docs/format_profile_policy.md --memory-root .

validate-plan-interpretation:
	$(PYTHON) -m sys_for_ai.cli validate-plan-interpretation registries/plan_scope_interpretation_registry.csv --trace registries/requirement_trace_registry.csv --ledger registries/evidence_closure_plan_registry.csv

generate-evidence-closure-ledger:
	$(PYTHON) -m sys_for_ai.cli generate-evidence-closure-ledger --write

generate-plan-interpretation:
	$(PYTHON) -m sys_for_ai.cli generate-plan-interpretation --write

validate-prd-modules:
	$(PYTHON) -m sys_for_ai.cli validate-prd-modules registries/prd_module_registry.csv

validate-walking-skeleton:
	$(PYTHON) -m sys_for_ai.cli walking-skeleton validate-flow --json

validate-target-package-smoke:
	$(PYTHON) -m sys_for_ai.cli target-package validate examples/target_systems/repo_steward_agent_package --json

generate-config-control-wiki:
	$(PYTHON) -m sys_for_ai.cli generate-config-control-wiki --check

generate-validation-contracts-catalog:
	$(PYTHON) -m sys_for_ai.cli generate-validation-contracts-catalog --check

generate-governance-docs:
	$(PYTHON) -m sys_for_ai.cli generate-governance-docs --check

validate-generated-derivatives:
	$(PYTHON) -m sys_for_ai.cli validate-generated-derivatives docs/generated registries/derivative_registry.csv

validate: doctor validate-skills validate-dev-skills validate-metrics validate-discovery-template bootstrap-memory validate-format-profiles validate-config-sources validate-control-records validate-system-layers validate-discovery-records validate-roles validate-artifact-contracts validate-core-skill-proposals validate-skill-lifecycle validate-director-decision-registry validate-handoff-registry validate-completion-receipt-registry validate-memory-preflight-registry validate-handoffs validate-completion-receipts validate-state-snapshots validate-validation-contract-registry validate-toml-config validate-jsonschema-contracts validate-registry-graph validate-strategic-intent validate-host-capability-profiles validate-lifecycle-and-patterns validate-safety-evaluation validate-prd-semantics validate-capability-migration validate-requirement-trace validate-requirement-trace-migration validate-evidence-closure-plan validate-local-evidence-execution validate-python-package-surface validate-yaml-control-surface validate-format-governance-surface validate-plan-interpretation validate-prd-modules validate-walking-skeleton validate-target-package-smoke generate-config-control-wiki generate-validation-contracts-catalog generate-governance-docs validate-generated-derivatives

clean-local:
	rm -rf .pytest_cache __pycache__ sys_for_ai/__pycache__ .local/receipts
