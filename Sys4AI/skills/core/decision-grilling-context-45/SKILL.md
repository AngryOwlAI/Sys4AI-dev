---
name: decision-grilling-context-45
description: Long-session decision grilling that checks metrics after each user answer and writes temp_prd.md only when context usage reaches the defined threshold, metrics are unavailable, or the user explicitly requests a handoff.
adaptation_status: adapter_shell
source_repo: https://github.com/AngryOwlAI/ai-skills-for-sys
source_path: skills/decision-grilling-context-45
required_skill: codex-usage-metrics
---

# Decision Grilling Context 45

## Purpose

Long-session decision grilling that checkpoints resumable context when Codex context usage reaches the defined threshold.

Use this local `Sys4AI` adapter when a decision interview may run long. It
preserves the one-question-at-a-time decision-grilling workflow and adds a
context metrics checkpoint after each user answer.

Do not create, overwrite, or refresh `temp_prd.md` after each question when
context is still safe. During normal safe-context turns, keep the evolving state
in live working context or an authorized derivative note, and refresh only
`usage-metrics.txt`.

## Local path bindings

```text
<SKILLS_ROOT>       -> skills/core
<TARGET_SKILL_PATH> -> skills/core/decision-grilling-context-45
```

## When to use

Use this skill when a `Sys4AI` project authority requires the `decision_clarification` capability and the governing PRD or implementation plan authorizes skill use.

## Inputs

- Current project authorization.
- Relevant canonical sources.
- Applicable registries.
- Any local validator commands named by explicit project authority.

## Outputs

- A bounded result appropriate to the skill family.
- Source and provenance notes.
- Validation notes or a pass/repair/block decision when applicable.
- Handoff or completion evidence when the project authority requires it.
- `skills/core/decision-grilling-context-45/usage-metrics.txt` when metrics can be collected.
- `skills/core/decision-grilling-context-45/temp_prd.md` only when context used is at least 45 percent, context left is at most 55 percent, metrics are unavailable or unknown, or the user explicitly requests a handoff.
- `skills/core/decision-grilling-context-45/archived_temp_prd/temp_prd_date_yyyy-mm-dd-hh-mm-ss.md` when the user confirms an existing checkpoint is from a prior context-45 run and should be archived before a fresh session.
- Resume instruction: `/decision-grilling-context-45 temp_prd`.
- End-of-questioning prompt: Questioning is complete. Should I create a PRD with `/conversation-to-prd` using the current discussion and `temp_prd.md` if it exists?

## Procedure

1. Confirm the project authority authorizes this skill.
2. When invoked with `temp_prd`, skip the archive preflight and read `skills/core/decision-grilling-context-45/temp_prd.md` first.
3. On normal invocation without `temp_prd`, run the archive preflight:

```bash
python3 skills/core/codex-usage-metrics/scripts/archive_temp_prd.py \
  --check --skill-dir skills/core/decision-grilling-context-45
```

If an existing `temp_prd.md` is found, ask whether it is from a previous `decision-grilling-context-45` run and should be archived before starting a fresh session. If the user confirms, run:

```bash
python3 skills/core/codex-usage-metrics/scripts/archive_temp_prd.py \
  --confirm-archive --skill-dir skills/core/decision-grilling-context-45
```

The archive path format is `skills/core/decision-grilling-context-45/archived_temp_prd/temp_prd_date_yyyy-mm-dd-hh-mm-ss.md`. If the user does not confirm or does not answer, stop; do not overwrite or archive the existing checkpoint.
4. Read canonical sources before generated derivatives.
5. Apply the decision-grilling procedure: identify the highest-leverage unresolved decision, inspect repository evidence when it can answer the question, ask one focused question, and include a recommended answer when useful.
6. After each user answer, record the answer in working context. Do not write that routine update to `temp_prd.md` while context is still safe.
7. Run the local context metrics checkpoint:

```bash
python3 skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py \
  --output skills/core/decision-grilling-context-45/usage-metrics.txt
```

8. Continue only when context left is known and greater than 55 percent.
9. If context left is 55 percent or lower, context used is 45 percent or higher, metrics are unavailable, context left is unknown, or the user explicitly requests a handoff before questioning is complete, write `temp_prd.md` and stop with the resume instruction. Do not ask for PRD creation yet.
10. When questioning is complete, ask:

```text
Questioning is complete. Should I create a PRD with `/conversation-to-prd` using the current discussion and `temp_prd.md` if it exists?
```

Use `/conversation-to-prd` as the canonical command spelling; treat `/conversation-to-PRD` as the same user-facing intent. If the user says yes, route to `/conversation-to-prd` with the current discussion and any existing `skills/core/decision-grilling-context-45/temp_prd.md`. If the user says no, stop with a concise summary and the logical next step. Do not create the PRD automatically.
11. Preserve source provenance and document assumptions.
12. Run or name validators before completion.

## `temp_prd.md` required sections

```markdown
# Temp PRD - decision-grilling-context-45

## Resume Command

/decision-grilling-context-45 temp_prd

## Objective
## Discussion Summary
## Requirements Gathered
## Confirmed Decisions
## Constraints
## Risks
## Unresolved Questions
## Last Exchange
### Last Question Asked
### User Answer
## Recommended Next Branch
## Metrics Snapshot
## Prior Temp PRD Integration
```

## Local authority boundaries

- This adapter does not override PRDs, source registries, decision records, or validators.
- Generated notes are derivative unless promoted through source authority.
- Upstream skill text must be reviewed before this adapter is marked `adapted`.

## Validation

Run:

```bash
cd Sys4AI && make validate-skills
```

## Known failure modes

- Using the skill without explicit project authority.
- Treating upstream placeholders as local facts.
- Producing output that is not traceable to canonical sources.
- Marking the adapter as fully adapted before local review.
- Creating, overwriting, or refreshing `temp_prd.md` after each safe-context question.
- Continuing the loop when metrics are unavailable or context left is unknown.
- Archiving or overwriting an existing `temp_prd.md` without explicit user confirmation during a fresh invocation.
- Creating a PRD automatically without explicit user confirmation.
