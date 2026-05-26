# Python Code Quality Reference

This reference expands the production-code rules in `SKILL.md`. Use it only when implementation details matter.

## 1. Priorities

Apply these priorities in order:

1. Correct behavior.
2. Minimal, reviewable diff.
3. Repository consistency.
4. Clear public interfaces.
5. Type clarity.
6. Simple control flow.
7. Low coupling.
8. Efficient enough implementation.
9. Formatting and lint cleanliness.

Do not optimize for abstraction before the code has a demonstrated repeated pattern.

## 2. Repository-first rule

Before applying generic Python advice, inspect existing project configuration and conventions.

Common sources:

- `pyproject.toml`
- `ruff.toml`
- `.ruff.toml`
- `setup.cfg`
- `mypy.ini`
- `tox.ini`
- `noxfile.py`
- `.pre-commit-config.yaml`
- `AGENTS.md`
- `README.md`
- `CONTRIBUTING.md`
- CI workflow files

When the repository has a clear convention, follow it even if this reference prefers another default.

## 3. Module design

A module should have one clear reason to change.

Good module responsibilities:

- Parse a specific input format.
- Implement a specific domain operation.
- Provide one adapter for an external service.
- Define domain models for one bounded concept.
- Provide a CLI entrypoint that delegates real work elsewhere.

Poor module responsibilities:

- Mixed parsing, validation, business logic, persistence, and CLI output.
- Unrelated utility collections.
- Side effects at import time.
- Large constants mixed with operational code.
- Test fixtures inside production code.

## 4. File length policy

Preferred structure:

- `models.py` for small domain/value objects.
- `service.py` or domain-specific name for orchestration.
- `repository.py`, `client.py`, or `gateway.py` for IO boundaries.
- `parser.py` or `serializer.py` for format conversion.
- `cli.py` for command-line interface.
- `exceptions.py` for domain exception types only when more than one module needs them.

Avoid creating a vague `utils.py`. If a helper is needed, name the module after the capability, such as `paths.py`, `dates.py`, `validation.py`, or `serialization.py`.

## 5. Function design

A function should do one thing at one abstraction level.

Prefer this shape:

1. Validate or normalize inputs.
2. Perform the core operation.
3. Return a clear result.

Avoid functions that:

- Mutate inputs unexpectedly.
- Read environment variables deep inside core logic.
- Perform logging, IO, transformation, and persistence together.
- Return multiple unrelated types.
- Use flags to select unrelated behaviors.
- Hide retries, network calls, or writes behind innocent names.

## 6. Naming

Names should reveal intent and domain meaning.

Use:

- `load_user_profile`
- `parse_invoice_date`
- `build_retry_policy`
- `is_eligible_for_discount`
- `normalized_email`

Avoid:

- `handle_data`
- `process_stuff`
- `do_work`
- `manager`
- `helper`
- `tmp`
- `obj`
- `data2`

Short names are acceptable only in tiny local scopes where meaning is obvious, such as `i`, `x`, `y`, `fd`.

## 7. Type annotations

Use annotations to make boundaries explicit.

Good:

```python
from collections.abc import Iterable, Mapping
from pathlib import Path


def read_user_ids(path: Path) -> list[int]:
    return [int(line) for line in path.read_text(encoding="utf-8").splitlines()]


def count_statuses(rows: Iterable[Mapping[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        status = row["status"]
        counts[status] = counts.get(status, 0) + 1
    return counts
```

Avoid unnecessary concrete inputs:

```python
def count_statuses(rows: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        status = row["status"]
        counts[status] = counts.get(status, 0) + 1
    return counts
```

Use concrete return types when callers benefit from knowing what they receive.

## 8. `Any` policy

`Any` is allowed at boundaries where the real type is unknowable, such as:

- JSON decoded from external systems.
- Third-party libraries without type stubs.
- Dynamic plugin interfaces.
- Legacy code being migrated gradually.

Rules:

- Keep `Any` local.
- Narrow it immediately.
- Do not let `Any` spread through domain logic.
- Prefer `object` when the code truly accepts any value but must narrow before use.

## 9. Dataclasses

Use `@dataclass(frozen=True)` for immutable value objects.

```python
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class AccessToken:
    value: str
    expires_at: datetime

    def is_expired(self, now: datetime) -> bool:
        return now >= self.expires_at
```

Avoid mutable dataclasses unless mutation is central to the domain.

## 10. Dictionaries and structured data

Do not pass untyped dictionaries across several layers.

For structured dictionaries, prefer `TypedDict`:

```python
from typing import TypedDict


class UserPayload(TypedDict):
    id: int
    email: str
    is_active: bool


def normalize_user(payload: UserPayload) -> UserPayload:
    return {
        "id": payload["id"],
        "email": payload["email"].strip().lower(),
        "is_active": payload["is_active"],
    }
```

For data with behavior or invariants, prefer a dataclass.

## 11. Protocols

Use `Protocol` to decouple code from concrete implementations.

```python
from typing import Protocol


class EmailSender(Protocol):
    def send_email(self, recipient: str, subject: str, body: str) -> None:
        ...


def notify_user(sender: EmailSender, email: str) -> None:
    sender.send_email(email, "Account update", "Your account was updated.")
```

Use protocols when they reduce coupling. Do not introduce them for one-off indirection.

## 12. Exceptions

Prefer precise exception handling.

```python
from pathlib import Path


class ConfigError(Exception):
    """Configuration could not be loaded or parsed."""


def load_config(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ConfigError(f"Config file does not exist: {path}") from exc
    except PermissionError as exc:
        raise ConfigError(f"Config file is not readable: {path}") from exc
```

Do not silently convert failures into empty values unless the empty value is explicitly correct domain behavior.

## 13. Logging

Production modules should create a module logger:

```python
import logging

logger = logging.getLogger(__name__)
```

Do not use `print()` in library or service modules.

Avoid logging:

- Passwords.
- API tokens.
- Session cookies.
- Full personal records.
- Raw request or response bodies unless explicitly sanitized.
- Large payloads.

## 14. IO

Prefer `pathlib.Path`.

```python
from pathlib import Path


def read_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")
```

Accept `str | Path` at user-facing boundaries only when useful. Core code should normalize once and then use `Path`.

## 15. Environment variables

Read environment variables at boundaries, not deep in domain logic.

```python
import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AppConfig:
    api_base_url: str
    request_timeout_seconds: float


def load_config_from_env() -> AppConfig:
    return AppConfig(
        api_base_url=os.environ["API_BASE_URL"],
        request_timeout_seconds=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "10")),
    )
```

## 16. Dependencies

Do not add a dependency when a simple standard-library solution is enough.

Before adding a dependency, verify:

- It is already used in the repository, or the task clearly needs it.
- It is actively maintained.
- It does not introduce avoidable security or licensing concerns.
- It does not duplicate existing internal utilities.
- It is added consistently to dependency files and lockfiles.

## 17. Backward compatibility

Before changing public behavior, check:

- Public function signatures.
- CLI flags and output.
- Serialized formats.
- Config keys.
- Environment variable names.
- Database schema expectations.
- Error types caught by callers.
- Import paths used by other modules.

If a breaking change is required, make it explicit in the final summary.

## 18. Performance

Default to readable code.

Optimize only when:

- There is an observed performance issue.
- The code is in a hot path.
- The data size makes the simple approach unsafe.
- The task explicitly asks for performance work.

Prefer algorithmic improvements over micro-optimizations.

## 19. Security hygiene

Apply these defaults:

- Validate untrusted input at boundaries.
- Avoid `eval` and `exec`.
- Avoid `shell=True`.
- Use parameterized database queries.
- Avoid logging secrets.
- Avoid writing secrets to temporary files.
- Use secure random generators from `secrets` for tokens.
- Do not hardcode credentials.

## 20. Final response expectations

When completing a production-code task, report:

- Files changed.
- Main behavior change.
- Validation run and result.
- Validation not run and exact reason, if applicable.
- Any compatibility or migration risk.
