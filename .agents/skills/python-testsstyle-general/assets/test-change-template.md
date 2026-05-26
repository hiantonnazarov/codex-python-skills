# Python Test Change Template

Use this only when the user asks for a test plan, coverage note, or test handoff.

## Behavior Under Test

- User-visible behavior or contract:
- Regression or edge case:
- Lowest useful test layer:

## Targeted Command

```bash
python -m pytest path/to/test_file.py::test_name
```

## Expected Red

- Failure reason before the fix:
- What would make the failure invalid:

## Expected Green

- Passing assertion:
- Nearby tests to rerun:
- Broader suite only if coupling risk justifies it:
