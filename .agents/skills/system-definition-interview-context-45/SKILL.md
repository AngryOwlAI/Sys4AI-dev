# System Definition Interview Context 45 - sys-for-ai-dev Runtime Adaptation

Canonical skill ID: `system-definition-interview-context-45`  
Canonical runtime path: `.agents/skills/system-definition-interview-context-45`  
Compatibility shim path: `.codex/skills/system-definition-interview-context-45/SKILL.md`  
Source import: `skills/system-definition-interview-context-45` from `/Volumes/P-SSD/AngryOwl/ai-skills-for-sys`

## sys-for-ai-dev Authority Rules

- Root PRDs, implementation plans, source registries, validators, and git-tracked files outrank generated outputs.
- `sys-for-ai/` is the product scaffold being developed; it is not the full development workspace.
- `.agents/skills/<skill-id>/` is the active runtime skill surface for this repository.
- `.codex/skills/<skill-id>/SKILL.md` is compatibility-only and must point back to this canonical path.
- Existing `sys-for-ai/skills/core/` files are scaffold and product-reference adapters, not the active runtime authority.
- Do not import local receipts, caches, generated `usage-metrics.txt`, or private operational state as skill source.
- Treat generated PRDs, plans, diagrams, warnings, and handoffs as derivative work until accepted by the relevant project authority.

The imported source guidance below remains valid where it does not conflict with these sys-for-ai-dev rules.

---

---
name: system-definition-interview-context-45
description: Interview stakeholders to establish or reconstruct system intent with a 45 percent context-used checkpoint, saving temp_prd.md only when context is low, metrics are unavailable, or the user explicitly requests a handoff.
---

# system-definition-interview-context-45

## Purpose

Provide the long-session variant of `system-definition-interview`.

This skill preserves the same elicitation workflow and
`requirements-discovery-record.md` output, then adds a context checkpoint after
each user answer. When context used reaches 45 percent, context left is 55
percent or lower, or metrics cannot be collected, write a resumable
`temp_prd.md` in this skill folder and instruct the user to continue with
`/system-definition-interview-context-45 temp_prd`.

Do not create, overwrite, or refresh `temp_prd.md` after each question when
context is still safe. During normal safe-context turns, keep the evolving state
in the discovery record, live working context, or chat summary, and refresh only
`usage-metrics.txt`.

## When To Use

- The user wants to establish or reconstruct a system and the interview may run
  across multiple discussions.
- The system definition needs stakeholder, boundary, scenario, requirements,
  driver, interface, evidence, and V&V discovery before document generation.
- A prior `temp_prd.md` should be used to resume system-definition discovery.
- Context-aware continuation is more important than finishing in one session.

Do not use this skill to generate final formal documents directly. Route to a
downstream PRD, requirements-analysis, or systems-document skill after the
discovery record is coherent enough.

## Inputs

- User prompt, stakeholder notes, interview transcript, source summary, or
  prior `temp_prd.md`.
- Optional <PROJECT_ROOT> and repository evidence for existing or partially
  built systems.
- Optional <PROJECT_AUTHORITY>, source hierarchy, glossary, ADRs, standards, or
  existing documents.
- Optional <OUTPUT_DIRECTORY> for `requirements-discovery-record.md`.
- `<SKILLS_ROOT>` containing `codex-usage-metrics`.
- `<TARGET_SKILL_PATH>` for this skill folder.

## Outputs

- `<OUTPUT_DIRECTORY>/requirements-discovery-record.md`, unless the user asks
  for chat-only output or a different path.
- A `System Intent Profile` and traceable discovery entries using stable IDs.
- `usage-metrics.txt` in this skill folder after each context check.
- `temp_prd.md` in this skill folder when context used is `>= 45%`, context
  left is `<= 55%`, metrics cannot be collected, context left is unknown, or
  the user explicitly requests a handoff.
- `archived_temp_prd/temp_prd_date_yyyy-mm-dd-hh-mm-ss.md` when the user
  confirms an existing checkpoint is from a prior context-45 run and should be
  archived before a fresh session.
- A resume instruction using `/system-definition-interview-context-45 temp_prd`.

## Procedure

1. When invoked with `temp_prd`, skip the archive preflight and read
   `<TARGET_SKILL_PATH>/temp_prd.md` first. If it is missing, state that no
   continuation file was found and proceed from the current user prompt.
2. On normal invocation without `temp_prd`, run the archive preflight:

   ```sh
   python3 <SKILLS_ROOT>/codex-usage-metrics/scripts/archive_temp_prd.py \
     --check --skill-dir <TARGET_SKILL_PATH>
   ```

   If an existing `temp_prd.md` is found, ask whether it is from a previous
   `system-definition-interview-context-45` run and should be archived before
   starting a fresh session. If the user confirms, run:

   ```sh
   python3 <SKILLS_ROOT>/codex-usage-metrics/scripts/archive_temp_prd.py \
     --confirm-archive --skill-dir <TARGET_SKILL_PATH>
   ```

   The archive path format is
   `<TARGET_SKILL_PATH>/archived_temp_prd/temp_prd_date_yyyy-mm-dd-hh-mm-ss.md`.
   If the user does not confirm or does not answer, stop; do not overwrite or
   archive the existing checkpoint.
3. Initialize or refresh the working context: objective, situation
   classification, System Intent Profile, stakeholders, boundary, as-is state,
   to-be state, scenarios, candidate requirements, quality attributes, drivers,
   interfaces, V&V seeds, evidence, assumptions, risks, open questions, last
   exchange, and recommended next branch.
4. Follow the `system-definition-interview` elicitation procedure. Inspect
   available repository or document evidence before asking questions that local
   evidence can answer.
5. Ask one focused question at a time when the answer changes scope, boundary,
   requirement meaning, or stakeholder priority. Use compact batches only for
   independent factual data.
6. After the user answers, record the answer in the working context and update
   the discovery record or chat summary. Do not write that routine update to
   `temp_prd.md` while context is still safe.
7. Run the context metrics checkpoint:

   ```sh
   python3 <SKILLS_ROOT>/codex-usage-metrics/scripts/collect_usage_metrics.py \
     --output <TARGET_SKILL_PATH>/usage-metrics.txt
   ```

8. Read `<TARGET_SKILL_PATH>/usage-metrics.txt` and inspect the `Context`
   section. Continue only when context left is known and greater than `55%`,
   unless the user explicitly requested a handoff.
9. If context left is `<= 55%`, context used is therefore `>= 45%`, or the user
   explicitly requested a handoff, write `<TARGET_SKILL_PATH>/temp_prd.md`,
   overwriting any previous file only after integrating still-relevant prior
   content, then tell the user:

   ```text
   The discussion has been saved to temp_prd.md. Please start a new discussion
   with /system-definition-interview-context-45 temp_prd so the system-definition
   interview can continue with the saved context.
   ```

10. If metrics cannot be collected, the metrics receipt is missing, or context
   left is unknown, fail closed: write the best available `temp_prd.md`, explain
   that metrics were unavailable, and give the same resume instruction.
11. When discovery is coherent enough, stop the interview loop and route
    unresolved material:
    - Use `decision-grilling-context-45` for unresolved design or scope
      decisions.
    - Use `domain-grilling-with-docs-context-45` for terminology, glossary,
      documentation, or ADR-worthy conflicts.
    - When product requirements are ready to synthesize, ask:

      ```text
      Questioning is complete. Should I create a PRD with `/conversation-to-prd` using the current discussion and `temp_prd.md` if it exists?
      ```

      Use `/conversation-to-prd` as the canonical command spelling; treat
      `/conversation-to-PRD` as the same user-facing intent. If the user says
      yes, route to `/conversation-to-prd` with the current discussion and any
      existing `<TARGET_SKILL_PATH>/temp_prd.md`. If the user says no, stop with
      a concise summary and the logical next step. Do not create the PRD
      automatically.
    - Use a future requirements-analysis or systems-document package skill for
      Mission Need, Charter, ConOps, SRD/SyRS, Architecture, SEMP, or V&V Plan
      generation.
    If context threshold, unknown context, unavailable metrics, or explicit
    handoff happens before questioning is complete, do not ask for PRD creation
    yet; write `temp_prd.md` and give the resume instruction.

## `temp_prd.md` Requirements

When writing `temp_prd.md`, include these sections:

```md
# Temp PRD - system-definition-interview-context-45

## Resume Command

`/system-definition-interview-context-45 temp_prd`

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

If the session was resumed from an earlier `temp_prd.md`, merge prior content
into the new file. Keep current trace IDs, preserve unresolved questions that
still matter, remove duplicates, and do not append the old file verbatim unless
the prior content cannot be safely merged.

## Validation

- The interview establishes system intent before document generation.
- The metrics checkpoint runs after each user answer.
- On normal invocation without `temp_prd`, the archive preflight runs before
  any fresh-session work.
- Resume invocation with `temp_prd` skips the archive preflight.
- `temp_prd.md` is written only at the threshold, on unknown/unavailable
  metrics, or on explicit user handoff request.
- `temp_prd.md` contains the last question and the user's answer.
- Resumed sessions integrate prior context instead of discarding it.
- Candidate requirements remain candidates until target-project authority
  baselines them.
- Stakeholders, boundaries, scenarios, candidates, drivers, interfaces, V&V
  seeds, evidence, and open questions remain traceable.
- At the end of questioning, the agent asks whether to create a PRD with
  `/conversation-to-prd` using the current discussion and `temp_prd.md` if it
  exists, and waits for explicit confirmation.

## Failure Modes

- Continuing the interview when context metrics are unavailable.
- Checking context before the user answer is captured.
- Creating, overwriting, or refreshing `temp_prd.md` after each safe-context
  question.
- Overwriting `temp_prd.md` without integrating prior resumable context.
- Archiving or overwriting an existing `temp_prd.md` without explicit user
  confirmation during a fresh invocation.
- Turning elicitation into a large questionnaire instead of a focused interview.
- Generating formal systems documents before intent and boundary are stable.
- Treating candidate requirements as approved requirements.
- Creating a PRD automatically instead of asking at the end of questioning.

## Provenance

Created from repository gap analysis as a reusable template. It was not copied
from a project-specific source. Project-bound names, paths, assumptions, and
sensitive operational details were excluded or replaced with parameters.

## Adaptation Guide

When adapting this skill to a specific project:

- Replace placeholders with project-specific paths, commands, authorities, and
  output locations.
- Define how the target project resolves `<SKILLS_ROOT>` and
  `<TARGET_SKILL_PATH>`.
- Add project-specific validation commands and authority hierarchy.
- Decide whether `requirements-discovery-record.md` is advisory, draft
  authority, or controlled project authority.
- Preserve the 45 percent context-used checkpoint unless the target project
  explicitly chooses a different threshold.
- Document any project-specific assumptions introduced during adaptation.
