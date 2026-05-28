---
name: python-architecture-general
description: Use when designing, reviewing, or refactoring Python project structure, package layout, module boundaries, public APIs, split decisions, configuration surfaces, settings loading, constants, or secret handling. Trigger on "organize this Python project", "split this package", "design module boundaries", "clean up settings", or "move constants out of code". Prefer the repository's existing structure first; use the default `code/` plus `configs.yaml` layout only when the repo does not already define a different convention.
---

# Python Architecture

## Overview

Design Python projects so structure communicates responsibility: clear package boundaries, explicit public APIs, predictable configuration surfaces, and minimal ambiguity about where code, tests, scripts, and settings belong.

Keep this skill focused on architecture and configuration decisions. Use `python-codingstyle-general` for implementation-code style and `python-testsstyle-general` for Python test authoring and execution.

Source order for Python architecture decisions: local package/build config first; then existing import/runtime patterns; then Python language reference import semantics; then PEP 8 and Google Python Style Guide naming and public-interface guidance.

## Decision Order

1. Inspect the repository and follow established layout and naming patterns first.
2. If the repo already defines structure, extend it rather than replacing it.
3. If the repo does not define a clear structure, apply the default preferred layout in this skill.
4. Check import paths, entrypoints, and configuration loading before moving files.
5. When moving or renaming modules, update every affected import path, entrypoint, script, config reference, and documented path in the same change.
6. Keep architecture decisions driven by responsibility boundaries, not aesthetics or novelty.

## Default Preferred Layout

Use this layout only when the repository does not already define a different convention:

```text
code/
  back/   # for backend part
    app/
      __init__.py
      api/
      domain/
      services/
      storage/
      settings.py
  front/    # for frontend (html css js etc) part
  tests/
    unit/
    integration/
    testlogs/
  scripts/
    sync_data.py
configs.yaml
```

Keep tests out of implementation packages unless the repository clearly uses co-located tests already.

## Core Rules

### Module and package boundaries

- Give each package one clear responsibility.
- Separate orchestration, domain logic, adapters, and infrastructure concerns.
- Avoid packages that mix API endpoints, persistence, CLI glue, and business rules without clear boundaries.
- Prefer standard library, existing utilities, and current dependencies before adding new packages; add a dependency only when it materially reduces risk or complexity.
- Keep cross-package imports directional and predictable.
- Avoid import cycles and import-time side effects; entrypoints should call runtime setup explicitly.
- Prefer shallow package trees; add depth only for genuine sub-domains or isolation needs.

### Public API design

- Make public entrypoints obvious through stable module paths and limited exported names.
- Keep internal helpers private by default.
- Prefer a small public API over exposing the entire package tree.
- For reusable packages, make the supported import surface explicit with stable re-exports or `__all__` where that fits the repo.
- Refactor internal structure without breaking public import paths unless the task explicitly allows it.
- Treat public imports as compatibility commitments; add adapters or re-exports when moving internals unless a breaking migration is requested.
- Treat script entrypoints, config paths, and documented module paths as compatibility surfaces too, not just Python imports.

### Split decisions

- If you cannot explain a module or package purpose in one sentence, the boundary is probably wrong.
- Split a module when it has multiple responsibilities, multiple change reasons, or unrelated dependency sets.
- Treat the 400-line guideline as a secondary review trigger, not the architectural reason to split. If the model or boundary is wrong at 200 lines, split it there.
- Split around owned models and boundaries: transport schemas, domain entities, persistence records, settings objects, and presentation formatting should not blur together in one module once they evolve independently.
- Split when one area coordinates workflow and another defines reusable rules or transformations. Orchestration and policy usually deserve separate modules.
- Split when the same package mixes boundary-specific error handling or dependency lifecycles, for example HTTP concerns, database concerns, and core business invariants.
- Do not split by syntactic bucket names alone such as `utils`, `helpers`, or `misc`. Create modules around owned responsibilities and stable boundaries instead.
- Split a package when one area can evolve, test, or deploy semi-independently from another.
- Do not split just to hit an arbitrary file count; split around boundaries that reduce confusion.
- Keep cohesive vertical slices together when they share one model, one dependency set, and one reason to change. Avoid turning one clear slice into many tiny files without distinct ownership.
- If a file keeps growing because it is becoming a router, coordinator, formatter, and service layer at once, break it apart.

### Configuration and secrets

- Keep `.env` for sensitive values only because it should remain gitignored.
- Keep non-secret configuration in `configs.yaml` when the repository does not already define a different versioned config surface.
- Add a clear descriptive comment for each setting when the config format supports comments.
- Load environment and config values at explicit boundaries, not ad hoc across the codebase.
- Keep secrets, user-specific values, and deploy-specific credentials out of versioned non-secret config files.
- Keep configuration names stable and descriptive; avoid scattering duplicate constants across modules.

### Settings flow

- Convert raw env and YAML values into a structured settings object near startup or another clear boundary.
- Validate required settings early and fail with clear startup errors.
- Pass typed settings inward instead of repeatedly reading env vars or config files.
- Keep default values explicit and documented.
- Separate deploy-time settings from domain constants. If a value changes by environment, it belongs in config; if it defines business behavior, keep it near the domain model or documented config surface.

## Documentation Expectations

- Document the intended package layout when it is non-obvious.
- Keep architecture notes short and close to the boundary they explain.
- Use config comments or nearby documentation to explain each setting's purpose, not just restate its key.
- Ensure implementation guidance keeps function-level docstrings and comments on important logic blocks so architectural intent remains understandable in code.
- Prefer self-explanatory package names and module names over long architecture prose.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Inventing a new layout in a repo that already has one | Follow the repo first and improve only where necessary |
| Letting public and internal modules blur together | Define stable entrypoints and keep helpers private |
| Reading env values from many modules | Centralize config loading and pass structured settings |
| Putting non-secret knobs into `.env` | Move them to `configs.yaml` or the repo's existing versioned config surface |
| Splitting files mechanically by length only | Split by responsibility and dependency boundaries |
| Moving code into `utils.py` because it feels shared | Create a module named for the owned behavior or boundary instead |

## Application Examples

- Constants cleanup: move deploy-tuned values to `configs.yaml` or the repo's existing versioned config surface, keep true domain constants near domain code, and pass a typed settings object inward.
- Package split: preserve old public imports with a thin compatibility module or re-export unless the task explicitly requests a breaking change.
- Script growth: keep script entrypoints thin and move reusable orchestration or domain logic into importable packages.

## Routing Examples

Use for: "Design the package structure for this Python service", "Move these constants and settings out of code", "Define the public API for this internal library".

Do not use for: "Write the parser implementation for this module", "Add pytest coverage for the bug fix", "Run this failing Python test".

## Reference

Read [references/architecture-reference.md](references/architecture-reference.md) for concrete layout examples, split heuristics, public API patterns, and `configs.yaml` or `.env` guidance.

Use [assets/architecture-decision-template.md](assets/architecture-decision-template.md) only when the user asks for a written architecture note, migration note, or handoff summary.
