---
name: python-codingstyle-general
description: Use when writing, editing, refactoring, reviewing, or restructuring Python implementation code - modules, libraries, scripts, CLIs, migrations, utilities, and mixed-purpose files. Trigger on "write Python code", "add a Python command", "fix this Python file", "split this module", or "clean up this script". Do not use when the main task is Python tests; route tests to python-testsstyle-general.
---

# Python Coding

## Overview

Write Python that stays easy for Codex and humans to reason about: small files, small functions, explicit boundaries, clear types, and predictable behavior.

Keep this skill focused on implementation code. Mention tests only where production code structure must support separate test files, use `python-testsstyle-general` when the main task is writing or running Python tests, and use `python-architecture-general` for project layout, package boundaries, and configuration-surface decisions.

Source order for Python decisions: configured formatters, linters, and type checkers first; then local Python patterns; then PEP 8, Google Python Style Guide, and Python tutorial/reference semantics. Do not reformat code just to satisfy a generic guide when local style is intentionally different.

## Workflow

1. Inspect the local repository patterns before introducing new structure.
2. Check the smallest relevant Python tooling first: `pyproject.toml`, linter or type-checker config, and the closest similar module.
3. Use configured formatters, linters, and type checkers as the mechanical authority; do not hand-apply style rules that tooling will decide.
4. Choose the smallest correct change that solves the task fully.
5. Preserve existing public interfaces unless the task explicitly allows a breaking change.
6. Keep implementation code and tests in separate files. If tests are needed, add or update dedicated test files rather than mixing test code into production modules.
7. Split large or mixed-responsibility files instead of extending them further.
8. Validate inputs and outputs at external boundaries: CLI args, env vars, files, network payloads, and public APIs.
9. Prefer the smallest relevant verification step before expanding scope.

## Core Rules

### File size and structure

- Target Python source files under 400 lines when practical.
- Reconsider structure before a file passes roughly 500 lines.
- Split by responsibility, not arbitrarily: parsing, I/O, orchestration, domain logic, and formatting often belong in separate modules.
- Keep scripts thin. Put reusable logic in importable functions or modules.
- Keep modules import-safe: no parsing CLI args, network calls, file writes, or process exits at import time.

### Function and module design

- Keep functions focused on one job with clear inputs and outputs.
- Separate orchestration from business logic.
- Avoid hidden global state, implicit mutation, and long parameter lists.
- Prefer early returns and simple control flow over deep nesting.
- Use descriptive names; do not rely on comments to explain vague code.
- Prefer normal Python naming: `lower_snake_case` for functions and variables, `CapWords` for classes and exceptions, `UPPER_SNAKE_CASE` for constants, and a leading underscore for non-public helpers.
- Introduce abstractions only when they remove real duplication or clarify a boundary.

### Types and contracts

- Add type hints to public functions, methods, and module-level constants where useful.
- Prefer precise standard types and small dataclasses or typed objects over loose dictionaries when the structure matters.
- Validate external data at boundaries instead of letting untrusted shapes leak inward.
- Make return values explicit; avoid functions that sometimes return data and sometimes print or exit.
- Avoid `Any` unless an external boundary forces it; narrow it quickly.

### Errors and failures

- Raise or handle narrow exceptions when practical.
- Keep `try` blocks as small as possible and avoid bare `except`.
- Use error messages that explain what failed and what input or operation caused it.
- Fail safely for scripts and CLIs: no partial destructive behavior without explicit intent.
- Do not swallow exceptions silently.
- Preserve exception context when translating failures.

### Configuration and secrets

- Do not hardcode secrets, tokens, or user-specific paths.
- Read configurable values from the smallest existing config surface or from explicit parameters.
- Keep non-secret defaults near the code only when they are true code defaults, not deployment settings.

### Comments and docstrings

- Add a function-level docstring for every function and method that explains purpose, key inputs/outputs, and side effects when present.
- Add short comments for important logic blocks, invariants, and tradeoffs, especially around parsing, branching, state changes, and error handling.
- Keep comments concise and useful; avoid narrative comments that just restate obvious code.

### Scripts and CLIs

- Use a `main()` entrypoint for executable scripts.
- Parse arguments explicitly and return process exit codes in a predictable way.
- Guard script execution with `if __name__ == "__main__":` so modules remain importable.
- Print deterministic, concise output suitable for terminal use and automation.
- Keep file operations, network calls, and destructive actions explicit.
- Keep `print()` in CLIs and user-facing scripts; prefer logging or returned values in library-style code.

### I/O and resources

- Prefer `pathlib.Path` and explicit text encodings for file paths and file I/O.
- Use context managers for files, connections, locks, and temporary resources.
- Keep I/O at the edges when practical so core logic stays easy to test and reuse.
- Prefer standard library, existing utilities, and current dependencies before adding new packages; add a dependency only when it materially reduces risk or complexity.

## Review Checklist

- Is the file still small enough to understand in one pass?
- Does each function do one clear job?
- Are I/O and side effects separated from core logic?
- Are public interfaces typed and boundary inputs validated?
- Are imports explicit, grouped consistently, and free of wildcard imports except for deliberate public re-export patterns?
- Is configuration externalized instead of hardcoded?
- Is reusable logic kept out of the CLI or script entrypoint?
- Are tests kept in separate test files rather than embedded in implementation code?

## Application Examples

- Utility script: keep `main()` small, move parsing/normalization into importable functions, use `Path`, explicit encodings, and return an exit code.
- Large module: split parser, I/O adapter, domain transformation, and formatting code only where those responsibilities already pull in different dependencies or change for different reasons.
- Error handling: catch `KeyError` only around the lookup that can raise it, then translate it with context; do not wrap the entire function in a broad handler.

## Routing Examples

Use for: "Write a Python script to normalize these CSV files", "Refactor this Python module into smaller files", "Add a CLI subcommand for exporting user data".

Do not use for: "Write pytest tests for this module", "Improve fixture design for this test suite", "Raise coverage on this Python package".

## Reference

Read [references/conventions.md](references/conventions.md) when you need concrete examples for file splitting, module layout, typing, config handling, or CLI structure.

Use [assets/refactor-handoff-template.md](assets/refactor-handoff-template.md) only when the user asks for a Python implementation plan, review note, or handoff summary.
