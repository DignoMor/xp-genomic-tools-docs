"""Helpers for acceptance tests that stage immutable documentation content."""

from __future__ import annotations

import shutil
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


def stage_docs_revision(docs_root: Path, destination: Path) -> str:
    """Create a disposable docs checkout whose commit contains all raw targets."""
    shutil.copytree(docs_root / "docs", destination / "docs")
    subprocess.run(["git", "init", "-q"], cwd=destination, check=True)
    subprocess.run(["git", "add", "docs"], cwd=destination, check=True)
    subprocess.run(
        ["git", "-c", "user.name=acceptance", "-c", "user.email=acceptance@example.invalid", "commit", "-qm", "staged docs"],
        cwd=destination,
        check=True,
    )
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=destination, text=True).strip()


@contextmanager
def preserve_agent_resources(docs_root: Path) -> Iterator[None]:
    """Keep acceptance generation from replacing source resources with temp SHAs."""
    resources = [docs_root / "docs/llms.txt", docs_root / "docs/llms-full.txt"]
    snapshots = [path.read_text() if path.exists() else None for path in resources]
    try:
        yield
    finally:
        for path, snapshot in zip(resources, snapshots):
            if snapshot is not None:
                path.write_text(snapshot)
