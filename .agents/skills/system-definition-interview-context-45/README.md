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

# system-definition-interview-context-45

## Purpose

Provide the long-session variant of `system-definition-interview`. It
establishes or reconstructs system intent while protecting extended stakeholder
interviews with context checkpoints and resumable `temp_prd.md` handoff.

Do not create, overwrite, or refresh `temp_prd.md` after each question when
context is still safe. Safe-context turns should update only the discovery
record or live working state and the point-in-time `usage-metrics.txt` receipt.

## When To Use

- A system-definition interview may run across multiple discussions.
- A prior session should resume from `temp_prd.md` by invoking
  `/system-definition-interview-context-45 temp_prd`.
- The work needs the same traceable discovery record as
  `system-definition-interview`, plus context-aware continuation behavior.

## What This Skill Produces

- `<OUTPUT_DIRECTORY>/requirements-discovery-record.md`.
- A `System Intent Profile` inside that record.
- Traceable entries using IDs such as `NEED-*`, `STK-*`, `SCN-*`,
  `REQ-CAND-*`, `NFR-CAND-*`, `DRV-*`, `IF-*`, `VVE-*`, and `OPEN-*`.
- `usage-metrics.txt` in this skill folder after each context check.
- `temp_prd.md` in this skill folder only when context used reaches 45 percent,
  context left is 55 percent or lower, metrics are unavailable/unknown, or the
  user explicitly requests a handoff.
- A resume instruction for `/system-definition-interview-context-45 temp_prd`.

## Required Files

This stored template package contains:

- `SKILL.md`: executable agent instructions.
- `README.md`: human-facing summary and adaptation notes.
- `AGENTS.md`: local maintenance rules for this template.
- `templates/requirements-discovery-record-template.md`: default record format.
- `examples/portable-example.md`: neutral example showing checkpoint behavior.
- `skill.yaml`: operating-layer manifest for registry validation.

Runtime files are generated only during use:

- `usage-metrics.txt`
- `temp_prd.md`

## Adaptation Summary

Replace placeholders such as `<PROJECT_ROOT>`, `<PROJECT_AUTHORITY>`,
`<OUTPUT_DIRECTORY>`, `<VALIDATION_COMMAND>`, `<SKILLS_ROOT>`, and
`<TARGET_SKILL_PATH>` before installing this template into a project.

Do not duplicate the `codex-usage-metrics` collector. Adapt this skill to call
the adjacent metrics dependency and fail closed to `temp_prd.md` when metrics
are unavailable.

## Validation Summary

A valid adaptation should satisfy these checks:

- Context metrics are checked after each user answer.
- `temp_prd.md` is not used as the normal per-question state file while context
  remains safe.
- `temp_prd.md` includes the last question, the user answer, System Intent
  Profile status, trace IDs, open questions, metrics snapshot, and resume
  command.
- Resumed sessions merge prior context instead of discarding it.
- Formal document generation remains a downstream route, not part of this
  skill.
