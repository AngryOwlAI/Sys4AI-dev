# Extremely Detailed Implementation Plan: Integrate the Updated `ai-skills-for-sys` Skillset into `sys-for-ai-dev`

**Repository:** `AngryOwlAI/sys-for-ai-dev`
**Target implementation root:** `sys-for-ai/`
**Upstream skill source:** `AngryOwlAI/ai-skills-for-sys`
**Plan date:** 2026-07-05
**Plan status:** Implementation-ready, not yet applied
**Primary objective:** Bring `sys-for-ai-dev` into alignment with the current retained systems-engineering skillset, especially the newly added `system-definition-interview` and `system-definition-interview-context-45` skills, while preserving the project’s source-first memory, AgentJob, validation, and artifact-governance model.

---

## 0. Executive Summary

`sys-for-ai-dev` currently has the Phase 1 scaffold needed to host core skill adapters, validate a core skill manifest, bootstrap source-first registries, and run local validation. However, its local skill universe is stale relative to the current `ai-skills-for-sys` template library.

The immediate integration gap is the missing system-definition front door:

1. `system-definition-interview`
2. `system-definition-interview-context-45`

These skills must be integrated into:

- `sys-for-ai/skills/core_skill_manifest.yaml`
- `sys-for-ai/sys_for_ai/validators.py`
- `sys-for-ai/registries/skill_registry.csv`
- `sys-for-ai/skills/core/<skill-id>/` adapter folders
- source-first registry evidence
- AgentJob control records
- requirements-discovery templates
- validation commands
- downstream documentation and lifecycle guidance

The plan also implements the prior recommendation to either operationalize the `codex-usage-metrics` dependency or explicitly fail closed for long-context system-definition sessions. The recommended path is operationalization: adapt the metrics script into the local `codex-usage-metrics` adapter and validate that it supports `--help` and output-path generation.

This plan intentionally does **not** make generated discovery records canonical by default. Discovery records are draft/evidence derivatives unless promoted through the project’s source-authority process.

---

## 1. Current-State Baseline

### 1.1 Existing repository model

The `sys-for-ai-dev` top-level README states that the developed project lives in `sys-for-ai/`. It also identifies current product-definition sources under `PRDs/` and states that Phase 1 implementation planning, validators, registries, skill adapters, and documentation policies live under `sys-for-ai/`.

Current important paths:

```text
sys-for-ai/
  Makefile
  README.md
  requirements.txt
  pyproject.toml
  sys_for_ai/
    cli.py
    validators.py
    skills.py
    memory.py
    yaml_io.py
  schemas/
    agentjob.schema.yaml
    skill.schema.yaml
  control_records/
    examples/phase1_smoke_agentjob.yaml
  registries/
    source_registry.csv
    derivative_registry.csv
    object_relationship_registry.csv
    skill_registry.csv
  skills/
    core_skill_manifest.yaml
    core/
      codex-usage-metrics/
      conversation-to-prd/
      decision-grilling/
      decision-grilling-context-45/
      domain-grilling-with-docs/
      domain-grilling-with-docs-context-45/
      mermaid-diagrams/
      plantuml-diagrams/
      prd-to-implementation-plan/
      skill-import-generalizer/
      technical-writing-quality-gate/
  docs/
  templates/
```

### 1.2 Existing validation behavior

`sys-for-ai/Makefile` currently exposes:

```make
make doctor
make validate-agentjob
make validate-skills
make bootstrap-memory
make validate
```

`make validate-skills` calls:

```bash
$(PYTHON) -m sys_for_ai.cli validate-skills skills/core_skill_manifest.yaml
```

`sys_for_ai.validators.validate_skill_manifest()` currently checks:

- the manifest root is a YAML mapping,
- `skills` is a list,
- every skill entry has an `id`,
- every adapter folder exists,
- every adapter folder contains:
  - `SKILL.md`
  - `README.md`
  - `AGENTS.md`
  - `examples/portable-example.md`
- listed skills exactly match the hard-coded `SKILL_MANIFEST_REQUIRED_SKILLS` set.

The problem is that the hard-coded set is now stale.

### 1.3 Existing local skill manifest gap

`sys-for-ai/skills/core_skill_manifest.yaml` currently lists these core skills:

```text
codex-usage-metrics
conversation-to-prd
decision-grilling
decision-grilling-context-45
domain-grilling-with-docs
domain-grilling-with-docs-context-45
mermaid-diagrams
plantuml-diagrams
prd-to-implementation-plan
skill-import-generalizer
technical-writing-quality-gate
```

It does not list:

```text
system-definition-interview
system-definition-interview-context-45
```

### 1.4 Existing registry gap

`sys-for-ai/registries/skill_registry.csv` mirrors the same stale eleven-skill set. It does not include either system-definition skill.

### 1.5 Existing adapter gap

The following adapter folders are missing:

```text
sys-for-ai/skills/core/system-definition-interview/
sys-for-ai/skills/core/system-definition-interview-context-45/
```

### 1.6 Existing `codex-usage-metrics` gap

The current local `codex-usage-metrics` adapter is an adapter shell only. It does not include the upstream script:

```text
scripts/collect_usage_metrics.py
```

This matters because `system-definition-interview-context-45` depends on `codex-usage-metrics` for its context checkpoint behavior.

---

## 2. Target State

When this plan is complete, `sys-for-ai-dev` will have:

1. A current core skill manifest that includes all retained systems-engineering skills needed by the project.
2. Validator expectations that include the system-definition skills.
3. Local adapter shell folders for both system-definition skills.
4. Local adapter behavior fitted to `sys-for-ai` authority rules.
5. A runnable or explicitly fail-closed context-metrics path for `system-definition-interview-context-45`.
6. A controlled `requirements-discovery-record` template.
7. Optional validator support for discovery records.
8. AgentJobs that authorize the integration and future use of the skills.
9. Source registry and skill registry entries preserving provenance.
10. A practical systems-document spine that prevents PRD overloading.
11. Validation evidence showing that `make validate-skills` and `make validate` pass only when the updated skill set is present.

Target new or changed file tree:

```text
sys-for-ai/
  control_records/
    examples/
      phase1_smoke_agentjob.yaml                       # maybe update allowed reads
    agentjobs/
      AJ-P1-SKILL-SYNC-001.yaml                       # new
      AJ-P1-SYSTEM-DEFINITION-TEMPLATE-001.yaml       # new
      AJ-P1-CODEX-METRICS-ADAPT-001.yaml              # new
    system_definition/
      README.md                                       # optional new controlled-output dir
  docs/
    skill_integration_policy.md                       # new or update existing skill docs
    system_document_spine.md                          # new
    source_first_authority_policy.md                  # if absent, add; if present, update
  registries/
    skill_registry.csv                                # update
    source_registry.csv                               # update
    derivative_registry.csv                           # update if generated docs are added
    object_relationship_registry.csv                  # update if relationships are tracked
  schemas/
    discovery_record.schema.yaml                      # new schema-like spec
    skill.schema.yaml                                 # update recommended fields
  skills/
    core_skill_manifest.yaml                          # update
    core/
      codex-usage-metrics/
        scripts/
          collect_usage_metrics.py                    # new if operational policy chosen
      system-definition-interview/
        SKILL.md                                      # new
        README.md                                     # new
        AGENTS.md                                     # new
        examples/
          portable-example.md                         # new
      system-definition-interview-context-45/
        SKILL.md                                      # new
        README.md                                     # new
        AGENTS.md                                     # new
        examples/
          portable-example.md                         # new
  sys_for_ai/
    cli.py                                           # optional update
    validators.py                                    # required update
    discovery.py                                     # optional new helper
    skills.py                                        # optional update
  templates/
    system_definition/
      requirements-discovery-record-template.md       # new
      temp-prd-template.md                            # new
```

---

## 3. Guiding Implementation Principles

### 3.1 Source-first authority

Canonical sources, PRDs, registries, control records, and explicit decision records outrank generated discovery records, notes, wikis, diagrams, semantic caches, or other reader surfaces.

### 3.2 Local adaptation, not blind copying

The upstream skill library stores reusable templates. `sys-for-ai-dev` must adapt those templates locally. The local adapter should preserve upstream method and provenance while binding all work to local AgentJob, registry, validation, and authority rules.

### 3.3 Candidate requirements remain candidates

Any output from `system-definition-interview` or `system-definition-interview-context-45` must label candidate requirements as:

```text
REQ-CAND-*
NFR-CAND-*
```

They must not become baselined system requirements until a project authority promotes them.

### 3.4 Every integration has validation evidence

Every implementation step must either:

- run a validation command successfully, or
- record why the validation could not be run and what remains blocked.

### 3.5 Context-45 must fail closed

If live context metrics cannot be collected, `system-definition-interview-context-45` must write `temp_prd.md` and stop rather than continuing a long interview with unknown context state.

### 3.6 Avoid PRD monoculture

A Product Requirements Document is not a complete system-program documentation model. The project must maintain a document spine that separates product intent, system requirements, architecture, verification, operations, and closeout.

---

## 4. Work Breakdown Structure

### Epic A: Preflight and repository state capture

**Goal:** Make the change auditable before editing.

Tasks:

1. Confirm clean working tree.
2. Record current branch and commit.
3. Run baseline validation.
4. Save validation output as a local receipt.
5. Confirm current skill manifest gap.
6. Confirm missing adapter folders.
7. Confirm current `codex-usage-metrics` adapter script gap.

Suggested commands:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
cd sys-for-ai
make doctor
make validate
```

Expected baseline result:

- `make validate` may pass because the validator is stale.
- The implementation receipt must explicitly state that passing baseline validation does **not** mean the new upstream skill set is integrated.

Receipt path:

```text
sys-for-ai/.local/receipts/AJ-P1-SKILL-SYNC-001-baseline.txt
```

Do not commit `.local/receipts/` unless the project explicitly promotes receipts into controlled evidence.

---

### Epic B: Update the core skill universe

**Goal:** Make the local manifest and validator aware of the new front-door system-definition skills.

Files:

```text
sys-for-ai/skills/core_skill_manifest.yaml
sys-for-ai/sys_for_ai/validators.py
sys-for-ai/registries/skill_registry.csv
```

#### B.1 Update `validators.py`

Current hard-coded set should become:

```python
SKILL_MANIFEST_REQUIRED_SKILLS = {
    "codex-usage-metrics",
    "system-definition-interview",
    "system-definition-interview-context-45",
    "conversation-to-prd",
    "decision-grilling",
    "decision-grilling-context-45",
    "domain-grilling-with-docs",
    "domain-grilling-with-docs-context-45",
    "mermaid-diagrams",
    "plantuml-diagrams",
    "prd-to-implementation-plan",
    "skill-import-generalizer",
    "technical-writing-quality-gate",
}
```

Recommended second-stage refactor:

Replace the hard-coded Python set with a loaded expected-skill baseline file, for example:

```text
sys-for-ai/skills/core_skill_baseline.yaml
```

Example future baseline:

```yaml
baseline_id: SFA-CORE-SKILL-BASELINE-001
status: draft
last_reviewed: 2026-07-05
source_repo: https://github.com/AngryOwlAI/ai-skills-for-sys
required_skill_ids:
  - codex-usage-metrics
  - system-definition-interview
  - system-definition-interview-context-45
  - conversation-to-prd
  - decision-grilling
  - decision-grilling-context-45
  - domain-grilling-with-docs
  - domain-grilling-with-docs-context-45
  - mermaid-diagrams
  - plantuml-diagrams
  - prd-to-implementation-plan
  - skill-import-generalizer
  - technical-writing-quality-gate
```

Do not do the refactor in the same patch if the aim is smallest safe change. Add it as a follow-up AgentJob unless implementation capacity is explicitly available.

#### B.2 Update `core_skill_manifest.yaml`

Insert after `codex-usage-metrics`:

```yaml
  - id: system-definition-interview
    name: System Definition Interview
    family: system_definition_elicitation
    source_repo: https://github.com/AngryOwlAI/ai-skills-for-sys
    source_path: skills/system-definition-interview
    local_path: core/system-definition-interview
    adaptation_status: adapter_shell
    required_files:
      - SKILL.md
      - README.md
      - AGENTS.md
      - examples/portable-example.md
    description: "Interview stakeholders to establish or reconstruct system intent, boundaries, stakeholders, scenarios, candidate requirements, architecture drivers, interfaces, evidence, and V&V seeds before PRD or formal systems-document generation."
  - id: system-definition-interview-context-45
    name: System Definition Interview Context 45
    family: system_definition_elicitation
    source_repo: https://github.com/AngryOwlAI/ai-skills-for-sys
    source_path: skills/system-definition-interview-context-45
    local_path: core/system-definition-interview-context-45
    adaptation_status: adapter_shell
    required_files:
      - SKILL.md
      - README.md
      - AGENTS.md
      - examples/portable-example.md
    description: "Long-session stakeholder elicitation workflow for system intent discovery with a 45 percent context-used checkpoint and resumable temp_prd.md handoff."
    required_skills:
      - codex-usage-metrics
    local_runtime_paths:
      skills_root: skills/core
      target_skill_path: skills/core/system-definition-interview-context-45
      default_discovery_output_dir: control_records/system_definition
```

If `validate_skill_manifest()` currently ignores `required_skills` and `local_runtime_paths`, that is acceptable as a forward-compatible manifest extension, but document it in `schemas/skill.schema.yaml`.

#### B.3 Update `skill.schema.yaml`

Add recommended fields:

```yaml
recommended_fields:
  validators:
    type: list[string]
  authority_boundaries:
    type: list[string]
  known_failure_modes:
    type: list[string]
  required_skills:
    type: list[string]
  optional_skills:
    type: list[string]
  local_runtime_paths:
    type: mapping
  source_provenance:
    type: mapping
```

#### B.4 Update `skill_registry.csv`

Add rows:

```csv
system-definition-interview,skills/core/system-definition-interview,https://github.com/AngryOwlAI/ai-skills-for-sys,skills/system-definition-interview,system_definition_elicitation,adapter_shell,2026-07-05,"Phase 1 adapter shell; upstream template added 2026-07-05; exact local adaptation pending."
system-definition-interview-context-45,skills/core/system-definition-interview-context-45,https://github.com/AngryOwlAI/ai-skills-for-sys,skills/system-definition-interview-context-45,system_definition_elicitation,adapter_shell,2026-07-05,"Phase 1 adapter shell; requires codex-usage-metrics support or fail-closed temp_prd.md handoff behavior."
```

Validation after Epic B, before adapter folders exist:

```bash
cd sys-for-ai
make validate-skills
```

Expected result:

- It should fail, because the manifest now requires missing adapter folders.
- This failure is useful evidence that the validator now sees the new skills.

Save output:

```text
sys-for-ai/.local/receipts/AJ-P1-SKILL-SYNC-001-validator-now-detects-gap.txt
```

---

### Epic C: Create local adapter shell folders

**Goal:** Provide the required local adapter surfaces for the two missing skills.

Create:

```text
sys-for-ai/skills/core/system-definition-interview/
  SKILL.md
  README.md
  AGENTS.md
  examples/portable-example.md

sys-for-ai/skills/core/system-definition-interview-context-45/
  SKILL.md
  README.md
  AGENTS.md
  examples/portable-example.md
```

#### C.1 Adapter shell design rules

Each adapter must include:

- YAML front matter with name, description, adaptation status, upstream repository, and upstream path.
- Purpose.
- When to use.
- Inputs.
- Outputs.
- Procedure.
- Local authority boundaries.
- Validation.
- Known failure modes.
- Provenance.
- Adaptation work remaining.

#### C.2 `system-definition-interview/SKILL.md` local adapter content

Recommended content:

```markdown
---
name: system-definition-interview
description: Establish or reconstruct system intent, boundaries, stakeholders, scenarios, candidate requirements, architecture drivers, interfaces, evidence, and V&V seeds before PRD or formal systems-document generation.
adaptation_status: adapter_shell
source_repo: https://github.com/AngryOwlAI/ai-skills-for-sys
source_path: skills/system-definition-interview
---

# System Definition Interview

## Purpose

Use this local `sys-for-ai` adapter to establish or reconstruct the intent of a target agentic system before downstream PRD, SRD, architecture, implementation-plan, or formal systems-document generation.

The adapter produces a traceable `requirements-discovery-record.md` or chat-only equivalent with a `System Intent Profile`, candidate requirements, evidence, assumptions, risks, open questions, and downstream routing recommendations.

## When to use

Use this skill when an authorized AgentJob or System Director decision requires front-door system-definition elicitation for:

- a new target agentic system,
- an existing target system,
- a partially built target system,
- documentation recovery,
- unclear stakeholder intent,
- unclear boundary,
- unclear as-is/to-be state,
- missing operational scenarios,
- missing candidate requirements,
- missing architecture drivers,
- missing V&V seeds.

Do not use this adapter to generate final formal PRDs, SRDs, SyRS, SRS, ARDs, SEMPs, or V&V plans directly. Route to downstream skills or roles after the discovery record is coherent enough.

## Inputs

- Current authorized AgentJob or System Director decision.
- User prompt, stakeholder notes, interview transcript, source summary, or current project context.
- Relevant canonical sources from the source registry.
- Optional existing repository evidence for the target system.
- Optional project authority hierarchy, glossary, ADRs, standards, or PRDs.
- Optional output path. Default: `control_records/system_definition/requirements-discovery-record.md` when authorized.

## Outputs

- `requirements-discovery-record.md`, unless chat-only output is authorized.
- `System Intent Profile`.
- Traceable entries with stable IDs:
  - `NEED-*`
  - `STK-*`
  - `SCN-*`
  - `REQ-CAND-*`
  - `NFR-CAND-*`
  - `DRV-*`
  - `IF-*`
  - `VVE-*`
  - `OPEN-*`
- Assumptions, risks, and constraints.
- Source and provenance notes.
- Downstream routing recommendation.
- Completion receipt if required by the AgentJob.

## Procedure

1. Confirm the current AgentJob or Director decision authorizes this skill.
2. Identify the system-of-interest and whether the request is:
   - new system,
   - existing system,
   - partially built system,
   - documentation recovery.
3. Read canonical sources before generated derivatives.
4. Inspect available repository or documentation evidence before asking questions that local evidence can answer.
5. Ask one focused question at a time when the answer affects scope, boundary, requirement meaning, stakeholder priority, or downstream routing.
6. Use compact factual batches only for independent information that does not require deliberation.
7. Elicit mission need, problem statement, desired outcome, value case, and feasibility constraints.
8. Identify stakeholders, users, operators, maintainers, owners, affected parties, approvers, and downstream consumers.
9. Define system boundary, including included capabilities, excluded capabilities, external systems, inputs, outputs, interfaces, operating environment, and lifecycle responsibilities.
10. For existing or partially built systems, separate observed as-is behavior from desired to-be intent.
11. Build ConOps seeds from concrete operational scenarios.
12. Extract candidate functional requirements as `REQ-CAND-*`.
13. Extract quality attributes as `NFR-CAND-*`.
14. Extract architecture drivers, interface candidates, data flows, assumptions, constraints, risks, and dependency questions.
15. Seed verification and validation with `VVE-*` entries.
16. Write or update the discovery record using `templates/system_definition/requirements-discovery-record-template.md` unless the AgentJob specifies another template.
17. Route unresolved material:
    - `decision-grilling-context-45` for unresolved scope or design choices.
    - `domain-grilling-with-docs-context-45` for terminology, glossary, documentation, or ADR-worthy conflicts.
    - `conversation-to-prd` only when product requirements are ready to synthesize.
    - future SRD/SyRS/SRS/ARD/SEMP/V&V document skills only after system intent is coherent.

## Local authority boundaries

- This adapter does not override canonical PRDs, source registries, decision records, or validators.
- Discovery records are draft discovery evidence unless promoted by project authority.
- Candidate requirements are not baselined requirements.
- Generated notes, summaries, and templates are derivative unless explicitly promoted.
- Missing facts, thresholds, actors, owners, constraints, environments, evidence, or acceptance criteria must become open issues rather than silent inventions.

## Validation

Run:

```bash
cd sys-for-ai
make validate-skills
```

When a discovery record is produced and the optional validator exists, also run:

```bash
.venv/bin/python -m sys_for_ai.cli validate-discovery-record control_records/system_definition/requirements-discovery-record.md
```

## Known failure modes

- Using the skill without an authorized AgentJob or Director decision.
- Generating a PRD before system intent and boundary are stable.
- Treating candidate requirements as approved requirements.
- Asking a large questionnaire instead of focused, decision-relevant questions.
- Ignoring repository evidence that can answer a question.
- Mixing as-is observations with to-be intent.
- Losing traceability from stakeholder statements to candidate requirements and V&V seeds.

## Provenance

Adapted from `AngryOwlAI/ai-skills-for-sys/skills/system-definition-interview` as a local `sys-for-ai` adapter. Upstream template behavior is preserved where compatible with `sys-for-ai` source-first authority, AgentJob, registry, and validation rules.

## Adaptation work remaining

1. Compare this adapter against the current upstream template.
2. Replace any unresolved placeholders with local paths, commands, and authority rules.
3. Add project-specific validators.
4. Record validation evidence.
5. Mark as `adapted` only after a skill-import AgentJob and review receipt.
```

#### C.3 `system-definition-interview-context-45/SKILL.md` local adapter content

Recommended content:

```markdown
---
name: system-definition-interview-context-45
description: Long-session system-definition interview with a 45 percent context-used checkpoint and resumable temp_prd.md handoff.
adaptation_status: adapter_shell
source_repo: https://github.com/AngryOwlAI/ai-skills-for-sys
source_path: skills/system-definition-interview-context-45
required_skill: codex-usage-metrics
---

# System Definition Interview Context 45

## Purpose

Use this local `sys-for-ai` adapter for long system-definition interviews that may cross context limits. It follows the `system-definition-interview` workflow and adds a context checkpoint after each user answer.

When context used is at least 45 percent, context left is at most 55 percent, or metrics cannot be collected, write a resumable `temp_prd.md` and stop.

## Local path bindings

```text
<SKILLS_ROOT>       -> skills/core
<TARGET_SKILL_PATH> -> skills/core/system-definition-interview-context-45
<OUTPUT_DIRECTORY>  -> control_records/system_definition
```

Repository-root invocation should run from `sys-for-ai/` unless the AgentJob states another working directory.

## When to use

Use this adapter when:

- system definition requires a long stakeholder interview,
- the user explicitly invokes `/system-definition-interview-context-45`,
- a prior `temp_prd.md` should be resumed,
- context-aware continuation is more important than finishing in one session,
- the root agent expects a resumable handoff before context becomes risky.

Do not use this adapter for short clarifications that do not need continuation protection. Use `system-definition-interview` instead.

## Inputs

- Current authorized AgentJob or System Director decision.
- User prompt, stakeholder notes, transcript, source summary, or prior `temp_prd.md`.
- Optional repository or documentation evidence.
- Local `codex-usage-metrics` adapter.
- Optional metrics session file or Codex home path if required by the metrics adapter.

## Outputs

- `control_records/system_definition/requirements-discovery-record.md`, unless chat-only output is authorized.
- `skills/core/system-definition-interview-context-45/usage-metrics.txt` when metrics can be collected.
- `skills/core/system-definition-interview-context-45/temp_prd.md` when context threshold is reached or metrics are unavailable.
- Resume instruction:

```text
/system-definition-interview-context-45 temp_prd
```

## Procedure

1. Confirm the AgentJob authorizes this skill.
2. If invoked with `temp_prd`, read `skills/core/system-definition-interview-context-45/temp_prd.md` first.
3. If `temp_prd.md` is missing, state that no continuation file was found and proceed from the current prompt only if authorized.
4. Initialize or refresh working context:
   - objective,
   - situation classification,
   - System Intent Profile,
   - stakeholders,
   - boundary,
   - as-is state,
   - to-be state,
   - operational scenarios,
   - candidate requirements,
   - quality attributes,
   - architecture drivers,
   - interfaces,
   - V&V seeds,
   - evidence,
   - assumptions,
   - risks,
   - open questions,
   - last exchange,
   - recommended next branch.
5. Follow the local `system-definition-interview` procedure.
6. Ask one focused question at a time unless a compact factual batch is safe.
7. After each user answer, record the answer before checking metrics.
8. Run the context metrics checkpoint if the operational metrics policy is enabled:

```bash
python3 skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py \
  --output skills/core/system-definition-interview-context-45/usage-metrics.txt
```

9. Read `usage-metrics.txt` and inspect the context section.
10. Continue only when context left is known and greater than 55 percent.
11. If context left is 55 percent or lower, context used is 45 percent or higher, metrics are unavailable, or context left is unknown, write `temp_prd.md` and stop.
12. Tell the user or downstream agent:

```text
The discussion has been saved to temp_prd.md. Start a new discussion with /system-definition-interview-context-45 temp_prd so the system-definition interview can continue with the saved context.
```

13. Route downstream only after the discovery state is coherent enough.

## Fail-closed behavior

If the metrics script does not exist, fails, returns no context section, returns unknown context left, or cannot identify the current session, do not continue the interview. Write `temp_prd.md` using the best available state and stop.

## `temp_prd.md` required sections

```markdown
# Temp PRD - system-definition-interview-context-45

## Resume Command

/system-definition-interview-context-45 temp_prd

## Objective
## Situation Classification
## System Intent Profile
## Stakeholders And Roles
## System Boundary
## As-Is State
## To-Be State
## Operational Scenarios And ConOps Seeds
## Candidate Requirements
## Quality Attribute Candidates
## Architecture Drivers
## Interface Candidates
## Verification And Validation Seeds
## Evidence Register
## Assumptions, Risks, And Constraints
## Open Questions
## Last Exchange
### Last Question Asked
### User Answer
## Recommended Next Branch
## Metrics Snapshot
## Prior Temp PRD Integration
```

## Local authority boundaries

- `temp_prd.md` is resumable context, not final authority.
- Candidate requirements remain candidates.
- Metrics receipts are point-in-time evidence only.
- The adapter may write only paths authorized by the AgentJob.
- It must not export conversation content through the metrics script.

## Validation

Required:

```bash
cd sys-for-ai
make validate-skills
```

If metrics are operational:

```bash
.venv/bin/python skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py --help
```

If discovery-record validator exists:

```bash
.venv/bin/python -m sys_for_ai.cli validate-discovery-record control_records/system_definition/requirements-discovery-record.md
```

## Known failure modes

- Continuing the interview when metrics are unavailable.
- Checking metrics before the user answer is recorded.
- Overwriting `temp_prd.md` without integrating prior continuation context.
- Treating `temp_prd.md` as a final PRD.
- Creating final formal systems documents before intent and boundary are stable.
- Treating candidate requirements as approved.

## Provenance

Adapted from `AngryOwlAI/ai-skills-for-sys/skills/system-definition-interview-context-45` as a local `sys-for-ai` adapter. Upstream template behavior is preserved where compatible with `sys-for-ai` AgentJob, source-first authority, and validation rules.

## Adaptation work remaining

1. Confirm the local metrics policy.
2. Import/adapt the metrics script or document Phase 1 fail-closed behavior.
3. Add validation evidence for `--help` if operational.
4. Add or validate the `temp_prd.md` template.
5. Mark as `adapted` only after review and validation receipt.
```

#### C.4 `README.md` for both adapters

Minimum structure:

```markdown
# <Skill Name>

## Status

Adapter shell for the core `sys-for-ai` skill `<skill-id>`.

## Source

- Repository: `https://github.com/AngryOwlAI/ai-skills-for-sys`
- Path: `<source_path>`

## Purpose

<local purpose>

## Local authority

This adapter is governed by `sys-for-ai` AgentJobs, canonical PRDs, source registries, decision records, and validation commands.

## Adaptation work remaining

1. Compare this adapter shell with the current upstream template.
2. Replace generic placeholders with local paths, validators, and authority boundaries.
3. Update `skills/core_skill_manifest.yaml` and `registries/skill_registry.csv` if status changes.
4. Mark status as `adapted` only after review and validation evidence.
```

#### C.5 `AGENTS.md` for both adapters

Minimum structure:

```markdown
# Maintenance rules for `<skill-id>`

- Preserve provenance to `<source_path>`.
- Do not remove source-first authority boundaries.
- Do not mark this skill as `adapted` without a skill-import AgentJob and validation receipt.
- Keep examples portable and free of private project assumptions.
- Candidate requirements produced by this skill remain candidates until promoted.
- If the upstream template changes, record the review date and adaptation decision.
```

For the context-45 variant, add:

```markdown
- Do not remove fail-closed context behavior.
- Do not continue long interviews when metrics are unavailable or threshold is reached.
- Do not treat `temp_prd.md` as canonical authority.
```

#### C.6 Portable examples

Use upstream portable examples as source guidance, but fit them locally.

Example for `system-definition-interview/examples/portable-example.md`:

```markdown
# Portable example for `system-definition-interview`

## Scenario

A root AI agent receives an AgentJob to define a target agentic system for coordinating maintenance requests. Stakeholders know pain points but have not established boundary, scenarios, candidate requirements, or V&V seeds.

## Minimal use

1. Confirm AgentJob authorization.
2. Read canonical sources first.
3. Classify the situation as new, existing, partially built, or documentation recovery.
4. Ask one focused question about the success criterion.
5. Record the answer in a discovery record.
6. Extract `NEED-*`, `STK-*`, `SCN-*`, `REQ-CAND-*`, and `VVE-*` entries.
7. Route unresolved decisions to decision grilling.

## Example output shape

```text
Skill: system-definition-interview
Status: pass | repair | block
Discovery record: control_records/system_definition/requirements-discovery-record.md
Candidate IDs created:
- NEED-001
- STK-001
- SCN-001
- REQ-CAND-001
- VVE-001
Validation:
- make validate-skills
- validate-discovery-record, if available
```
```

Example for `system-definition-interview-context-45/examples/portable-example.md`:

```markdown
# Portable example for `system-definition-interview-context-45`

## Scenario

A system-definition interview spans multiple sessions. The agent captures user answers, checks context after each answer, and writes `temp_prd.md` when context used reaches 45 percent or metrics are unavailable.

## Minimal use

1. Confirm AgentJob authorization.
2. Resume from `temp_prd.md` if requested.
3. Ask one focused system-definition question.
4. Record the answer.
5. Run the metrics checkpoint.
6. Continue only if context left is known and greater than 55 percent.
7. Otherwise write `temp_prd.md` and stop.

## Example resume command

```text
/system-definition-interview-context-45 temp_prd
```
```

Validation after Epic C:

```bash
cd sys-for-ai
make validate-skills
```

Expected result:

- Passes if the four files exist in both adapter folders.
- May still not validate operational metrics behavior unless additional checks are added.

---

### Epic D: Operationalize or fail-close `codex-usage-metrics`

**Goal:** Make `system-definition-interview-context-45` real rather than ceremonial.

Two implementation policies are available.

#### D.1 Recommended operational policy

Import/adapt the upstream metrics script into:

```text
sys-for-ai/skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py
```

Also update:

```text
sys-for-ai/skills/core_skill_manifest.yaml
sys-for-ai/registries/skill_registry.csv
sys-for-ai/skills/core/codex-usage-metrics/SKILL.md
sys-for-ai/skills/core/codex-usage-metrics/README.md
sys-for-ai/skills/core/codex-usage-metrics/AGENTS.md
```

Add `scripts/collect_usage_metrics.py` to the `codex-usage-metrics` manifest entry:

```yaml
    required_files:
      - SKILL.md
      - README.md
      - AGENTS.md
      - examples/portable-example.md
      - scripts/collect_usage_metrics.py
    scripts:
      - scripts/collect_usage_metrics.py
```

Because the current validator only checks a fixed four-file set, do not add this to `SKILL_ADAPTER_REQUIRED_FILES` globally unless every adapter is expected to have a script. Instead add optional per-skill script validation.

##### D.1.1 Extend validator for optional `scripts`

In `validate_skill_manifest()`, after required file checks, add:

```python
        scripts = item.get("scripts", [])
        if scripts is None:
            scripts = []
        if not isinstance(scripts, list):
            messages.append(f"{target}: {skill_id} field 'scripts' must be a list when present")
        else:
            for rel_script in scripts:
                if not isinstance(rel_script, str) or not rel_script:
                    messages.append(f"{target}: {skill_id} has invalid script path entry: {rel_script!r}")
                    continue
                if not (adapter / rel_script).exists():
                    messages.append(f"{target}: {skill_id} missing declared script {rel_script}")
```

This keeps the four-file minimum but validates declared scripts when present.

##### D.1.2 Add `validate-metrics` CLI command

In `sys_for_ai/cli.py`, add:

```python
    validate_metrics = sub.add_parser("validate-metrics", help="Validate local Codex usage metrics script entry point")
    validate_metrics.add_argument("path", default="skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py", nargs="?")
```

Add implementation:

```python
    if args.command == "validate-metrics":
        script = Path(args.path)
        if not script.exists():
            return print_result(ValidationResult(False, [f"{script}: missing metrics script"]))
        return print_result(ValidationResult(True, [f"{script}: metrics script present; run --help for runtime validation"]))
```

Optional stronger runtime validation via `subprocess`:

```python
import subprocess


def validate_metrics_script(path: str | Path) -> ValidationResult:
    script = Path(path)
    if not script.exists():
        return ValidationResult(False, [f"{script}: missing metrics script"])
    proc = subprocess.run([sys.executable, str(script), "--help"], text=True, capture_output=True)
    messages = [proc.stdout.strip() or proc.stderr.strip() or f"{script}: --help produced no output"]
    return ValidationResult(proc.returncode == 0, messages)
```

Then wire it into `cli.py` and optionally `make validate`.

##### D.1.3 Update Makefile

Add:

```make
.PHONY: validate-metrics

validate-metrics:
	$(PYTHON) -m sys_for_ai.cli validate-metrics skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py
```

Optional:

```make
validate: doctor validate-agentjob validate-skills validate-metrics bootstrap-memory
```

Do this only if the metrics script is always expected to exist in Phase 1 after this patch.

##### D.1.4 Metrics acceptance criteria

The operational policy is accepted when:

```bash
cd sys-for-ai
make validate-skills
.venv/bin/python skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py --help
make validate
```

Expected:

- `--help` exits with code `0`.
- The script does not export conversation content.
- The context-45 adapter references the local metrics path.
- Metrics failure still triggers fail-closed handoff behavior.

#### D.2 Alternative fail-closed policy

If adapting the script is too much for the current patch, document in the context-45 adapter:

```text
Phase 1 adapter-shell policy: live metrics are not operational. When this skill is used and metrics cannot be collected, write temp_prd.md and stop.
```

This policy is safe but less useful. It should be treated as temporary.

Acceptance criteria for fail-closed policy:

- `system-definition-interview-context-45/SKILL.md` explicitly states metrics are unavailable in Phase 1 unless a future AgentJob adapts the script.
- The skill says to write `temp_prd.md` and stop when metrics are unavailable.
- `core_skill_manifest.yaml` records dependency on `codex-usage-metrics` even if not operational.
- An open issue is created for metrics operationalization.

Recommended open issue:

```text
OPEN-SKILL-METRICS-001: Adapt local codex-usage-metrics script so system-definition-interview-context-45 can make live continuation decisions instead of always failing closed.
```

---

### Epic E: Add system-definition output templates

**Goal:** Provide controlled local templates for the new skills’ outputs.

Create:

```text
sys-for-ai/templates/system_definition/requirements-discovery-record-template.md
sys-for-ai/templates/system_definition/temp-prd-template.md
```

#### E.1 `requirements-discovery-record-template.md`

Recommended template:

```markdown
# Requirements Discovery Record

**Record ID:** RDR-<YYYYMMDD>-<NNN>
**Status:** draft_discovery_evidence
**System name:** <system name>
**Prepared by role:** <role or agent>
**Authorized by AgentJob:** <AgentJob ID or Director decision ID>
**Source authority status:** derivative_draft
**Created:** <YYYY-MM-DD>
**Last updated:** <YYYY-MM-DD>

---

## 1. Authority Notice

This record is a discovery artifact. It captures stakeholder statements, evidence, assumptions, candidate requirements, risks, and open questions. It is not a canonical requirements baseline unless promoted by the project source-authority process.

Canonical PRDs, source registries, decision records, approved requirements, and control records outrank this document.

---

## 2. System Intent Profile

| Field | Value | Source | Evidence status |
|---|---|---|---|
| Mission need | <text> | <source> | stated / inferred / missing |
| Problem statement | <text> | <source> | stated / inferred / missing |
| Desired outcome | <text> | <source> | stated / inferred / missing |
| Value case | <text> | <source> | stated / inferred / missing |
| System-of-interest | <text> | <source> | stated / inferred / missing |
| System type | new / existing / partially built / documentation recovery | <source> | stated / inferred |
| Success criteria | <text> | <source> | stated / inferred / missing |
| Primary constraints | <text> | <source> | stated / inferred / missing |

---

## 3. Stakeholders And Roles

| ID | Stakeholder class | Role in system | Primary need | Decision authority | Source | Evidence status |
|---|---|---|---|---|---|---|
| STK-001 | <class> | <role> | <need> | <yes/no/unknown> | <source> | stated / inferred / missing |

---

## 4. System Boundary

### 4.1 In scope

| ID | Capability / responsibility | Source | Evidence status |
|---|---|---|---|
| BND-IN-001 | <text> | <source> | stated / inferred |

### 4.2 Out of scope

| ID | Exclusion | Rationale | Source | Evidence status |
|---|---|---|---|---|
| BND-OUT-001 | <text> | <why excluded> | <source> | stated / inferred |

### 4.3 External systems and interfaces

| ID | External system / actor | Relationship | Input/output | Owner | Source | Open issues |
|---|---|---|---|---|---|---|
| EXT-001 | <name> | <relationship> | <I/O> | <owner> | <source> | <OPEN-*> |

---

## 5. As-Is State

| ID | Observation | Source | Evidence type | Confidence | Notes |
|---|---|---|---|---|---|
| ASIS-001 | <text> | <source> | observed / stated / inferred | high / medium / low | <notes> |

---

## 6. To-Be State

| ID | Desired future behavior | Source | Evidence status | Related need |
|---|---|---|---|---|
| TOBE-001 | <text> | <source> | stated / inferred | NEED-001 |

---

## 7. Operational Scenarios And ConOps Seeds

| ID | Scenario | Actors | Trigger | Normal flow | Exception/degraded flow | Related needs | Evidence |
|---|---|---|---|---|---|---|---|
| SCN-001 | <name> | <actors> | <trigger> | <flow> | <exceptions> | NEED-001 | <source> |

---

## 8. Candidate Requirements

### 8.1 Candidate functional requirements

| ID | Candidate requirement | Source need/scenario | Rationale | Priority | Verification seed | Status |
|---|---|---|---|---|---|---|
| REQ-CAND-001 | The system should <candidate behavior>. | NEED-001 / SCN-001 | <why> | Must / Should / Could / Later / unknown | VVE-001 | candidate |

### 8.2 Candidate quality attributes

| ID | Quality attribute | Candidate statement | Source | Threshold / measure | Verification seed | Status |
|---|---|---|---|---|---|---|
| NFR-CAND-001 | <attribute> | <candidate statement> | <source> | <measure or OPEN-*> | VVE-002 | candidate |

---

## 9. Architecture Drivers

| ID | Driver | Type | Source | Why it matters | Related candidates | Open issues |
|---|---|---|---|---|---|---|
| DRV-001 | <driver> | quality / interface / data / safety / security / operations / constraint | <source> | <rationale> | REQ-CAND-001 | OPEN-001 |

---

## 10. Interface Candidates

| ID | Interface candidate | Producer | Consumer | Data / command / event | Frequency | Owner | Related scenario | Open issues |
|---|---|---|---|---|---|---|---|---|
| IF-001 | <interface> | <producer> | <consumer> | <payload> | <frequency> | <owner> | SCN-001 | OPEN-002 |

---

## 11. Verification And Validation Seeds

| ID | Candidate evidence or check | Traces to | Method | Owner/gate | Acceptance idea | Status |
|---|---|---|---|---|---|---|
| VVE-001 | <evidence/check> | REQ-CAND-001 | inspection / analysis / demonstration / test / review | <owner> | <acceptance idea> | seed |

---

## 12. Evidence Register

| ID | Source | Source type | Authority class | Used for | Notes |
|---|---|---|---|---|---|
| EVD-001 | <path, statement, interview note, source ID> | user statement / repo file / PRD / ADR / test / diagram | canonical / controlled / derivative / external / unavailable | <IDs> | <notes> |

---

## 13. Assumptions, Risks, And Constraints

### 13.1 Assumptions

| ID | Assumption | Source | Risk if wrong | Owner | Status |
|---|---|---|---|---|---|
| ASM-001 | <text> | <source> | <risk> | <owner> | open / accepted / rejected |

### 13.2 Risks

| ID | Risk | Cause | Impact | Likelihood | Mitigation | Owner | Related IDs |
|---|---|---|---|---|---|---|---|
| RISK-001 | <risk> | <cause> | <impact> | high / medium / low | <mitigation> | <owner> | <IDs> |

### 13.3 Constraints

| ID | Constraint | Source | Binding status | Related IDs | Open issues |
|---|---|---|---|---|---|
| CON-001 | <constraint> | <source> | binding / candidate / unknown | <IDs> | <OPEN-*> |

---

## 14. Open Questions

| ID | Question | Why it matters | Owner | Blocks | Recommended next route | Status |
|---|---|---|---|---|---|---|
| OPEN-001 | <question> | <impact> | <owner> | <IDs> | decision-grilling / domain-grilling / stakeholder answer / source inspection | open |

---

## 15. Downstream Routing Recommendation

| Route | Use when | Current recommendation | Blocking open issues |
|---|---|---|---|
| decision-grilling-context-45 | scope or design decision unclear | yes / no / later | OPEN-* |
| domain-grilling-with-docs-context-45 | terminology or documentation conflict | yes / no / later | OPEN-* |
| conversation-to-prd | product requirements ready to synthesize | yes / no / later | OPEN-* |
| SRD/SyRS generation | system requirements ready to baseline | yes / no / later | OPEN-* |
| architecture requirements | requirements stable enough for architecture | yes / no / later | OPEN-* |

---

## 16. Completion Evidence

| Evidence item | Value |
|---|---|
| AgentJob ID | <ID> |
| Sources inspected | <list> |
| Questions asked | <count/list> |
| Candidate requirements created | <count/list> |
| Open issues created | <count/list> |
| Validators run | <commands> |
| Validation status | pass / repair / block |
| Next recommended role | <role/skill> |
```

#### E.2 `temp-prd-template.md`

Recommended template:

```markdown
# Temp PRD - system-definition-interview-context-45

## Resume Command

/system-definition-interview-context-45 temp_prd

## Authority Notice

This file is resumable context for the `system-definition-interview-context-45` adapter. It is not a canonical PRD and does not baseline requirements. Candidate requirements remain candidates until promoted by project authority.

## Objective

## Situation Classification

## System Intent Profile

## Stakeholders And Roles

## System Boundary

## As-Is State

## To-Be State

## Operational Scenarios And ConOps Seeds

## Candidate Requirements

## Quality Attribute Candidates

## Architecture Drivers

## Interface Candidates

## Verification And Validation Seeds

## Evidence Register

## Assumptions, Risks, And Constraints

## Open Questions

## Last Exchange

### Last Question Asked

### User Answer

## Recommended Next Branch

## Metrics Snapshot

## Prior Temp PRD Integration

## Completion / Handoff Notes
```

#### E.3 Add `control_records/system_definition/README.md`

Recommended content:

```markdown
# System Definition Control Records

This directory stores authorized system-definition discovery records and related controlled handoff artifacts produced by local `sys-for-ai` skills.

Files here are not automatically canonical requirements. Unless a file explicitly says otherwise and appears in the source registry as canonical or controlled authority, records in this directory are draft discovery evidence.

Expected artifacts:

- `requirements-discovery-record.md`
- skill completion receipts
- reviewed handoff notes
- promoted source-authority records, when approved

Do not store unreviewed chat transcripts, secrets, credentials, or private session exports here.
```

#### E.4 Optional discovery record schema

Create:

```text
sys-for-ai/schemas/discovery_record.schema.yaml
```

Example:

```yaml
schema_id: SFA-SCHEMA-DISCOVERY-RECORD-001
schema_kind: schema_like_markdown_contract
status: draft
purpose: Define required sections for requirements discovery records created by system-definition skills.
required_sections:
  - Authority Notice
  - System Intent Profile
  - Stakeholders And Roles
  - System Boundary
  - Operational Scenarios And ConOps Seeds
  - Candidate Requirements
  - Architecture Drivers
  - Interface Candidates
  - Verification And Validation Seeds
  - Evidence Register
  - Assumptions, Risks, And Constraints
  - Open Questions
  - Downstream Routing Recommendation
  - Completion Evidence
id_prefixes:
  needs: NEED-
  stakeholders: STK-
  scenarios: SCN-
  functional_candidates: REQ-CAND-
  quality_candidates: NFR-CAND-
  drivers: DRV-
  interfaces: IF-
  verification_validation: VVE-
  open_questions: OPEN-
authority_policy:
  default_status: draft_discovery_evidence
  candidate_requirements_not_baselined: true
  source_first_required: true
```

---

### Epic F: Add optional discovery-record validator

**Goal:** Catch missing sections and accidental authority inversion.

This is optional for the minimum patch but strongly recommended.

Create:

```text
sys-for-ai/sys_for_ai/discovery.py
```

Implementation sketch:

```python
"""Discovery record validation helpers."""

from __future__ import annotations

from pathlib import Path

from .validators import ValidationResult


REQUIRED_DISCOVERY_SECTIONS = [
    "Authority Notice",
    "System Intent Profile",
    "Stakeholders And Roles",
    "System Boundary",
    "Operational Scenarios And ConOps Seeds",
    "Candidate Requirements",
    "Architecture Drivers",
    "Interface Candidates",
    "Verification And Validation Seeds",
    "Evidence Register",
    "Assumptions, Risks, And Constraints",
    "Open Questions",
    "Downstream Routing Recommendation",
    "Completion Evidence",
]

FORBIDDEN_AUTHORITY_PHRASES = [
    "canonical requirements baseline",
    "approved requirements baseline",
    "baselined requirement",
]


def validate_discovery_record(path: str | Path) -> ValidationResult:
    target = Path(path)
    messages: list[str] = []
    if not target.exists():
        return ValidationResult(False, [f"{target}: missing discovery record"])

    text = target.read_text(encoding="utf-8")
    for section in REQUIRED_DISCOVERY_SECTIONS:
        if f"## {section}" not in text and f"# {section}" not in text:
            messages.append(f"{target}: missing required section {section!r}")

    if "REQ-CAND-" not in text and "NFR-CAND-" not in text:
        messages.append(f"{target}: no candidate requirement IDs found; record may be incomplete")

    if "Authority Notice" in text:
        lower = text.lower()
        if "not a canonical requirements baseline" not in lower and "draft discovery" not in lower:
            messages.append(f"{target}: authority notice does not clearly mark discovery status")

    # Soft warning pattern, not a perfect NLP check.
    for phrase in FORBIDDEN_AUTHORITY_PHRASES:
        if phrase in text.lower() and "not a canonical requirements baseline" not in text.lower():
            messages.append(f"{target}: possible authority inversion phrase found: {phrase!r}")

    return ValidationResult(not messages, messages or [f"{target}: discovery record validation passed"])
```

Update `cli.py`:

```python
from .discovery import validate_discovery_record
```

Parser:

```python
validate_discovery = sub.add_parser("validate-discovery-record", help="Validate a requirements discovery record")
validate_discovery.add_argument("path")
```

Command handling:

```python
    if args.command == "validate-discovery-record":
        return print_result(validate_discovery_record(args.path))
```

Update Makefile:

```make
.PHONY: validate-discovery-template

validate-discovery-template:
	$(PYTHON) -m sys_for_ai.cli validate-discovery-record templates/system_definition/requirements-discovery-record-template.md
```

Do not add this to `make validate` unless the template is designed to pass despite placeholders. A template may need a separate template-contract validator rather than the live-record validator.

---

### Epic G: Update source-first registries

**Goal:** Preserve provenance and authority boundaries.

#### G.1 Update `source_registry.csv`

Add source rows for new controlled project files that should be canonical or controlled.

Recommended rows:

```csv
SRC-SKILL-MANIFEST,sys-for-ai/skills/core_skill_manifest.yaml,skill_manifest,controlled,skill_governance,2026-07-05,Core local skill manifest for sys-for-ai adapters.
SRC-SKILL-VALIDATORS,sys-for-ai/sys_for_ai/validators.py,validator,controlled,validation_engineering,2026-07-05,Validator enforcing core AgentJob skill and registry scaffold expectations.
SRC-SKILL-REGISTRY,sys-for-ai/registries/skill_registry.csv,registry,controlled,skill_governance,2026-07-05,Skill provenance and adaptation-status registry.
SRC-TEMPLATE-RDR,sys-for-ai/templates/system_definition/requirements-discovery-record-template.md,template,controlled,system_definition,2026-07-05,Controlled template for requirements discovery records.
SRC-TEMPLATE-TEMP-PRD,sys-for-ai/templates/system_definition/temp-prd-template.md,template,controlled,system_definition,2026-07-05,Controlled resumable handoff template for context-45 system-definition interviews.
```

If the project treats source registry paths as relative to `sys-for-ai/`, use paths without the leading `sys-for-ai/`. Preserve current convention. The current registry contains top-level PRD paths, so be consistent with the existing registry owner’s expectation.

#### G.2 Update `derivative_registry.csv`

If generated discovery record examples or local documentation summaries are created, add derivative rows.

Example:

```csv
DER-SYS-DOC-SPINE,sys-for-ai/docs/system_document_spine.md,documentation_derivative,"SRC-PRD-P0;SRC-PRD-P1;SRC-TEMPLATE-RDR",manual_synthesis,2026-07-05,draft,Explains practical system-document spine and PRD boundary.
```

Only use derivative registry if the file is derivative. If a new policy document is declared controlled authority, put it in the source registry instead.

#### G.3 Update `object_relationship_registry.csv`

Add relationships such as:

```csv
REL-SKILL-001,system-definition-interview,precedes,conversation-to-prd,sys-for-ai/skills/core_skill_manifest.yaml,System definition discovery precedes PRD synthesis when intent or boundary is unclear.
REL-SKILL-002,system-definition-interview-context-45,requires,codex-usage-metrics,sys-for-ai/skills/core_skill_manifest.yaml,Context-45 workflow requires metrics or fail-closed handoff behavior.
REL-SKILL-003,requirements-discovery-record-template.md,produced_by,system-definition-interview,sys-for-ai/templates/system_definition/requirements-discovery-record-template.md,Discovery template supports front-door system-definition skills.
```

Validation:

```bash
cd sys-for-ai
make bootstrap-memory
make validate
```

---

### Epic H: Add AgentJob control records

**Goal:** Make the integration executable by AI agents using bounded work packets.

Create:

```text
sys-for-ai/control_records/agentjobs/AJ-P1-SKILL-SYNC-001.yaml
sys-for-ai/control_records/agentjobs/AJ-P1-CODEX-METRICS-ADAPT-001.yaml
sys-for-ai/control_records/agentjobs/AJ-P1-SYSTEM-DEFINITION-TEMPLATE-001.yaml
```

#### H.1 `AJ-P1-SKILL-SYNC-001.yaml`

```yaml
agentjob_id: AJ-P1-SKILL-SYNC-001
objective: Integrate the current system-definition skills from ai-skills-for-sys into the sys-for-ai core skill manifest, validator expectations, local adapter folders, and skill registry.
role: skill_integration_agent
allowed_reads:
  - PRDs/sys-for-ai_phase-0_product_system_design_prd.md
  - PRDs/sys-for-ai_phase-1_implementation_initialization_prd.md
  - sys-for-ai/skills/core_skill_manifest.yaml
  - sys-for-ai/sys_for_ai/validators.py
  - sys-for-ai/registries/skill_registry.csv
  - sys-for-ai/skills/core/**
  - sys-for-ai/schemas/skill.schema.yaml
  - https://github.com/AngryOwlAI/ai-skills-for-sys/tree/main/skills/system-definition-interview
  - https://github.com/AngryOwlAI/ai-skills-for-sys/tree/main/skills/system-definition-interview-context-45
allowed_writes:
  - sys-for-ai/skills/core_skill_manifest.yaml
  - sys-for-ai/sys_for_ai/validators.py
  - sys-for-ai/registries/skill_registry.csv
  - sys-for-ai/registries/source_registry.csv
  - sys-for-ai/registries/object_relationship_registry.csv
  - sys-for-ai/schemas/skill.schema.yaml
  - sys-for-ai/skills/core/system-definition-interview/**
  - sys-for-ai/skills/core/system-definition-interview-context-45/**
  - sys-for-ai/.local/receipts/AJ-P1-SKILL-SYNC-001*.txt
forbidden_actions:
  - Delete existing skill adapters.
  - Mark adapter_status as adapted without review and validation evidence.
  - Treat upstream templates as opaque external authority.
  - Promote discovery records to canonical requirements.
  - Modify Phase 0 product identity or Phase 1 phase boundary.
required_inputs:
  - Current ai-skills-for-sys retained systems-engineering skillset.
  - Current sys-for-ai core skill manifest and validator.
expected_outputs:
  - Updated core_skill_manifest.yaml including system-definition-interview and system-definition-interview-context-45.
  - Updated validators.py required skill set.
  - Updated skill_registry.csv rows.
  - New adapter shell folders with SKILL.md, README.md, AGENTS.md, and examples/portable-example.md.
  - Registry updates preserving provenance.
validators:
  - cd sys-for-ai && make validate-skills
  - cd sys-for-ai && make validate
completion_evidence:
  - Validation receipt path.
  - List of changed files.
  - Any skipped validator with reason.
stop_conditions:
  - Existing local adapter folder would be overwritten without review.
  - Upstream skill source cannot be inspected.
  - Validator failure cannot be explained by an expected intermediate state.
```

#### H.2 `AJ-P1-CODEX-METRICS-ADAPT-001.yaml`

```yaml
agentjob_id: AJ-P1-CODEX-METRICS-ADAPT-001
objective: Adapt the codex-usage-metrics script into the local sys-for-ai core adapter so context-45 skills can make operational continuation decisions or fail closed with evidence.
role: skill_dependency_adaptation_agent
allowed_reads:
  - sys-for-ai/skills/core/codex-usage-metrics/**
  - sys-for-ai/skills/core/system-definition-interview-context-45/**
  - sys-for-ai/skills/core_skill_manifest.yaml
  - sys-for-ai/sys_for_ai/validators.py
  - sys-for-ai/sys_for_ai/cli.py
  - https://github.com/AngryOwlAI/ai-skills-for-sys/tree/main/skills/codex-usage-metrics
allowed_writes:
  - sys-for-ai/skills/core/codex-usage-metrics/**
  - sys-for-ai/skills/core_skill_manifest.yaml
  - sys-for-ai/sys_for_ai/validators.py
  - sys-for-ai/sys_for_ai/cli.py
  - sys-for-ai/Makefile
  - sys-for-ai/registries/skill_registry.csv
  - sys-for-ai/registries/source_registry.csv
  - sys-for-ai/.local/receipts/AJ-P1-CODEX-METRICS-ADAPT-001*.txt
forbidden_actions:
  - Export chat messages, secrets, tool arguments, reasoning content, or full session logs.
  - Require heavy dependencies for Phase 1.
  - Break make validate for users without live Codex session files.
required_inputs:
  - Local codex-usage-metrics adapter shell.
  - Upstream metrics script and documentation.
expected_outputs:
  - Local scripts/collect_usage_metrics.py or explicit fail-closed policy.
  - Updated adapter docs.
  - Optional validate-metrics CLI command.
  - Validation receipt for --help or documented reason metrics are fail-closed.
validators:
  - cd sys-for-ai && make validate-skills
  - cd sys-for-ai && .venv/bin/python skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py --help
  - cd sys-for-ai && make validate
completion_evidence:
  - Metrics policy decision.
  - Command output from --help, if operational.
  - Updated context-45 adapter behavior.
stop_conditions:
  - Metrics script requires unavailable secrets or private session content.
  - Script cannot be adapted without violating source-first or privacy constraints.
```

#### H.3 `AJ-P1-SYSTEM-DEFINITION-TEMPLATE-001.yaml`

```yaml
agentjob_id: AJ-P1-SYSTEM-DEFINITION-TEMPLATE-001
objective: Add controlled templates and optional validation for requirements discovery records and context-45 temp_prd handoffs.
role: system_definition_template_agent
allowed_reads:
  - PRDs/sys-for-ai_phase-0_product_system_design_prd.md
  - PRDs/sys-for-ai_phase-1_implementation_initialization_prd.md
  - sys-for-ai/skills/core/system-definition-interview/**
  - sys-for-ai/skills/core/system-definition-interview-context-45/**
  - sys-for-ai/schemas/skill.schema.yaml
allowed_writes:
  - sys-for-ai/templates/system_definition/**
  - sys-for-ai/control_records/system_definition/**
  - sys-for-ai/schemas/discovery_record.schema.yaml
  - sys-for-ai/sys_for_ai/discovery.py
  - sys-for-ai/sys_for_ai/cli.py
  - sys-for-ai/Makefile
  - sys-for-ai/registries/source_registry.csv
  - sys-for-ai/registries/derivative_registry.csv
  - sys-for-ai/registries/object_relationship_registry.csv
  - sys-for-ai/.local/receipts/AJ-P1-SYSTEM-DEFINITION-TEMPLATE-001*.txt
forbidden_actions:
  - Treat discovery records as canonical requirements.
  - Generate formal PRD/SRD/Architecture documents as part of template creation.
  - Add heavyweight dependencies.
required_inputs:
  - Local system-definition skill adapters.
  - Existing source-first authority policy.
expected_outputs:
  - requirements-discovery-record-template.md
  - temp-prd-template.md
  - Optional discovery record schema and validator.
  - Registry entries.
validators:
  - cd sys-for-ai && make validate
  - cd sys-for-ai && .venv/bin/python -m sys_for_ai.cli validate-discovery-record <example-or-template-path>
completion_evidence:
  - Changed file list.
  - Validator output.
  - Registry updates.
stop_conditions:
  - Template conflicts with source-first authority rules.
  - Validator cannot distinguish template placeholders from missing live record fields.
```

---

### Epic I: Add documentation spine and PRD boundary policy

**Goal:** Prevent future PRD overloading and align `sys-for-ai` with systems-program documentation needs.

Create:

```text
sys-for-ai/docs/system_document_spine.md
```

Recommended content outline:

```markdown
# System Document Spine

## Purpose

Define the document chain used by `sys-for-ai` when designing, developing, running, improving, and maintaining target agentic systems.

## PRD acronym rule

Always expand PRD on first use. In this repository, `PRD` usually means Product Requirements Document unless a document explicitly says Project Requirements Document. A PRD is not the only requirements source for complex systems.

## Practical document chain

Mission Need / Business Case
→ Program or Project Charter
→ System Definition Discovery Record
→ ConOps
→ Stakeholder Requirements
→ Product Requirements Document or Business Requirements Document, when product-facing
→ SRD / SyRS
→ SRS for software-specific obligations
→ Architecture Description / ARD
→ ICDs / interface specifications
→ SEMP and technical management plans
→ RTM / RVM
→ V&V Plan and Test Plan
→ Deployment / Operations / Maintenance Plan
→ Closeout / Lessons Learned

## Phase 1 immediate scope

Phase 1 does not create every formal document. It creates:

- skill adapters,
- discovery templates,
- validators,
- registries,
- AgentJobs,
- source-first authority rules.

## Authority rules

- Discovery records are draft evidence until promoted.
- PRDs define product intent and phase boundary.
- SRD/SyRS define system obligations.
- SRS defines software obligations.
- Architecture documents explain solution structure and tradeoffs.
- V&V artifacts define evidence.
- Operations and maintenance artifacts define sustainment obligations.
```

Update `sys-for-ai/README.md` to point to:

```text
docs/system_document_spine.md
```

Potential README addition:

```markdown
## System-document spine

`sys-for-ai` does not treat PRDs as the only systems-engineering source. See `docs/system_document_spine.md` for the recommended chain from mission need and system definition through requirements, architecture, V&V, operations, and closeout.
```

---

### Epic J: Update skill routing and operating sequence

**Goal:** Make the new system-definition skills the front door when intent is unclear.

Add or update:

```text
sys-for-ai/docs/skill_integration_policy.md
```

Recommended routing policy:

```markdown
# Skill Integration Policy

## Core routing sequence

When the target system intent, boundary, stakeholders, operational scenarios, candidate requirements, architecture drivers, or V&V seeds are unclear, use:

1. `system-definition-interview` or `system-definition-interview-context-45`
2. `decision-grilling` or `decision-grilling-context-45`
3. `domain-grilling-with-docs` or `domain-grilling-with-docs-context-45`
4. `conversation-to-prd`
5. `prd-to-implementation-plan`

## Long-session rule

Use `*-context-45` variants when the interview or clarification may cross context limits.

## Context-45 rule

After every user answer:

1. record the answer,
2. run metrics if operational,
3. continue only when context left is known and greater than 55 percent,
4. otherwise write `temp_prd.md` and stop.

## Authority rule

No skill output overrides canonical sources, registries, PRDs, decision records, validators, or AgentJobs.
```

Update `sys-for-ai/README.md` useful commands if new validators exist:

```markdown
make validate-metrics
# optional
.venv/bin/python -m sys_for_ai.cli validate-discovery-record <path>
```

---

### Epic K: Validation strategy

**Goal:** Ensure integration is repeatable, deterministic, and catches drift.

#### K.1 Required validation gates

Gate 1, baseline:

```bash
cd sys-for-ai
make doctor
make validate
```

Gate 2, validator detects missing adapters after manifest update:

```bash
cd sys-for-ai
make validate-skills
```

Expected intermediate failure until adapters are created.

Gate 3, adapter surfaces exist:

```bash
cd sys-for-ai
make validate-skills
```

Expected pass.

Gate 4, full Phase 1 scaffold:

```bash
cd sys-for-ai
make validate
```

Expected pass.

Gate 5, metrics dependency if operational:

```bash
cd sys-for-ai
.venv/bin/python skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py --help
```

Expected pass.

Gate 6, discovery record validator if implemented:

```bash
cd sys-for-ai
.venv/bin/python -m sys_for_ai.cli validate-discovery-record control_records/system_definition/requirements-discovery-record.md
```

Expected pass on a complete example record, not necessarily on a placeholder template unless validator supports template mode.

#### K.2 Recommended validator improvements

1. Detect duplicate `local_path` values.
2. Validate `required_skills` references exist in the manifest.
3. Validate declared `scripts` paths exist relative to adapter root.
4. Validate `source_path` is nonempty.
5. Validate `adaptation_status` is one of:
   - `adapter_shell`
   - `imported_unadapted`
   - `adapted`
   - `deprecated`
6. Validate `skill_registry.csv` and `core_skill_manifest.yaml` agree.

#### K.3 Skill registry agreement check

Add a future helper:

```python
validate_skill_registry_agreement(manifest_path, registry_path)
```

Rules:

- every manifest skill appears in `skill_registry.csv`,
- every registry skill appears in manifest unless marked deprecated or external,
- `local_path`, `source_repo`, `source_path`, `family`, and `adaptation_status` agree,
- no duplicate IDs.

Add CLI:

```bash
.venv/bin/python -m sys_for_ai.cli validate-skill-registry skills/core_skill_manifest.yaml registries/skill_registry.csv
```

Do not block the current integration on this unless time permits.

---

## 5. Implementation Sequence

### Phase 0: Branch and baseline

1. Create branch:

```bash
git checkout -b feature/system-definition-skill-integration
```

2. Run baseline:

```bash
cd sys-for-ai
make doctor
make validate
```

3. Record results.

### Phase 1: Make validator and manifest see the missing skills

1. Edit `validators.py` required set.
2. Edit `core_skill_manifest.yaml`.
3. Edit `skill.schema.yaml` recommended fields.
4. Edit `skill_registry.csv`.
5. Run `make validate-skills` and confirm it fails because adapter folders are missing.
6. Record this as expected intermediate evidence.

### Phase 2: Add adapter folders

1. Create `system-definition-interview` adapter files.
2. Create `system-definition-interview-context-45` adapter files.
3. Run `make validate-skills`.
4. Fix any missing required files.
5. Run `make validate`.

### Phase 3: Metrics dependency

Recommended:

1. Add `scripts/collect_usage_metrics.py` to `codex-usage-metrics`.
2. Update codex adapter docs.
3. Add per-skill `scripts` validation.
4. Add optional `validate-metrics` CLI command.
5. Run `--help` validation.
6. Run `make validate`.

Alternative:

1. Document fail-closed policy in context-45 adapter.
2. Add open issue for operational metrics.
3. Run `make validate`.

### Phase 4: Templates and optional validator

1. Add `templates/system_definition/requirements-discovery-record-template.md`.
2. Add `templates/system_definition/temp-prd-template.md`.
3. Add `control_records/system_definition/README.md`.
4. Optional: add `schemas/discovery_record.schema.yaml`.
5. Optional: add `sys_for_ai/discovery.py` and CLI command.
6. Run validators.

### Phase 5: AgentJobs

1. Add skill sync AgentJob.
2. Add metrics adaptation AgentJob.
3. Add template AgentJob.
4. Validate AgentJobs individually:

```bash
cd sys-for-ai
.venv/bin/python -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-SKILL-SYNC-001.yaml
.venv/bin/python -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-CODEX-METRICS-ADAPT-001.yaml
.venv/bin/python -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-SYSTEM-DEFINITION-TEMPLATE-001.yaml
```

5. Optionally update `make validate-agentjobs` to validate all AgentJobs.

### Phase 6: Documentation spine and policy

1. Add `docs/system_document_spine.md`.
2. Add or update `docs/skill_integration_policy.md`.
3. Update `README.md` links.
4. Update registries.
5. Run `make validate`.

### Phase 7: Final review and acceptance

1. Run full validation:

```bash
cd sys-for-ai
make doctor
make validate-skills
make validate-agentjob
make bootstrap-memory
make validate
```

2. Run any added validators.
3. Produce final implementation receipt.
4. Review diff.
5. Confirm no generated derivatives were promoted silently.
6. Commit.

---

## 6. Exact Acceptance Criteria

The implementation is complete when all of the following are true.

### 6.1 Skill universe acceptance

- `core_skill_manifest.yaml` includes `system-definition-interview`.
- `core_skill_manifest.yaml` includes `system-definition-interview-context-45`.
- `validators.py` requires both IDs.
- `skill_registry.csv` includes both rows.
- `make validate-skills` fails if either adapter folder is missing.
- `make validate-skills` passes when both adapter folders contain all required files.

### 6.2 Adapter acceptance

Each new adapter folder contains:

- `SKILL.md`
- `README.md`
- `AGENTS.md`
- `examples/portable-example.md`

Each adapter:

- preserves upstream provenance,
- says `adaptation_status: adapter_shell` initially,
- binds behavior to AgentJob authorization,
- preserves source-first authority,
- keeps candidate requirements as candidates,
- states validation commands,
- lists known failure modes.

### 6.3 Context-45 acceptance

`system-definition-interview-context-45`:

- requires or references `codex-usage-metrics`,
- records answer before metrics check,
- continues only when context left is known and greater than 55 percent,
- writes `temp_prd.md` when context used is 45 percent or more, context left is 55 percent or less, or metrics are unavailable,
- provides resume command:

```text
/system-definition-interview-context-45 temp_prd
```

### 6.4 Metrics acceptance

If operational policy is chosen:

- `collect_usage_metrics.py` exists locally.
- The codex adapter manifest declares the script.
- `--help` exits with status `0`.
- The script does not export conversation content.
- `make validate` passes.

If fail-closed policy is chosen:

- Context-45 adapter explicitly states metrics are unavailable in Phase 1.
- Context-45 writes `temp_prd.md` and stops when metrics are unavailable.
- An open issue exists for operational metrics adaptation.

### 6.5 Template acceptance

- `requirements-discovery-record-template.md` exists.
- `temp-prd-template.md` exists.
- Templates include authority notices.
- Templates separate stakeholder statements, evidence, assumptions, candidates, risks, and open questions.
- Templates include stable ID conventions.
- Templates do not imply canonical baseline status.

### 6.6 AgentJob acceptance

- At least one AgentJob authorizes skill integration.
- AgentJobs include objective, role, allowed reads, allowed writes, forbidden actions, expected outputs, validators, and stop conditions.
- New AgentJobs pass `validate-agentjob`.

### 6.7 System-document spine acceptance

- Documentation states PRD acronym expansion rule.
- Documentation says PRD is not the only system requirements source.
- Documentation defines the practical chain from mission need through V&V and operations.
- README points to the spine.

### 6.8 Final validation acceptance

All applicable commands pass:

```bash
cd sys-for-ai
make doctor
make validate-skills
make validate-agentjob
make bootstrap-memory
make validate
```

Plus, if operational metrics are implemented:

```bash
.venv/bin/python skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py --help
```

---

## 7. Risk Register

| ID | Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---:|---:|---|---|
| RISK-SKILL-001 | Validator remains hard-coded and drifts again. | High | High | Add expected-skill baseline or derive from registry in future AgentJob. | validation_engineering |
| RISK-SKILL-002 | Adapter shells are mistaken for fully adapted runtime skills. | Medium | Medium | Keep `adaptation_status: adapter_shell`; require validation receipt before `adapted`. | skill_governance |
| RISK-SKILL-003 | Context-45 continues without metrics. | High | Medium | Fail closed and write `temp_prd.md` when metrics unavailable. | control_loop_planner |
| RISK-SKILL-004 | `temp_prd.md` is mistaken for canonical PRD. | High | Medium | Add authority notice and registry policy. | documentation_librarian |
| RISK-SKILL-005 | Discovery record silently baselines candidate requirements. | High | Medium | Use `REQ-CAND-*`, `NFR-CAND-*`, authority notice, and optional validator. | requirements_verifier |
| RISK-SKILL-006 | Metrics script leaks conversation content. | High | Low/Medium | Preserve no-content-export rule; validate only metrics events; document privacy boundaries. | privacy_security_reviewer |
| RISK-SKILL-007 | Additional validators overfit templates and fail on placeholders. | Medium | Medium | Separate live-record validation from template-contract validation. | validation_engineering |
| RISK-SKILL-008 | PRD continues to absorb system-program documents. | Medium | High | Add document spine and PRD acronym rule. | system_engineer |
| RISK-SKILL-009 | New registries are inconsistently path-rooted. | Medium | Medium | Choose one path convention and document it. | memory_governance |
| RISK-SKILL-010 | Upstream skill updates are missed later. | Medium | High | Add periodic skill-review AgentJob and upstream review date fields. | skill_governance |

---

## 8. Rollback Plan

Rollback should be safe because this plan mostly adds files and small validator/manifest changes.

### 8.1 Rollback trigger

Rollback if:

- `make validate` cannot be restored to pass,
- existing adapter validation breaks unrelated skills,
- metrics script introduces unacceptable privacy or dependency risk,
- files are accidentally promoted as canonical authority.

### 8.2 Rollback steps

1. Revert changes to:

```text
sys-for-ai/sys_for_ai/validators.py
sys-for-ai/sys_for_ai/cli.py
sys-for-ai/sys_for_ai/discovery.py
sys-for-ai/Makefile
sys-for-ai/skills/core_skill_manifest.yaml
sys-for-ai/registries/*.csv
sys-for-ai/schemas/*.yaml
sys-for-ai/docs/*.md
sys-for-ai/templates/system_definition/**
sys-for-ai/control_records/agentjobs/**
sys-for-ai/control_records/system_definition/**
sys-for-ai/skills/core/system-definition-interview/**
sys-for-ai/skills/core/system-definition-interview-context-45/**
sys-for-ai/skills/core/codex-usage-metrics/scripts/**
```

2. Restore prior validation state:

```bash
cd sys-for-ai
make validate
```

3. Record rollback reason in an issue or decision record.

### 8.3 Partial rollback option

If only metrics adaptation fails:

- remove or disable `validate-metrics`,
- keep system-definition adapters,
- document fail-closed context behavior,
- create `OPEN-SKILL-METRICS-001`.

---

## 9. Post-Implementation Review Checklist

Use this checklist before marking the integration complete.

### 9.1 Manifest and registry

- [ ] `system-definition-interview` appears in `core_skill_manifest.yaml`.
- [ ] `system-definition-interview-context-45` appears in `core_skill_manifest.yaml`.
- [ ] Both appear in `skill_registry.csv`.
- [ ] Both appear in `validators.py` required set.
- [ ] Source provenance is correct.
- [ ] Adaptation status is not overstated.

### 9.2 Adapter folders

- [ ] `system-definition-interview/SKILL.md` exists.
- [ ] `system-definition-interview/README.md` exists.
- [ ] `system-definition-interview/AGENTS.md` exists.
- [ ] `system-definition-interview/examples/portable-example.md` exists.
- [ ] `system-definition-interview-context-45/SKILL.md` exists.
- [ ] `system-definition-interview-context-45/README.md` exists.
- [ ] `system-definition-interview-context-45/AGENTS.md` exists.
- [ ] `system-definition-interview-context-45/examples/portable-example.md` exists.

### 9.3 Authority model

- [ ] Adapters require AgentJob or Director authorization.
- [ ] Adapters read canonical sources first.
- [ ] Candidate requirements remain candidates.
- [ ] Discovery records are draft evidence unless promoted.
- [ ] `temp_prd.md` is resumable context only.

### 9.4 Metrics behavior

- [ ] Operational or fail-closed policy is explicit.
- [ ] If operational, metrics script exists.
- [ ] If operational, `--help` passes.
- [ ] If fail-closed, open issue exists.
- [ ] Context-45 stops when metrics unavailable or threshold reached.

### 9.5 Templates

- [ ] Requirements discovery template exists.
- [ ] Temp PRD template exists.
- [ ] Templates include authority notice.
- [ ] Templates include evidence register.
- [ ] Templates include open questions.
- [ ] Templates include downstream routing.

### 9.6 Validation

- [ ] `make doctor` passes.
- [ ] `make validate-skills` passes.
- [ ] `make validate-agentjob` passes for sample.
- [ ] New AgentJobs pass individually.
- [ ] `make bootstrap-memory` passes.
- [ ] `make validate` passes.
- [ ] Any skipped validation is documented.

---

## 10. Recommended Commit Structure

Use small commits so the history tells a clean story.

### Commit 1

```text
Update core skill baseline for system definition skills
```

Files:

```text
sys-for-ai/skills/core_skill_manifest.yaml
sys-for-ai/sys_for_ai/validators.py
sys-for-ai/registries/skill_registry.csv
sys-for-ai/schemas/skill.schema.yaml
```

### Commit 2

```text
Add system definition skill adapter shells
```

Files:

```text
sys-for-ai/skills/core/system-definition-interview/**
sys-for-ai/skills/core/system-definition-interview-context-45/**
```

### Commit 3

```text
Add requirements discovery templates and control records
```

Files:

```text
sys-for-ai/templates/system_definition/**
sys-for-ai/control_records/system_definition/**
sys-for-ai/schemas/discovery_record.schema.yaml
```

### Commit 4

```text
Add AgentJobs for skill integration and system definition templates
```

Files:

```text
sys-for-ai/control_records/agentjobs/**
```

### Commit 5, optional

```text
Adapt codex usage metrics for context-aware skill handoff
```

Files:

```text
sys-for-ai/skills/core/codex-usage-metrics/**
sys-for-ai/sys_for_ai/cli.py
sys-for-ai/sys_for_ai/validators.py
sys-for-ai/Makefile
```

### Commit 6

```text
Document system document spine and skill routing policy
```

Files:

```text
sys-for-ai/docs/system_document_spine.md
sys-for-ai/docs/skill_integration_policy.md
sys-for-ai/README.md
sys-for-ai/registries/*.csv
```

---

## 11. Final Definition of Done

This integration is done when a future root agent can answer all of these without re-deriving the project state:

1. Which core skills exist locally?
2. Which upstream template each local adapter came from?
3. Whether each adapter is shell, imported, adapted, or deprecated?
4. What skill should be used first when system intent is unclear?
5. How a long system-definition interview is checkpointed?
6. Where a requirements discovery record should be written?
7. Why discovery records are not canonical requirements by default?
8. How candidate requirements are identified?
9. What validator catches missing skill adapter folders?
10. What command validates the Phase 1 scaffold?
11. What AgentJob authorized the integration?
12. What evidence proves validation passed?
13. What document chain comes after discovery and PRD?
14. What remains open for future operational hardening?

---

## 12. Follow-On Improvements After This Plan

These are intentionally outside the minimum integration but are logical next steps.

1. Replace hard-coded `SKILL_MANIFEST_REQUIRED_SKILLS` with a checked baseline file.
2. Add manifest-registry agreement validator.
3. Add a skill dependency resolver and lock file.
4. Add `.agents/skill_registry` scaffold if `sys-for-ai` needs runtime bundle profiles.
5. Add full `skill.yaml` local manifests for adapted skills.
6. Add template-mode and live-record-mode discovery validators.
7. Add CI workflow for `make validate`.
8. Add periodic upstream skill-drift review AgentJob.
9. Add formal SRD/SyRS/SRS/ARD/SEMP/V&V templates in later phases.
10. Add source-authority promotion workflow for discovery records.

---

## 13. Compact Implementation Command Script

This is not a complete patch, but it shows the expected implementation rhythm.

```bash
# 0. Start
git checkout -b feature/system-definition-skill-integration
cd sys-for-ai
make doctor
make validate
cd ..

# 1. Edit required files manually or via patch
$EDITOR sys-for-ai/sys_for_ai/validators.py
$EDITOR sys-for-ai/skills/core_skill_manifest.yaml
$EDITOR sys-for-ai/registries/skill_registry.csv
$EDITOR sys-for-ai/schemas/skill.schema.yaml

# 2. Confirm validator sees missing adapters
cd sys-for-ai
make validate-skills || true
cd ..

# 3. Add adapter folders
mkdir -p sys-for-ai/skills/core/system-definition-interview/examples
mkdir -p sys-for-ai/skills/core/system-definition-interview-context-45/examples
$EDITOR sys-for-ai/skills/core/system-definition-interview/SKILL.md
$EDITOR sys-for-ai/skills/core/system-definition-interview/README.md
$EDITOR sys-for-ai/skills/core/system-definition-interview/AGENTS.md
$EDITOR sys-for-ai/skills/core/system-definition-interview/examples/portable-example.md
$EDITOR sys-for-ai/skills/core/system-definition-interview-context-45/SKILL.md
$EDITOR sys-for-ai/skills/core/system-definition-interview-context-45/README.md
$EDITOR sys-for-ai/skills/core/system-definition-interview-context-45/AGENTS.md
$EDITOR sys-for-ai/skills/core/system-definition-interview-context-45/examples/portable-example.md

# 4. Validate skill surfaces
cd sys-for-ai
make validate-skills
make validate
cd ..

# 5. Add templates and AgentJobs
mkdir -p sys-for-ai/templates/system_definition
mkdir -p sys-for-ai/control_records/system_definition
mkdir -p sys-for-ai/control_records/agentjobs
$EDITOR sys-for-ai/templates/system_definition/requirements-discovery-record-template.md
$EDITOR sys-for-ai/templates/system_definition/temp-prd-template.md
$EDITOR sys-for-ai/control_records/system_definition/README.md
$EDITOR sys-for-ai/control_records/agentjobs/AJ-P1-SKILL-SYNC-001.yaml
$EDITOR sys-for-ai/control_records/agentjobs/AJ-P1-CODEX-METRICS-ADAPT-001.yaml
$EDITOR sys-for-ai/control_records/agentjobs/AJ-P1-SYSTEM-DEFINITION-TEMPLATE-001.yaml

# 6. Optional metrics operationalization
mkdir -p sys-for-ai/skills/core/codex-usage-metrics/scripts
$EDITOR sys-for-ai/skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py

# 7. Final validation
cd sys-for-ai
make doctor
make validate-skills
make validate-agentjob
.venv/bin/python -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-SKILL-SYNC-001.yaml
.venv/bin/python -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-CODEX-METRICS-ADAPT-001.yaml
.venv/bin/python -m sys_for_ai.cli validate-agentjob control_records/agentjobs/AJ-P1-SYSTEM-DEFINITION-TEMPLATE-001.yaml
make bootstrap-memory
make validate
cd ..

git status --short
git diff --stat
```

---

## 14. Summary

This plan changes `sys-for-ai-dev` from a Phase 1 scaffold with stale skill coverage into a governed, validation-backed integration of the current systems-engineering skillset.

The critical shift is that system definition becomes the front door:

```text
system-definition-interview/context-45
→ decision clarification
→ domain/document clarification
→ PRD synthesis
→ implementation planning
```

The project then avoids the two dangerous traps:

1. building from underspecified intent, and
2. treating a PRD as the entire systems-engineering universe.

The result is a small but sturdy bridge: upstream reusable templates on one side, local `sys-for-ai` authority and validation on the other, with AgentJobs as the rivets.
