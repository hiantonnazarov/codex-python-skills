---
name: python-architecture-general
description: Use when designing, reviewing, or refactoring Python project structure, package layout, module boundaries, public APIs, split decisions, configuration surfaces, settings loading, or secret handling. Trigger on requests such as "organize this Python project", "split this package", "design module boundaries", "clean up settings", or "move constants out of code". Prefer the repository's existing structure first; use the default code-folder and configs.yaml layout only when the repo does not already define a different convention.
---

# Python Architecture

## Overview

Design Python projects so structure communicates responsibility: clear package boundaries, explicit public APIs, predictable configuration surfaces, and minimal ambiguity about where code, tests, scripts, and settings belong.

Keep this skill focused on architecture and configuration decisions. Use `python-codingstyle-general` for implementation-code style and `python-testsstyle-general` for Python test authoring and execution.

## Use This Skill For

- Planning or refactoring Python project layout
- Defining package boundaries and module responsibilities
- Deciding when to split files, packages, or subsystems
- Designing public API surfaces for packages and modules
- Organizing configuration, settings, constants, env usage, and secrets handling

## Do Not Use This Skill For

- Low-level implementation-style decisions inside already well-scoped modules
- Python test-writing and test-running tasks
- Framework-specific architecture rules when a more precise skill or repo convention exists

## Decision Order

1. Inspect the repository and follow established layout and naming patterns first.
2. If the repo already defines structure, extend it rather than replacing it.
3. If the repo does not define a clear structure, apply the default preferred layout in this skill.
4. Keep architecture decisions driven by responsibility boundaries, not aesthetics or novelty.

## Default Preferred Layout

Use this layout only when the repository does not already define a different convention:

- Put project code under `code/`.
- Use `code/back/` for backend and shared Python application packages.
- Use `code/front/` for frontend code when the project includes it.
- Use `code/tests/` for tests and test-related support.
- Use `code/tests/testlogs/` and nearby subfolders for test artifacts when the repo keeps them.
- Use `code/scripts/` for project scripts and operational entrypoints.

Keep tests out of implementation packages unless the repository clearly uses co-located tests already.

## Core Rules

### Module and package boundaries

- Give each package one clear responsibility.
- Separate orchestration, domain logic, adapters, and infrastructure concerns.
- Avoid packages that mix API endpoints, persistence, CLI glue, and business rules without clear boundaries.
- Keep cross-package imports directional and predictable.
- Prefer shallow package trees; add depth only for genuine sub-domains or isolation needs.

### Public API design

- Make public entrypoints obvious through stable module paths and limited exported names.
- Keep internal helpers private by default.
- Prefer a small public API over exposing the entire package tree.
- For reusable packages, make the supported import surface explicit with stable re-exports or `__all__` where that fits the repo.
- Refactor internal structure without breaking public import paths unless the task explicitly allows it.

### Split decisions

- Split a module when it has multiple responsibilities, multiple change reasons, or unrelated dependency sets.
- Split a package when one area can evolve, test, or deploy semi-independently from another.
- Do not split just to hit an arbitrary file count; split around boundaries that reduce confusion.
- If a file keeps growing because it is becoming a router, coordinator, formatter, and service layer at once, break it apart.

### Configuration and secrets

- Keep `.env` for sensitive values only because it should remain gitignored.
- Keep major constants and non-secret configuration in `configs.yaml` when the repository does not already define a different config surface.
- Add a clear descriptive comment for every value in `.env` and `configs.yaml`.
- Load environment and config values at explicit boundaries, not ad hoc across the codebase.
- Keep secrets, user-specific values, and deploy-specific credentials out of versioned non-secret config files.

### Settings flow

- Convert raw env and YAML values into a structured settings object near startup or another clear boundary.
- Validate required settings early and fail with clear startup errors.
- Pass typed settings inward instead of repeatedly reading env vars or config files.
- Keep default values explicit and documented.

## Documentation Expectations

- Document the intended package layout when it is non-obvious.
- Keep architecture notes short and close to the boundary they explain.
- Use comments in `configs.yaml` and `.env` to explain each setting's purpose, not just restate its key.
- Prefer self-explanatory package names and module names over long architecture prose.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Inventing a new layout in a repo that already has one | Follow the repo first and improve only where necessary |
| Letting public and internal modules blur together | Define stable entrypoints and keep helpers private |
| Reading env values from many modules | Centralize config loading and pass structured settings |
| Putting non-secret knobs into `.env` | Move them to `configs.yaml` with comments |
| Splitting files mechanically by length only | Split by responsibility and dependency boundaries |

## Examples

### Good triggers

- "Design the package structure for this Python service."
- "Move these constants and settings out of code."
- "Split this large Python package into clearer modules."
- "Define the public API for this internal library."

### Bad triggers

- "Write the parser implementation for this module."
- "Add pytest coverage for the bug fix."
- "Run this failing Python test."

## Reference

Read [references/architecture-reference.md](references/architecture-reference.md) for concrete layout examples, split heuristics, public API patterns, and `configs.yaml` or `.env` guidance.
