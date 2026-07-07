# Skill Integration Policy

## Purpose

Define how core `Sys4AI` skills are sequenced when agents convert unclear target-system intent into controlled requirements, implementation plans, and validation evidence.

## Core routing sequence

When the user invokes `/init`, `/init greenfield`, `/init brownfield`, or
`/init temp_prd`, use `init` first. `init` is the user-facing front door that
classifies the situation, inspects available evidence, summarizes the route,
and asks for approval before any controlled discovery record, Product
Requirements Document, implementation plan, AgentJob, or scaffold is created.

For brownfield repositories, `/init` first pass is read-only inspection and
classification only.

When target-system intent, boundary, stakeholders, operational scenarios, candidate requirements, architecture drivers, interfaces, or verification seeds are unclear, use this route:

1. `init` when invoked or when adoption/state classification is needed
2. `system-definition-interview` or `system-definition-interview-context-45`
3. `decision-grilling` or `decision-grilling-context-45`
4. `domain-grilling-with-docs` or `domain-grilling-with-docs-context-45`
5. `conversation-to-prd`
6. `prd-to-implementation-plan`

Use the earliest skill that can resolve the present uncertainty. Do not skip to Product Requirements Document synthesis when the system boundary or stakeholder intent is still unclear.

`/init` must ask for explicit approval before creating downstream artifacts.
The required approval prompts are:

```text
I have enough evidence to create a draft Requirements Discovery Record. Should I write it to the controlled discovery area? This will not modify source code or install scaffolding.
```

```text
Discovery is complete. Should I create a Product Requirements Document with `/conversation-to-prd` using the current discovery evidence?
```

```text
For this brownfield project, should I create an implementation plan or AgentJob for Sys4AI governance adoption?
```

## Long-session rule

Use `*-context-45` variants when the interview or clarification work may cross context limits.

Before starting a fresh context-45 workflow, run the `temp_prd.md` archive
preflight. If the invocation includes `temp_prd`, skip this preflight and resume
from the existing checkpoint. If a normal invocation finds an existing
`temp_prd.md`, ask whether it is from a prior context-45 run and should be
archived. Archive only after explicit confirmation, using the helper script and
the path format
`archived_temp_prd/temp_prd_date_yyyy-mm-dd-hh-mm-ss.md`. If the user does not
confirm or does not answer, stop before overwriting or archiving.

Example preflight command:

```text
python3 skills/core/codex-usage-metrics/scripts/archive_temp_prd.py --check --skill-dir skills/core/system-definition-interview-context-45
```

After every user answer in a context-45 workflow:

1. record the answer,
2. run metrics when operational,
3. continue only when context left is known and greater than 55 percent,
4. otherwise write `temp_prd.md` and stop with a resume command.

Do not create, overwrite, or refresh `temp_prd.md` after each question when
context is still safe. `temp_prd.md` is a threshold or fail-closed handoff file,
not the normal per-question state file. If metrics cannot determine context
left, fail closed by writing the best available `temp_prd.md` and stopping.

When a `*-context-45` workflow reaches the end of questioning while context is
still safe, ask exactly:

```text
Questioning is complete. Should I create a PRD with `/conversation-to-prd` using the current discussion and `temp_prd.md` if it exists?
```

Use `/conversation-to-prd` as the canonical command spelling; treat
`/conversation-to-PRD` as the same user-facing intent. If the user says yes,
route the current discussion and any existing `temp_prd.md` into
`conversation-to-prd`. If the user says no, stop with a concise summary and the
logical next step. Do not create the PRD automatically; explicit user
confirmation is required. If the context threshold, unknown context, unavailable
metrics, or explicit handoff request happens before questioning is complete,
write `temp_prd.md` and provide the resume command without asking for PRD
creation yet.

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

The matching `Sys4AI/skills/core/*` folders are product-scaffold templates for future target systems. They must remain generic, portable, and not locked to one execution harness.
