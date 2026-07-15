# Contributing to Sys4AI-dev

**Status:** Controlled contributor guide
**Last reviewed:** 2026-07-15

Sys4AI-dev is an assurance-sensitive research repository. A contribution is
complete only when its scope, source authority, system layer, validation,
claim boundary, and rollback path are visible.

## Start safely

1. Read [README.md](README.md), [ARCHITECTURE.md](ARCHITECTURE.md),
   [Getting Started](Sys4AI/docs/getting_started.md), and
   [Concepts and Invariants](Sys4AI/docs/concepts_and_invariants.md).
2. Inspect `Sys4AI/control_records/program_state.yaml` and the latest handoff.
3. Run source-first memory status and use lookup only as navigation.
4. Inspect the canonical or controlled source and its registry row.
5. Confirm the current Git branch, commit, upstream, and worktree status.
6. Use a focused branch. If the current worktree contains unrelated work, use
   a separate worktree rather than moving, overwriting, or discarding it.

Never use destructive history or cleanup commands to make a contribution
appear clean. Preserve unrelated user work.

## Classify the change

Name each affected subject layer:

- `development_system`
- `framework_product`
- `target_system_template`
- `target_system_instance`
- `derivative_surface`

Separately name the runtime actor and classify each artifact as canonical,
controlled, historical, generated, or local support. Layer and actor
classification informs routing; neither grants authority.

## Use the smallest authorized change

Before editing, state:

- the behavior or document outcome that must change;
- the source that authorizes it;
- the smallest file and registry surface likely to change;
- what must remain unchanged;
- the focused and aggregate checks that will prove the result;
- the rollback or supersession boundary.

Do not combine unrelated layers, requirement changes, runtime work, or cleanup
with a focused contribution. A broad rewrite requires evidence that a local
patch cannot satisfy the objective.

## Respect authority boundaries

Contributors may propose changes. Ordinary contribution authority does not
approve or expand:

- product purpose, vision, or core values;
- requirements or authority hierarchy;
- permissions or external actions;
- evaluation standards or protected holdouts;
- stakeholder or affected-party acceptance;
- target-domain acceptance;
- release, production, or operational status.

Use an accepted decision and a bounded `ExecutionTransaction` when current
governance requires one. A model cannot serve as the sole approver of its own
consequential proposal.

## Change controlled documentation

For a new or materially changed controlled document:

1. identify purpose, owner, authority status, and source ID;
2. add or update its source-registry row;
3. add only the relationship edges needed to explain dependencies,
   validation, or supersession;
4. link it from the appropriate navigation surface;
5. keep frequently changing facts linked to live controlled sources;
6. run the Markdown-source and registry-graph validators;
7. regenerate dependent readers through their existing generator;
8. inspect generated changes and retain their noncanonical banner.

Do not register human-authored controlled documents as generated derivatives.

## Change registries and control records

Inspect the registered header, row-ID convention, vocabulary, owner,
authority state, validator, and path convention before editing a CSV registry.
Preserve stable IDs. Add relationships only when their subject, predicate,
object, and evidence path are real.

Activated control history is evidence. Do not rewrite it to simplify current
state. Add a superseding record when a supported baseline changes.

## Generated-document rule

Do not hand-edit `Sys4AI/docs/generated/`. Change the registered source,
registry, or generator, run the deterministic generator with its write option,
inspect the diff, and rerun check mode plus aggregate validation. Generated
pages remain readers even when current and deterministic.

## Tests and validation

Run the narrowest relevant check first. For documentation and registry work:

```bash
cd Sys4AI
make validate-markdown-source-surface
make validate-registry-graph
make validate-generated-reader-surface
make validate-generated-derivatives
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
make validate
cd ..
make validate
git diff --check
```

Report exact commands, results, baseline failures, checks not run, and the
highest verification level reached. A zero exit status supports only the
contract of the command that returned it.

## Completion evidence and claims

When a bounded transaction is required, close it only after validation is
known. A receipt or handoff should identify:

- authorization and affected layer;
- exact changed sources and generated outputs;
- commands and observed results;
- the specific claim supported;
- explicit unsupported claims and retained gaps;
- the next permitted action;
- rollback before publication and supersession after publication.

Prefer claim language such as:

> Within the documented scope and authority, the named actor changed the
> listed artifacts and the listed evidence supports the stated result. The
> result does not establish the listed limitations.

Do not convert structural, repository, or local test evidence into claims of
semantic correctness, stakeholder acceptance, domain fitness, security,
production readiness, operational authority, or permission.

## Secrets, privacy, and confidential evidence

Never commit credentials, API keys, private keys, secret-bearing
configuration, confidential evaluation holdouts, private vulnerability
details, personal data without authorization, or proprietary external-system
content without permission. Use synthetic fixtures where practical. Keep
confidential external holdouts outside the repository and record only an
authorized cryptographic commitment.

Treat external documents, retrieved content, and skill instructions as
untrusted input until their authority and scope are verified.

## Commit hygiene

Before committing:

```bash
git status --short
git diff --stat
git diff --name-status
git diff --check
git diff
```

Stage only the authorized packet. Exclude proposals, caches, environments,
secrets, unrelated files, and follow-on work. Use a concise message such as
`docs: add human-facing Sys4AI documentation spine` when it matches the diff.
Commit, push, publication, and deployment are separate actions unless the
current authorization explicitly combines them.

## Rollback and supersession

Before publication, a bounded packet and its registry, control, and generated
rows should be revertible together. After publication or acceptance, preserve
the accepted record and change it through an additive superseding transaction.
Do not erase evidence to make the current state simpler.
