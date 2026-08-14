from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from release_test_helpers import preserve_agent_resources, stage_docs_revision


DOCS_ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = DOCS_ROOT.parent / "code"


class ReleaseDocumentationAcceptanceTest(unittest.TestCase):
    def test_representative_reference_builds_as_a_release_artifact(self) -> None:
        """SPEC001: the release command proves the representative built-site seam."""
        with tempfile.TemporaryDirectory() as directory:
            staged_root = Path(directory) / "staged-docs"
            staged_root.mkdir()
            docs_revision = stage_docs_revision(DOCS_ROOT, staged_root)
            with preserve_agent_resources(DOCS_ROOT):
                completed = subprocess.run(
                    [
                        sys.executable,
                        "scripts/build_release_docs.py",
                        "--code-root",
                        str(CODE_ROOT),
                        "--site-dir",
                        directory,
                        "--code-revision",
                        subprocess.check_output(
                            ["git", "-C", str(CODE_ROOT), "rev-parse", "HEAD"],
                            text=True,
                        ).strip(),
                        "--docs-revision",
                        docs_revision,
                        "--raw-source-root",
                        str(staged_root),
                    ],
                    cwd=DOCS_ROOT,
                    capture_output=True,
                    text=True,
                )

        self.assertEqual(
            completed.returncode,
            0,
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
