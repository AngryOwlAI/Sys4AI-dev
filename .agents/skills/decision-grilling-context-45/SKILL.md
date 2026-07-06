# Decision Grilling Context 45 - sys-for-ai-dev Runtime Adaptation

Canonical skill ID: `decision-grilling-context-45`  
Canonical runtime path: `.agents/skills/decision-grilling-context-45`  
Compatibility shim path: `.codex/skills/decision-grilling-context-45/SKILL.md`  
Source import: `skills/decision-grilling-context-45` from `/Volumes/P-SSD/AngryOwl/ai-skills-for-sys`

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
name: decision-grilling-context-45
description: Interview the user one question at a time to stress-test a plan or design, checking Codex context after each answer and saving temp_prd.md only when context used reaches 45%, metrics are unavailable, or the user explicitly requests a handoff.
---

# decision-grilling-context-45

## Purpose

Provide a reusable Socratic design-review workflow that resolves dependencies
between decisions while protecting long interviews from exhausting the Codex
context window.

This variant preserves the one-question loop from `decision-grilling` and adds a
context checkpoint after each user answer. When context used reaches 45% or more
of the available window, the skill writes a resumable `temp_prd.md` in this
skill folder and instructs the user to continue in a new discussion with the
`temp_prd` parameter.

Do not create, overwrite, or refresh `temp_prd.md` after each question when
context is still safe. During normal safe-context turns, keep the evolving state
in the live working context and refresh only `usage-metrics.txt`.

## When To Use

- The user asks to be grilled, challenged, or stress-tested on a plan and the
  interview may run long.
- A design tree has unresolved branches or hidden assumptions.
- A decision can be clarified by either asking the user or inspecting the codebase.
- A prior `temp_prd.md` should be used to resume a multi-discussion grilling
  session.

## Inputs

- The plan, proposal, or design under review.
- Optional repository evidence, docs, or constraints.
- Any stated decision criteria or risk tolerance.
- Optional `temp_prd` parameter, meaning read this skill folder's
  `temp_prd.md` before asking the next question.
- `<SKILLS_ROOT>` containing `codex-usage-metrics`.
- `<TARGET_SKILL_PATH>` for this skill folder.

## Outputs

- One question at a time.
- A recommended answer for each question.
- A progressively clarified decision tree.
- `usage-metrics.txt` in this skill folder after each context check.
- `temp_prd.md` in this skill folder when context used is `>= 45%`, context
  left is `<= 55%`, metrics cannot be collected, context left is unknown, or
  the user explicitly requests a handoff.
- A resume instruction using `/decision-grilling-context-45 temp_prd`.

## Procedure

1. If invoked with `temp_prd`, read `<TARGET_SKILL_PATH>/temp_prd.md` first.
   If it is missing, state that no continuation file was found and proceed from
   the current user prompt.
2. Initialize or refresh the working context: objective, discussion summary,
   gathered requirements, confirmed decisions, constraints, risks, unresolved
   questions, the last exchange, and the next recommended branch.
3. Identify the highest-leverage unresolved decision.
4. If repository inspection can answer it, inspect evidence instead of asking.
5. Ask exactly one focused question and include a recommended answer.
6. Wait for the user before moving to the next branch.
7. After the user answers, record the answer in the working context. Do not
   write that routine update to `temp_prd.md` while context is still safe.
8. Run the context metrics checkpoint:

   ```sh
   python3 <SKILLS_ROOT>/codex-usage-metrics/scripts/collect_usage_metrics.py \
     --output <TARGET_SKILL_PATH>/usage-metrics.txt
   ```

9. Read `<TARGET_SKILL_PATH>/usage-metrics.txt` and inspect the `Context`
   section. Continue only when the context-left value is known and greater than
   `55%`, unless the user explicitly requested a handoff.
10. If context left is `<= 55%`, context used is therefore `>= 45%`, or the user
    explicitly requested a handoff, write `<TARGET_SKILL_PATH>/temp_prd.md`,
    overwriting any previous file only after integrating still-relevant prior
    content, then tell the user:

    ```text
    The discussion has been saved to temp_prd.md. Please start a new discussion
    with /decision-grilling-context-45 temp_prd so the grilling can continue
    with the saved context.
    ```

11. If metrics cannot be collected, the metrics receipt is missing, or the
    context-left value is unknown, fail closed: write the best available
    `temp_prd.md`, explain that metrics were unavailable, and give the same
    resume instruction.
12. When enough information has been gathered, stop the grilling loop and
    recommend using `/conversation-to-prd` to create the final PRD. Do not create
    the final PRD automatically unless the user asks.

## `temp_prd.md` Requirements

When writing `temp_prd.md`, include these sections:

```md
# Temp PRD - decision-grilling-context-45

## Resume Command

`/decision-grilling-context-45 temp_prd`

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

If the session was resumed from an earlier `temp_prd.md`, merge prior content
into the new file. Keep current requirements and decisions, preserve unresolved
questions that still matter, remove duplicates, and do not append the old file
verbatim unless the prior content cannot be safely merged.

## Validation

- Questions are sequential, not a questionnaire dump.
- Each question maps to a real dependency or risk.
- Recommendations are grounded in evidence or clearly marked assumptions.
- The metrics checkpoint runs after each user answer.
- `temp_prd.md` is written only at the threshold, on unknown/unavailable
  metrics, or on explicit user handoff request.
- `temp_prd.md` contains the last question and the user's answer.
- Resumed sessions integrate prior `temp_prd.md` content instead of discarding
  it.

## Failure Modes

- Asking broad multi-part questions that block progress.
- Ignoring codebase evidence that could answer the question.
- Letting the interview drift away from implementation-relevant decisions.
- Checking context before the user answer is captured.
- Creating, overwriting, or refreshing `temp_prd.md` after each safe-context
  question.
- Continuing the loop when context metrics are unavailable.
- Overwriting `temp_prd.md` without integrating the prior resumable context.

## Provenance

Derived from a project-specific skill and generalized as a reusable template.
Original project-specific names, paths, assumptions, and private operational
details were removed or replaced with parameters.

## Adaptation Guide

- Replace placeholders with project-specific paths, commands, and authorities.
- Add project-specific validation commands.
- Add domain-specific constraints only when they are required.
- Define how the target project resolves `<SKILLS_ROOT>` and
  `<TARGET_SKILL_PATH>`.
- Preserve the 45% context-used checkpoint unless the target project explicitly
  chooses a different threshold.
- Preserve the reusable procedure unless local evidence shows a better structure.
- Document any project-specific assumptions introduced during adaptation.
