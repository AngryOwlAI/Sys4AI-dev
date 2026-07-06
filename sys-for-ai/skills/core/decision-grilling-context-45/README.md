# Decision Grilling Context 45

## Status

Adapter shell for the core `sys-for-ai` skill `decision-grilling-context-45`.

## Source

- Repository: `https://github.com/AngryOwlAI/ai-skills-for-sys`
- Path: `skills/decision-grilling-context-45`

## Purpose

Long-session decision grilling that checkpoints resumable context when Codex context usage reaches the defined threshold.

This adapter checks context metrics after each user answer, but it writes
`temp_prd.md` only at the handoff threshold, on unavailable/unknown metrics, or
on explicit user request.

Do not create, overwrite, or refresh `temp_prd.md` after each question when
context is still safe.

When questioning is complete, ask whether to create a PRD with
`/conversation-to-prd` using the current discussion and `temp_prd.md` if it
exists. Do not create the PRD automatically.

## Archive preflight

On normal invocation without `temp_prd`, run
`skills/core/codex-usage-metrics/scripts/archive_temp_prd.py --check` against
this skill folder before starting fresh work. If an existing `temp_prd.md` is
found, ask whether it is from a prior `decision-grilling-context-45` run and
should be archived. Only after explicit confirmation, run the same helper with
`--confirm-archive`.

Resume invocation with `temp_prd` skips this archive preflight and reads the
existing checkpoint. Confirmed archives use
`archived_temp_prd/temp_prd_date_yyyy-mm-dd-hh-mm-ss.md`.

## Metrics policy

Use `skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py` and write
the receipt to `skills/core/decision-grilling-context-45/usage-metrics.txt`.
If context left is unknown or at most 55 percent, write
`skills/core/decision-grilling-context-45/temp_prd.md` and stop.

## Adaptation work remaining

1. Compare this adapter shell with the current upstream template.
2. Replace generic placeholders with local `sys-for-ai` paths, validators, and authority boundaries.
3. Keep the threshold-only `temp_prd.md` timing and archive-preflight rules synchronized with `SKILL.md`.
4. Keep the end-of-questioning PRD handoff prompt synchronized with `SKILL.md`.
5. Update `skills/core_skill_manifest.yaml` and `registries/skill_registry.csv`.
6. Mark status as `adapted` only after review.
