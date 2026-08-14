from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


DOCS_ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = DOCS_ROOT.parent / "code"


class ReleaseDocumentationAcceptanceTest(unittest.TestCase):
    def test_representative_reference_builds_as_a_release_artifact(self) -> None:
        """The release command proves the representative built-site seam."""
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_release_docs.py",
                    "--code-root",
                    str(CODE_ROOT),
                    "--site-dir",
                    directory,
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
