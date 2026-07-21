# Sys4AI Development Repository

Sys4AI is a host-neutral framework product and meta-agent runtime for designing,
building, verifying, operating, improving, and retiring governed agentic
systems. This repository, Sys4AI-dev, is the development system used to build
that product. They are related, but they are not the same system.

The governing dependency rule is:

> Sys4AI-dev may depend on Sys4AI. Sys4AI must not depend on Sys4AI-dev.

## Your Soul

The SOUL.md file is mandatory for all agents to read and understand. It define core aspect of your personality, 
the way you think, reason, and act.  It is the most important file in the repository and should be read first by any agent before doing any work in the project.

## Sixty-second orientation

| Object | Meaning | Location |
|---|---|---|
| Development system (D) | Bootstrap agent, project authority, current work, tools, and evidence | repository root and `development/` |
| Host system (H) | Codex, CLI, CI, or another execution environment | adapters and host profiles |
| Sys4AI (M2) | Portable framework product and executable meta-agent runtime | `Sys4AI/` |
| Target framework (M1) | A governed framework produced for a class of targets | generated outside the product source |
| Target instance (M0) | A concrete agent, workflow, multi-agent system, or application | a target workspace |
| Reader/evidence surface (R) | Reports, logs, generated readers, and release evidence | `development/evidence/` or ignored runtime state |

Self-hosting means a trusted Sys4AI release may help produce a separate
candidate successor. It does not merge development authority, product
authority, target authority, or mutable runtime state.

## Current authority

Read these in order:

1. [PROJECT_STATUS.md](PROJECT_STATUS.md) — what is true now.
2. [Product baseline PRD](PRDs/active/Sys4AI_product_baseline_prd.md) — what
   Sys4AI must be.
3. [Repository reboot PRD](PRDs/active/Sys4AI_repository_reboot_prd.md) — the
   current approved change boundary.
4. [Active implementation plan](implementation_plans/active/repository-reboot-implementation-plan.md)
   — how the current change is being implemented and verified.
5. [Architecture index](architecture/README.md) and [decision index](decisions/README.md)
   — system structure and consequential decisions.

Generated documents, local caches, runtime logs, and memory indexes are
navigation or evidence. They are not requirement or approval authority.

## Repository map

- `PRDs/`: product and change requirements.
- `architecture/`: current system architecture and boundary models.
- `decisions/`: accepted architecture decision records.
- `implementation_plans/active/`: exactly one active implementation plan.
- `development/`: canonical bootstrap-development runtime, tools, state, and
  evidence.
- `.agents/` and `.codex/`: generated host bindings only.
- `Sys4AI/`: extractable, independently buildable product.
- `integration/`: target fixtures and cross-boundary tests.

See [SYSTEM_MAP.md](SYSTEM_MAP.md) for the dependency and authority flows.

## Validation

From the repository root:

    make validate-development
    make validate-product
    make validate-integration
    make validate

From inside `Sys4AI/`:

    make lint
    make test
    make validate-contracts
    make validate-assets
    make build

The product commands must work without reading a parent path, root PRD,
development skill, root workflow, or development transaction history.

## Status boundary

The repository is a non-production reboot candidate. Structural validation does
not establish stakeholder acceptance, domain truth, production readiness, or
operational authority. Those require separate evidence and accountable human
decisions.
