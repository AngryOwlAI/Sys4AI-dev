# Self-Hosting Mode Policy

## Purpose And Scope

This policy governs self-hosting work where the `sys-for-ai-dev` development workspace uses `sys-for-ai` concepts to improve the `sys-for-ai` framework product.

## Layer Definitions

- `development_system`: the active `sys-for-ai-dev` workspace and runtime skill surface.
- `framework_product`: the `sys-for-ai/` product scaffold.
- `target_system_template`: reusable target-system templates.
- `target_system_instance`: a concrete future system produced or maintained through the framework.
- `derivative_surface`: generated reader pages and local navigation surfaces.

## Active Runtime Versus Product Scaffold

Active runtime skills live under `.agents/skills/`. Product scaffold skills under `sys-for-ai/skills/core/` are references until a Director Decision explicitly promotes them.

## Authority Hierarchy

PRDs, controlled registries, validation contracts, AgentJobs, completion receipts, and handoffs outrank generated docs, local caches, and chat memory.

## Required System-Layer Classification Fields

Controlled work must identify the subject system, subject layer, work type, canonical authorities, allowed mutations, forbidden mutations, Director Decision requirement, next gate, evidence, and open issues.

## When Director Decision Is Required

A Director Decision is required for authority expansion, promotion of generated derivatives, cross-layer mutation, new AgentJob creation after a completed packet, or product-scaffold promotion to runtime authority.

## Forbidden Mutations

Generated derivatives, local caches, and compatibility shims must not authorize changes to PRDs, registries, control records, validation contracts, role catalogs, or skill manifests.

## Generated Derivative Limitations

Generated pages are navigation only. They must carry noncanonical metadata, source trace, generator identity, and stale/orphan status.

## AgentJob Implications

Every self-hosting change must be bounded by one AgentJob, list allowed reads and writes, preserve stop conditions, and produce completion evidence before updating handoff state.

## Validation Commands

- `make validate-dev-skills`
- `cd sys-for-ai && make validate-system-layers`
- `cd sys-for-ai && make validate`

## Examples

- Runtime skill repair belongs to `development_system`.
- Product scaffold registry work belongs to `framework_product`.
- Generated governance pages belong to `derivative_surface`.

## Failure Modes

- Treating product scaffold skills as active runtime authority.
- Using a generated page as source authority.
- Running multiple AgentJobs through one continuation.
- Mutating a target-system instance as though it were framework-product authority.
