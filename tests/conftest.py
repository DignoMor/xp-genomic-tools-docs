"""Reset mutable docs fixtures after tests that patch sources in place."""

from __future__ import annotations

from pathlib import Path

import pytest


DOCS_ROOT = Path(__file__).resolve().parents[1]
_FIXTURES = DOCS_ROOT / "tests/fixtures"
_MASK_INTERSECT = (
    DOCS_ROOT
    / "docs/reference/cli/authored/genomic-element-tools/mask-op/intersect.md"
)


def _golden(name: str) -> str:
    return (_FIXTURES / name).read_text()


@pytest.fixture(autouse=True)
def _restore_docs_fixtures() -> None:
    (DOCS_ROOT / "mkdocs.yml").write_text(_golden("mkdocs.golden.yml"))
    (DOCS_ROOT / "docs/library.md").write_text(_golden("library.golden.md"))
    (DOCS_ROOT / "docs/llms.txt").write_text(_golden("llms.golden.txt"))
    (
        DOCS_ROOT / "docs/reference/python/elements/genomic-elements.md"
    ).write_text(_golden("genomic-elements.golden.md"))
    _MASK_INTERSECT.write_text(_golden("mask-op-intersect.golden.md"))
    yield
    (DOCS_ROOT / "mkdocs.yml").write_text(_golden("mkdocs.golden.yml"))
    (DOCS_ROOT / "docs/library.md").write_text(_golden("library.golden.md"))
    (DOCS_ROOT / "docs/llms.txt").write_text(_golden("llms.golden.txt"))
    (
        DOCS_ROOT / "docs/reference/python/elements/genomic-elements.md"
    ).write_text(_golden("genomic-elements.golden.md"))
    _MASK_INTERSECT.write_text(_golden("mask-op-intersect.golden.md"))
