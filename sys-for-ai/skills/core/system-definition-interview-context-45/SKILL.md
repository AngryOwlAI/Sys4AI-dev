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
- `skills/core/system-definition-interview-context-45/temp_prd.md` only when context threshold is reached, metrics are unavailable or unknown, or the user explicitly requests a handoff.
- Resume instruction:

```text
/system-definition-interview-context-45 temp_prd
```

## Procedure

1. Confirm the AgentJob authorizes this skill.
2. If invoked with `temp_prd`, read `skills/core/system-definition-interview-context-45/temp_prd.md` first.
3. If `temp_prd.md` is missing, state that no continuation file was found and proceed from the current prompt only if authorized.
4. Initialize or refresh working context: objective, situation classification, System Intent Profile, stakeholders, boundary, as-is state, to-be state, operational scenarios, candidate requirements, quality attributes, architecture drivers, interfaces, V&V seeds, evidence, assumptions, risks, open questions, last exchange, and recommended next branch.
5. Follow the local `system-definition-interview` procedure.
6. Ask one focused question at a time unless a compact factual batch is safe.
7. After each user answer, record the answer before checking metrics. Do not write that routine update to `temp_prd.md` while context is still safe.
8. Run the local context metrics checkpoint:

```bash
python3 skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py \
  --output skills/core/system-definition-interview-context-45/usage-metrics.txt
```

9. Read `usage-metrics.txt` and inspect the context section.
10. Continue only when context left is known and greater than 55 percent, unless the user explicitly requested a handoff.
11. If context left is 55 percent or lower, context used is 45 percent or higher, metrics are unavailable, context left is unknown, or the user explicitly requests a handoff, write `temp_prd.md` and stop.
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
- Creating, overwriting, or refreshing `temp_prd.md` after each safe-context question.
- Overwriting `temp_prd.md` without integrating prior continuation context.
- Treating `temp_prd.md` as a final PRD.
- Creating final formal systems documents before intent and boundary are stable.
- Treating candidate requirements as approved.

## Provenance

Adapted from `AngryOwlAI/ai-skills-for-sys/skills/system-definition-interview-context-45` as a local `sys-for-ai` adapter. Upstream template behavior is preserved where compatible with `sys-for-ai` AgentJob, source-first authority, and validation rules.

## Adaptation work remaining

1. Confirm the local metrics policy.
2. Import or adapt the metrics script, or document Phase 1 fail-closed behavior.
3. Add validation evidence for `--help` if operational.
4. Add or validate the `temp_prd.md` template.
5. Mark as `adapted` only after review and validation receipt.
