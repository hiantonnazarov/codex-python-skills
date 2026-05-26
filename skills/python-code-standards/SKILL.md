---
name: python-code-standards
description: Use this skill when writing, editing, refactoring, or reviewing production Python code. Applies to Python modules, packages, scripts, APIs, services, CLIs, data-processing code, and internal libraries. Do not use this as the primary guide for Python test files; use python-test-standards for tests, fixtures, mocks, coverage, red-green-refactor, and TDD.
---

# Python Code Standards

Use this skill for production Python code. Prioritize maintainability, small diffs, type clarity, readable control flow, and repository consistency.

## Activation rules

Use this skill when the task involves any of these actions:

- Writing new Python production code.
- Editing existing Python production code.
- Refactoring Python modules, packages, services, scripts, CLIs, or internal libraries.
- Reviewing Python implementation quality.
- Improving readability, typing, error handling, logging, or module boundaries.

Do not use this as the primary guide for test files. If the task is mainly about tests, fixtures, mocks, coverage, red-green-refactor, or TDD, use `python-test-standards`. If production code and tests are both involved, apply this skill to production files only and `python-test-standards` to test files.

## Context discovery

Before editing code, inspect the smallest useful context:

1. Read repository guidance:
   - `AGENTS.md`
   - `README.md`
   - `CONTRIBUTING.md`
   - `pyproject.toml`
   - `setup.cfg`
   - `ruff.toml`
   - `.ruff.toml`
   - `mypy.ini`
   - `tox.ini`
   - `.pre-commit-config.yaml`

2. Identify:
   - Supported Python version.
   - Existing formatter, linter, and type-checker.
   - Package layout.
   - Naming conventions.
   - Existing error-handling and logging style.
   - Closest similar implementation.

3. Follow repository conventions when they conflict with this skill.

## Core workflow

For every production-code change:

1. Restate the implementation target in one sentence.
2. Locate the minimal code path that must change.
3. Preserve public API compatibility unless the task explicitly asks for a breaking change.
4. Make the smallest cohesive edit.
5. Keep functions, classes, modules, and files below the size limits below.
6. Add or update type annotations for new or modified public boundaries.
7. Use explicit, domain-meaningful names.
8. Prefer simple control flow over abstraction.
9. Run or recommend the narrowest relevant validation command available in the repository.
10. Summarize changed files and remaining risks.

## File and function size limits

| Unit | Target | Hard stop | Required action |
|---|---:|---:|---|
| Python file | <= 300 lines | > 500 lines | Split by responsibility before adding more logic |
| Function/method | <= 40 lines | > 80 lines | Extract cohesive helpers or simplify control flow |
| Class | <= 200 lines | > 300 lines | Split responsibilities or move collaborators |
| Function parameters | <= 5 regular parameters | > 7 regular parameters | Introduce a typed config object or dataclass |
| Cyclomatic branches | <= 6 meaningful branches | > 10 branches | Refactor dispatch, mapping, strategy, or smaller functions |

Do not expand a file beyond the hard stop unless the task is only a localized emergency fix and no safe split can be made in the current change.

## Style rules

Follow these defaults unless the repository specifies otherwise:

- Use `snake_case` for functions, variables, and modules.
- Use `PascalCase` for classes.
- Use `UPPER_SNAKE_CASE` for constants.
- Prefer explicit code over clever code.
- Prefer early returns over deeply nested conditionals.
- Avoid boolean parameters that change behavior drastically; use named strategies, enums, or separate functions.
- Avoid global mutable state.
- Avoid hidden IO, network calls, or environment reads in constructors.
- Avoid unrelated cleanup in files touched for a focused change.
- Add comments only for non-obvious decisions, invariants, tradeoffs, or external constraints.

## Type rules

For new or modified production code:

- Annotate all public functions, methods, and class attributes.
- Annotate private helpers when the type is not obvious.
- Prefer built-in generics: `list[str]`, `dict[str, int]`, `set[str]`.
- Prefer `collections.abc` for interfaces: `Mapping`, `Sequence`, `Iterable`, `Callable`.
- Use `Path` for filesystem paths at boundaries where possible.
- Use `dataclass(frozen=True)` for simple immutable value objects.
- Use `TypedDict` for structured dictionaries crossing function boundaries.
- Use `Protocol` when behavior matters more than concrete inheritance.
- Avoid `Any` unless it is required at an external boundary. Isolate it and narrow it quickly.
- Avoid broad `cast()` usage; prefer better narrowing.
- Do not introduce type ignores unless necessary. If required, make them narrow and explain why.

## Imports

- Use absolute imports for package code unless the repository consistently uses relative imports.
- Keep imports at module top unless delayed import prevents a real cycle or expensive optional dependency.
- Remove unused imports.
- Do not create import cycles.
- Keep `__init__.py` light; avoid heavy runtime side effects.

## Data and object design

Choose the simplest representation that preserves invariants:

- Use plain functions for stateless behavior.
- Use `dataclass` for data containers with small behavior.
- Use classes when state, invariants, lifecycle, or polymorphism are real.
- Use enums for closed sets of named states.
- Avoid inheritance unless substitutability is clear.
- Prefer composition over inheritance.
- Keep validation near input boundaries.
- Keep domain rules near the domain model, not scattered across callers.

## Error handling

- Raise specific built-in or domain exceptions.
- Catch the narrowest exception that can be handled correctly.
- Preserve exception context with `raise NewError(...) from exc` when translating exceptions.
- Do not swallow exceptions silently.
- Do not use `except Exception` unless at a process boundary, worker boundary, CLI boundary, or logging boundary where continuing is intentional.
- Do not use exceptions for normal control flow when a clear return type is better.
- Error messages must include actionable context without leaking secrets.

## Logging and output

- Use `logging.getLogger(__name__)` in production modules.
- Do not use `print()` in libraries or services.
- `print()` is acceptable only for CLI user output or intentionally user-facing scripts.
- Do not configure global logging in library modules.
- Log facts and identifiers needed for debugging.
- Do not log secrets, tokens, credentials, full personal data, or large payloads.
- Prefer structured context through logger arguments rather than f-string interpolation for routine logs.

## IO, paths, and resources

- Use `pathlib.Path` for filesystem paths.
- Use context managers for files, locks, connections, temporary resources, and cleanup-sensitive objects.
- Specify encodings for text file IO.
- Keep IO at boundaries; keep core logic pure where practical.
- Avoid changing working directory in production code.
- Avoid shelling out when a standard-library or existing internal API is available.
- When shelling out is required, avoid `shell=True` unless explicitly justified.

## Dependencies

Before adding a dependency:

1. Check whether the standard library or existing dependency already solves the problem.
2. Check repository dependency policy.
3. Prefer small, mature, maintained dependencies.
4. Avoid adding a dependency for trivial code.
5. Update lock/config files consistently if the repository uses them.
6. Explain why the dependency is necessary.

## Test boundary

This skill does not define the test strategy.

Still obey these boundaries:

- Do not put tests inside production modules.
- Do not add test-only helpers to production code unless they are legitimate public seams or internal abstractions.
- Do not weaken production behavior to make tests easier.
- If a production change requires tests, apply `python-test-standards` to test files.

## Validation

Prefer repository-native commands. Look for commands in `README.md`, `AGENTS.md`, `pyproject.toml`, `tox.ini`, `noxfile.py`, `Makefile`, and CI config.

Typical commands, only when supported by the repository:

```bash
ruff format .
ruff check .
mypy .
python -m compileall .
```

Do not invent tools that are not installed or configured. If validation cannot be run, state exactly why.

## When more detail is needed

Read these references only when relevant:

- `references/python-code-quality.md` for detailed Python standards.
- `references/python-design-examples.md` for examples of preferred refactors and anti-patterns.
