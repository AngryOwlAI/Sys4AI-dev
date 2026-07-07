# Sys4AI Phase 1 Implementation Initialization PRD

**Document status:** Draft baseline
**Product name:** `Sys4AI`
**Phase:** Phase 1: Implementation initialization
**Depends on:** `PRDs/Sys4AI_phase-0_product_system_design_prd.md`
**Last updated:** 2026-07-07

---

## 1. Executive summary

Phase 1 initializes the `Sys4AI` implementation repository so development can begin safely, reproducibly, and with source-first governance. Phase 1 does not finish the framework. It creates the first executable spine: Python environment, dependency policy, YAML control records, validators, skill adapters, memory registries, documentation policies, and a Docker decision record.

This revision also initializes the core file-format memory profile spine required by Phase 0: Markdown, CSV, YAML, TOML, and JSON Schema. Phase 1 adds minimal registries, examples, validators, dependency policy, and generated derivative stubs for YAML/TOML configuration-control artifacts and JSON Schema validation contracts. Phase 1 does not build a full wiki engine, does not introduce a vector database, does not make Obsidian canonical, and does not create a standalone JSON wiki by default.

This revision also initializes the discovery-gate, system-layer, self-hosting, role-governance, and skill-lifecycle obligations added to Phase 0. Phase 1 records the first executable registries, templates, validators, and control records needed to keep those concerns auditable without treating discovery candidates as approved requirements.

The default Phase 1 environment is a local Python virtual environment. Docker is deferred unless the environment decision record identifies concrete OS-level dependencies, multi-service orchestration needs, CI parity needs, or target-runtime template needs.

---

## 2. Goals

1. Create a minimal but real Python reference implementation scaffold.
2. Add `PyYAML` and safe YAML parsing as a first dependency.
3. Provide a repo-local `.venv` setup path.
4. Add a Makefile and CLI for validation commands.
5. Create initial YAML examples and schema-like specs.
6. Add source-first memory registries and bootstrap logic.
7. Add all core skill adapter shells from `ai-skills-for-sys`.
8. Add implementation plans and task packets for the next agent pass.
9. Decide whether Docker is needed now, later, or only for generated target systems.
10. Initialize core file-format memory profiles for Markdown, CSV, YAML, TOML, and JSON Schema.
11. Add initial format-profile, configuration-source, control-record, and validation-contract registries.
12. Add TOML configuration examples and parser support.
13. Add JSON Schema validation-contract examples and executable contract validation.
14. Add generated or stub-generated Configuration and Control Wiki pages for registered YAML and TOML artifacts.
15. Add generated or stub-generated Validation Contracts Catalog pages for JSON Schema contracts.
16. Extend Makefile and CLI validation commands to cover format profiles, TOML configuration, JSON Schema contracts, and derivative trace checks.
17. Initialize a Requirements Discovery Record gate before formal USRD generation for new or substantially changed system definitions.
18. Initialize system-layer and self-hosting controls for development-system, framework-product, target-template, target-instance, and derivative-surface work.
19. Initialize controlled role governance, role-to-skill crosswalks, temporary-role policy, and role execution-binding validation.
20. Initialize core skill lifecycle statuses and governed core skill expansion workflow.
21. Initialize `/init` as the gated Sys4AI system-definition and adoption front door.

---

## 3. Non-goals

- Do not implement a production runtime service.
- Do not add a vector database.
- Do not build a full generated wiki engine.
- Do not force Docker as the default developer environment.
- Do not treat Obsidian as canonical memory.
- Do not import external skill files without local adaptation and provenance records.
- Do not implement target-domain agent systems yet.
- Do not build a production memory database.
- Do not build a full interactive wiki engine.
- Do not create a standalone JSON wiki unless a later PRD introduces general JSON source or memory artifacts.
- Do not treat generated Configuration and Control Wiki pages as canonical.
- Do not treat generated Validation Contracts Catalog pages as canonical.
- Do not support TOML writing or style-preserving TOML editing in Phase 1.
- Do not support secret-bearing YAML or TOML configuration files in Phase 1.
- Do not treat JSON Schema validation as semantic or domain acceptance.
- Do not convert all existing schema-like YAML specs in one step if doing so would destabilize the scaffold.
- Do not treat Requirements Discovery Record candidate requirements as approved or baselined requirements.
- Do not promote product-scaffold skills into active development runtime without a runtime registry decision.
- Do not implement all proposed core organizational skills in this PRD-only integration step.

---

## 4. Initialization requirements

### 4.1 Repository layout

`SFA-P1-INIT-REPO-001`: Add a Python scaffold under `Sys4AI/sys_for_ai/`.

`SFA-P1-INIT-REPO-002`: Add `Sys4AI/requirements.txt`, `Sys4AI/pyproject.toml`, and `Sys4AI/Makefile`.

`SFA-P1-INIT-REPO-003`: Add folders for `schemas`, `control_records`, `registries`, `skills`, `docs`, and `templates`.

`SFA-P1-INIT-REPO-004`: Preserve top-level PRDs and implementation plans outside the implementation package.

`SFA-P1-INIT-REPO-005`: Add `configs/`, `schemas/contracts/`, `docs/generated/configuration_control/`, and `docs/generated/validation_contracts/` for the initial format-profile scaffold.

### 4.2 Python environment

`SFA-P1-INIT-ENV-001`: Use a local `.venv` as the required Phase 1 development environment.

`SFA-P1-INIT-ENV-002`: Keep `.venv/`, cache files, generated local vaults, and local receipts out of source control unless explicitly promoted.

`SFA-P1-INIT-ENV-003`: Provide setup commands through the Makefile:

```bash
cd Sys4AI
make venv
make install
make doctor
```

`SFA-P1-INIT-ENV-004`: Provide direct interpreter examples:

```bash
.venv/bin/python -m sys_for_ai.cli doctor
.venv/bin/python -m sys_for_ai.cli validate
```

### 4.3 Dependencies

`SFA-P1-INIT-DEP-001`: Add `PyYAML` as the initial required dependency.

`SFA-P1-INIT-DEP-002`: Pin the dependency family conservatively enough to avoid accidental major-version breaks.

`SFA-P1-INIT-DEP-003`: Add no heavy runtime dependencies until an implementation plan justifies them.

`SFA-P1-INIT-DEP-004`: Add JSON Schema validation support through a lightweight Python dependency.

`SFA-P1-INIT-DEP-005`: Add TOML parser support consistent with the supported Python version range. If Python `>=3.10` remains supported, Phase 1 shall add a conditional `tomli` dependency for Python versions below 3.11. If the project raises its minimum Python version to `>=3.11`, Phase 1 may use standard-library `tomllib` without `tomli`.

`SFA-P1-INIT-DEP-006`: Phase 1 shall not add TOML writing, style-preserving TOML editing, vector databases, production memory services, or heavy runtime dependencies for this feature.

### 4.4 YAML records and validators

`SFA-P1-INIT-YAML-001`: Create a smoke-test AgentJob YAML file.

`SFA-P1-INIT-YAML-002`: Create schema-like YAML specifications for AgentJobs and skills.

`SFA-P1-INIT-YAML-003`: Add validators that use `yaml.safe_load`.

`SFA-P1-INIT-YAML-004`: The validation command shall fail on missing required AgentJob fields or malformed skill manifest entries.

`SFA-P1-INIT-YAML-005`: Add handoff, completion receipt, and state snapshot YAML examples that carry source-first format-profile evidence.

`SFA-P1-INIT-YAML-006`: YAML control/state examples shall parse with safe YAML loading and validate against JSON Schema contracts where contracts exist.

### 4.5 Skill import and adaptation

`SFA-P1-INIT-SKILL-001`: Add a `core_skill_manifest.yaml` listing every current core skill from `ai-skills-for-sys`.

`SFA-P1-INIT-SKILL-002`: Add adapter shell folders for each core skill.

`SFA-P1-INIT-SKILL-003`: Each adapter shall include `SKILL.md`, `README.md`, `AGENTS.md`, and `examples/portable-example.md`.

`SFA-P1-INIT-SKILL-004`: Each adapter shall record source provenance and local adaptation status.

`SFA-P1-INIT-SKILL-005`: Exact upstream content synchronization shall be done by a later explicit import task, not silently.

### 4.6 Memory scaffold

`SFA-P1-INIT-MEM-001`: Add initial CSV registries for sources, derivatives, object relationships, and skills.

`SFA-P1-INIT-MEM-002`: Add a memory bootstrap command that creates missing registries with expected headers.

`SFA-P1-INIT-MEM-003`: Add documentation for source-first authority and derivative-surface policy.

`SFA-P1-INIT-MEM-004`: Obsidian support shall be documented as optional and derivative.

`SFA-P1-INIT-MEM-005`: Add `format_profile_registry.csv` for Markdown, CSV, YAML, TOML, and JSON Schema profile rows.

`SFA-P1-INIT-MEM-006`: Add `config_source_registry.csv` for registered TOML configuration sources and later configuration formats.

`SFA-P1-INIT-MEM-007`: Add `control_record_registry.csv` for registered YAML control/state artifacts.

`SFA-P1-INIT-MEM-008`: Add `validation_contract_registry.csv` for JSON Schema contracts and later validation-contract formats.

`SFA-P1-INIT-MEM-009`: Update source and derivative registries so canonical source files and generated derivative stubs remain distinguishable.

### 4.7 Core format-profile scaffold

`SFA-P1-INIT-FORMAT-001`: Initialize the core file-format profile scaffold without promoting generated derivatives to canonical authority.

`SFA-P1-INIT-FORMAT-002`: Add TOML examples under `configs/examples/` for framework configuration and target-project configuration.

`SFA-P1-INIT-FORMAT-003`: Add JSON Schema contracts under `schemas/contracts/` for initial AgentJob, handoff, completion receipt, state snapshot, TOML configuration, and registry-row structures.

`SFA-P1-INIT-FORMAT-004`: Add policy documents for format profiles, Configuration and Control Wiki behavior, and Validation Contracts Catalog behavior.

`SFA-P1-INIT-FORMAT-005`: Add generated or stub-generated Configuration and Control Wiki pages under `docs/generated/configuration_control/`.

`SFA-P1-INIT-FORMAT-006`: Add generated or stub-generated Validation Contracts Catalog pages under `docs/generated/validation_contracts/`.

`SFA-P1-INIT-FORMAT-007`: Generated wiki/catalog pages shall contain non-canonical authority notices, source trace placeholders or populated source trace, registry evidence, generator metadata, and stale/orphan status.

### 4.8 Docker decision

`SFA-P1-INIT-DOCKER-001`: Add an environment decision record that chooses `.venv` as the Phase 1 baseline.

`SFA-P1-INIT-DOCKER-002`: Defer development Docker until a trigger exists: OS-level rendering dependencies, multi-service runtime, strict CI parity, contributor environment drift, or target-runtime generation.

`SFA-P1-INIT-DOCKER-003`: Keep development environment containers separate from target-system runtime container templates.

### 4.9 Validation

`SFA-P1-INIT-VAL-001`: Add `make doctor` to check Python, PyYAML, package import, and expected folders.

`SFA-P1-INIT-VAL-002`: Add `make validate-agentjob`, `make validate-skills`, `make bootstrap-memory`, and `make validate`.

`SFA-P1-INIT-VAL-003`: Validation shall be deterministic and runnable offline after dependencies are installed.

`SFA-P1-INIT-VAL-004`: Add validation commands for format profiles, configuration sources, control records, validation contracts, TOML configuration, JSON Schema contracts, registry graph consistency, generated Configuration and Control Wiki stubs, and generated Validation Contracts Catalog stubs.

`SFA-P1-INIT-VAL-005`: Validation shall fail or warn when governed YAML, TOML, JSON Schema, or CSV artifacts are missing registry rows, reference missing validation contracts, point to missing source files, or appear as generated derivatives with canonical authority.

`SFA-P1-INIT-VAL-006`: Validation shall fail or warn when YAML or TOML examples contain secret-like keys or values according to Phase 1 security policy.

`SFA-P1-INIT-VAL-007`: Validation shall preserve the distinction between structural admissibility and semantic/domain correctness.

`SFA-P1-INIT-VAL-008`: Add a PRD requirement trace validator that checks requirement ID uniqueness and verifies that Phase 0 requirement IDs have explicit Phase 1 coverage, partial coverage, deferral, or not-applicable trace rows with semantic trace classes, justification for partial, deferred, or out-of-phase mappings, and a semantic review verdict for each non-implemented trace row.

`SFA-P1-INIT-VAL-009`: Add a dedicated `make validate-roles` target for controlled role catalogs, role-to-skill crosswalks, execution-binding constraints, generated role Markdown freshness, and role-related proposed skill references. The aggregate `make validate` target shall include `make validate-roles` so role-catalog drift is checked by default.

### 4.10 Discovery Gate Initialization

`SFA-P1-INIT-DISC-001`: Add the Requirements Discovery Record to the artifact catalog, source registry, derivative registry policy, and trace model.

`SFA-P1-INIT-DISC-002`: Add or extend a discovery-record registry that records RDR path, subject system ID, subject layer, producer AgentJob, authority status, candidate requirement count, open question count, downstream USRD link, validation status, source hash, and last validation timestamp.

`SFA-P1-INIT-DISC-003`: Add a sample AgentJob for running `system-definition-interview-context-45` on a new target system or framework-product change.

`SFA-P1-INIT-DISC-004`: Add a sample completion receipt showing RDR creation, validation evidence, open issues, and recommended next route.

`SFA-P1-INIT-DISC-005`: Extend aggregate validation so discovery-record templates and registered discovery records are validated by default.

### 4.10.1 `/init` Front-Door Initialization

`SFA-P1-INIT-FRONTDOOR-001`: Add active runtime skill package `.agents/skills/init/` with `SKILL.md`, `README.md`, `AGENTS.md`, `skill.yaml`, and a portable example.

`SFA-P1-INIT-FRONTDOOR-002`: Add `.codex/skills/init/SKILL.md` as a compatibility shim that points to `.agents/skills/init/` and does not carry independent behavior.

`SFA-P1-INIT-FRONTDOOR-003`: Add `Sys4AI/skills/core/init/` as the product-scaffold reference package for future target systems.

`SFA-P1-INIT-FRONTDOOR-004`: Register `init` in the runtime skill registry, core systems engineering bundle, product core skill manifest, skill registry, core skill proposal registry, role-to-skill crosswalk, object relationship registry, source registry, and requirement trace registry.

`SFA-P1-INIT-FRONTDOOR-005`: Extend the skill-manifest validator so `init` is required by the core skill set.

`SFA-P1-INIT-FRONTDOOR-006`: Add a Current-State Baseline template for brownfield discovery and mark it as draft evidence rather than canonical authority.

`SFA-P1-INIT-FRONTDOOR-007`: Add tests that verify `/init` exists in runtime, shim, and product-scaffold surfaces; brownfield first pass is read-only; Product Requirements Document creation is gated; candidate requirement labels are preserved; and product-scaffold wording does not claim active runtime authority.

`SFA-P1-INIT-FRONTDOOR-008`: Add Director decision, AgentJob, memory preflight receipt, completion receipt, and handoff control records for `/init` front-door implementation.

### 4.11 System-Layer and Self-Hosting Initialization

`SFA-P1-INIT-LAYER-001`: Add a controlled system-layer registry for `development_system`, `framework_product`, `target_system_template`, `target_system_instance`, and `derivative_surface`.

`SFA-P1-INIT-LAYER-002`: Add a self-hosting mode policy document that distinguishes `Sys4AI-dev` active runtime authority from `Sys4AI` product scaffold authority.

`SFA-P1-INIT-LAYER-003`: Add a self-hosting TOML configuration source and register it in `config_source_registry.csv`.

`SFA-P1-INIT-LAYER-004`: Add `validate-system-layers` to verify allowed layer IDs, canonical roots, derivative roots, authority mutation rules, and self-hosting constraints.

### 4.12 Role Governance Initialization

`SFA-P1-INIT-ROLE-001`: Phase 1 shall implement a controlled role registry.

`SFA-P1-INIT-ROLE-002`: Phase 1 shall implement a role-to-skill crosswalk registry.

`SFA-P1-INIT-ROLE-003`: Phase 1 shall implement role execution-binding validation.

`SFA-P1-INIT-ROLE-004`: Phase 1 shall support one-Job temporary roles with expiry, authority scope, required skills, allowed artifacts, validators, and supersession policy.

`SFA-P1-INIT-ROLE-005`: Phase 1 aggregate validation shall include role-governance checks by default.

### 4.13 Core Skill Expansion Initialization

`SFA-P1-INIT-CORESKILL-001`: Phase 1 shall extend skill registry data with lifecycle status, authority surface, provenance, role bindings, validation commands, and activation constraints.

`SFA-P1-INIT-CORESKILL-002`: Phase 1 shall add or update a skill-lifecycle validator that checks controlled statuses and rejects active-runtime use of non-active skill packages.

`SFA-P1-INIT-CORESKILL-003`: Phase 1 shall add governed proposal surfaces for core organizational skills and shall distinguish them from project-specific domain packs.

`SFA-P1-INIT-CORESKILL-004`: Phase 1 shall provide minimal scaffold or runtime packages for approved core organizational skills only through controlled AgentJobs.

`SFA-P1-INIT-CORESKILL-005`: Phase 1 aggregate validation shall include skill-lifecycle checks by default after the registry/schema expansion slice creates the required data model.

---

## 5. Acceptance criteria

Phase 1 initialization is acceptable when:

1. `make doctor` passes inside `Sys4AI/`.
2. `make validate` passes inside `Sys4AI/`.
3. The sample AgentJob YAML validates.
4. The core skill manifest validates and all adapter folders exist.
5. Memory registries exist with expected headers.
6. The Docker decision record exists and distinguishes development environment from target runtime.
7. Phase 0 product requirements and Phase 1 initialization requirements are no longer mixed in one PRD.
8. `format_profile_registry.csv` exists with expected headers and rows for Markdown, CSV, YAML, TOML, and JSON Schema.
9. `config_source_registry.csv` exists with expected headers and at least one TOML example row.
10. `control_record_registry.csv` exists with expected headers and rows for AgentJob, handoff, completion receipt, and state snapshot examples.
11. `validation_contract_registry.csv` exists with expected headers and rows for initial JSON Schema contracts.
12. `pyproject.toml` and `requirements.txt` include PyYAML, JSON Schema validation support, and TOML parsing support consistent with the selected Python version policy.
13. TOML examples parse successfully and validate against their declared JSON Schema contracts.
14. YAML control examples parse with safe YAML loading and validate against their declared JSON Schema contracts where contracts exist.
15. JSON Schema files load and pass schema checks for the selected dialect.
16. CSV registry headers pass validation.
17. Registry graph validation detects missing source paths, missing contract IDs, invalid authority classes, orphan derivatives, and generated derivatives marked as canonical.
18. Generated Configuration and Control Wiki stubs exist, contain non-canonical authority banners, and link to YAML/TOML source and registry evidence.
19. Generated Validation Contracts Catalog stubs exist, contain non-canonical authority banners, and link to JSON Schema source and registry evidence.
20. No standalone JSON wiki is created.
21. Secret-like keys in YAML/TOML examples are absent or cause validation warnings/failures according to Phase 1 policy.
22. `make validate` passes after dependencies are installed.
23. The Phase 1 recommended AgentJob includes the new validators and generated derivative checks.
24. The PRD requirement trace validator passes against the canonical Phase 0 PRD, Phase 1 PRD, and requirement trace registry, including semantic trace class, partial-justification, and non-implemented semantic review verdict checks.
25. `make validate-roles` exists, passes for the controlled role-catalog surface, and is included in `make validate`.
26. Requirements Discovery Record templates, registry rows, and validation commands exist before RDR artifacts can feed USRD baseline.
27. System-layer and self-hosting controls distinguish `Sys4AI-dev` development runtime authority from `Sys4AI` product scaffold authority.
28. Role registries, role-to-skill crosswalks, and temporary-role execution-binding checks are registered and validated.
29. Core skill lifecycle status and runtime-authority validation prevent scaffold or proposal skills from becoming active authority by implication.

---

## 6. Recommended next AgentJob

```yaml
agentjob_id: AJ-P1-BOOTSTRAP-001
objective: Apply the Phase 1 repository overlay, create the Python virtual environment, install dependencies, and run validation.
role: implementation_initialization_agent
allowed_reads:
  - PRDs/Sys4AI_phase-0_product_system_design_prd.md
  - PRDs/Sys4AI_phase-1_implementation_initialization_prd.md
  - implementation_plans/phase-1_environment_decision_record.md
allowed_writes:
  - Sys4AI/**
  - implementation_plans/**
forbidden_actions:
  - Delete repository root license or notice files.
  - Treat generated derivatives as canonical sources.
  - Force Docker as default without updating the decision record.
expected_outputs:
  - Passing validation command receipt.
  - Updated source registry entries if files are promoted as canonical.
validators:
  - cd Sys4AI && make doctor
  - cd Sys4AI && make validate
stop_conditions:
  - Required dependency installation fails.
  - Existing repository file would be overwritten without maintainer approval.
```

```yaml
agentjob_id: AJ-P1-FORMAT-PROFILES-001
objective: Integrate core file-format memory profile requirements into the Phase 1 scaffold, including TOML configuration support, JSON Schema validation contracts, new registries, and generated derivative stubs.
role: implementation_initialization_agent
allowed_reads:
  - PRDs/Sys4AI_phase-0_product_system_design_prd.md
  - PRDs/Sys4AI_phase-1_implementation_initialization_prd.md
  - Sys4AI/**
  - implementation_plans/**
allowed_writes:
  - PRDs/Sys4AI_phase-0_product_system_design_prd.md
  - PRDs/Sys4AI_phase-1_implementation_initialization_prd.md
  - implementation_plans/**
  - Sys4AI/configs/**
  - Sys4AI/control_records/**
  - Sys4AI/schemas/**
  - Sys4AI/registries/**
  - Sys4AI/docs/**
  - Sys4AI/sys_for_ai/**
  - Sys4AI/tests/**
  - Sys4AI/requirements.txt
  - Sys4AI/pyproject.toml
  - Sys4AI/Makefile
forbidden_actions:
  - Delete repository root license or notice files.
  - Treat generated derivatives as canonical sources.
  - Create a standalone JSON wiki for JSON Schema.
  - Add vector database or production memory service dependencies.
  - Add secret-bearing TOML or YAML examples.
  - Use unsafe YAML loaders.
expected_outputs:
  - Updated Phase 0 PRD with core file-format profile requirements.
  - Updated Phase 1 PRD with implementation initialization requirements.
  - New registries for format profiles, config sources, control records, and validation contracts.
  - TOML example files and parser support.
  - JSON Schema contract files and validator support.
  - Generated Configuration and Control Wiki stubs.
  - Generated Validation Contracts Catalog stubs.
  - Passing validation command receipt.
validators:
  - cd Sys4AI && make doctor
  - cd Sys4AI && make validate
  - cd Sys4AI && make validate-roles
  - cd Sys4AI && make validate-format-profiles
  - cd Sys4AI && make validate-toml-config
  - cd Sys4AI && make validate-jsonschema-contracts
  - cd Sys4AI && make validate-registry-graph
  - cd Sys4AI && make validate-requirement-trace
  - cd Sys4AI && make validate-generated-derivatives
stop_conditions:
  - Required dependency installation fails.
  - Existing repository file would be overwritten without review.
  - Generated derivative would be marked canonical.
  - JSON wiki creation becomes necessary because requirements changed.
  - Secret-like value is discovered in a config/control example.
```
