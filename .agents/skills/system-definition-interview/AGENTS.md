# System Definition Interview - Sys4AI-dev Runtime Adaptation

Canonical skill ID: `system-definition-interview`  
Canonical runtime path: `.agents/skills/system-definition-interview`  
Compatibility shim path: `.codex/skills/system-definition-interview/SKILL.md`  
Source import: `skills/system-definition-interview` from `/Volumes/P-SSD/AngryOwl/ai-skills-for-sys`

## Sys4AI-dev Authority Rules

- Root PRDs, implementation plans, source registries, validators, and git-tracked files outrank generated outputs.
- `Sys4AI/` is the product scaffold being developed; it is not the full development workspace.
- `.agents/skills/<skill-id>/` is the active runtime skill surface for this repository.
- `.codex/skills/<skill-id>/SKILL.md` is compatibility-only and must point back to this canonical path.
- Existing `Sys4AI/skills/core/` files are scaffold and product-reference adapters, not the active runtime authority.
- Do not import local receipts, caches, generated `usage-metrics.txt`, or private operational state as skill source.
- Treat generated PRDs, plans, diagrams, warnings, and handoffs as derivative work until accepted by the relevant project authority.

The imported source guidance below remains valid where it does not conflict with these Sys4AI-dev rules.

---

# AGENTS.md

## Local Mission

Maintain `system-definition-interview` as a reusable elicitation-layer template
skill for establishing or reconstructing system intent before downstream PRD,
requirements-analysis, or systems-document work.

## Maintenance Rules

- Keep `SKILL.md`, `README.md`, `AGENTS.md`, `skill.yaml`, templates, and
  examples synchronized when the workflow changes.
- Preserve placeholders for project-specific paths, commands, authorities,
  registries, standards, output directories, and validation commands.
- Do not add local absolute paths, repository names, branch names, task IDs,
  credentials, non-public URLs, or organization-specific operational state.
- Keep examples neutral and portable.
- Add scripts only when they are portable and documented.
- Keep the skill focused on elicitation and traceable discovery records; route
  formal document generation to downstream skills.

## Portability Requirements

- Use parameters such as `<PROJECT_ROOT>`, `<PROJECT_AUTHORITY>`,
  `<OUTPUT_DIRECTORY>`, and `<VALIDATION_COMMAND>` for target-specific values.
- Treat generated records as derivatives unless the target project explicitly
  baselines them.
- Keep candidate requirements labeled as candidates until target-project
  authority approves them.
- Keep vision and core-value candidates labeled `VISION-CAND-*` and `VALUE-CAND-*`; record anti-values, missing stakeholders, accountable approval identity, conflicts, waivers, and review cadence.
- Do not treat silence, model authorship, controlled-file location, or structural validation as approval.
- Avoid assumptions about framework, package manager, operating system, file
  layout, organization, or domain.

## Validation Requirements

Before finalizing changes to this template, check that:

- The skill can be understood without access to any source project.
- Required inputs and expected outputs are explicit.
- The record template includes stable trace IDs.
- Validation and failure modes match the procedure.
- No hard-coded local source paths or project-bound names remain.
- Downstream routing remains separate from elicitation.

## Adaptation Instructions

When adapting this template into a target project, replace placeholders, add
project-specific authority rules, add validation commands, document new
assumptions, and run the target project's own checks before relying on the
adapted skill.
