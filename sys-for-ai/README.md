# sys-for-ai

`sys-for-ai` is a domain-agnostic system development and management framework for AI agents.

Its purpose is meta-agentic: a root AI agent uses `sys-for-ai` to design, develop, run, improve, and maintain target agentic systems for specific use cases.

Phase 0 defines the product and system-design baseline. Phase 1 initializes the implementation: Python environment, YAML control records, validators, skill adapters, memory registries, and documentation policies.

## Phase 1 setup

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
make doctor
make validate
```

## Useful commands

```bash
make doctor
make validate-agentjob
make validate-agentjobs
make validate-skills
make validate-metrics
make validate-discovery-template
make bootstrap-memory
make validate
.venv/bin/python -m sys_for_ai.cli validate-discovery-record <path>
```

## Repository areas

```text
sys_for_ai/          Python reference implementation scaffold
schemas/             YAML schema-like specs
control_records/     Example AgentJobs and manifests
registries/          Source-first memory starter registries
skills/              Core skill manifest and adapter shells
docs/                Authority and environment policies
templates/           Project and target-runtime templates
```

## Authority rule

Canonical sources and registries outrank generated derivatives. Obsidian, wiki, HTML, PDF, diagram, semantic-cache, and index surfaces are reader aids unless explicitly promoted through a source-authority workflow.

## System-document spine

`sys-for-ai` does not treat Product Requirements Documents as the only systems-engineering source. See [`docs/system_document_spine.md`](docs/system_document_spine.md) for the practical chain from mission need and system definition through requirements, architecture, verification and validation, operations, and closeout.

Skill routing for unclear target-system intent is defined in [`docs/skill_integration_policy.md`](docs/skill_integration_policy.md).
