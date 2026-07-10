# System Definition Interview Context 45 - Sys4AI-dev Runtime Adaptation

Canonical skill ID: `system-definition-interview-context-45`  
Canonical runtime path: `.agents/skills/system-definition-interview-context-45`  
Compatibility shim path: `.codex/skills/system-definition-interview-context-45/SKILL.md`  
Source import: `skills/system-definition-interview-context-45` from `/Volumes/P-SSD/AngryOwl/ai-skills-for-sys`

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

Maintain `system-definition-interview-context-45` as a reusable long-session
template skill. It should preserve the system-definition interview workflow
while adding context-window checkpoints and resumable `temp_prd.md` handoff
behavior.

In `Sys4AI-dev`, preserve its role as the default discovery gate for new or
substantially changed system definitions. The gate must classify the subject
layer and produce or update a Requirements Discovery Record before downstream
USRD, PRD, SRD, ARD, TRP, or SRP generation.

## Maintenance Rules

- Keep `SKILL.md`, `README.md`, `AGENTS.md`, `skill.yaml`, templates, and
  examples synchronized when the workflow changes.
- Preserve placeholders for project-specific paths, commands, authorities,
  registries, standards, output directories, and validation commands.
- Do not add local absolute paths, repository names, branch names, task IDs,
  credentials, non-public URLs, or organization-specific operational state.
- Do not duplicate the `codex-usage-metrics` collector. This skill should call
  it as a required adjacent template dependency.
- Do not create, overwrite, or refresh `temp_prd.md` after each question when
  context is still safe.
- Keep the end-of-questioning `/conversation-to-prd` prompt synchronized across
  `SKILL.md`, `README.md`, examples, and `skill.yaml`.
- Keep discovery gate rules synchronized across runtime docs, product scaffold
  adapter docs, and the RDR template.
- Keep examples neutral and portable.
- Treat `usage-metrics.txt` and `temp_prd.md` as runtime artifacts, not static
  template content.

## Portability Requirements

- Use parameters such as `<PROJECT_ROOT>`, `<PROJECT_AUTHORITY>`,
  `<OUTPUT_DIRECTORY>`, and `<VALIDATION_COMMAND>` for target-specific values.
- Use `<SKILLS_ROOT>` and `<TARGET_SKILL_PATH>` for context-metrics and runtime
  file paths.
- Treat generated records as derivatives unless the target project explicitly
  baselines them.
- Keep candidate requirements labeled as candidates until target-project
  authority approves them.
- Keep candidate strategic intent labeled `VISION-CAND-*` and `VALUE-CAND-*`; checkpoint anti-values, missing stakeholders, human approval identity, conflicts, waiver state, and review cadence.
- Do not treat silence, model authorship, controlled-file location, or structural validation as approval.

## Validation Requirements

Before finalizing changes to this template, check that:

- The skill can be understood without access to any source project.
- Required inputs and expected outputs are explicit.
- The 45 percent context-used threshold is documented as equivalent to 55
  percent context left.
- Resume behavior from `temp_prd.md` is explicit.
- Threshold-only `temp_prd.md` creation is explicit.
- PRD creation is user-gated and uses the current discussion plus
  `temp_prd.md` when it exists.
- The record template includes stable trace IDs.
- The record template includes system layer classification and discovery gate
  exit checklist sections.
- No hard-coded local source paths or project-bound names remain.

## Adaptation Instructions

When adapting this template into a target project, replace placeholders, add
project-specific authority rules, add validation commands, document new
assumptions, define metrics paths, and run the target project's own checks
before relying on the adapted skill.
