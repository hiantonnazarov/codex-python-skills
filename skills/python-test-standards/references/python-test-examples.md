# Python Test Examples

Use these examples as patterns. Follow existing repository style first.

## 1. Regression test for a parser bug

Poor:

```python
def test_bug_fix() -> None:
    assert parse_money("JPY 1200") is not None
```

Better:

```python
def test_parse_money_accepts_zero_decimal_currency() -> None:
    amount = parse_money("JPY 1200")

    assert amount.currency == "JPY"
    assert amount.minor_units == 1200
```

The better test names the behavior and asserts the meaningful output.

## 2. Exception behavior

Poor:

```python
def test_missing_config(tmp_path) -> None:
    try:
        load_config(tmp_path / "missing.toml")
    except Exception:
        assert True
```

Better:

```python
import pytest


def test_load_config_raises_config_error_when_file_is_missing(tmp_path) -> None:
    missing_path = tmp_path / "missing.toml"

    with pytest.raises(ConfigError, match="missing.toml"):
        load_config(missing_path)
```

The better test checks the exception type and useful message context.

## 3. Parametrized validation

Poor:

```python
def test_email_validation() -> None:
    assert is_valid_email("a@example.com") is True
    assert is_valid_email("bad") is False
    assert is_valid_email("") is False
```

Better:

```python
import pytest


@pytest.mark.parametrize(
    ("email", "expected"),
    [
        pytest.param("a@example.com", True, id="valid"),
        pytest.param("bad", False, id="missing-at"),
        pytest.param("", False, id="empty"),
    ],
)
def test_is_valid_email_classifies_addresses(email: str, expected: bool) -> None:
    assert is_valid_email(email) is expected
```

Use parametrization when cases share one behavior and one assertion shape.

## 4. Filesystem test with `tmp_path`

Poor:

```python
def test_write_report() -> None:
    write_report("report.txt", ["a"])
    assert open("report.txt").read() == "a\n"
```

Better:

```python
def test_write_report_writes_lines_to_target_file(tmp_path) -> None:
    report_path = tmp_path / "report.txt"

    write_report(report_path, ["a"])

    assert report_path.read_text(encoding="utf-8") == "a\n"
```

The better test is isolated and does not write into the repository.

## 5. Environment variable test with `monkeypatch`

Poor:

```python
import os


def test_config() -> None:
    os.environ["API_URL"] = "https://example.test"
    assert load_config_from_env().api_url == "https://example.test"
```

Better:

```python
def test_load_config_from_env_reads_api_url(monkeypatch) -> None:
    monkeypatch.setenv("API_URL", "https://example.test")

    config = load_config_from_env()

    assert config.api_url == "https://example.test"
```

The better test automatically restores environment state.

## 6. Mock external boundary with autospec

Poor:

```python
def test_notify_user(mocker) -> None:
    sender = mocker.Mock()

    notify_user(sender, "user@example.com")

    assert sender.send_email.called
```

Better:

```python
from unittest.mock import create_autospec


def test_notify_user_sends_expected_message() -> None:
    sender = create_autospec(EmailSender)

    notify_user(sender, "user@example.com")

    sender.send_email.assert_called_once_with(
        "user@example.com",
        "Account update",
        "Your account was updated.",
    )
```

The better test catches wrong method names and wrong call signatures.

## 7. Fake instead of deep mocks

Poor:

```python
def test_is_user_active(mocker) -> None:
    client = mocker.Mock()
    client.get_user.return_value.status.value = "active"

    assert is_user_active(client, "user-1") is True
```

Better:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class FakeUserDirectory:
    users: dict[str, DirectoryUser]

    def get_user(self, user_id: str) -> DirectoryUser:
        return self.users[user_id]


def test_is_user_active_returns_true_for_active_user() -> None:
    directory = FakeUserDirectory(
        users={"user-1": DirectoryUser(id="user-1", active=True)}
    )

    assert is_user_active(directory, "user-1") is True
```

A fake is often clearer than a mock for simple domain collaborators.

## 8. Avoid testing implementation details

Poor:

```python
def test_invoice_total_calls_rounding(mocker) -> None:
    round_money = mocker.patch("billing.invoice.round_money")

    calculate_invoice_total([LineItem(price_cents=101, quantity=1)])

    round_money.assert_called_once()
```

Better:

```python
def test_invoice_total_rounds_to_nearest_cent() -> None:
    total = calculate_invoice_total([LineItem(price_cents=101, quantity=1)])

    assert total.payable_cents == 101
```

Prefer output behavior unless the call itself is the contract.

## 9. Integration test marked explicitly

```python
import pytest


@pytest.mark.integration
def test_user_repository_persists_and_loads_user(database) -> None:
    repository = UserRepository(database)
    user = User(id="user-1", email="user@example.com")

    repository.save(user)

    assert repository.get("user-1") == user
```

Integration tests should be easy to include or exclude from command-line selection.

## 10. Property-based invariant

```python
from hypothesis import given, strategies as st


@given(st.lists(st.integers()))
def test_sort_numbers_is_ordered_and_preserves_values(values: list[int]) -> None:
    result = sort_numbers(values)

    assert result == sorted(values)
    assert values == values
```

Only use property-based tests when the repository has Hypothesis or the task explicitly allows adding it.
