---
name: python-testsstyle-general
description: Use when writing, editing, refactoring, reviewing, debugging, or running Python tests - pytest, unittest, targeted failures, fixtures, mocks, flaky tests, coverage, and TDD. Trigger on "write Python tests", "run pytest", "fix this failing test", "add a regression test", or "increase Python coverage". Do not use for implementation-only Python work; route that to python-codingstyle-general.
---

# Python Tests Style

## Overview

Write Python tests that prove user-visible behavior, fail for the right reason, and stay cheap to rerun.

Keep this skill focused on test code and test execution. Use `python-codingstyle-general` for non-test implementation style and `python-architecture-general` for project layout or configuration-surface decisions.

Source order for Python test decisions: configured test tooling first; then local test patterns; then pytest or unittest semantics; then PEP 8 and Google Python Style Guide readability rules. Prefer the Python standard library and existing helpers before adding new test dependencies.

## Workflow

1. Inspect the smallest useful test context first: repo test commands, `pyproject.toml` or `pytest.ini`, markers, fixture layout, and the nearest similar test.
2. Start at the lowest useful test layer that proves the behavior.
3. For behavior changes or bug fixes, write or update the test first when practical.
4. Run the smallest relevant test selection first and confirm the failure matches the intended behavior gap.
5. Change code or the test only after understanding why it failed; do not edit assertions blindly to get green.
6. Rerun the same targeted test until it passes cleanly.
7. Expand to the next relevant scope only after the focused check is green.

## Red-Green-Refactor

### Red

- Add one focused failing test for the behavior, bug, or edge case.
- Name the test after the observable behavior.
- Confirm the test fails for the expected reason, not because of syntax, imports, or setup mistakes.

### Green

- Make the smallest change needed to pass the failing test.
- Keep the test targeted; do not dilute it with multiple behaviors.
- Prefer fixing the real defect over weakening assertions.

### Refactor

- Clean up duplication in tests after they pass.
- Extract fixtures or helpers only when reuse is real.
- Keep the assertions and failure messages at least as clear as before.

## Core Rules

### Test placement and naming

- Keep tests in dedicated test files, never inside production modules.
- Follow repository naming conventions first; otherwise prefer `tests/`, `test_*.py`, and `test_*` function names.
- Keep one test focused on one behavior. If the name needs "and", split it.
- Keep test files import-safe and deterministic; top-level setup should not perform I/O, network calls, or irreversible state changes.

### What to test

- Test behavior, contracts, and user-visible outcomes before internal implementation details.
- Cover normal flow, invalid input, boundary cases, and the regression that motivated the change.
- Prefer one strong regression test over many weak variations.
- Add integration or end-to-end coverage only when lower layers cannot prove the behavior.

### Assertions

- Make assertions specific and readable.
- Assert the behavior that matters most first.
- Avoid vague assertions such as "result is not None" when the real expected value is known.
- Do not over-assert unrelated details that make tests brittle.
- For exceptions, assert the specific exception type and meaningful message or context when that is part of the contract.

### Fixtures and setup

- Keep fixtures small, explicit, and local unless they are clearly reused.
- Prefer factory helpers over large fixture pyramids.
- Avoid autouse fixtures unless the repository already relies on them and the behavior is obvious.
- Keep each test independent and safe to run alone.
- Put cleanup in fixtures, context managers, or `tearDown`-style hooks so failed tests still release files, env changes, patches, and services.

### Mocks and isolation

- Mock only true boundaries: network, time, filesystem, subprocesses, randomness, and expensive services.
- Prefer fakes or temporary directories over deep mocking when practical.
- Do not mock the function you are trying to test.
- Patch where the dependency is looked up, not where it originally comes from.
- If a mock expectation duplicates implementation steps, the test is probably too coupled.
- Keep fake data small but realistic enough to exercise the contract, not just the happy-path shape.

### Running tests

- Run the smallest relevant command first: a single test, file, or marker.
- Expand to broader suites after the focused test passes.
- Use repository-defined commands first. If none exist, prefer the local project environment, for example `.venv/bin/python -m pytest`, `python -m pytest`, or the repository's wrapper.
- Save broad reruns for when coupling risk justifies them.

### Flaky and slow tests

- Remove timing assumptions, hidden shared state, and order dependence.
- Use deterministic data and explicit waits or polling helpers where the repository already supports them.
- Avoid sleeps unless there is no better synchronization mechanism in the repo.
- Do not paper over flakiness with retries unless the repository explicitly treats retries as the correct mechanism.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Writing tests after changing code without verifying they fail first | Add or adjust the test first and confirm a meaningful failure |
| Testing private helper internals instead of behavior | Move assertions to outputs, side effects, or public contracts |
| Hiding many scenarios inside one giant test | Split into named tests with one intent each |
| Reusing huge fixtures everywhere | Replace with smaller local builders or focused fixtures |
| Making tests pass by deleting assertions | Strengthen the behavior check instead of weakening it |
| Running the full suite on every iteration | Start narrow, then widen only when useful |

## Application Examples

- Bug fix: add one regression test that fails on the old behavior, name it after the user-visible bug, then make the smallest implementation change.
- Flaky test: identify the shared state, timing assumption, or uncontrolled boundary; replace sleep-based timing with existing polling or deterministic synchronization.
- Fixture refactor: extract only duplicated setup that appears in multiple tests; keep test-specific values visible at the call site.

## Routing Examples

Use for: "Write pytest coverage for this Python bug fix", "Run this failing Python test file and fix the regression", "Add a regression test before changing the parser".

Do not use for: "Write a new Python CLI for this workflow", "Split this application module into smaller files", "Improve typing in this Python library".

## Reference

Read [references/testing-reference.md](references/testing-reference.md) for concrete pytest patterns, test command examples, fixture guidance, and red-green examples.

Use [assets/test-change-template.md](assets/test-change-template.md) only when the user asks for a test plan, coverage note, or test handoff.
