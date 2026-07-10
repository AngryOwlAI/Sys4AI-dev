# Completion Receipt: TX-15 Target-Package Contract

- Receipt ID: `CR-SFADEV-STRATEGIC-BASELINE-TX15-001`
- Execution transaction: `TX-15-TARGET-PACKAGE`
- Entry dependencies: completed and shared `TX-13-VALIDATORS` and `TX-14-PHASE2`
- Subject system: `Sys4AI` framework product in the `Sys4AI-dev` development system
- Baseline change class: controlled schema and validator migration with derivative example refresh
- Result: `PASS`

## Outcome

TX-15 replaces the prior one-target, fixed-file, retired-packet validation logic
with a registered manifest-driven target-package contract. The validator now accepts
arbitrary conforming target IDs, resolves manifest-declared artifacts, verifies
strategic-intent approval or waiver state, active versions, hashes, pattern and
maturity, host requirements, portable execution transactions, trace, validation
summaries, and derivative authority boundaries.

The repo-steward package remains a non-production derivative smoke example. Its
named approval principal and evidence are explicitly fictional instructional
fixtures; they grant no real stakeholder, host, operational, or production authority.

## Changes made

- Added and registered `target_system_package_manifest.schema.json` and a narrow
  target-package manifest artifact contract.
- Rebuilt `target_package.py` around manifest-declared contents and actionable
  path-specific failures instead of a hard-coded target ID and fixed task files.
- Added thirteen package tests covering a passing example, arbitrary target ID,
  a valid active-waiver route, missing artifact, derivative authority, model
  self-approval, duplicate IDs, stale hash, stale active version, approval-state
  mismatch, retired active vocabulary, production maturity overclaim, and
  package-root escape.
- Migrated the derivative repo-steward example to separate target vision and core
  values, fictional approval evidence, pattern decision, permission-dependent host
  requirements, portable execution transactions, trace, artifact index, hashes,
  and four distinct validation summaries.
- Split capability-migration inventory so TX-15 rejection logic and negative probes
  are active-valid while the separate older target-project configuration contract
  remains explicitly deferred.
- Advanced only `SFA-P2-ADD-PACKAGE-001` and `SFA-P2-ADD-SEM-001` to passing
  verification. The other eleven additive Phase 2 rows remain `not_run`.
- Advanced portable program state only to the post-TX-15 boundary and routed the
  next action solely to `TX-16-WALKING-SKELETON`.
- Regenerated only affected noncanonical configuration-control, validation-contract,
  artifact-contract, and registry-catalog readers.

## Verification

- Focused target-package and trace suite: 49/49 passed.
- Product unit suite: 197/197 passed.
- Target-package, validation-contract, JSON-Schema, artifact-contract, capability-
  migration, trace, trace-migration, registry, strategic-intent, lifecycle, PRD-
  semantic, and generated-derivative validators passed.
- Product and repository-root `make validate`: passed.
- Requirement trace remains 227 rows: 214 preserved TX-12 rows plus 13 additive
  Phase 2 rows. Verification state is 16 `pass`, 200 `planned`, and 11 `not_run`.
- Preserved gaps remain exactly 7 `needs_evidence` and 200 `planned`.
- Exact TX-11 rollback digest remains
  `95e59cf5befc4f9fd29d857d1f609a4c0d2c321c1b3adf1efca1a69cdb01b28c`.
- Accepted Phase 2 SHA-256 remains
  `98567cf4f4af8ca99650a6220a78d840dae5e11195891fc808c69c4828528038`.
- Accepted Phase 2 draft SHA-256 remains
  `9e290964200137329827a0164f50c2d3e97dc194fac65dd086c8b1dd7e57d84f`.
- Both protected sources have zero Git diff.
- Generated derivatives and `git diff --check` passed.
- Memory status: `PASS_WITH_WARNINGS`; 915 objects, 395 pending-hash warnings,
  and zero derivative-authority inversions.

Structural validation does not prove strategic quality, ethical correctness,
stakeholder consensus, behavioral alignment, production readiness, or domain truth.
Those claims require accountable review and additional evidence. TX-15 does not
satisfy `G-07`, `G-08`, production readiness, or domain acceptance.

## System-layer and authority record

The schema, validator, tests, artifact contracts, registries, and portable control
records are `framework_product` changes inside the `development_system` workspace.
The repo-steward package is a `target_system_instance` with `derivative_draft`
authority. Generated reader pages are noncanonical `derivative_surface` outputs.
No production target instance or derivative PRD module authority changes in TX-15.

## Rollback

Revert the complete TX-15 schema, validator, test, package, capability inventory,
trace, registry, state, control-record, and generated-reader packet. Retain both
protected Phase 2 sources and all activated historical evidence. If the package
contract proves insufficient, supersede it through a new bounded contract change;
do not weaken fail-closed authority, approval, hash, or maturity checks in place.

## Handoff

`HANDOFF-SFADEV-STRATEGIC-BASELINE-TX15-001` routes only to
`TX-16-WALKING-SKELETON`. TX-17 and later transactions remain out of scope.

## References

AngryOwlAI. (2026, July 9). *Sys4AI strategic-baseline identity and execution-model decision* [Director Decision Record]. `Sys4AI/control_records/director_decisions/DDR-SFADEV-STRATEGIC-BASELINE-001.yaml`.

Sys4AI-dev. (2026a). *Sys4AI Phase 2 strategic baseline addendum* [Product requirements document addendum]. `PRDs/Sys4AI_phase-2_strategic_baseline_addendum.md`.

Sys4AI-dev. (2026b). *Strategic baseline migration full implementation plan* [Implementation plan]. `implementation_plans/Sys4AI-dev_strategic_baseline_migration_full_implementation_plan.md`.
