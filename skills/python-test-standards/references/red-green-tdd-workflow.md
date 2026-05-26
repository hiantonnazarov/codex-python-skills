# Red-Green-Refactor and TDD Workflow

Use this reference for test-first development, bug fixes, and regression tests.

## 1. TDD contract

When the user asks for TDD, red-green-refactor, or a regression-first fix, follow this contract:

1. Write or update a test before changing production code.
2. Run the narrow test target.
3. Confirm the test fails for the expected behavior gap.
4. Change production code minimally.
5. Run the same test and confirm it passes.
6. Refactor only after the test is green.
7. Run the affected group of tests.

If the repository cannot run tests, still write the test first and state exactly why execution was not possible.

## 2. Red step

A red test must fail for the right reason.

Good red test properties:

- It targets one behavior.
- It fails on the current implementation.
- Its failure message points to the behavior gap.
- It does not require unrelated infrastructure.
- It is minimal but realistic.

If the test passes immediately:

- The behavior may already exist.
- The test may be asserting the wrong thing.
- The fixture may not reproduce the bug.
- The test may be too broad and missing the specific condition.

Do not proceed to production changes until this is understood.

## 3. Green step

The green step should be the smallest behavior-correct change.

Rules:

- Do not redesign unrelated code.
- Do not add abstractions just for the test.
- Do not weaken validation to satisfy the test.
- Do not hardcode only the exact test case unless the behavior is explicitly case-specific.
- Keep production-code changes under `python-code-standards`.

## 4. Refactor step

Refactor only after tests pass.

Safe refactors:

- Rename unclear local variables.
- Extract setup helpers in tests.
- Remove duplicated test setup.
- Simplify production control flow.
- Move helpers to clearer modules when file-size limits require it.

After each meaningful refactor, rerun the focused test.

## 5. Bug-fix workflow

For a bug report:

1. Reproduce the bug with the smallest failing test.
2. Include the exact input or state that caused the failure.
3. Assert the externally visible corrected behavior.
4. Make the minimal fix.
5. Add adjacent edge cases only when they protect the same risk.

Example shape:

```python
def test_parse_duration_accepts_zero_seconds() -> None:
    assert parse_duration("0s") == Duration(seconds=0)
```

Avoid naming the test only after an issue number:

```python
def test_issue_813() -> None:
    ...
```

Prefer behavior-first naming. Add an issue comment only if the repository values traceability.

## 6. Characterization tests

Use characterization tests before refactoring unclear legacy behavior.

Rules:

- Capture current externally visible behavior.
- Do not assert accidental internals.
- Name the behavior as neutrally as possible.
- Add TODO comments only for known incorrect behavior that must be preserved temporarily.

Characterization tests are not a substitute for clarifying desired behavior when the task requires a behavior change.

## 7. Selecting test scope

Start narrow, then broaden.

Recommended sequence:

1. Exact test node:
   `python -m pytest tests/test_file.py::test_name`
2. Test file:
   `python -m pytest tests/test_file.py`
3. Test directory or marker:
   `python -m pytest tests/unit`
4. Full relevant suite:
   `python -m pytest`

For unittest projects:

1. Exact method:
   `python -m unittest tests.test_module.TestClass.test_method`
2. Module:
   `python -m unittest tests.test_module`
3. Discovery:
   `python -m unittest discover`

## 8. Commit-sized test changes

A good TDD edit usually changes:

- One test file.
- One production module.
- Maybe one fixture/helper file.

If many unrelated tests need edits, pause and reassess whether the production API changed too broadly.

## 9. Acceptance checks

Before finishing, verify:

- The new test fails without the production change, or the failure was observed before the fix.
- The new test passes with the production change.
- Existing nearby tests still pass.
- No production tests were placed inside production modules.
- No real external services are required by default.
- Test naming explains the behavior.
