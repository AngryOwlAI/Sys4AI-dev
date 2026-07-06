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

# decision-grilling-context-45

## Purpose

Provide a reusable Socratic design-review workflow that resolves dependencies
between decisions while protecting long interviews from context exhaustion.

This is the long-session variant of `decision-grilling`. It keeps the original
one-question-at-a-time behavior and adds a Codex usage checkpoint after each
user answer.

Do not create, overwrite, or refresh `temp_prd.md` after each question when
context is still safe. Safe-context turns should update only the live working
state and the point-in-time `usage-metrics.txt` receipt.

## When To Use

- The user asks to be grilled, challenged, or stress-tested on a plan and the
  interview may run across multiple discussions.
- A design tree has unresolved branches or hidden assumptions.
- A decision can be clarified by either asking the user or inspecting the codebase.
- A prior session should resume from `temp_prd.md` by invoking
  `/decision-grilling-context-45 temp_prd`.

## What This Skill Produces

- One question at a time.
- A recommended answer for each question.
- A progressively clarified decision tree.
- `usage-metrics.txt` in this skill folder as a refreshed point-in-time metrics
  receipt.
- `temp_prd.md` in this skill folder only when context used reaches 45%,
  context left is 55% or lower, metrics are unavailable/unknown, or the user
  explicitly requests a handoff.
- A resume instruction for `/decision-grilling-context-45 temp_prd`.

## Required Files

This stored template package contains:

- `SKILL.md`: executable agent instructions.
- `README.md`: human-facing summary and adaptation notes.
- `AGENTS.md`: local maintenance rules for this template.
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

- Questions are sequential, not a questionnaire dump.
- Each question maps to a real dependency or risk.
- Recommendations are grounded in evidence or clearly marked assumptions.
- Context metrics are checked after each user answer.
- `temp_prd.md` is not used as the normal per-question state file while context
  remains safe.
- `temp_prd.md` includes the last question, the user answer, gathered
  requirements, unresolved questions, and the resume command.
