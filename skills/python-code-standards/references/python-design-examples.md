# Python Design Examples

Use these examples to choose better production-code shapes. They are patterns, not mandatory templates.

## 1. Split a god function

Poor:

```python
import json
import os
from pathlib import Path


def import_users(path: str) -> int:
    raw = Path(path).read_text()
    payload = json.loads(raw)
    api_url = os.environ["API_URL"]
    imported = 0
    for item in payload["users"]:
        if "email" not in item:
            continue
        email = item["email"].strip().lower()
        if "@" not in email:
            continue
        print(f"Importing {email} to {api_url}")
        imported += 1
    return imported
```

Better:

```python
import json
import logging
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

logger = logging.getLogger(__name__)


class RawUser(TypedDict, total=False):
    email: str


@dataclass(frozen=True, slots=True)
class User:
    email: str


class UserImportError(Exception):
    """User import input could not be loaded or parsed."""


def load_user_payload(path: Path) -> list[RawUser]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise UserImportError(f"Could not read user payload: {path}") from exc
    except json.JSONDecodeError as exc:
        raise UserImportError(f"Could not parse user payload as JSON: {path}") from exc

    users = payload.get("users")
    if not isinstance(users, list):
        raise UserImportError(f"User payload must contain a users list: {path}")

    return users


def normalize_users(raw_users: Iterable[RawUser]) -> list[User]:
    users: list[User] = []
    for raw_user in raw_users:
        email = raw_user.get("email", "").strip().lower()
        if is_valid_email(email):
            users.append(User(email=email))
    return users


def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email.rsplit("@", maxsplit=1)[-1]


def import_users(path: Path) -> int:
    raw_users = load_user_payload(path)
    users = normalize_users(raw_users)

    for user in users:
        logger.info("Importing user", extra={"email": user.email})

    return len(users)
```

## 2. Replace boolean flag with separate functions

Poor:

```python
def format_name(first_name: str, last_name: str, reverse: bool) -> str:
    if reverse:
        return f"{last_name}, {first_name}"
    return f"{first_name} {last_name}"
```

Better:

```python
def format_display_name(first_name: str, last_name: str) -> str:
    return f"{first_name} {last_name}"


def format_sortable_name(first_name: str, last_name: str) -> str:
    return f"{last_name}, {first_name}"
```

## 3. Replace untyped dictionary with dataclass

Poor:

```python
def calculate_total(order: dict) -> int:
    return order["unit_price_cents"] * order["quantity"]
```

Better:

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrderLine:
    unit_price_cents: int
    quantity: int

    def total_cents(self) -> int:
        return self.unit_price_cents * self.quantity
```

## 4. Keep adapters at boundaries

Poor:

```python
import requests


def is_user_active(user_id: str) -> bool:
    response = requests.get(f"https://internal.example/users/{user_id}", timeout=10)
    response.raise_for_status()
    return bool(response.json()["active"])
```

Better:

```python
from dataclasses import dataclass
from typing import Protocol


class UserDirectory(Protocol):
    def get_user(self, user_id: str) -> "DirectoryUser":
        ...


@dataclass(frozen=True, slots=True)
class DirectoryUser:
    id: str
    active: bool


def is_user_active(directory: UserDirectory, user_id: str) -> bool:
    return directory.get_user(user_id).active
```

## 5. Prefer explicit result models for non-exception outcomes

Poor:

```python
def parse_port(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return -1
```

Better:

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PortParseResult:
    ok: bool
    value: int | None
    error: str | None


def parse_port(value: str) -> PortParseResult:
    try:
        port = int(value)
    except ValueError:
        return PortParseResult(ok=False, value=None, error="Port must be an integer")

    if not 1 <= port <= 65535:
        return PortParseResult(ok=False, value=None, error="Port must be between 1 and 65535")

    return PortParseResult(ok=True, value=port, error=None)
```

## 6. Avoid import-time side effects

Poor:

```python
import os

API_TOKEN = os.environ["API_TOKEN"]
```

Better:

```python
import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApiConfig:
    token: str


def load_api_config_from_env() -> ApiConfig:
    return ApiConfig(token=os.environ["API_TOKEN"])
```

## 7. Avoid vague utility modules

Poor:

```text
src/app/utils.py
```

Better:

```text
src/app/path_rules.py
src/app/date_ranges.py
src/app/email_normalization.py
src/app/json_payloads.py
```

A helper module should communicate its domain. Vague utility modules become dumping grounds.

## 8. Prefer mapping dispatch over long equality chains

Poor:

```python
def fee_for_plan(plan: str) -> int:
    if plan == "free":
        return 0
    if plan == "starter":
        return 900
    if plan == "pro":
        return 2900
    if plan == "enterprise":
        return 99900
    raise ValueError(f"Unknown plan: {plan}")
```

Better:

```python
PLAN_FEES_CENTS: dict[str, int] = {
    "free": 0,
    "starter": 900,
    "pro": 2900,
    "enterprise": 99900,
}


def fee_for_plan(plan: str) -> int:
    try:
        return PLAN_FEES_CENTS[plan]
    except KeyError as exc:
        raise ValueError(f"Unknown plan: {plan}") from exc
```
