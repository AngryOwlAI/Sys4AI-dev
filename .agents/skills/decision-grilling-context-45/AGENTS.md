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

# AGENTS.md

## Local Mission

Maintain `decision-grilling-context-45` as a reusable long-session template
skill. It should preserve the portable decision-grilling workflow while adding
context-window checkpoints and resumable `temp_prd.md` handoff behavior.

## Maintenance Rules

- Keep `SKILL.md`, `README.md`, and `AGENTS.md` synchronized when the workflow changes.
- Keep `examples/portable-example.md` synchronized with the context-check and
  resume behavior.
- Keep the end-of-questioning `/conversation-to-prd` prompt synchronized across
  `SKILL.md`, `README.md`, examples, and `skill.yaml`.
- Preserve placeholders for project-specific paths, commands, authorities, registries, tools, and output directories.
- Do not add secrets, private URLs, absolute local paths, branch names, task IDs, or organization-specific operational state.
- Add scripts, templates, or examples only when they are portable and documented.
- Keep instructions specific enough for a future agent to execute after adaptation.
- Do not duplicate the `codex-usage-metrics` collector. This skill should call
  it as a sub-skill or adjacent template dependency.

## Portability Requirements

- Use parameters such as `<PROJECT_ROOT>`, `<VALIDATION_COMMAND>`, `<OUTPUT_DIRECTORY>`, and `<PROJECT_AUTHORITY>` for target-specific values.
- Use `<SKILLS_ROOT>` and `<TARGET_SKILL_PATH>` for context-metrics and runtime
  file paths.
- Explain any required external tool or API as an adaptation dependency.
- Keep generated artifacts non-authoritative unless the target project explicitly defines them as authority.
- Treat `usage-metrics.txt` and `temp_prd.md` as runtime artifacts, not static
  template content.
- Do not create, overwrite, or refresh `temp_prd.md` after each question when
  context is still safe.

## Validation Requirements

Before finalizing changes to this template, check that:

- The skill can be understood without access to the source project.
- Required inputs and expected outputs are explicit.
- The validation and failure modes still match the procedure.
- No hard-coded local source paths or private project names remain.
- The 45% context-used threshold is documented as equivalent to 55% context
  left.
- Resume behavior from `temp_prd.md` is explicit.
- Threshold-only `temp_prd.md` creation is explicit.
- PRD creation is user-gated and uses the current discussion plus
  `temp_prd.md` when it exists.

## Adaptation Instructions

When adapting this template into a target project, replace placeholders, add
project-specific commands, document new assumptions, and run the target
project's own validation before relying on the adapted skill.
