# System Definition Interview - Sys4AI-dev Runtime Adaptation

Canonical skill ID: `system-definition-interview`  
Canonical runtime path: `.agents/skills/system-definition-interview`  
Compatibility shim path: `.codex/skills/system-definition-interview/SKILL.md`  
Source import: `skills/system-definition-interview` from `/Volumes/P-SSD/AngryOwl/ai-skills-for-sys`

## Sys4AI-dev Authority Rules

- Root PRDs, implementation plans, source registries, validators, and git-tracked files outrank generated outputs.
- `Sys4AI/` is the product scaffold being developed; it is not the full development workspace.
- `.agents/skills/<skill-id>/` is the active runtime skill surface for this repository.
- `.codex/skills/<skill-id>/SKILL.md` is compatibility-only and must point back to this canonical path.
- Existing `Sys4AI/skills/core/` files are scaffold and product-reference adapters, not the active runtime authority.
- Do not import local receipts, caches, generated `usage-metrics.txt`, or private operational state as skill source.
- Treat generated PRDs, plans, diagrams, warnings, and handoffs as derivative work until accepted by the relevant project authority.

The imported source guidance below remains valid where it does not conflict with these Sys4AI-dev rules.

---

---
name: system-definition-interview
description: Interview stakeholders to establish or reconstruct system intent, boundaries, stakeholders, scenarios, candidate requirements, architecture drivers, interfaces, evidence, and V&V seeds before creating PRDs or formal systems documents.
---

# system-definition-interview

## Purpose

Establish or reconstruct the definition of a system before downstream document
generation begins.

Use this skill as the elicitation front door for new systems, existing systems,
partially built systems, and documentation-recovery efforts. It produces a
traceable `requirements-discovery-record.md` with a `System Intent Profile`
section so later PRDs, Mission Need statements, ConOps drafts, SRD/SyRS drafts,
architecture notes, SEMP material, and V&V plans can preserve evidence and
decision traceability.

## When To Use

- The user wants to define, establish, scope, or reconstruct a system.
- A stakeholder interview is needed before PRD or systems-document creation.
- The current state, target state, system boundary, users, operators,
  maintainers, or affected parties are unclear.
- Candidate requirements, quality attributes, architecture drivers, interfaces,
  or verification seeds must be discovered before formal analysis.
- Existing decision-grilling skills are too narrow because the system intent
  itself has not yet been established.

Do not use this skill to generate final formal documents directly. Route to a
downstream PRD, requirements-analysis, or systems-document skill after the
discovery record is coherent enough.

## Inputs

- User prompt, stakeholder notes, interview transcript, or source summary.
- Optional <PROJECT_ROOT> and repository evidence for existing or partially
  built systems.
- Optional <PROJECT_AUTHORITY>, source hierarchy, glossary, ADRs, standards, or
  existing documents.
- Optional <OUTPUT_DIRECTORY> for `requirements-discovery-record.md`.
- Optional constraints: schedule, budget, compliance, safety, reliability,
  accessibility, operations, deployment, migration, data, security, or support.

## Outputs

- `<OUTPUT_DIRECTORY>/requirements-discovery-record.md`, unless the user asks
  for chat-only output or a different path.
- A `System Intent Profile` summarizing the system purpose, boundary, outcome,
  current state, target state, stakeholders, and success criteria.
- Traceable discovery entries using stable IDs such as `NEED-*`, `STK-*`,
  `SCN-*`, `VISION-CAND-*`, `VALUE-CAND-*`, `WAIVER-CAND-*`, `REQ-CAND-*`,
  `NFR-CAND-*`, `DRV-*`, `IF-*`, `VVE-*`, and `OPEN-*`.
- A routing recommendation for unresolved decisions, terminology conflicts,
  PRD creation, or future systems-document generation.

## Procedure

1. Classify the situation as one of: new system, existing system, partially
   built system, or documentation recovery. If multiple labels apply, record
   the dominant label and the secondary label.
2. Inspect available repository or document evidence before asking questions
   that local evidence can answer.
3. Identify the highest-leverage missing information. Ask one focused question
   at a time when the answer changes scope, boundary, requirement meaning, or
   stakeholder priority. Use compact batches only for independent factual data.
4. Elicit the mission need, problem statement, desired outcome, value case, and
   feasibility constraints.
5. For a new or substantially changed target, separate mission from future-state vision and elicit candidate vision, intended beneficiaries, value commitments, anti-values, conflicts and precedence, inherited constraints, missing stakeholders, accountable human approval identity, waiver state, and review cadence. Label statements as stated, inferred, or missing and keep `VISION-CAND-*` and `VALUE-CAND-*` IDs until approval.
6. Identify stakeholders, user groups, operators, maintainers, owners, affected
   parties, approvers, and downstream consumers of the generated record.
7. Define the system boundary: included capabilities, excluded capabilities,
   external systems, inputs, outputs, interfaces, operating environment, and
   lifecycle responsibilities.
8. For existing or partially built systems, distinguish as-is behavior from
   to-be intent. Mark observed facts separately from stakeholder preferences.
9. Build ConOps seeds from concrete operational scenarios, including normal
   use, exception paths, degraded operation, handoff points, and support paths.
10. Extract candidate functional requirements as `REQ-CAND-*` entries and
   quality attributes as `NFR-CAND-*` entries. Do not overstate candidates as
   baselined requirements.
11. Extract architecture drivers, interface candidates, data or information
    flows, assumptions, constraints, risks, and dependency questions.
12. Seed verification and validation thinking with `VVE-*` entries: observable
    acceptance checks, inspection evidence, analysis needs, test ideas, review
    gates, or human approval points.
13. Write or update `requirements-discovery-record.md` using this skill's
    template unless the target project provides a local replacement.
14. Route unresolved material:
    - Use `decision-grilling-context-45` for unresolved design or scope
      decisions.
    - Use `domain-grilling-with-docs-context-45` for terminology, glossary,
      documentation, or ADR-worthy conflicts.
    - Use `conversation-to-prd` only when product requirements are ready to
      synthesize.
    - Use a future requirements-analysis or systems-document package skill for
      Mission Need, Charter, ConOps, SRD/SyRS, Architecture, SEMP, or V&V Plan
      generation.

## Record Requirements

The discovery record must:

- Include a `System Intent Profile` section.
- Separate observations, stakeholder statements, assumptions, inferences, and
  open questions.
- Preserve trace IDs for needs, stakeholders, scenarios, candidate
  vision and values, waivers, requirements, quality attributes, drivers,
  interfaces, V&V seeds, and open questions.
- Record coordination-pattern candidates, operational maturity, autonomy, integrations, communication, monitoring, degraded mode, and promotion evidence when they affect strategic intent.
- Treat silence, model authorship, controlled-file location, and structural validation as insufficient for strategic-content approval.
- Mark candidate requirements as candidates until a target-project authority
  baselines them.
- Name evidence sources or state that evidence is unavailable.
- Record downstream routing recommendations and remaining blockers.

## Validation

- The interview establishes system intent before document generation.
- The record distinguishes new, existing, partially built, or
  documentation-recovery context.
- Stakeholder classes and system boundaries are explicit.
- As-is and to-be states are not conflated.
- Candidate requirements, quality attributes, drivers, interfaces, and V&V
  seeds are traceable.
- Unsupported assumptions and missing evidence are visible.
- Downstream routing does not skip unresolved decisions or terminology
  conflicts.

## Failure Modes

- Turning elicitation into a large questionnaire instead of a focused interview.
- Generating formal systems documents before intent and boundary are stable.
- Treating candidate requirements as approved requirements.
- Mixing observed current behavior with desired future behavior.
- Ignoring repository or document evidence that can answer a question.
- Losing traceability between stakeholder statements, scenarios, requirements,
  drivers, interfaces, and verification seeds.

## Provenance

Created from repository gap analysis as a reusable template. It was not copied
from a project-specific source. Project-bound names, paths, assumptions, and
sensitive operational details were excluded or replaced with parameters.

## Adaptation Guide

When adapting this skill to a specific project:

- Replace placeholders with project-specific paths, commands, authorities, and
  output locations.
- Add project-specific validation commands and authority hierarchy.
- Add domain-specific constraints only when they are required.
- Decide whether `requirements-discovery-record.md` is advisory, draft
  authority, or controlled project authority.
- Preserve the elicitation-first workflow unless local evidence shows a better
  structure.
- Document any project-specific assumptions introduced during adaptation.
