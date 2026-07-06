# Skill Integration Policy

## Purpose

Define how core `sys-for-ai` skills are sequenced when agents convert unclear target-system intent into controlled requirements, implementation plans, and validation evidence.

## Core routing sequence

When target-system intent, boundary, stakeholders, operational scenarios, candidate requirements, architecture drivers, interfaces, or verification seeds are unclear, use this route:

1. `system-definition-interview` or `system-definition-interview-context-45`
2. `decision-grilling` or `decision-grilling-context-45`
3. `domain-grilling-with-docs` or `domain-grilling-with-docs-context-45`
4. `conversation-to-prd`
5. `prd-to-implementation-plan`

Use the earliest skill that can resolve the present uncertainty. Do not skip to Product Requirements Document synthesis when the system boundary or stakeholder intent is still unclear.

## Long-session rule

Use `*-context-45` variants when the interview or clarification work may cross context limits.

After every user answer in a context-45 workflow:

1. record the answer,
2. run metrics when operational,
3. continue only when context left is known and greater than 55 percent,
4. otherwise write `temp_prd.md` and stop with a resume command.

Do not create, overwrite, or refresh `temp_prd.md` after each question when
context is still safe. `temp_prd.md` is a threshold or fail-closed handoff file,
not the normal per-question state file. If metrics cannot determine context
left, fail closed by writing the best available `temp_prd.md` and stopping.

For `system-definition-interview-context-45`, the resume command is:

```text
/system-definition-interview-context-45 temp_prd
```

## Authority rule

No skill output overrides canonical sources, registries, Product Requirements Documents, decision records, validators, or AgentJobs.

Discovery records and temporary handoff files are controlled evidence only when they are registered or authorized by an AgentJob. Candidate requirements must remain `REQ-CAND-*` or `NFR-CAND-*` until a source-authority workflow promotes them.

## Integration rule

Upstream skills from `ai-skills-for-sys` must be adapted locally before they are marked `adapted`. Adapter shells must preserve provenance, local authority boundaries, required files, validation commands, known failure modes, and adaptation work remaining.

## Continuation and memory surfaces

The active development-runtime surfaces for continuation and source-first memory live under `.agents/skills/continue/` and `.agents/skills/source-first-memory/`.

The matching `.codex/skills/*/SKILL.md` files are compatibility shims only. They point to the `.agents` runtime surfaces and should not carry independent behavior.

The matching `sys-for-ai/skills/core/*` folders are product-scaffold templates for future target systems. They must remain generic, portable, and not locked to one execution harness.
