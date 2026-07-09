---
name: plantuml-diagrams
description: Generate, review, repair, render, and validate source-grounded PlantUML diagrams with portable include and verification guidance.
adaptation_status: adapter_shell
source_repo: https://github.com/AngryOwlAI/ai-skills-for-sys
source_path: skills/plantuml-diagrams
---

# PlantUML Diagrams

## Purpose

Generate, review, repair, render, and validate source-grounded PlantUML diagrams with portable include and verification guidance.

## When to use

Use this skill when a `Sys4AI` project authority requires the `technical_communication` capability and the governing PRD or implementation plan authorizes skill use.

## Inputs

- Current project authorization.
- Relevant canonical sources.
- Applicable registries.
- Any local validator commands named by explicit project authority.

## Outputs

- A bounded result appropriate to the skill family.
- Source and provenance notes.
- Validation notes or a pass/repair/block decision when applicable.
- Handoff or completion evidence when the project authority requires it.

## Procedure

1. Confirm the project authority authorizes this skill.
2. Read canonical sources before generated derivatives.
3. Apply the upstream skill procedure after local adaptation is completed.
4. Preserve source provenance and document assumptions.
5. Run or name validators before completion.

## Local authority boundaries

- This adapter does not override PRDs, source registries, decision records, or validators.
- Generated notes are derivative unless promoted through source authority.
- Upstream skill text must be reviewed before this adapter is marked `adapted`.

## Validation

Run:

```bash
cd Sys4AI && make validate-skills
```

## Known failure modes

- Using the skill without explicit project authority.
- Treating upstream placeholders as local facts.
- Producing output that is not traceable to canonical sources.
- Marking the adapter as fully adapted before local review.
