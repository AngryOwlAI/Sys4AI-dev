# sys-for-ai-dev

This repository is the development workspace for `sys-for-ai`.

The project being developed lives in [`sys-for-ai/`](sys-for-ai/).

The current product-definition sources are:

- [`PRDs/sys-for-ai_phase-0_product_system_design_prd.md`](PRDs/sys-for-ai_phase-0_product_system_design_prd.md)
- [`PRDs/sys-for-ai_phase-1_implementation_initialization_prd.md`](PRDs/sys-for-ai_phase-1_implementation_initialization_prd.md)

The earlier Phase 0 draft remains available at
[`PRDs/sys-for-ai_phase-0_prd.md`](PRDs/sys-for-ai_phase-0_prd.md) as a
superseded historical reference.

Phase 1 implementation planning lives in
[`implementation_plans/`](implementation_plans/). The executable reference
scaffold, validators, registries, skill adapters, and documentation policies
live under [`sys-for-ai/`](sys-for-ai/).

Development-system runtime skills live under [`.agents/skills/`](.agents/skills/).
Thin Codex compatibility shims live under [`.codex/skills/`](.codex/skills/)
and point back to the `.agents` runtime surface. The `sys-for-ai/skills/core/`
directory remains a product-scaffold reference surface, not the active
development-system runtime.

Validate the root skill layer with:

```bash
make validate-dev-skills
```

Validate the product scaffold with:

```bash
make validate-product-scaffold
```

Run both checks with:

```bash
make validate
```

## License

This repository is licensed under the Apache License, Version 2.0. Unless a
file states otherwise, the license applies to all copyrightable materials in
this project, including code, documents, project files, repository structure,
architecture descriptions, templates, and associated artifacts.

Credit and attribution notices for Alexander Samuel Ricciardi and the AngryOwl
label are preserved in [`NOTICE`](NOTICE).
