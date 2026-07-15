# Getting Started with Sys4AI

**Status:** Controlled contributor guide
**Audience:** Maintainers, researchers, systems engineers, software engineers,
evaluators, and documentation contributors
**Last reviewed:** 2026-07-15

## Current boundary

Sys4AI is version `0.1.0` at lifecycle stage `test`. The accepted repository
baseline is bounded and non-production. It provides a governed framework
scaffold, reference implementation, validators, evidence controls, and a
non-production target-package flow. It does not provide an authorized
production target runtime or establish independent evaluation, stakeholder,
affected-party, target-domain, production, operational, or permission
acceptance.

Read the repository as an assurance-sensitive system. Inspect registered
sources before writing.

## Prerequisites

- Git
- Make
- Python 3.10 or newer
- a POSIX-like shell for the documented Make targets

The package declares Python `>=3.10`. The checked-in cross-version workflow
covers Python 3.10 through 3.14, but a workflow definition and prior successful
run do not prove the current local checkout on every interpreter.

## Set up the environment

From a repository checkout:

```bash
cd Sys4AI
make install
make doctor
```

`make install` creates `Sys4AI/.venv`, upgrades its `pip`, and installs the
declared dependencies from `requirements.txt`. It does not install the package
itself in editable mode.

## Recommended reading order

### Orientation

1. [`README.md`](../../README.md)
2. [`ARCHITECTURE.md`](../../ARCHITECTURE.md)
3. [`concepts_and_invariants.md`](concepts_and_invariants.md)
4. [`program_state.yaml`](../control_records/program_state.yaml)

### Product and authority

1. [Phase 0 Product and System-Design PRD](../../PRDs/Sys4AI_phase-0_product_system_design_prd.md)
2. [Phase 1 Implementation Initialization PRD](../../PRDs/Sys4AI_phase-1_implementation_initialization_prd.md)
3. [`system_document_spine.md`](system_document_spine.md)
4. [`skill_integration_policy.md`](skill_integration_policy.md)
5. [`documentation_map.md`](documentation_map.md)

### Implementation and validation

1. [`Makefile`](../Makefile)
2. [`pyproject.toml`](../pyproject.toml)
3. [`sys_for_ai/`](../sys_for_ai/)
4. [`tests/`](../tests/)
5. [cross-version workflow](../../.github/workflows/cross-version-python.yml)

## Validate the repository

Run focused checks for the surface you changed before aggregate validation.

From `Sys4AI/`:

```bash
make doctor
make validate-markdown-source-surface
make validate-registry-graph
make validate-generated-reader-surface
make validate-generated-derivatives
```

Run the Python unit suite directly:

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

Run product aggregate validation:

```bash
make validate
```

Run development-system and product validation together from the repository
root:

```bash
make validate
```

The root also exposes:

```bash
make validate-dev-skills
make validate-product-scaffold
```

There is no dedicated `make test` target in the current transaction.

## Inspect memory and state

Memory results are navigation. Always inspect the source path and registry row
returned by a useful hit.

```bash
cd Sys4AI
.venv/bin/python -m sys_for_ai.cli memory status --json
.venv/bin/python -m sys_for_ai.cli memory lookup SRC-PRD-P0 --json
.venv/bin/python -m sys_for_ai.cli memory lookup SRC-PRD-P1 --json
.venv/bin/python -m sys_for_ai.cli target-package status --json
.venv/bin/python -m sys_for_ai.cli walking-skeleton status --json
```

For current authority and limitations, inspect:

- [`program_state.yaml`](../control_records/program_state.yaml)
- the latest accepted decision, receipt, and handoff named there;
- [`codex_app_reference.toml`](../configs/host_profiles/codex_app_reference.toml)
- [`source_registry.csv`](../registries/source_registry.csv)
- [`object_relationship_registry.csv`](../registries/object_relationship_registry.csv)

## Understand the three skill surfaces

| Surface | Meaning |
|---|---|
| [`.agents/skills/`](../../.agents/skills/) | Active skills for developing Sys4AI in this workspace. |
| [`.codex/skills/`](../../.codex/skills/) | Compatibility pointers to the active runtime. |
| [`Sys4AI/skills/core/`](../skills/core/) | Portable framework-product scaffolds for future targets. |

Do not copy behavior between these surfaces by implication. Adapt and register
it under the authority and validation rules of the destination.

## Safe first-change workflow

1. Confirm `git status --short`, the branch, and the starting commit.
2. Use a separate branch or worktree when unrelated work is present.
3. Run memory status and inspect the exact registered sources that control the
   change.
4. Classify the subject layer, runtime actor, authority class, and generated
   dependencies.
5. Define one observable success condition and the smallest write surface.
6. Create a bounded `ExecutionTransaction` when the controlled process
   requires it.
7. Patch the source rather than a generated reader.
8. Run the focused validator, the unit suite, product validation, root
   validation, and `git diff --check` as applicable.
9. Inspect the complete diff before staging.
10. Record completion and handoff evidence only after results are known.

## Documentation and generated readers

A Markdown file is not authoritative merely because it is tracked. For a new
controlled document, add a source-registry row, use an existing source type and
authority class, add only necessary relationships, and link it from a suitable
navigation source.

Never hand-edit `docs/generated/`. Use only the generator required by actual
drift:

```bash
.venv/bin/python -m sys_for_ai.cli generate-governance-docs --write
.venv/bin/python -m sys_for_ai.cli generate-config-control-wiki --write
.venv/bin/python -m sys_for_ai.cli generate-validation-contracts-catalog --write
```

Inspect every generated diff. Generated files remain noncanonical and must
trace to changed inputs.

## Troubleshooting

### `.venv` is missing or invalid

Confirm the path and interpreter first:

```bash
test -x .venv/bin/python
.venv/bin/python --version
```

If the environment must be recreated, preserve any useful diagnostics, remove
only the local `.venv`, then rerun `make install` and `make doctor`. Do not
change tracked dependency files merely to conceal an environment failure.

### A registry validator fails

Read the registry header and its row in
[`registry_definition_registry.csv`](../registries/registry_definition_registry.csv).
Check stable ID uniqueness, allowed authority state, exact path convention,
owner, relationship vocabulary, and evidence-path resolution. Do not weaken the
validator.

### Generated drift is reported

Identify the registered source or registry change that caused drift. Run only
the corresponding generator with `--write`, inspect the diff, then rerun check
mode and aggregate validation.

### Host evidence is stale

The checked-in reference profile reaches its current freshness horizon at
`2026-07-18T15:19:10Z`. Reverify through a separately authorized transaction.
Do not extend timestamps manually or treat prior capability as current
permission.

### Memory reports warnings

Warnings constrain freshness claims but do not make every source unusable.
Inspect the warning class, the registered source, and its disposition. Block or
qualify a claim when required evidence cannot be verified.

### Validation fails

Run the narrowest failing command in verbose or fail-fast mode, distinguish a
pre-existing baseline failure from a packet regression, and repair the
smallest source-supported cause. Do not skip, suppress, or weaken a valid
check.
