# Init - Sys4AI-dev Runtime Adaptation

Canonical skill ID: `init`
Canonical runtime path: `.agents/skills/init`
Compatibility shim path: `.codex/skills/init/SKILL.md`

## Purpose

Use `/init` as the reversible, gated front door for Sys4AI system definition and adoption.

`/init` classifies the user's situation, inspects available evidence before asking questions, summarizes the current route, and asks for explicit approval before creating controlled discovery records, Product Requirements Documents, system requirements, implementation plans, AgentJobs, or scaffolding.

## Sys4AI-dev Authority Rules

- `Sys4AI-dev` is the development-system runtime surface.
- `Sys4AI/` is the framework-product scaffold being developed.
- `.agents/skills/<skill-id>/` is the active runtime skill surface for this repository.
- `.codex/skills/<skill-id>/SKILL.md` is compatibility-only and must point back to this canonical path.
- `Sys4AI/skills/core/<skill-id>/` is product-scaffold/reference authority, not the active development runtime.
- Root Product Requirements Documents, implementation plans, registries, validators, control records, and git-tracked files outrank generated summaries.
- Generated discovery records, current-state baselines, PRDs, plans, diagrams, warning reports, metrics receipts, and handoffs are derivative work until accepted by the relevant project authority.

## Invocation

```text
/init
/init greenfield
/init brownfield
/init temp_prd
```

Treat `/init` without an argument as a request to classify the situation before choosing a branch.

## When To Use

- The user wants to start Sys4AI system definition or adoption.
- The user invokes `/init`, `/init greenfield`, `/init brownfield`, or `/init temp_prd`.
- A new system needs front-door discovery before requirements, architecture, planning, or scaffold generation.
- An existing repository needs read-only classification before Sys4AI governance adoption.
- The system-of-interest, lifecycle intent, subject layer, stakeholder intent, or downstream route is unclear.

Do not use `/init` to mutate a repository, generate final requirements, install scaffolding, or create Product Requirements Documents without explicit approval.

## Inputs

- User prompt and any `/init` argument.
- Current repository context when running inside an existing project.
- Root PRDs, implementation plans, registries, validators, docs, schemas, tests, Makefiles, control records, and source files when present.
- Optional prior `temp_prd.md`, Requirements Discovery Record, Current-State Baseline, handoff, or stakeholder notes.

## Outputs

- Chat-visible situation classification and evidence summary.
- Identified system-of-interest and subject layer.
- Lifecycle intent: `build`, `improve`, `maintain`, `operate`, `migrate`, or `recover`.
- Recommended branch: `greenfield`, `brownfield`, `partially_built`, or `documentation_recovery`.
- Approval prompt before writing a Requirements Discovery Record, Current-State Baseline, Product Requirements Document, system requirements document, implementation plan, AgentJob, or scaffold.
- Downstream routing recommendation to existing skills after approval.

## Procedure

1. Classify the requested branch.
   - Use `greenfield` when the user wants a new system.
   - Use `brownfield` when a repository or existing system is present.
   - Use `partially_built` when implementation exists but system intent is incomplete.
   - Use `documentation_recovery` when docs or authority surfaces must be reconstructed.
2. Identify the system-of-interest.
3. Classify the subject layer as `development_system`, `framework_product`, `target_system_template`, `target_system_instance`, or `derivative_surface`. Route to `system-layer-classifier` when classification is unclear.
4. Identify lifecycle intent: `build`, `improve`, `maintain`, `operate`, `migrate`, or `recover`.
5. Inspect available repository or document evidence before asking questions that local evidence can answer.
6. Produce a concise classification and evidence summary in chat before writing any controlled artifact.
7. For greenfield work, ask what system the user wants to develop if the system-of-interest is missing.
8. For brownfield work, keep the first pass read-only. Inspect repo structure, README, PRDs, implementation plans, tests, Makefile or CLI entry points, schemas, registries, docs, architecture hints, risks, and existing governance surfaces.
9. Preserve all discovered requirements as `REQ-CAND-*` or `NFR-CAND-*` until promoted by project authority.
10. Use `requirements-discovery-governor` to decide whether discovery is ready, needs more elicitation, or must remain blocked.
11. Ask the required approval prompt before writing a Requirements Discovery Record:

```text
I have enough evidence to create a draft Requirements Discovery Record. Should I write it to the controlled discovery area? This will not modify source code or install scaffolding.
```

12. Ask the required approval prompt before creating a Product Requirements Document:

```text
Discovery is complete. Should I create a Product Requirements Document with `/conversation-to-prd` using the current discovery evidence?
```

13. Ask the required approval prompt before brownfield governance adoption planning:

```text
For this brownfield project, should I create an implementation plan or AgentJob for Sys4AI governance adoption?
```

14. Route downstream only after the relevant approval:
    - `system-definition-interview-context-45` for long discovery.
    - `conversation-to-prd` for approved Product Requirements Document synthesis.
    - `prd-to-implementation-plan` for approved implementation planning.
    - `interface-and-integration-discovery` for unclear external interfaces.
    - `operations-and-maintenance-planner` for maintenance or operations scope.

## Brownfield First-Pass Checklist

Inspect only. Do not write files during the first pass.

- Repository identity and likely system-of-interest.
- README and front-door docs.
- Product Requirements Documents, system requirements, implementation plans, or equivalent.
- Makefile, CLI, scripts, tests, schemas, registries, and control records.
- Architecture hints, interface surfaces, external systems, dependencies, and deployment clues.
- Evidence of source authority, generated derivatives, stale docs, risks, maintenance goals, migration pressures, and missing governance surfaces.

## Required Gates

- No repo mutation during brownfield first-pass inspection.
- No Requirements Discovery Record without explicit approval.
- No Current-State Baseline file without explicit approval.
- No Product Requirements Document without explicit approval.
- No system requirements document without explicit approval.
- No implementation plan or AgentJob without explicit approval.
- No scaffold generation or governance-surface installation without explicit approval.

## Validation

Run:

```bash
python3 scripts/skills/validate_skill_manifest.py --manifest .agents/skills/init/skill.yaml
python3 scripts/skills/validate_skill_manifest.py --bundle .agents/skill_registry/SKILL_BUNDLES/core-systems-engineering.yaml
```

When a discovery record is created, also run the project-local discovery validator if available.

## Failure Modes

- Treating `/init` as immediate scaffold generation.
- Mutating a brownfield repository during first-pass inspection.
- Creating a Product Requirements Document before discovery is coherent and approved.
- Treating candidate requirements as baselined requirements.
- Treating generated derivative material as authority.
- Confusing the active development runtime surface with the product-scaffold reference surface.

