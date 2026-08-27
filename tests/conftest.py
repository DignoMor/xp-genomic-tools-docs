"""Reset mutable docs fixtures after tests that patch sources in place."""

from __future__ import annotations

from pathlib import Path

import pytest

from release_test_helpers import restore_golden_docs


DOCS_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def _restore_docs_fixtures() -> None:
    restore_golden_docs(DOCS_ROOT)
    yield
    restore_golden_docs(DOCS_ROOT)
