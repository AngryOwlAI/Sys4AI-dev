# Domain Grilling With Docs Context 45 - sys-for-ai-dev Runtime Adaptation

Canonical skill ID: `domain-grilling-with-docs-context-45`  
Canonical runtime path: `.agents/skills/domain-grilling-with-docs-context-45`  
Compatibility shim path: `.codex/skills/domain-grilling-with-docs-context-45/SKILL.md`  
Source import: `skills/domain-grilling-with-docs-context-45` from `/Volumes/P-SSD/AngryOwl/ai-skills-for-sys`

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
name: domain-grilling-with-docs-context-45
description: Stress-test a plan against project language one question at a time, checking Codex context after each answer and saving temp_prd.md only when context used reaches 45%, metrics are unavailable, or the user explicitly requests a handoff.
---

# domain-grilling-with-docs-context-45

## Purpose

Provide a reusable workflow for clarifying domain terminology, surfacing
contradictions between plans and code, and recording stable glossary or
architecture decisions while protecting long interviews from exhausting the
Codex context window.

This variant preserves the documentation-aware one-question loop from
`domain-grilling-with-docs` and adds a context checkpoint after each user
answer. When context used reaches 45% or more of the available window, the skill
writes a resumable `temp_prd.md` in this skill folder and instructs the user to
continue in a new discussion with the `temp_prd` parameter.

Do not create, overwrite, or refresh `temp_prd.md` after each question when
context is still safe. During normal safe-context turns, keep the evolving state
in the live working context, approved glossary/context files, ADR candidates, or
chat summary, and refresh only `usage-metrics.txt`.

## When To Use

- The user wants a grilling session grounded in existing docs or domain language
  and the interview may run long.
- Terms are overloaded, fuzzy, or inconsistent with the project glossary.
- A decision may warrant an ADR because it is hard to reverse, surprising, and tradeoff-heavy.
- A prior `temp_prd.md` should be used to resume a multi-discussion
  documentation-aware grilling session.

## Inputs

- The plan or design under review.
- <CONTEXT_FILE> or <CONTEXT_MAP> when present.
- <ADR_DIRECTORY> when present.
- `templates/context-format.md` and `templates/adr-format.md` from this skill
  package, unless the target project provides a local replacement.
- Repository code and tests for evidence checks.
- Optional `temp_prd` parameter, meaning read this skill folder's
  `temp_prd.md` before asking the next question.
- `<SKILLS_ROOT>` containing `codex-usage-metrics`.
- `<TARGET_SKILL_PATH>` for this skill folder.

## Outputs

- Sequential questions with recommendations.
- Updated glossary/context entries when terms are resolved.
- Optional ADRs for qualifying decisions.
- `usage-metrics.txt` in this skill folder after each context check.
- `temp_prd.md` in this skill folder when context used is `>= 45%`, context
  left is `<= 55%`, metrics cannot be collected, context left is unknown, or
  the user explicitly requests a handoff.
- `archived_temp_prd/temp_prd_date_yyyy-mm-dd-hh-mm-ss.md` when the user
  confirms an existing checkpoint is from a prior context-45 run and should be
  archived before a fresh session.
- A resume instruction using `/domain-grilling-with-docs-context-45 temp_prd`.

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
   `domain-grilling-with-docs-context-45` run and should be archived before
   starting a fresh session. If the user confirms, run:

   ```sh
   python3 <SKILLS_ROOT>/codex-usage-metrics/scripts/archive_temp_prd.py \
     --confirm-archive --skill-dir <TARGET_SKILL_PATH>
   ```

   The archive path format is
   `<TARGET_SKILL_PATH>/archived_temp_prd/temp_prd_date_yyyy-mm-dd-hh-mm-ss.md`.
   If the user does not confirm or does not answer, stop; do not overwrite or
   archive the existing checkpoint.
3. Initialize or refresh the working context: objective, discussion summary,
   gathered requirements, confirmed decisions, constraints, risks, unresolved
   questions, terminology decisions, glossary/context updates, ADR candidates,
   documentation evidence, the last exchange, and the next recommended branch.
4. Discover whether the repository uses one context file or a context map with multiple bounded contexts.
5. Use `templates/context-format.md` as the default glossary format unless the
   target project has already defined a local format.
6. Use `templates/adr-format.md` as the default ADR format unless the target
   project has already defined a local format.
7. Create glossary or ADR files lazily only when there is settled content to record.
8. When the user uses a conflicting term, surface the conflict immediately.
9. Use concrete scenarios and code inspection to test boundaries between concepts.
10. Ask exactly one focused question and include a recommended answer.
11. Wait for the user before moving to the next branch.
12. After the user answers, record the answer in the working context. Do not
    write that routine update to `temp_prd.md` while context is still safe.
13. Update <CONTEXT_FILE> inline when a term is resolved, keeping it free of implementation details.
14. Offer an ADR only when the decision is hard to reverse, surprising without context, and based on a real tradeoff.
15. Run the context metrics checkpoint:

   ```sh
   python3 <SKILLS_ROOT>/codex-usage-metrics/scripts/collect_usage_metrics.py \
     --output <TARGET_SKILL_PATH>/usage-metrics.txt
   ```

16. Read `<TARGET_SKILL_PATH>/usage-metrics.txt` and inspect the `Context`
    section. Continue only when the context-left value is known and greater than
    `55%`, unless the user explicitly requested a handoff.
17. If context left is `<= 55%`, context used is therefore `>= 45%`, or the user
    explicitly requested a handoff, write `<TARGET_SKILL_PATH>/temp_prd.md`,
    overwriting any previous file only after integrating still-relevant prior
    content, then tell the user:

    ```text
    The discussion has been saved to temp_prd.md. Please start a new discussion
    with /domain-grilling-with-docs-context-45 temp_prd so the grilling can
    continue with the saved context.
    ```

18. If metrics cannot be collected, the metrics receipt is missing, or the
    context-left value is unknown, fail closed: write the best available
    `temp_prd.md`, explain that metrics were unavailable, and give the same
    resume instruction.
19. If context threshold, unknown context, unavailable metrics, or explicit
    handoff happens before questioning is complete, do not ask for PRD creation
    yet; write `temp_prd.md` and give the resume instruction.
20. When enough information has been gathered and questioning is complete, ask:

    ```text
    Questioning is complete. Should I create a PRD with `/conversation-to-prd` using the current discussion and `temp_prd.md` if it exists?
    ```

    Use `/conversation-to-prd` as the canonical command spelling; treat
    `/conversation-to-PRD` as the same user-facing intent. If the user says yes,
    route to `/conversation-to-prd` with the current discussion and any existing
    `<TARGET_SKILL_PATH>/temp_prd.md`. If the user says no, stop with a concise
    summary and the logical next step. Do not create the PRD automatically.

## `temp_prd.md` Requirements

When writing `temp_prd.md`, include these sections:

```md
# Temp PRD - domain-grilling-with-docs-context-45

## Resume Command

`/domain-grilling-with-docs-context-45 temp_prd`

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

If the session was resumed from an earlier `temp_prd.md`, merge prior content
into the new file. Keep current requirements and decisions, preserve unresolved
questions that still matter, carry forward relevant terminology and ADR context,
remove duplicates, and do not append the old file verbatim unless the prior
content cannot be safely merged.

## Validation

- Glossary entries define domain language, not implementation details.
- ADRs are used sparingly and explain the tradeoff.
- Code contradictions are reported with evidence.
- Questions remain one at a time.
- The metrics checkpoint runs after each user answer.
- On normal invocation without `temp_prd`, the archive preflight runs before
  any fresh-session work.
- Resume invocation with `temp_prd` skips the archive preflight.
- `temp_prd.md` is written only at the threshold, on unknown/unavailable
  metrics, or on explicit user handoff request.
- `temp_prd.md` contains the last question and the user's answer.
- Resumed sessions integrate prior requirements, terminology, and ADR context
  instead of discarding it.
- At the end of questioning, the agent asks whether to create a PRD with
  `/conversation-to-prd` using the current discussion and `temp_prd.md` if it
  exists, and waits for explicit confirmation.

## Failure Modes

- Turning the glossary into a spec or scratchpad.
- Creating ADRs for obvious or reversible choices.
- Accepting user terminology that contradicts existing project language without resolving it.
- Checking context before the user answer is captured.
- Creating, overwriting, or refreshing `temp_prd.md` after each safe-context
  question.
- Continuing the loop when context metrics are unavailable.
- Overwriting `temp_prd.md` without integrating the prior resumable context.
- Archiving or overwriting an existing `temp_prd.md` without explicit user
  confirmation during a fresh invocation.
- Creating a PRD automatically instead of asking at the end of questioning.

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
