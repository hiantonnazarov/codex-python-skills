---
name: python-test-standards
description: Use this skill when writing, editing, refactoring, reviewing, selecting, or running Python tests. Applies to pytest, unittest, regression tests, unit tests, integration tests, fixtures, mocks, parametrization, coverage, red-green-refactor, and test-driven development. Do not use this as the primary guide for production Python implementation files; use python-code-standards for production code.
---

# Python Test Standards

Use this skill for Python test files and test execution. Optimize tests for signal, isolation, reproducibility, speed, and clear failure diagnostics.

## Activation rules

Use this skill when the task involves any of these actions:

- Writing or updating Python tests.
- Running, selecting, debugging, or triaging Python tests.
- Adding regression tests for a bug.
- Practicing red-green-refactor or test-driven development.
- Designing fixtures, mocks, parametrized tests, or integration-test boundaries.
- Reviewing test quality, coverage quality, flaky tests, or test layout.

Do not use this as the primary guide for production implementation files. If production code must change, apply `python-code-standards` to production files and this skill to test files.

## Context discovery

Before editing tests, inspect the smallest relevant context:

1. Repository guidance:
   - `AGENTS.md`
   - `README.md`
   - `CONTRIBUTING.md`
   - `pyproject.toml`
   - `pytest.ini`
   - `tox.ini`
   - `noxfile.py`
   - `setup.cfg`
   - `.pre-commit-config.yaml`
   - CI workflow files

2. Existing test conventions:
   - Test framework: `pytest`, `unittest`, or mixed.
   - Test root: usually `tests/`, but follow the repository.
   - Naming pattern: usually `test_*.py` or `*_test.py`.
   - Marker policy: `slow`, `integration`, `e2e`, `network`, `db`, or project-specific markers.
   - Fixture style and `conftest.py` layout.
   - Coverage command and threshold, if configured.
   - Existing factories, builders, sample data, and helper modules.

3. Follow repository conventions when they conflict with this skill.

## Core workflow

For every test task:

1. State the behavior under test in one sentence.
2. Identify the smallest test file or test area to modify.
3. Prefer a focused regression or unit test before broad integration coverage.
4. Add or update tests in separate test files, not inside production modules.
5. Keep tests deterministic: no real network, real time, random behavior, or shared mutable state unless explicitly controlled.
6. Use existing fixtures and factories when they are clear and local enough.
7. Run the narrowest useful test command first.
8. If the narrow command passes, run the broader relevant command when practical.
9. Report commands run, results, and any unrun validation with exact reasons.

## Red-green-refactor workflow

Use this workflow when adding behavior, fixing a bug, or working test-first:

1. Red: write the smallest test that proves the missing behavior or bug.
2. Run only that test and confirm it fails for the expected reason.
3. Green: make the smallest production-code change needed to pass.
4. Run the same test and confirm it passes.
5. Refactor: improve production and test code without changing behavior.
6. Run the focused test again.
7. Run the nearest affected test group.

Never skip the red step when the task explicitly asks for TDD or a regression test. If the test unexpectedly passes before the fix, reassess whether the test actually proves the bug.

## Test file and test unit size limits

Use these limits to prevent unreadable test suites.

| Unit | Target | Hard stop | Required action |
|---|---:|---:|---|
| Test file | <= 300 lines | > 500 lines | Split by behavior, module, or scenario group |
| Test function | <= 30 lines | > 60 lines | Extract setup helpers, fixtures, or clearer assertions |
| Fixture | <= 35 lines | > 70 lines | Split setup, builder, and resource lifecycle |
| `conftest.py` | <= 200 lines per test tree | > 350 lines | Move local fixtures closer to tests or into helper modules |
| Parametrize table | <= 12 inline cases | > 20 inline cases | Move cases to a named constant or case builder |
| Assertion block | <= 5 related assertions | > 10 assertions | Split by behavior or use structured expected output |

Do not expand a test file beyond the hard stop unless the change is a narrow emergency patch and splitting is unsafe in the current task.

## Test layout

Prefer this layout unless the repository already differs:

```text
tests/
  unit/
  integration/
  conftest.py
  test_<module_or_behavior>.py
```

Rules:

- Keep tests outside production modules.
- Mirror production module names when it improves discoverability.
- Group by behavior when behavior is clearer than module mirroring.
- Keep slow, network, database, and end-to-end tests separated by directory, marker, or both.
- Keep reusable test helpers under `tests/helpers/`, `tests/factories/`, or the repository's existing helper location.
- Avoid dumping unrelated fixtures into a global `conftest.py`.

## Test naming

Use names that describe behavior and expected result:

```python
def test_load_config_raises_when_file_is_missing() -> None:
    ...
```

Prefer:

- `test_<unit>_<expected_behavior>()`
- `test_<operation>_<condition>_<result>()`
- `Test<ClassOrFeature>` only when grouping methods improves readability.

Avoid vague names:

- `test_works`
- `test_success`
- `test_error`
- `test_case_1`
- `test_misc`

## Assertions

With pytest:

- Use plain `assert` for value checks.
- Compare complete values when the complete value is meaningful.
- Assert exception type and important message fragments with `pytest.raises`.
- Avoid custom assertion messages unless they add context that pytest introspection cannot show.

With unittest:

- Use `self.assertEqual`, `self.assertRaises`, and related `TestCase` assertions.
- Use `subTest` for related cases when pytest parametrization is not used.

Assertions should verify externally observable behavior, not incidental implementation details.

## Fixtures and setup

Use fixtures for reusable setup, not for hiding important test behavior.

Rules:

- Keep fixtures explicit through function arguments.
- Keep fixture scope as narrow as practical; default to function scope.
- Use `tmp_path` for filesystem tests.
- Use `monkeypatch` for environment variables, attributes, dictionaries, current directory, and import path changes.
- Prefer local fixtures in the test module when only one module needs them.
- Move fixtures to `conftest.py` only when multiple test modules use them.
- Avoid autouse fixtures unless they enforce a global safety invariant, such as blocking network access.
- Fixtures should return named objects or dataclasses when setup becomes non-trivial.

## Parametrization

Use parametrization to express the same behavior over multiple inputs.

Rules:

- Each case should be easy to read.
- Add `ids=` when cases are not self-explanatory.
- Do not hide complex logic inside parametrize tables.
- Use separate tests when cases verify different behavior.
- For many cases, use a named constant or helper that returns cases.

## Mocks, monkeypatching, and fakes

Prefer real objects for pure domain logic and fakes for external boundaries.

Use mocks when:

- The dependency is slow, nondeterministic, expensive, unsafe, or external.
- The behavior under test is interaction with a boundary.
- A fake would be more complex than the test.

Rules:

- Patch where the object is looked up, not where it is originally defined.
- Prefer `autospec=True` or `create_autospec` for `unittest.mock`.
- Prefer `monkeypatch` for environment variables and simple attribute replacement.
- Avoid asserting every internal call unless the call is the behavior.
- Avoid over-mocking domain code.
- Never allow tests to hit real network services unless explicitly marked and isolated.

## Time, randomness, and concurrency

Tests must be reproducible.

- Inject clocks instead of using real current time deep in tests.
- Freeze, monkeypatch, or pass fixed time values when behavior depends on time.
- Seed randomness or inject deterministic random providers.
- Avoid sleeping in tests. Use polling helpers with tight timeouts only when unavoidable.
- For async code, use the repository's existing async test framework and markers.
- For concurrency tests, assert stable outcomes rather than exact scheduling.

## Integration tests

Integration tests are valuable but must be explicit.

Rules:

- Mark or place integration tests separately.
- Keep them deterministic and hermetic where possible.
- Prefer local temporary resources over shared developer or CI resources.
- Do not require external services by default.
- If credentials or services are required, skip clearly when unavailable.
- Do not hide integration behavior inside unit tests.

## Coverage policy

Coverage is a signal, not the goal.

Use coverage to find untested risk, not to reward shallow assertions.

Prioritize coverage for:

- Branches with business rules.
- Error handling.
- Boundary parsing and validation.
- Security-sensitive behavior.
- Past regressions.

Avoid adding tests that execute lines without asserting meaningful behavior.

## Running tests

Use repository-native commands first.

Look for commands in:

- `AGENTS.md`
- `README.md`
- `Makefile`
- `pyproject.toml`
- `pytest.ini`
- `tox.ini`
- `noxfile.py`
- CI config

Common pytest commands, only when appropriate:

```bash
python -m pytest tests/test_module.py::test_name
python -m pytest tests/test_module.py
python -m pytest tests/unit
python -m pytest -k "keyword and not slow"
python -m pytest -m "not slow"
python -m pytest --lf
python -m pytest --collect-only -q
```

Common unittest commands, only when appropriate:

```bash
python -m unittest discover
python -m unittest tests.test_module.TestClass.test_method
```

Coverage commands, only when configured:

```bash
python -m pytest --cov=PACKAGE --cov-report=term-missing
python -m pytest --cov=PACKAGE --cov-branch --cov-report=term-missing
```

Do not invent tools that are not installed or configured.

## Optional helper script

This skill includes `scripts/run-targeted-python-tests.py`.

Use it only when the repository has no clearer native command and the task needs a safe targeted run. It detects pytest first, then unittest, and supports test node selectors.

Examples:

```bash
python .agents/skills/python-test-standards/scripts/run-targeted-python-tests.py tests/test_config.py
python .agents/skills/python-test-standards/scripts/run-targeted-python-tests.py tests/test_config.py::test_missing_file
python .agents/skills/python-test-standards/scripts/run-targeted-python-tests.py --keyword config
```

## When more detail is needed

Read these references only when relevant:

- `references/python-test-quality.md` for detailed test quality rules.
- `references/red-green-tdd-workflow.md` for TDD and bug-fix workflows.
- `references/python-test-examples.md` for examples of preferred and avoided patterns.
