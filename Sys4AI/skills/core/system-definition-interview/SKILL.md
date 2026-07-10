---
name: system-definition-interview
description: Establish or reconstruct system intent, boundaries, stakeholders, scenarios, candidate requirements, architecture drivers, interfaces, evidence, and V&V seeds before PRD or formal systems-document generation.
adaptation_status: adapter_shell
source_repo: https://github.com/AngryOwlAI/ai-skills-for-sys
source_path: skills/system-definition-interview
---

# System Definition Interview

## Purpose

Use this local `Sys4AI` adapter to establish or reconstruct the intent of a target agentic system before downstream PRD, SRD, architecture, implementation-plan, or formal systems-document generation.

The adapter produces a traceable `requirements-discovery-record.md` or chat-only equivalent with a `System Intent Profile`, candidate requirements, evidence, assumptions, risks, open questions, and downstream routing recommendations.

## When to use

Use this skill when an explicit project authorization or System Director decision requires front-door system-definition elicitation for:

- a new target agentic system,
- an existing target system,
- a partially built target system,
- documentation recovery,
- unclear stakeholder intent,
- unclear boundary,
- unclear as-is or to-be state,
- missing operational scenarios,
- missing candidate requirements,
- missing architecture drivers,
- missing V&V seeds.

Do not use this adapter to generate final formal PRDs, SRDs, SyRS, SRS, ARDs, SEMPs, or V&V plans directly. Route to downstream skills or roles after the discovery record is coherent enough.

## Inputs

- Current explicit project authorization or System Director decision.
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
  - `VISION-CAND-*`
  - `VALUE-CAND-*`
  - `WAIVER-CAND-*`
  - `REQ-CAND-*`
  - `NFR-CAND-*`
  - `DRV-*`
  - `IF-*`
  - `VVE-*`
  - `OPEN-*`
- Assumptions, risks, and constraints.
- Source and provenance notes.
- Downstream routing recommendation.
- Completion receipt if required by explicit project authority.

## Procedure

1. Confirm the current project authorization or Director decision authorizes this skill.
2. Identify the system-of-interest and classify the request as new system, existing system, partially built system, or documentation recovery.
3. Read canonical sources before generated derivatives.
4. Inspect available repository or documentation evidence before asking questions that local evidence can answer.
5. Ask one focused question at a time when the answer affects scope, boundary, requirement meaning, stakeholder priority, or downstream routing.
6. Use compact factual batches only for independent information that does not require deliberation.
7. Elicit mission need, problem statement, desired outcome, value case, and feasibility constraints.
8. For a new or substantially changed target, separate mission from future-state vision and capture vision and value candidates, anti-values, source or inference state, missing stakeholders, accountable human approval identity, inherited constraints, conflicts, waiver state, review cadence, pattern, maturity, autonomy, integrations, communication, monitoring, degraded mode, and promotion evidence.
9. Identify stakeholders, users, operators, maintainers, owners, affected parties, approvers, and downstream consumers.
10. Define system boundary, including included capabilities, excluded capabilities, external systems, inputs, outputs, interfaces, operating environment, and lifecycle responsibilities.
11. For existing or partially built systems, separate observed as-is behavior from desired to-be intent.
12. Build ConOps seeds from concrete operational scenarios.
13. Extract candidate functional requirements as `REQ-CAND-*`.
14. Extract quality attributes as `NFR-CAND-*`.
15. Extract architecture drivers, interface candidates, data flows, assumptions, constraints, risks, and dependency questions.
16. Seed verification and validation with `VVE-*` entries.
17. Write or update the discovery record using `templates/system_definition/requirements-discovery-record-template.md` unless the project authority specifies another template.
18. Route unresolved material:
    - `decision-grilling-context-45` for unresolved scope or design choices.
    - `domain-grilling-with-docs-context-45` for terminology, glossary, documentation, or ADR-worthy conflicts.
    - `conversation-to-prd` only when product requirements are ready to synthesize.
    - Future SRD, SyRS, SRS, ARD, SEMP, or V&V document skills only after system intent is coherent.

## Local authority boundaries

- This adapter does not override canonical PRDs, source registries, decision records, or validators.
- Discovery records are draft discovery evidence unless promoted by project authority.
- Candidate requirements are not baselined requirements.
- Candidate vision and core values retain `VISION-CAND-*` and `VALUE-CAND-*` IDs until accountable human approval; silence, model authorship, controlled-file location, and structural validation are not approval.
- Generated notes, summaries, and templates are derivative unless explicitly promoted.
- Missing facts, thresholds, actors, owners, constraints, environments, evidence, or acceptance criteria must become open issues rather than silent inventions.

## Validation

Run:

```bash
cd Sys4AI
make validate-skills
```

When a discovery record is produced and the optional validator exists, also run:

```bash
.venv/bin/python -m sys_for_ai.cli validate-discovery-record control_records/system_definition/requirements-discovery-record.md
```

## Known failure modes

- Using the skill without explicit project authority or Director decision.
- Generating a PRD before system intent and boundary are stable.
- Treating candidate requirements as approved requirements.
- Asking a large questionnaire instead of focused, decision-relevant questions.
- Ignoring repository evidence that can answer a question.
- Mixing as-is observations with to-be intent.
- Losing traceability from stakeholder statements to candidate requirements and V&V seeds.

## Provenance

Adapted from `AngryOwlAI/ai-skills-for-sys/skills/system-definition-interview` as a local `Sys4AI` adapter. Upstream template behavior is preserved where compatible with `Sys4AI` source-first authority, explicit project authority, registry, and validation rules.

## Adaptation work remaining

1. Compare this adapter against the current upstream template.
2. Replace any unresolved placeholders with local paths, commands, and authority rules.
3. Add project-specific validators.
4. Record validation evidence.
5. Mark as `adapted` only after a skill-import review receipt.
