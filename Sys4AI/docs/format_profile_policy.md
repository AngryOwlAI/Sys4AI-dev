# Format Profile Policy

## Authority Notice

This policy defines Phase 1 handling for governed file-format memory profiles. Canonical authority remains with the PRDs, controlled source files, registries, and validation contracts.

## Scope

Phase 1 recognizes five core profiles: Markdown, CSV, YAML, TOML, and JSON Schema.

## Core Profiles

Markdown is for human-authored PRDs, policies, guides, templates, and source documentation. CSV is for registries, ledgers, relationship maps, and provenance rows. YAML is for agent control and state records. TOML is for project, package, tool, runtime, framework, and target-project configuration. JSON Schema is for executable validation contracts.

## Registry Requirements

Governed profile definitions belong in `registries/format_profile_registry.csv`. Configuration sources belong in `registries/config_source_registry.csv`. YAML control and state records belong in `registries/control_record_registry.csv`. JSON Schema contracts belong in `registries/validation_contract_registry.csv`.

## Validation Requirements

CSV registries require stable header validation. YAML records require safe parsing and contract validation where a contract exists. TOML sources require size-limited parsing and contract validation where a contract exists. JSON Schema contracts require schema checks against the declared dialect.

## Derivative Surface Requirements

YAML and TOML artifacts are surfaced through the generated Configuration and Control Wiki. JSON Schema contracts are surfaced through the generated Validation Contracts Catalog. Generated derivatives are reader aids only.

## Promotion Workflow

Generated derivatives, local vault notes, semantic caches, and summaries do not become canonical unless a future ExecutionTransaction explicitly promotes them through a source-authority workflow.

## Security And Secrets Rules

Phase 1 examples must not contain secret-bearing YAML or TOML values. Validators may reject secret-like keys or private key blocks in examples.

## Drift, Orphan, And Stale Rules

A governed artifact is invalid when its registry row points to a missing source, its declared validation contract is missing, or a generated derivative claims canonical authority. Later passes may replace pending source hashes with deterministic hash checks.

## Project-Specific Profile Extension Workflow

A project-specific profile requires an accountable PRD or Director Decision, an additive row in the controlled format-profile registry, an executable validation contract, and passing authority-boundary review before use. An extension shall not weaken the core authority hierarchy, relax source-first promotion, or permit a generated derivative, local vault, semantic cache, or wiki page to become canonical implicitly. Changes and rollback use a bounded registry-change transaction; existing activated profile history is superseded rather than rewritten.

## Phase 1 Limitations

Phase 1 provides scaffold validation. It does not implement a production memory database, full wiki engine, TOML writing, or semantic acceptance validation.
