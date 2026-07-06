---
name: domain-grilling-with-docs-context-45
description: Long-session documentation-aware grilling that checks metrics after each user answer and writes temp_prd.md only when context usage reaches the defined threshold, metrics are unavailable, or the user explicitly requests a handoff.
adaptation_status: adapter_shell
source_repo: https://github.com/AngryOwlAI/ai-skills-for-sys
source_path: skills/domain-grilling-with-docs-context-45
required_skill: codex-usage-metrics
---

# Domain Grilling With Docs Context 45

## Purpose

Long-session documentation-aware grilling with resumable checkpoint behavior for extended discovery.

Use this local `sys-for-ai` adapter when a documentation-aware domain interview
may run long. It preserves the one-question-at-a-time domain-grilling workflow
and adds a context metrics checkpoint after each user answer.

Do not create, overwrite, or refresh `temp_prd.md` after each question when
context is still safe. During normal safe-context turns, keep the evolving state
in live working context, approved glossary/context artifacts, ADR candidates, or
an authorized derivative note, and refresh only `usage-metrics.txt`.

## Local path bindings

```text
<SKILLS_ROOT>       -> skills/core
<TARGET_SKILL_PATH> -> skills/core/domain-grilling-with-docs-context-45
```

## When to use

Use this skill when a `sys-for-ai` AgentJob requires the `domain_documentation_clarification` capability and the governing PRD or implementation plan authorizes skill use.

## Inputs

- Current AgentJob.
- Relevant canonical sources.
- Applicable registries.
- Any local validator commands named by the AgentJob.

## Outputs

- A bounded result appropriate to the skill family.
- Source and provenance notes.
- Validation notes or a pass/repair/block decision when applicable.
- Handoff or completion evidence when the AgentJob requires it.
- `skills/core/domain-grilling-with-docs-context-45/usage-metrics.txt` when metrics can be collected.
- `skills/core/domain-grilling-with-docs-context-45/temp_prd.md` only when context used is at least 45 percent, context left is at most 55 percent, metrics are unavailable or unknown, or the user explicitly requests a handoff.
- Resume instruction: `/domain-grilling-with-docs-context-45 temp_prd`.

## Procedure

1. Confirm the AgentJob authorizes this skill.
2. If invoked with `temp_prd`, read `skills/core/domain-grilling-with-docs-context-45/temp_prd.md` first.
3. Read canonical sources before generated derivatives.
4. Apply the domain-grilling-with-docs procedure: identify the highest-leverage unresolved terminology, documentation, or ADR-worthy decision; inspect repository evidence when it can answer the question; ask one focused question; and include a recommended answer when useful.
5. After each user answer, record the answer in working context. Do not write that routine update to `temp_prd.md` while context is still safe.
6. Update authorized glossary/context artifacts or ADR candidates only when the content is settled enough for that artifact.
7. Run the local context metrics checkpoint:

```bash
python3 skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py \
  --output skills/core/domain-grilling-with-docs-context-45/usage-metrics.txt
```

8. Continue only when context left is known and greater than 55 percent.
9. If context left is 55 percent or lower, context used is 45 percent or higher, metrics are unavailable, context left is unknown, or the user explicitly requests a handoff, write `temp_prd.md` and stop with the resume instruction.
10. Preserve source provenance and document assumptions.
11. Run or name validators before completion.

## `temp_prd.md` required sections

```markdown
# Temp PRD - domain-grilling-with-docs-context-45

## Resume Command

/domain-grilling-with-docs-context-45 temp_prd

## Objective
## Discussion Summary
## Requirements Gathered
## Confirmed Decisions
## Constraints
## Risks
## Unresolved Questions
## Domain Terminology
## Glossary Or Context Updates
## ADR Candidates
## Terminology Conflicts
## Documentation Evidence
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
cd sys-for-ai && make validate-skills
```

## Known failure modes

- Using the skill without an authorized AgentJob.
- Treating upstream placeholders as local facts.
- Producing output that is not traceable to canonical sources.
- Marking the adapter as fully adapted before local review.
- Creating, overwriting, or refreshing `temp_prd.md` after each safe-context question.
- Continuing the loop when metrics are unavailable or context left is unknown.
