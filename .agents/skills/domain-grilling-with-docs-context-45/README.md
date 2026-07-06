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

# domain-grilling-with-docs-context-45

## Purpose

Provide a reusable workflow for clarifying domain terminology, surfacing
contradictions between plans and code, and recording stable glossary or
architecture decisions while protecting long interviews from context
exhaustion.

This is the long-session variant of `domain-grilling-with-docs`. It keeps the
original documentation-aware one-question behavior and adds a Codex usage
checkpoint after each user answer.

Do not create, overwrite, or refresh `temp_prd.md` after each question when
context is still safe. Safe-context turns should update only the live working
state, approved documentation artifacts, and the point-in-time
`usage-metrics.txt` receipt.

## When To Use

- The user wants a grilling session grounded in existing docs or domain language
  and the interview may run across multiple discussions.
- Terms are overloaded, fuzzy, or inconsistent with the project glossary.
- A decision may warrant an ADR because it is hard to reverse, surprising, and tradeoff-heavy.
- A prior session should resume from `temp_prd.md` by invoking
  `/domain-grilling-with-docs-context-45 temp_prd`.

## What This Skill Produces

- Sequential questions with recommendations.
- Updated glossary/context entries when terms are resolved.
- Optional ADRs for qualifying decisions.
- `usage-metrics.txt` in this skill folder as a refreshed point-in-time metrics
  receipt.
- `temp_prd.md` in this skill folder only when context used reaches 45%,
  context left is 55% or lower, metrics are unavailable/unknown, or the user
  explicitly requests a handoff.
- A resume instruction for `/domain-grilling-with-docs-context-45 temp_prd`.
- An end-of-questioning prompt asking whether to create a PRD with
  `/conversation-to-prd` using the current discussion and `temp_prd.md` if it
  exists.

## Required Files

This stored template package contains:

- `SKILL.md`: executable agent instructions.
- `README.md`: human-facing summary and adaptation notes.
- `AGENTS.md`: local maintenance rules for this template.
- `templates/context-format.md`: portable glossary/context format guidance.
- `templates/adr-format.md`: portable ADR format and qualification guidance.
- `examples/portable-example.md`: portable example with context-check behavior.

Target projects may add `templates/`, `scripts/`, `examples/`, or reference material when adapting the skill.

Runtime files are generated only during use:

- `usage-metrics.txt`
- `temp_prd.md`

## Adaptation Summary

Replace placeholders such as `<PROJECT_ROOT>`, `<VALIDATION_COMMAND>`,
`<OUTPUT_DIRECTORY>`, and any domain-specific registry, role, source, or tool
names before installing this template into a project.

Also define `<SKILLS_ROOT>` and `<TARGET_SKILL_PATH>` so the skill can call
`codex-usage-metrics` and save its runtime files in the active skill folder.

Preserve the reusable workflow, but add project-specific authority boundaries,
commands, and stop conditions only when local evidence requires them.

## Validation Summary

A valid adaptation should satisfy these checks:

- Glossary entries define domain language, not implementation details.
- ADRs are used sparingly and explain the tradeoff.
- Code contradictions are reported with evidence.
- Questions remain one at a time.
- Context metrics are checked after each user answer.
- `temp_prd.md` is not used as the normal per-question state file while context
  remains safe.
- `temp_prd.md` includes the last question, the user answer, gathered
  requirements, terminology context, ADR candidates, unresolved questions, and
  the resume command.
- PRD creation is explicitly user-gated and never automatic.
