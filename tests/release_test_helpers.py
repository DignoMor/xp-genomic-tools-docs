"""Helpers for acceptance tests that stage immutable documentation content."""

from __future__ import annotations

import shutil
import subprocess
import re
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


def restore_golden_docs(docs_root: Path) -> None:
    """Restore mutable docs sources from committed golden fixtures."""
    fixtures = docs_root / "tests/fixtures"
    (docs_root / "mkdocs.yml").write_text((fixtures / "mkdocs.golden.yml").read_text())
    (docs_root / "docs/library.md").write_text((fixtures / "library.golden.md").read_text())
    (docs_root / "docs/llms.txt").write_text((fixtures / "llms.golden.txt").read_text())
    (
        docs_root / "docs/agent-reference.md"
    ).write_text((fixtures / "agent-reference.golden.md").read_text())
    (
        docs_root / "docs/reference/python/elements/genomic-elements.md"
    ).write_text((fixtures / "genomic-elements.golden.md").read_text())
    (
        docs_root
        / "docs/reference/cli/authored/genomic-element-tools/mask-op/intersect.md"
    ).write_text((fixtures / "mask-op-intersect.golden.md").read_text())


def stage_docs_revision(docs_root: Path, destination: Path) -> str:
    """Create a disposable docs checkout whose commit contains all raw targets."""
    shutil.copytree(docs_root / "docs", destination / "docs")
    code_root = docs_root.parent / "code"
    code_revision = subprocess.check_output(
        ["git", "-C", str(code_root), "rev-parse", "HEAD"], text=True
    ).strip()
    for resource in (
        destination / "docs/llms.txt",
        destination / "docs/llms-full.txt",
        destination / "docs/agent-reference.md",
    ):
        content = resource.read_text()
        content = re.sub(r"(?m)^Code revision: `[0-9a-f]{40}`$", f"Code revision: `{code_revision}`", content)
        content = re.sub(
            r"(?m)^\*\*Code revision:\*\* `[0-9a-f]{40}`$",
            f"**Code revision:** `{code_revision}`",
            content,
        )
        resource.write_text(content)
    subprocess.run(["git", "init", "-q"], cwd=destination, check=True)
    subprocess.run(["git", "add", "docs"], cwd=destination, check=True)
    subprocess.run(
        ["git", "-c", "user.name=acceptance", "-c", "user.email=acceptance@example.invalid", "commit", "-qm", "staged docs"],
        cwd=destination,
        check=True,
    )
    first_revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=destination, text=True).strip()
    for resource in (
        destination / "docs/llms.txt",
        destination / "docs/llms-full.txt",
        destination / "docs/agent-reference.md",
    ):
        content = resource.read_text()
        content = re.sub(
            r"(raw\.githubusercontent\.com/[^/]+/[^/]+/)[0-9a-f]{40}(/docs/)",
            rf"\g<1>{first_revision}\g<2>",
            content,
        )
        resource.write_text(content)
    subprocess.run(["git", "add", "docs"], cwd=destination, check=True)
    subprocess.run(
        ["git", "-c", "user.name=acceptance", "-c", "user.email=acceptance@example.invalid", "commit", "-qm", "bind staged resources"],
        cwd=destination,
        check=True,
    )
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=destination, text=True).strip()


@contextmanager
def preserve_agent_resources(docs_root: Path) -> Iterator[None]:
    """Release builds rewrite llms resources; conftest golden fixtures restore them."""
    yield
