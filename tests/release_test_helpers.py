"""Helpers for acceptance tests that stage immutable documentation content."""

from __future__ import annotations

import shutil
import subprocess
import re
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


def stage_docs_revision(docs_root: Path, destination: Path) -> str:
    """Create a disposable docs checkout whose commit contains all raw targets."""
    shutil.copytree(docs_root / "docs", destination / "docs")
    code_root = docs_root.parent / "code"
    code_revision = subprocess.check_output(
        ["git", "-C", str(code_root), "rev-parse", "HEAD"], text=True
    ).strip()
    for resource in (destination / "docs/llms.txt", destination / "docs/llms-full.txt"):
        content = resource.read_text()
        content = re.sub(r"(?m)^Code revision: `[0-9a-f]{40}`$", f"Code revision: `{code_revision}`", content)
        resource.write_text(content)
    subprocess.run(["git", "init", "-q"], cwd=destination, check=True)
    subprocess.run(["git", "add", "docs"], cwd=destination, check=True)
    subprocess.run(
        ["git", "-c", "user.name=acceptance", "-c", "user.email=acceptance@example.invalid", "commit", "-qm", "staged docs"],
        cwd=destination,
        check=True,
    )
    first_revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=destination, text=True).strip()
    for resource in (destination / "docs/llms.txt", destination / "docs/llms-full.txt"):
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
    """Keep acceptance generation from replacing source resources with temp SHAs."""
    resources = [docs_root / "docs/llms.txt", docs_root / "docs/llms-full.txt"]
    snapshots = [path.read_text() if path.exists() else None for path in resources]
    try:
        yield
    finally:
        for path, snapshot in zip(resources, snapshots):
            if snapshot is not None and snapshot.strip():
                path.write_text(snapshot)
