# Portable Example: Resolving Readiness Terminology With Context Guard

## Scenario

The team uses "ready," "approved," and "green" interchangeably when discussing
release status. Repository evidence shows these terms are not equivalent. The
terminology grilling session may continue long enough to need a context handoff.

## Skill Role In The Chain

Use `domain-grilling-with-docs-context-45` when terminology affects the PRD,
dashboard labels, or future architecture decisions, and the interview may need
to continue across multiple discussions.

## Example Inputs

- Plan under review: "Show whether a release is ready."
- `<CONTEXT_FILE>`: glossary, domain-language document, or context map.
- `<ADR_DIRECTORY>`: optional location for architecture decision records.
- Repository evidence: release policy and CI status conventions.
- Optional resume parameter: `/domain-grilling-with-docs-context-45 temp_prd`.

## Example Interaction

```text
Analysis:
The term "ready" is ambiguous. The release policy distinguishes technical
checks from approval, while the proposed dashboard label collapses them.

Question:
Should "release ready" mean "technical checks passed" or "approved to deploy"?

Recommendation:
Use "checks passed" for the dashboard state unless the approval source is also
integrated. Reserve "approved" for an explicit human or policy approval record.
```

After the user answers, the agent records the answer and runs:

```sh
python3 <SKILLS_ROOT>/codex-usage-metrics/scripts/collect_usage_metrics.py \
  --output <TARGET_SKILL_PATH>/usage-metrics.txt
```

When context remains above the safe threshold, the agent continues the interview
without creating, overwriting, or refreshing `temp_prd.md`.

## Example Documentation Update

```md
## Glossary Entry

`checks passed`: Automated required checks are passing according to configured
source systems.

`approved`: A human or policy approval record permits deployment. This is not
implied by `checks passed`.
```

## Example Context Handoff

If `usage-metrics.txt` reports context left at `55%` or lower, the agent writes
`<TARGET_SKILL_PATH>/temp_prd.md` with gathered requirements, confirmed
decisions, unresolved questions, terminology conflicts, glossary/context
updates, ADR candidates, documentation evidence, last question, user answer,
metrics snapshot, and this resume command:

```text
/domain-grilling-with-docs-context-45 temp_prd
```

## Validation

- The glossary records domain language, not implementation detail.
- Any ADR is created only if the term choice is hard to reverse or materially
  affects architecture.
- Contradictions between user wording and source documents are explicit.
- The context check happens after the user answer.
- `temp_prd.md` is written only at the handoff threshold, on unavailable/unknown
  metrics, or on explicit user request.
- The handoff file contains enough requirements and terminology context to
  resume without restarting the interview.

## Adaptation Notes

Replace `<CONTEXT_FILE>` and `<ADR_DIRECTORY>` with the target project's
documentation locations only during adaptation. Preserve the context checkpoint
unless the target project explicitly chooses a different threshold.
