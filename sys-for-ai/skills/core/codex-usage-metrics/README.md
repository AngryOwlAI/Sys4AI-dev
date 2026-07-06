# Codex Usage Metrics

## Status

Adapter shell for the core `sys-for-ai` skill `codex-usage-metrics`.

## Source

- Repository: `https://github.com/AngryOwlAI/ai-skills-for-sys`
- Path: `skills/codex-usage-metrics`

## Purpose

Capture Codex app context, token, and rate-limit metrics into a refreshed local receipt without exporting conversation content.

This adapter is operational for local Codex session metrics through `scripts/collect_usage_metrics.py`. It is not an OpenAI API billing reporter, ChatGPT usage reporter, or generic telemetry tool.

## Local command

```bash
cd sys-for-ai
.venv/bin/python skills/core/codex-usage-metrics/scripts/collect_usage_metrics.py --help
make validate-metrics
```

## Local authority

Metrics receipts are point-in-time implementation evidence. They do not override AgentJobs, canonical PRDs, source registries, decision records, or validators.

When a context-45 adapter cannot collect metrics or cannot determine context left, it must fail closed by writing resumable context and stopping.

## Adaptation work remaining

1. Compare this adapter shell with the current upstream template.
2. Replace generic placeholders with local `sys-for-ai` paths, validators, and authority boundaries.
3. Add structured receipt validation if future adapters require more than `--help` validation.
4. Update `skills/core_skill_manifest.yaml` and `registries/skill_registry.csv` if status changes.
5. Mark status as `adapted` only after review and validation evidence.
