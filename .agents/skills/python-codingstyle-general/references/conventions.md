# Python Conventions Reference

Use this reference when the task needs concrete implementation patterns, not just the high-level rules in `SKILL.md`.

## File splitting heuristics

Split a Python file when one or more of these are true:

- It is hard to explain the file's purpose in one sentence.
- It mixes CLI parsing, filesystem or network I/O, formatting, and domain logic.
- It owns multiple data models, request or response shapes, or persistence records that change independently.
- One section exists to coordinate work while another section implements the underlying rules.
- Different sections need different dependencies, mocks, or failure handling.
- New edits require scrolling through unrelated helpers.
- The file is approaching 400 lines and still growing.
- Multiple functions operate on different concepts that could be tested and reused independently.

Do not split mechanically by line count alone. Treat size as a warning sign only. Split around responsibility, model, and boundary ownership, including when that becomes clear before 400 lines.

Good split axes:

- domain model versus transport schema
- pure transformations versus side-effecting adapters
- orchestration versus reusable business rules
- human-facing formatting versus machine-facing serialization

Do not over-split:

- Keep one cohesive pipeline together when all functions serve the same model and same change reason.
- Do not create separate files for tiny helpers that are only meaningful inside one module.

Avoid fake modularity:

- Do not move unrelated leftovers into `utils.py`, `helpers.py`, or `misc.py`.
- Prefer names that describe the owned behavior, contract, or model, for example `slug_rules.py`, `csv_loader.py`, or `response_formatting.py`.

## Preferred module shape

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Record:
    name: str
    value: int


def load_records(path: Path) -> list[Record]:
    rows = path.read_text(encoding="utf-8").splitlines()
    return [parse_record(row) for row in rows if row.strip()]


def parse_record(raw: str) -> Record:
    name, value_text = raw.split(",", maxsplit=1)
    return Record(name=name.strip(), value=int(value_text))


def summarize(records: list[Record]) -> int:
    return sum(record.value for record in records)
```

Why this shape works:

- Data model is explicit.
- Parsing, loading, and domain logic are separate.
- Functions return values instead of printing.

## Thin CLI pattern

```python
from __future__ import annotations

import argparse
from pathlib import Path

from .service import load_records, summarize


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    total = summarize(load_records(args.input_path))
    print(total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Keep the CLI focused on:

- argument parsing
- calling application logic
- printing final output
- returning the exit status

Do not bury the real logic inside `main()`.

## Configuration pattern

Prefer explicit config loading at the boundary:

```python
from dataclasses import dataclass
import os


@dataclass(slots=True)
class Settings:
    api_base_url: str
    timeout_seconds: float


def load_settings() -> Settings:
    return Settings(
        api_base_url=os.environ["API_BASE_URL"],
        timeout_seconds=float(os.environ.get("TIMEOUT_SECONDS", "30")),
    )
```

Rules:

- Read environment variables once near the boundary.
- Convert raw strings into typed values immediately.
- Pass structured settings inward instead of calling `os.environ` everywhere.

Use the same rule for request payloads, CLI args, and file formats:

- normalize once at the edge
- convert to a typed or clearly-shaped internal object
- avoid repeated `dict.get(...)` parsing deep inside business logic

## Error handling pattern

Prefer errors with context:

```python
def load_payload(path: Path) -> dict[str, object]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Payload file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in payload file: {path}") from exc
```

Avoid:

- bare `except Exception:`
- printing and continuing after invalid state
- returning inconsistent sentinel values such as `None`, `False`, and `{}` for the same failure mode

## Production code versus tests

Implementation files should not contain inline test cases, debug assertions that behave like tests, or ad hoc test harnesses that belong in dedicated test files.

This skill does not define test style. Use the separate Python tests skill when the main task is test authoring or test refactoring.
