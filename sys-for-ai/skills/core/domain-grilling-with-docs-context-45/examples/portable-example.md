# Portable example for `domain-grilling-with-docs-context-45`

## Scenario

A `sys-for-ai` implementation agent receives an AgentJob requiring `domain_documentation_clarification` support.

## Minimal use

1. Read the AgentJob objective and allowed files.
2. Read canonical sources before generated notes.
3. Ask one focused documentation or terminology question and record the answer in working context.
4. Refresh `usage-metrics.txt` after the answer.
5. Continue when context left is known and greater than 55 percent.
6. Write `temp_prd.md` only when context used is at least 45 percent, context left is at most 55 percent, metrics are unavailable or unknown, or the user explicitly requests a handoff.
7. Produce bounded output with provenance notes.
8. Run the named validator or record why it could not be run.

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
```
