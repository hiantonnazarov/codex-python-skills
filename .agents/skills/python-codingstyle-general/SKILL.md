---
name: python-codingstyle-general
description: Use whenever Codex writes, edits, refactors, reviews, or restructures any Python code, including application code, libraries, scripts, CLIs, migrations, utilities, and mixed-purpose modules. Trigger on requests such as "write Python code", "add a Python command", "fix this Python file", "split this module", or "clean up this script". Do not use when the main task is authoring or redesigning tests; route those tasks to python-testsstyle-general instead.
---

# Python Coding

## Overview

Write Python that stays easy for Codex and humans to reason about: small files, small functions, explicit boundaries, clear types, and predictable behavior.

Keep this skill focused on implementation code. Mention tests only where production code structure must support separate test files, use `python-testsstyle-general` when the main task is writing or running Python tests, and use `python-architecture-general` for project layout, package boundaries, and configuration-surface decisions.

## Use This Skill For

- Writing or editing Python modules, packages, scripts, CLIs, and one-off utilities
- Refactoring large or tangled Python files into smaller units
- Adding new implementation logic while preserving existing repository patterns
- Reviewing Python code quality, maintainability, and structure

## Do Not Use This Skill For

- Tasks mainly about test strategy, pytest style, fixtures, mocks, or coverage
- Pure packaging, release, CI, or environment setup work unless Python code is the main artifact
- Framework-specific rules that already have a more precise skill

## Workflow

1. Inspect the local repository patterns before introducing new structure.
2. Choose the smallest correct change that solves the task fully.
3. Keep implementation code and tests in separate files. If tests are needed, add or update dedicated test files rather than mixing test code into production modules.
4. Split large or mixed-responsibility files instead of extending them further.
5. Validate inputs and outputs at external boundaries: CLI args, env vars, files, network payloads, and public APIs.
6. Prefer the smallest relevant verification step before expanding scope.

## Core Rules

### File size and structure

- Target Python source files under 400 lines when practical.
- Reconsider structure before a file passes roughly 500 lines.
- Split by responsibility, not arbitrarily: parsing, I/O, orchestration, domain logic, and formatting often belong in separate modules.
- Keep scripts thin. Put reusable logic in importable functions or modules.

### Function and module design

- Keep functions focused on one job with clear inputs and outputs.
- Separate orchestration from business logic.
- Avoid hidden global state, implicit mutation, and long parameter lists.
- Use descriptive names; do not rely on comments to explain vague code.
- Introduce abstractions only when they remove real duplication or clarify a boundary.

### Types and contracts

- Add type hints to public functions, methods, and module-level constants where useful.
- Prefer precise standard types and small dataclasses or typed objects over loose dictionaries when the structure matters.
- Validate external data at boundaries instead of letting untrusted shapes leak inward.
- Make return values explicit; avoid functions that sometimes return data and sometimes print or exit.

### Errors and failures

- Raise or handle narrow exceptions when practical.
- Use error messages that explain what failed and what input or operation caused it.
- Fail safely for scripts and CLIs: no partial destructive behavior without explicit intent.
- Do not swallow exceptions silently.

### Configuration and secrets

- Do not hardcode secrets, tokens, or user-specific paths.
- Read configurable values from the smallest existing config surface or from explicit parameters.
- Keep non-secret defaults near the code only when they are true code defaults, not deployment settings.

### Comments and docstrings

- Add comments only for non-obvious reasoning, invariants, or tradeoffs.
- Avoid narrative comments that restate the code.
- Add docstrings when they clarify behavior, inputs, outputs, or side effects for public modules and functions.

### Scripts and CLIs

- Use a `main()` entrypoint for executable scripts.
- Parse arguments explicitly and return process exit codes in a predictable way.
- Print deterministic, concise output suitable for terminal use and automation.
- Keep file operations, network calls, and destructive actions explicit.

## Review Checklist

- Is the file still small enough to understand in one pass?
- Does each function do one clear job?
- Are I/O and side effects separated from core logic?
- Are public interfaces typed and boundary inputs validated?
- Is configuration externalized instead of hardcoded?
- Is reusable logic kept out of the CLI or script entrypoint?
- Are tests kept in separate test files rather than embedded in implementation code?

## Examples

### Good triggers

- "Write a Python script to normalize these CSV files."
- "Refactor this Python module into smaller files."
- "Add a CLI subcommand for exporting user data."
- "Clean up this one-off utility so it is safer to rerun."

### Bad triggers

- "Write pytest tests for this module."
- "Improve fixture design for this test suite."
- "Raise coverage on this Python package."

## Reference

Read [references/conventions.md](references/conventions.md) when you need concrete examples for file splitting, module layout, typing, config handling, or CLI structure.
