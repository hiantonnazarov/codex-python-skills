#!/usr/bin/env python3
"""Run targeted Python tests with the repository's available test runner.

This helper is intentionally conservative. It prefers pytest when installed or
configured, falls back to unittest discovery, and supports explicit test targets.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path


PYTEST_CONFIG_FILES = (
    "pytest.ini",
    "pyproject.toml",
    "tox.ini",
    "setup.cfg",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run targeted Python tests.")
    parser.add_argument(
        "targets",
        nargs="*",
        help="Test files, directories, or pytest node ids to run.",
    )
    parser.add_argument(
        "-k",
        "--keyword",
        help="Pytest keyword expression, for example: 'config and not slow'.",
    )
    parser.add_argument(
        "-m",
        "--marker",
        help="Pytest marker expression, for example: 'not slow'.",
    )
    parser.add_argument(
        "--runner",
        choices=("auto", "pytest", "unittest"),
        default="auto",
        help="Test runner to use. Defaults to auto detection.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the command without executing it.",
    )
    return parser.parse_args()


def has_module(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def has_pytest_config(root: Path) -> bool:
    for filename in PYTEST_CONFIG_FILES:
        path = root / filename
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "pytest" in text or "tool.pytest" in text:
            return True
    return False


def choose_runner(root: Path, requested: str) -> str:
    if requested != "auto":
        return requested
    if has_module("pytest") or has_pytest_config(root):
        return "pytest"
    return "unittest"


def build_pytest_command(args: argparse.Namespace) -> list[str]:
    command = [sys.executable, "-m", "pytest"]
    command.extend(args.targets)
    if args.keyword:
        command.extend(["-k", args.keyword])
    if args.marker:
        command.extend(["-m", args.marker])
    if not args.targets and not args.keyword and not args.marker:
        command.append("tests")
    return command


def node_id_to_unittest_target(target: str) -> str:
    if "::" not in target:
        return target

    path_part, *node_parts = target.split("::")
    path = Path(path_part)
    module = ".".join(path.with_suffix("").parts)
    clean_node_parts = [part.split("[", maxsplit=1)[0] for part in node_parts]
    return ".".join([module, *clean_node_parts])


def build_unittest_command(args: argparse.Namespace) -> list[str]:
    command = [sys.executable, "-m", "unittest"]
    if args.keyword or args.marker:
        raise SystemExit("unittest runner does not support pytest -k/-m selection")
    if args.targets:
        command.extend(node_id_to_unittest_target(target) for target in args.targets)
    else:
        command.append("discover")
    return command


def main() -> int:
    args = parse_args()
    root = Path.cwd()
    runner = choose_runner(root, args.runner)

    if runner == "pytest":
        command = build_pytest_command(args)
    else:
        command = build_unittest_command(args)

    print("Running:", " ".join(command))
    if args.dry_run:
        return 0

    completed = subprocess.run(command, cwd=root, env=os.environ.copy(), check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
