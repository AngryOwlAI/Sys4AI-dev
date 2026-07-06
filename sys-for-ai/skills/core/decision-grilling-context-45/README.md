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

## Metrics policy

Use `skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py` and write
the receipt to `skills/core/decision-grilling-context-45/usage-metrics.txt`.
If context left is unknown or at most 55 percent, write
`skills/core/decision-grilling-context-45/temp_prd.md` and stop.

## Adaptation work remaining

1. Compare this adapter shell with the current upstream template.
2. Replace generic placeholders with local `sys-for-ai` paths, validators, and authority boundaries.
3. Keep the threshold-only `temp_prd.md` timing rule synchronized with `SKILL.md`.
4. Update `skills/core_skill_manifest.yaml` and `registries/skill_registry.csv`.
5. Mark status as `adapted` only after review.
