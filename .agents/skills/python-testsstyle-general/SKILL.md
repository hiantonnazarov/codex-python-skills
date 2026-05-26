---
name: python-testsstyle-general
description: Use whenever Codex writes, edits, refactors, reviews, debugs, or runs any Python tests, including pytest and unittest suites, single test files, targeted test cases, fixture changes, flaky-test fixes, and TDD work. Trigger on requests such as "write Python tests", "run pytest", "fix this failing test", "add a regression test", or "increase Python coverage". Do not use when the main task is writing non-test Python implementation code; route those tasks to python-codingstyle-general.
---

# Python Tests Style

## Overview

Write Python tests that prove user-visible behavior, fail for the right reason, and stay cheap to rerun.

Keep this skill focused on test code and test execution. Use `python-codingstyle-general` for non-test implementation structure and style.

## Use This Skill For

- Writing or editing Python tests in `pytest`, `unittest`, or repository-specific wrappers
- Running targeted Python tests and expanding to broader checks when needed
- Practicing red-green-refactor and adding regression coverage for bugs
- Fixing flaky, brittle, or over-coupled Python tests
- Reviewing Python test quality, isolation, and failure clarity

## Do Not Use This Skill For

- Pure implementation-code tasks with no meaningful test work
- General Python module structure or script style outside test code
- Non-Python test frameworks unless the repository intentionally mixes them

## Workflow

1. Start at the lowest useful test layer that proves the behavior.
2. For behavior changes or bug fixes, write or update the test first when practical.
3. Run the smallest relevant test selection first and confirm the failure matches the intended behavior gap.
4. Change code or the test only after understanding why it failed.
5. Rerun the same targeted test until it passes cleanly.
6. Expand to the next relevant scope only after the focused check is green.

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

### Fixtures and setup

- Keep fixtures small, explicit, and local unless they are clearly reused.
- Prefer factory helpers over large fixture pyramids.
- Avoid autouse fixtures unless the repository already relies on them and the behavior is obvious.
- Keep each test independent and safe to run alone.

### Mocks and isolation

- Mock only true boundaries: network, time, filesystem, subprocesses, randomness, and expensive services.
- Prefer fakes or temporary directories over deep mocking when practical.
- Do not mock the function you are trying to test.
- If a mock expectation duplicates implementation steps, the test is probably too coupled.

### Running tests

- Run the smallest relevant command first: a single test, file, or marker.
- Expand to broader suites after the focused test passes.
- Use repository-defined commands first. If none exist, prefer the local project environment, for example `.venv/bin/python -m pytest`, `python -m pytest`, or the repository's wrapper.
- Save broad reruns for when coupling risk justifies them.

### Flaky and slow tests

- Remove timing assumptions, hidden shared state, and order dependence.
- Use deterministic data and explicit waits or polling helpers where the repository already supports them.
- Do not paper over flakiness with retries unless the repository explicitly treats retries as the correct mechanism.

## Execution Pattern

1. Identify the narrowest command that exercises the target behavior.
2. Run it and inspect the failure.
3. Make the smallest test or code change required.
4. Rerun the same command.
5. Expand to nearby tests or the full relevant suite.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Writing tests after changing code without verifying they fail first | Add or adjust the test first and confirm a meaningful failure |
| Testing private helper internals instead of behavior | Move assertions to outputs, side effects, or public contracts |
| Hiding many scenarios inside one giant test | Split into named tests with one intent each |
| Reusing huge fixtures everywhere | Replace with smaller local builders or focused fixtures |
| Making tests pass by deleting assertions | Strengthen the behavior check instead of weakening it |
| Running the full suite on every iteration | Start narrow, then widen only when useful |

## Examples

### Good triggers

- "Write pytest coverage for this Python bug fix."
- "Run this failing Python test file and fix the regression."
- "Add a regression test before changing the parser."
- "Refactor these fixtures so the tests are easier to understand."

### Bad triggers

- "Write a new Python CLI for this workflow."
- "Split this application module into smaller files."
- "Improve typing in this Python library."

## Reference

Read [references/testing-reference.md](references/testing-reference.md) for concrete pytest patterns, test command examples, fixture guidance, and red-green examples.
