# Python Test Quality Reference

Use this reference when writing, reviewing, or repairing Python tests.

## 1. Priorities

Apply these priorities in order:

1. Prove the required behavior.
2. Fail for one clear reason.
3. Be deterministic and isolated.
4. Be easy to read and maintain.
5. Run quickly at the appropriate test level.
6. Reuse setup without hiding intent.
7. Use repository conventions.
8. Provide useful failure diagnostics.

A test that is hard to understand is a liability even when it passes.

## 2. Test pyramid guidance

Prefer the cheapest test that proves the behavior.

| Test type | Use for | Avoid |
|---|---|---|
| Unit | Pure logic, validation, branching, transformations | Real network, real database, broad workflows |
| Component | Several internal collaborators together | Full external stack |
| Integration | Adapters, persistence, framework wiring | Business rule permutations better covered by unit tests |
| End-to-end | Critical user flows | Exhaustive edge cases |
| Regression | A specific bug that must not return | Overfitting to implementation details |
| Property-based | Invariants over broad input space | Exact scenario narratives where examples are clearer |

## 3. Arrange-act-assert

Use a clear structure:

```python
def test_discount_is_applied_to_eligible_customer() -> None:
    customer = Customer(is_active=True, order_count=5)
    order = Order(subtotal_cents=10_000)

    total = calculate_total(customer, order)

    assert total.discount_cents == 1_000
    assert total.payable_cents == 9_000
```

Keep setup minimal. If setup dominates the test, use a builder or fixture.

## 4. One behavior per test

A test may contain multiple assertions when they describe one behavior.

Good:

```python
def test_parse_user_normalizes_email_and_preserves_id() -> None:
    user = parse_user({"id": 7, "email": " USER@EXAMPLE.COM "})

    assert user.id == 7
    assert user.email == "user@example.com"
```

Poor:

```python
def test_user_features() -> None:
    assert parse_user({"id": 7, "email": "a@b.com"}).id == 7
    assert is_admin("root") is True
    assert send_email("a@b.com") is None
```

## 5. Regression tests

For a bug fix:

1. Write a test that fails on the current buggy behavior.
2. Name the test after the user-visible failure, not the internal bug.
3. Keep the reproduction minimal.
4. Assert the corrected behavior.
5. Do not assert implementation details introduced by the fix.

Good:

```python
def test_parse_amount_accepts_zero_decimal_currency() -> None:
    assert parse_amount("JPY 1200").minor_units == 1200
```

Poor:

```python
def test_bug_1429() -> None:
    assert parse_amount("JPY 1200")._currency_parser._uses_decimal is False
```

A bug number may appear in a comment only if it adds useful traceability.

## 6. Pytest assertions

Use direct asserts:

```python
def test_slugify_removes_extra_whitespace() -> None:
    assert slugify("  Hello   World  ") == "hello-world"
```

For exceptions:

```python
import pytest


def test_load_config_raises_for_missing_file(tmp_path) -> None:
    path = tmp_path / "missing.toml"

    with pytest.raises(ConfigError, match="missing.toml"):
        load_config(path)
```

Avoid catching exceptions manually unless the exception object needs multiple assertions.

## 7. Unittest assertions

When the repository uses unittest, follow its style consistently:

```python
import unittest


class ConfigTests(unittest.TestCase):
    def test_load_config_raises_for_missing_file(self) -> None:
        with self.assertRaises(ConfigError):
            load_config(Path("missing.toml"))
```

Use `subTest` for related cases:

```python
class SlugTests(unittest.TestCase):
    def test_slugify_examples(self) -> None:
        cases = {
            "Hello World": "hello-world",
            "already-clean": "already-clean",
        }

        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(slugify(raw), expected)
```

## 8. Fixtures

Fixtures should make tests clearer.

Good fixture:

```python
import pytest


@pytest.fixture
def user_payload() -> dict[str, object]:
    return {"id": 7, "email": "user@example.com", "active": True}
```

Bad fixture:

```python
import pytest


@pytest.fixture
def setup_everything():
    user = create_user()
    org = create_org()
    token = login(user)
    patch_global_state()
    return user, org, token
```

The bad fixture hides too much. Prefer named fixtures or a builder object.

## 9. Fixture scope

Default to function scope.

Use broader scopes only when:

- Setup is expensive.
- The object is immutable or safely reset.
- Tests cannot leak state through it.

Never use session-scoped mutable state without a reset strategy.

## 10. `conftest.py` policy

Use `conftest.py` for fixtures shared by multiple files in the same test tree.

Do not put all fixtures in the top-level `conftest.py` by default.

Preferred progression:

1. Test function local setup.
2. Test module fixture.
3. Package-level `conftest.py`.
4. Top-level `conftest.py` only for global test infrastructure.

## 11. Parametrization

Good:

```python
import pytest


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param("Hello World", "hello-world", id="spaces"),
        pytest.param("Already Clean", "already-clean", id="case"),
        pytest.param("multiple   spaces", "multiple-spaces", id="repeated-spaces"),
    ],
)
def test_slugify_examples(raw: str, expected: str) -> None:
    assert slugify(raw) == expected
```

Avoid parametrization when each case needs a different assertion or different setup.

## 12. Builders and factories

Use builders when object setup is verbose but domain defaults are stable.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class UserBuilder:
    id: int = 7
    email: str = "user@example.com"
    active: bool = True

    def build(self) -> User:
        return User(id=self.id, email=self.email, active=self.active)
```

Keep builders in tests unless production code genuinely needs them.

## 13. Temporary files

Use `tmp_path` for filesystem tests:

```python
def test_write_report_creates_expected_file(tmp_path) -> None:
    output_path = tmp_path / "report.txt"

    write_report(output_path, ["alpha", "beta"])

    assert output_path.read_text(encoding="utf-8") == "alpha\nbeta\n"
```

Do not write tests to real project directories unless explicitly testing project file generation and cleanup is guaranteed.

## 14. Environment variables

Use `monkeypatch`:

```python
def test_load_config_reads_api_url(monkeypatch) -> None:
    monkeypatch.setenv("API_URL", "https://example.test")

    config = load_config_from_env()

    assert config.api_url == "https://example.test"
```

Never depend on a developer's real shell environment unless the test is explicitly marked and skipped when unset.

## 15. Network and external services

Default rule: no real network in unit tests.

Preferred approaches:

- Inject a client interface and use a fake.
- Use a local test server for integration behavior.
- Use recorded responses only if the repository already has that convention.
- Mark real-service tests and skip unless explicitly enabled.

A test suite should run safely offline by default.

## 16. Mock quality

Good:

```python
from unittest.mock import create_autospec


def test_notify_user_sends_email() -> None:
    sender = create_autospec(EmailSender)

    notify_user(sender, "user@example.com")

    sender.send_email.assert_called_once_with(
        "user@example.com",
        "Account update",
        "Your account was updated.",
    )
```

Poor:

```python
def test_notify_user_sends_email(mocker) -> None:
    sender = mocker.Mock()
    notify_user(sender, "user@example.com")
    assert sender.method_calls
```

A mock assertion should be specific enough to catch a real regression.

## 17. Avoid implementation-detail tests

Prefer behavior:

```python
def test_total_includes_tax() -> None:
    assert calculate_total(subtotal_cents=1000, tax_rate=0.1) == 1100
```

Avoid internals:

```python
def test_total_calls_rounder(mocker) -> None:
    rounder = mocker.patch("billing.total.round_currency")
    calculate_total(subtotal_cents=1000, tax_rate=0.1)
    rounder.assert_called_once()
```

Test interactions only when the interaction is the observable contract.

## 18. Property-based tests

Use property-based tests for invariants:

- Encoding then decoding returns the original valid value.
- Sorting output is ordered and preserves elements.
- Normalization is idempotent.
- Parser either returns a valid model or a documented error.

Example:

```python
from hypothesis import given, strategies as st


@given(st.text())
def test_slugify_is_idempotent(value: str) -> None:
    slug = slugify(value)

    assert slugify(slug) == slug
```

Do not introduce Hypothesis unless it is already available or the task explicitly allows adding it.

## 19. Skip, xfail, and markers

Use markers honestly.

- `skip`: test cannot run in the current environment.
- `skipif`: test requires a missing optional dependency or platform.
- `xfail`: known bug or unsupported behavior, ideally linked to a tracking issue in a comment.
- `slow`: test is valid but not suitable for default fast runs.
- `integration`: test crosses process, database, filesystem service, or network boundaries.

Do not use `xfail` to hide a newly introduced failure without explanation.

## 20. Flaky test handling

When a test is flaky:

1. Reproduce with repeated focused runs when practical.
2. Remove uncontrolled time, randomness, ordering, network, or shared state.
3. Tighten assertions around deterministic behavior.
4. Avoid simply increasing sleeps or timeouts.
5. Marking flaky is a last resort and must include a reason.

## 21. Test data

Prefer small inline data when readable.

Use fixture files when:

- The data is large.
- The format itself is under test.
- Reuse across tests is valuable.

Rules:

- Keep fixture files minimal.
- Name fixture files by scenario.
- Do not store secrets in test fixtures.
- Avoid opaque binary fixtures unless the binary format is the behavior under test.

## 22. Coverage review

Coverage is useful when reviewing missing risk.

Ask:

- Are important branches tested?
- Are errors tested?
- Are boundary values tested?
- Are security-sensitive paths tested?
- Are past regressions locked down?

Do not write tests only to raise a percentage.

## 23. Final response expectations

When completing a test task, report:

- Test files changed.
- Behavior covered.
- Test command run.
- Result of each command.
- Any command not run and exact reason.
- Any production files touched, if applicable.
