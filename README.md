# Sys4AI-dev

`Sys4AI-dev` is the development workspace for **Sys4AI**, a governance-first
framework for designing and stewarding AI agents and agentic systems.

> **Current boundary:** Sys4AI is version `0.1.0` at the `test` lifecycle
> stage. Its accepted baseline is bounded and non-production. Repository
> validation does not establish stakeholder or affected-party acceptance,
> target-domain fitness, independent evaluation, operational authority,
> production readiness, or permission to act.

## What Sys4AI is

Sys4AI keeps four objects distinct:

1. the **Sys4AI Framework Product**, containing governed requirements,
   methods, roles, skills, contracts, registries, validators, templates, and
   reference code;
2. the **Sys4AI Meta-Agent Runtime**, which applies that framework only within
   current human, host, project, role, and transaction authority;
3. the **host harness**, which supplies tools and enforces platform and
   permission constraints; and
4. each **target AI agent or target agentic system**, which retains its own
   purpose, data, risk, approval, and operating boundary.

The governing distinctions are simple:

- memory finds; registered sources decide;
- capability does not grant permission;
- an artifact does not prove execution;
- structural validation does not prove semantic or domain correctness;
- evidence informs acceptance but does not perform it;
- generated readers do not outrank their sources;
- self-hosting does not create self-authorization.

See [ARCHITECTURE.md](ARCHITECTURE.md) and
[Sys4AI/docs/concepts_and_invariants.md](Sys4AI/docs/concepts_and_invariants.md).

## What is implemented

The repository contains:

- canonical Phase 0 and Phase 1 Product Requirements Documents;
- a Python reference scaffold and command-line validators;
- portable bounded-execution, permission, state, closeout, and handoff
  contracts;
- controlled source, relationship, trace, role, skill, contract, decision,
  transaction, and evidence registries;
- reference-host, lifecycle, target-package, safety, and evidence controls;
- a non-production target-package and walking-skeleton demonstration;
- deterministic, noncanonical reader pages generated from registered inputs;
- local unit tests and repository-wide validation.

The current accepted migration state is recorded in
[program_state.yaml](Sys4AI/control_records/program_state.yaml). The latest
accepted baseline preserved independent evaluation, stakeholder and
affected-party review, target-domain acceptance, and production and
operational evidence as unexecuted, unwaived future work.

## What is not established

Sys4AI does not currently provide or claim:

- a configured or authorized production target runtime;
- production deployment, monitoring, incident, rollback, or kill capability;
- independent external evaluation results;
- broad stakeholder or affected-party acceptance;
- target-domain acceptance or domain truth;
- production or operational authority;
- permission expansion from host or model capability.

The checked-in Codex reference-host profile is environment-specific and fresh
only through `2026-07-18T15:19:10Z`. Reinspect
[the live profile](Sys4AI/configs/host_profiles/codex_app_reference.toml) after
that horizon or whenever host behavior, tools, permissions, or task semantics
change. Host evidence never grants transaction permission by itself.

## Repository authority map

| Area | Purpose and authority |
|---|---|
| [`PRDs/`](PRDs/) | Canonical product and phase requirements, plus explicitly classified historical or derivative material. |
| [`implementation_plans/`](implementation_plans/) | Controlled planning, acceptance, and completion evidence; not a competing requirements baseline. |
| [`.agents/skills/`](.agents/skills/) | Active development-runtime skills for this workspace. |
| [`.codex/skills/`](.codex/skills/) | Compatibility shims only; no independent behavior. |
| [`Sys4AI/skills/core/`](Sys4AI/skills/core/) | Portable framework-product skill scaffolds; not active development-runtime authority. |
| [`Sys4AI/control_records/`](Sys4AI/control_records/) | Decisions, portable transactions, state, receipts, preflights, and handoffs. |
| [`Sys4AI/registries/`](Sys4AI/registries/) | Controlled source, trace, role, skill, contract, and evidence indexes. |
| [`Sys4AI/schemas/`](Sys4AI/schemas/) | Structural contracts; a schema pass proves structure only. |
| [`Sys4AI/sys_for_ai/`](Sys4AI/sys_for_ai/) | Python reference implementation and validators. |
| [`Sys4AI/docs/generated/`](Sys4AI/docs/generated/) | Deterministic reader aids that are never source authority by convenience. |

Use the
[documentation map](Sys4AI/docs/documentation_map.md) to find the smallest
relevant source set. The map routes readers; the source registry decides
authority.

## Setup and validation

Prerequisites are Git, Make, Python 3.10 or newer, and a POSIX-like shell.

```bash
cd Sys4AI
make install
make doctor
```

Run the unit suite from `Sys4AI/`:

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

Run all repository validation from the repository root:

```bash
make validate
```

For focused root checks:

```bash
make validate-dev-skills
make validate-product-scaffold
```

See [Getting Started](Sys4AI/docs/getting_started.md) for reading order,
focused validators, state inspection, generated-document rules, and
troubleshooting.

## Read next

1. [Architecture](ARCHITECTURE.md)
2. [Getting Started](Sys4AI/docs/getting_started.md)
3. [Concepts and Invariants](Sys4AI/docs/concepts_and_invariants.md)
4. [Phase 0 Product and System-Design PRD](PRDs/Sys4AI_phase-0_product_system_design_prd.md)
5. [Phase 1 Implementation Initialization PRD](PRDs/Sys4AI_phase-1_implementation_initialization_prd.md)
6. [Current Program State](Sys4AI/control_records/program_state.yaml)
7. [Documentation Map](Sys4AI/docs/documentation_map.md)

## Contributing safely

Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing controlled sources,
registries, control records, generated pages, or skill surfaces. Work from a
focused branch or worktree, classify the affected system layer and authority
class, inspect registered sources before editing, and use the smallest
authorized change. Do not hand-edit generated pages.

## Security reporting status

This repository does not currently publish a `SECURITY.md` because a private
vulnerability-reporting route and supported-version scope have not been
verified. Do not place vulnerability details, secrets, credentials,
confidential evaluation holdouts, or affected-party data in a public issue.
Repository maintainers must establish and verify a private reporting route
before promoting a security-reporting policy.

## License

This repository is licensed under the Apache License, Version 2.0. See
[LICENSE](LICENSE) and [NOTICE](NOTICE).
