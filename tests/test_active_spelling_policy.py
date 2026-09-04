"""Fail if Exogeneous/exogeneous appears outside the Delivery Spec allowlist."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

DOCS_ROOT = Path(__file__).resolve().parents[1]
SPELLING_RE = re.compile(r"Exogeneous|exogeneous")

SCAN_ROOTS = (
    DOCS_ROOT / "docs",
    DOCS_ROOT / "scripts",
    DOCS_ROOT / "tests",
    DOCS_ROOT / "mkdocs.yml",
    DOCS_ROOT / "README.md",
)

SKIP_DIR_NAMES = {".venv", "__pycache__", ".pytest_cache", "site"}
SKIP_SUFFIXES = {".pyc", ".pyo"}

ALLOWLIST_FILES = {
    DOCS_ROOT / "tests" / "test_exogenous_identifier_cutover.py",
    DOCS_ROOT / "tests" / "test_active_spelling_policy.py",
}


def _iter_scan_paths() -> list[Path]:
    paths: list[Path] = []
    for root in SCAN_ROOTS:
        if root.is_file():
            paths.append(root)
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue
            if path.suffix in SKIP_SUFFIXES:
                continue
            paths.append(path)
    return paths


def _collect_violations() -> list[str]:
    violations: list[str] = []
    for path in _iter_scan_paths():
        if path in ALLOWLIST_FILES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if SPELLING_RE.search(line):
                rel = path.relative_to(DOCS_ROOT)
                violations.append(f"{rel}:{line_no}: {line.strip()}")
    return violations


def test_active_surfaces_use_canonical_exogenous_spelling() -> None:
    violations = _collect_violations()
    assert not violations, "Forbidden misspellings outside allowlist:\n" + "\n".join(
        violations
    )
