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

Use this local `Sys4AI` adapter for long system-definition interviews that may cross context limits. It follows the `system-definition-interview` workflow and adds a context checkpoint after each user answer.

This adapter is the default discovery gate for new or substantially changed
system definitions in `Sys4AI`. It must classify the subject layer and
produce or update a Requirements Discovery Record before any USRD, PRD, SRD,
ARD, TRP, or SRP is generated.

When context used is at least 45 percent, context left is at most 55 percent, or metrics cannot be collected, write a resumable `temp_prd.md` and stop.

Do not create, overwrite, or refresh `temp_prd.md` after each question when
context is still safe. During normal safe-context turns, keep the evolving state
in the discovery record, live working context, or chat summary, and refresh only
`usage-metrics.txt`.

## Local path bindings

```text
<SKILLS_ROOT>       -> skills/core
<TARGET_SKILL_PATH> -> skills/core/system-definition-interview-context-45
<OUTPUT_DIRECTORY>  -> control_records/system_definition
```

Repository-root invocation should run from `Sys4AI/` unless explicit project authority states another working directory.

## When to use

Use this adapter when:

- system definition requires a long stakeholder interview,
- the user explicitly invokes `/system-definition-interview-context-45`,
- a new or substantially changed system definition needs front-door discovery
  before downstream requirements or architecture artifacts,
- a prior `temp_prd.md` should be resumed,
- context-aware continuation is more important than finishing in one session,
- the root agent expects a resumable handoff before context becomes risky.

Do not use this adapter for short clarifications that do not need continuation protection. Use `system-definition-interview` instead.

## Inputs

- Current explicit project authorization or System Director decision.
- User prompt, stakeholder notes, transcript, source summary, or prior `temp_prd.md`.
- Optional repository or documentation evidence.
- Local `codex-usage-metrics` adapter.
- Optional metrics session file or Codex home path if required by the metrics adapter.

## Outputs

- `control_records/system_definition/requirements-discovery-record.md`, unless chat-only output is authorized.
- Candidate `VISION-CAND-*`, `VALUE-CAND-*`, and `WAIVER-CAND-*` state with source or inference labels, missing stakeholders, approval principal, conflicts, and review cadence.
- `skills/core/system-definition-interview-context-45/usage-metrics.txt` when metrics can be collected.
- `skills/core/system-definition-interview-context-45/temp_prd.md` only when context threshold is reached, metrics are unavailable or unknown, or the user explicitly requests a handoff.
- `skills/core/system-definition-interview-context-45/archived_temp_prd/temp_prd_date_yyyy-mm-dd-hh-mm-ss.md` when the user confirms an existing checkpoint is from a prior context-45 run and should be archived before a fresh session.
- End-of-questioning prompt: Questioning is complete. Should I create a PRD with `/conversation-to-prd` using the current discussion and `temp_prd.md` if it exists?
- Resume instruction:

```text
/system-definition-interview-context-45 temp_prd
```

## Procedure

1. Confirm the project authority authorizes this skill.
2. When invoked with `temp_prd`, skip the archive preflight and read `skills/core/system-definition-interview-context-45/temp_prd.md` first.
3. If `temp_prd.md` is missing during resume, state that no continuation file was found and proceed from the current prompt only if authorized.
4. On normal invocation without `temp_prd`, run the archive preflight:

```bash
python3 skills/core/codex-usage-metrics/scripts/archive_temp_prd.py \
  --check --skill-dir skills/core/system-definition-interview-context-45
```

If an existing `temp_prd.md` is found, ask whether it is from a previous `system-definition-interview-context-45` run and should be archived before starting a fresh session. If the user confirms, run:

```bash
python3 skills/core/codex-usage-metrics/scripts/archive_temp_prd.py \
  --confirm-archive --skill-dir skills/core/system-definition-interview-context-45
```

The archive path format is `skills/core/system-definition-interview-context-45/archived_temp_prd/temp_prd_date_yyyy-mm-dd-hh-mm-ss.md`. If the user does not confirm or does not answer, stop; do not overwrite or archive the existing checkpoint.
5. Initialize or refresh working context: objective, situation classification, System Intent Profile, candidate vision and values, anti-values, source or inference state, missing stakeholders, accountable human approval identity, inherited constraints, conflicts, waiver and review state, pattern, maturity, autonomy, integrations, communication, monitoring, degraded mode, promotion evidence, stakeholders, boundary, as-is state, to-be state, operational scenarios, candidate requirements, quality attributes, architecture drivers, interfaces, V&V seeds, evidence, assumptions, risks, open questions, last exchange, and recommended next branch.
6. Classify the subject layer as `development_system`, `framework_product`,
   `target_system_template`, `target_system_instance`, or
   `derivative_surface`. Route to `system-layer-classifier` when available and
   classification is not clear from current evidence.
7. Produce or update `control_records/system_definition/requirements-discovery-record.md`
   before any USRD, PRD, SRD, ARD, TRP, or SRP is created.
8. Preserve candidate requirement IDs as `REQ-CAND-*` or `NFR-CAND-*`.
9. Preserve candidate strategic-intent IDs as `VISION-CAND-*` or `VALUE-CAND-*`; silence, model authorship, controlled-file location, and structural validation are not approval.
10. Follow the local `system-definition-interview` procedure.
11. Ask one focused question at a time unless a compact factual batch is safe.
12. After each user answer, record the answer before checking metrics. Do not write that routine update to `temp_prd.md` while context is still safe.
13. Run the local context metrics checkpoint:

```bash
python3 skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py \
  --output skills/core/system-definition-interview-context-45/usage-metrics.txt
```

14. Read `usage-metrics.txt` and inspect the context section.
15. Continue only when context left is known and greater than 55 percent, unless the user explicitly requested a handoff.
16. If context left is 55 percent or lower, context used is 45 percent or higher, metrics are unavailable, context left is unknown, or the user explicitly requests a handoff before questioning is complete, write `temp_prd.md` and stop. Do not ask for PRD creation yet.
17. Tell the user or downstream agent:

```text
The discussion has been saved to temp_prd.md. Start a new discussion with /system-definition-interview-context-45 temp_prd so the system-definition interview can continue with the saved context.
```

18. When questioning is complete and product requirements are ready to synthesize, ask:

```text
Questioning is complete. Should I create a PRD with `/conversation-to-prd` using the current discussion and `temp_prd.md` if it exists?
```

Use `/conversation-to-prd` as the canonical command spelling; treat `/conversation-to-PRD` as the same user-facing intent. If the user says yes, route to `/conversation-to-prd` with the current discussion and any existing `skills/core/system-definition-interview-context-45/temp_prd.md`. If the user says no, stop with a concise summary and the logical next step. Do not create the PRD automatically.
19. Route downstream only after the discovery state is coherent enough and the user confirms the downstream route.

## Fail-closed behavior

If the metrics script does not exist, fails, returns no context section, returns unknown context left, or cannot identify the current session, do not continue the interview. Write `temp_prd.md` using the best available state and stop. Do not ask for PRD creation before the resumed interview reaches genuine completion.

## `temp_prd.md` required sections

```markdown
# Temp PRD - system-definition-interview-context-45

## Resume Command

/system-definition-interview-context-45 temp_prd

## Objective
## Situation Classification
## System Intent Profile
## Strategic Intent Candidates
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
- Candidate vision and core values remain unapproved until accountable human approval evidence exists.
- Metrics receipts are point-in-time evidence only.
- The adapter may write only paths authorized by explicit project authority.
- It must not export conversation content through the metrics script.

## Validation

Required:

```bash
cd Sys4AI
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
- Creating, overwriting, or refreshing `temp_prd.md` after each safe-context question.
- Overwriting `temp_prd.md` without integrating prior continuation context.
- Archiving or overwriting an existing `temp_prd.md` without explicit user confirmation during a fresh invocation.
- Treating `temp_prd.md` as a final PRD.
- Creating a PRD automatically without explicit user confirmation.
- Creating final formal systems documents before intent and boundary are stable.
- Treating candidate requirements as approved.

## Provenance

Adapted from `AngryOwlAI/ai-skills-for-sys/skills/system-definition-interview-context-45` as a local `Sys4AI` adapter. Upstream template behavior is preserved where compatible with `Sys4AI` explicit project authority, source-first authority, and validation rules.

## Adaptation work remaining

1. Confirm the local metrics policy.
2. Import or adapt the metrics script, or document Phase 1 fail-closed behavior.
3. Add validation evidence for `--help` if operational.
4. Add or validate the `temp_prd.md` template.
5. Mark as `adapted` only after review and validation receipt.
