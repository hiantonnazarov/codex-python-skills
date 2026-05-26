# Python Testing Reference

Use this reference when you need concrete Python testing patterns or example commands.

## Quick command ladder

Prefer the narrowest command that proves the current point:

```bash
# Single test function
python -m pytest tests/test_service.py::test_parses_empty_input

# Single file
python -m pytest tests/test_service.py

# Keyword selection
python -m pytest -k "empty_input and service"

# Marker selection if the repo uses markers
python -m pytest -m "unit"
```

If the repository defines a wrapper, make target, task runner, or virtualenv command, use that first.

## Red-green example

```python
def test_parse_user_rejects_missing_id() -> None:
    with pytest.raises(ValueError, match="missing user id"):
        parse_user({"name": "Ada"})
```

Why this is good:

- one behavior
- visible contract
- precise exception and message

After writing it:

1. Run the single test and confirm it fails for the right reason.
2. Make the smallest code change.
3. Rerun the same test.
4. Expand to nearby parser tests.

## Good test shape

```python
def test_normalize_title_trims_outer_whitespace() -> None:
    assert normalize_title("  Hello  ") == "Hello"
```

Prefer:

- direct setup
- one clear assertion cluster
- observable behavior

Avoid tests that need a paragraph to explain their setup.

## Fixture guidance

Use a fixture when it clearly reduces duplication:

```python
@pytest.fixture
def sample_config(tmp_path: Path) -> Path:
    path = tmp_path / "config.json"
    path.write_text('{"enabled": true}', encoding="utf-8")
    return path
```

Prefer local fixtures in the test module before promoting them to shared fixtures.

Move a fixture to `conftest.py` only when:

- it is reused across multiple files
- its name is still obvious out of local context
- the shared setup does not hide critical behavior

## Mock boundary example

```python
def test_fetch_profile_wraps_http_error(mocker: MockerFixture) -> None:
    client = mocker.Mock()
    client.get.side_effect = TimeoutError("timed out")

    with pytest.raises(ProfileError, match="profile request failed"):
        fetch_profile(client, "user-123")
```

Why this mock is acceptable:

- external boundary
- expensive or nondeterministic dependency
- assertion stays on contract, not call choreography

## Regression test pattern

For a bug fix, encode the smallest reproducible case:

```python
def test_slugify_preserves_ascii_digits_after_dash_bug() -> None:
    assert slugify("Plan 2025") == "plan-2025"
```

Name the test so the historical failure is obvious.

## Review prompts for Python tests

Ask these questions while editing or reviewing:

- Would this test fail if the real behavior regressed?
- Is the failure message specific enough to diagnose quickly?
- Can this test run alone?
- Is any fixture or mock hiding too much?
- Am I testing behavior or just replaying implementation steps?

## Documentation expectation

Document test intent through:

- test names that describe behavior
- short fixture names tied to their role
- comments only for non-obvious setup, invariants, or historical regressions

Do not add long prose when a clearer test name or helper would solve the problem.
