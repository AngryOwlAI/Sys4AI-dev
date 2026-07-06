# Portable example for `domain-grilling-with-docs-context-45`

## Scenario

A `sys-for-ai` implementation agent receives an AgentJob requiring `domain_documentation_clarification` support.

## Minimal use

1. Read the AgentJob objective and allowed files.
2. Read canonical sources before generated notes.
3. On normal invocation without `temp_prd`, run `archive_temp_prd.py --check`; if a prior checkpoint exists, ask before archiving it.
4. When invoked with `temp_prd`, skip the archive preflight and resume from the checkpoint.
5. Ask one focused documentation or terminology question and record the answer in working context.
6. Refresh `usage-metrics.txt` after the answer.
7. Continue when context left is known and greater than 55 percent.
8. Write `temp_prd.md` only when context used is at least 45 percent, context left is at most 55 percent, metrics are unavailable or unknown, or the user explicitly requests a handoff.
9. When questioning is complete, ask whether to create a PRD with `/conversation-to-prd`.
10. Produce bounded output with provenance notes if the user declines PRD creation.
11. Run the named validator or record why it could not be run.

## Example PRD handoff

```text
Questioning is complete. Should I create a PRD with `/conversation-to-prd` using the current discussion and `temp_prd.md` if it exists?
```

If the user says yes, route the current discussion and any existing
`temp_prd.md` into `/conversation-to-prd`. If the user says no, stop with a
concise summary and next step. Do not create the PRD automatically.

## Example output shape

```text
Skill: domain-grilling-with-docs-context-45
Status: pass | repair | block
Sources used:
- <source path or source ID>
Output:
- <bounded result>
Validation:
- <command or reasoning>
Checkpoint:
- Do not create, overwrite, or refresh temp_prd.md after each question when context is still safe.
- Archive confirmed prior checkpoints as archived_temp_prd/temp_prd_date_yyyy-mm-dd-hh-mm-ss.md.
- PRD creation requires explicit user confirmation.
```
