# Python Architecture Reference

Use this reference for concrete project layout, package boundary, and configuration examples.

## Default layout example

Apply this only when the repository does not already establish a different structure:

```text
code/
  back/   # for backend part
    app/
      __init__.py
      api/
      domain/
      services/
      storage/
      settings.py
  front/    # for frontend (html css js etc) part
  tests/
    unit/
    integration/
    testlogs/
  scripts/
    sync_data.py
configs.yaml
```

Intent:

- `code/back/` holds Python application packages
- `code/front/` holds frontend assets when the project includes a frontend surface
- `code/tests/` holds test code and test support, including `testlogs/` when the repo stores test artifacts
- `code/scripts/` holds operational scripts
- `configs.yaml` holds non-secret project configuration

## Split heuristics

Split a module when:

- you cannot explain its purpose in one sentence
- it has more than one primary responsibility
- it owns multiple models or boundary contracts that change independently
- one part orchestrates work while another part defines reusable policy or domain rules
- transport concerns, persistence concerns, and domain invariants are entangled
- it depends on two unrelated parts of the system
- changes in one area force risky edits in another
- imports suggest circular or tangled relationships

Split a package when:

- one sub-area has a stable public API and another is internal-only
- adapters or integrations dominate one section while domain logic dominates another
- tests naturally cluster around different responsibilities

Treat file length as a warning sign, not the architectural reason. A 200-line file can already need decomposition if boundaries are mixed, and a 350-line file can still be fine if it owns one cohesive flow over one model.

Useful split axes:

- API or CLI schema versus domain model
- domain model versus persistence mapping
- orchestration versus pure transformation
- user-facing rendering versus machine-facing serialization
- settings loading versus runtime consumers

Avoid over-splitting:

- keep small helpers near the module they support when they are not meaningful elsewhere
- keep a short vertical slice together when the same people change it for the same reasons
- do not create micro-modules unless they introduce a real ownership or dependency boundary

Avoid fake structure:

- do not default to `utils.py`, `helpers.py`, or `misc.py` as a substitute for naming the real boundary
- do not split just because functions have different syntax shapes if they still serve one cohesive model

## Boundary example

Prefer a package shape like:

```text
app/
  api/
    handlers.py
  domain/
    models.py
    rules.py
  services/
    billing.py
  storage/
    repository.py
```

This keeps:

- `api/` at the request boundary
- `domain/` on core business rules
- `services/` on orchestration
- `storage/` on persistence details

Avoid a single package where handlers, SQL, business rules, and formatting all sit in one module tree without clear separation.

## Public API pattern

For a reusable package, expose a stable surface deliberately:

```python
from .client import Client
from .models import Result

__all__ = ["Client", "Result"]
```

Use this when the package should promise a narrow import surface.

Do not export internal helpers just because they are convenient today.

When reorganizing modules, check more than imports:

- script entrypoints and `python -m ...` paths
- config strings or plugin references that name modules directly
- docs, examples, and generated snippets that show import paths
- compatibility shims when existing callers still rely on old paths

## Settings pattern

Use `.env` for sensitive values:

```dotenv
# API token used for outbound authenticated requests
API_TOKEN=...

# Database password for the local development environment
DB_PASSWORD=...
```

Use `configs.yaml` for non-secret settings and major constants:

```yaml
# Default host for the local HTTP server
host: "127.0.0.1"

# Default application port for local runs
port: 8000

# Number of worker tasks used by background processing
worker_count: 4
```

Rules:

- every entry gets a clear descriptive comment
- non-secret tunables do not belong in `.env`

## Loading pattern

Load config once and convert it to a typed object:

```python
from dataclasses import dataclass
import os


@dataclass(slots=True)
class Settings:
    api_token: str
    host: str
    port: int


def load_settings(config: dict[str, object]) -> Settings:
    return Settings(
        api_token=os.environ["API_TOKEN"],
        host=str(config["host"]),
        port=int(config["port"]),
    )
```

Keep file reading and env access at the boundary. Pass `Settings` inward rather than re-reading config in many modules.

## Documentation expectation

Document architecture through:

- clear package and module names
- function-level docstrings across implementation modules
- comments on important logic blocks, invariants, and non-obvious branches
- concise exported interfaces
- comments for each `.env` and `configs.yaml` entry
- short local notes only where the structure would otherwise be surprising

Do not rely on long prose to compensate for poor boundaries.
