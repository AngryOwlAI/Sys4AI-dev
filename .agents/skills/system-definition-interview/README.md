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

# system-definition-interview

## Purpose

Provide a reusable stakeholder-interview workflow for establishing or
reconstructing system intent before PRDs or formal systems documents are
generated.

## When To Use

- A new, existing, partially built, or poorly documented system needs a
  structured definition interview.
- The mission need, system boundary, stakeholders, as-is state, to-be state,
  ConOps scenarios, requirements candidates, architecture drivers, interfaces,
  or V&V seeds are not yet explicit.
- Existing decision-grilling skills are useful but too narrow because the
  system itself has not been defined.

## What This Skill Produces

- `<OUTPUT_DIRECTORY>/requirements-discovery-record.md`.
- A `System Intent Profile` inside that record.
- Traceable entries using IDs such as `NEED-*`, `STK-*`, `SCN-*`,
  `VISION-CAND-*`, `VALUE-CAND-*`, `WAIVER-CAND-*`, `REQ-CAND-*`,
  `NFR-CAND-*`, `DRV-*`, `IF-*`, `VVE-*`, and `OPEN-*`.
- Routing guidance for decision grilling, terminology review, PRD synthesis, or
  future systems-document generation.

## Required Files

This stored template package contains:

- `SKILL.md`: executable agent instructions.
- `README.md`: human-facing summary and adaptation notes.
- `AGENTS.md`: local maintenance rules for this template.
- `templates/requirements-discovery-record-template.md`: default record format.
- `examples/portable-example.md`: neutral example showing discovery output.
- `skill.yaml`: operating-layer manifest for registry validation.

Target projects may add local templates, scripts, standards, examples, or
reference material when adapting the skill.

## Adaptation Summary

Replace placeholders such as `<PROJECT_ROOT>`, `<PROJECT_AUTHORITY>`,
`<OUTPUT_DIRECTORY>`, and `<VALIDATION_COMMAND>` before installing this
template into a project.

Define whether the generated discovery record is an advisory working artifact,
a review draft, or a controlled source. Preserve trace IDs so later PRDs and
systems documents can connect back to elicitation evidence.

## Validation Summary

A valid adaptation should satisfy these checks:

- The interview classifies the effort as new, existing, partially built, or
  documentation recovery.
- The record separates observations, stakeholder statements, assumptions,
  inferences, and open questions.
- Stakeholders, boundary, scenarios, candidate requirements, quality
  attributes, drivers, interfaces, and V&V seeds are traceable.
- Candidate vision, values, anti-values, missing stakeholders, approval principal, inherited constraints, conflicts, waivers, review cadence, pattern, maturity, autonomy, integrations, communication, monitoring, degraded mode, and promotion evidence are explicit for new or substantially changed targets.
- Structurally valid or model-authored strategic content remains unapproved without accountable human evidence.
- Formal document generation is routed downstream rather than performed inside
  this skill.
