"""Built-reference contract coverage for foundation and BedTable APIs."""

from __future__ import annotations

import html
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from release_test_helpers import preserve_agent_resources, stage_docs_revision


DOCS_ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = DOCS_ROOT.parent / "code"
INVENTORY = DOCS_ROOT / "docs/reference/python/inventory.json"
BUILD_SCRIPT = DOCS_ROOT / "scripts/build_release_docs.py"
API_SEMANTIC_FIELDS = (
    "Status",
    "Purpose",
    "Canonical import",
    "Signature",
    "Parameters",
    "Return or yield behavior",
    "Raised exceptions",
    "Constraints",
    "Ordering",
    "Side effects",
    "Lifecycle behavior",
    "Supported protocols and inheritance",
    "Example",
    "Related formats or commands",
)
FOUNDATION_BEDTABLE_PREFIXES = (
    "reference/python/foundation/",
    "reference/python/bedtable/",
)


class FoundationBedTableArtifactTest(unittest.TestCase):
    def _run_release_build(self, directory: str) -> subprocess.CompletedProcess[str]:
        staged_root = Path(directory) / "staged-docs"
        staged_root.mkdir()
        docs_revision = stage_docs_revision(DOCS_ROOT, staged_root)
        with preserve_agent_resources(DOCS_ROOT):
            return subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
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

    def test_declared_foundation_and_bedtable_pages_are_complete(self) -> None:
        inventory = json.loads(INVENTORY.read_text())
        pages = [
            page
            for page in inventory["pages"]
            if any(page["path"].startswith(prefix) for prefix in FOUNDATION_BEDTABLE_PREFIXES)
        ]
        self.assertTrue(pages)
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            site = Path(directory)
            for page in pages:
                path = site / page["path"] / "index.html"
                self.assertTrue(path.is_file(), f"missing page for {page['path']}")
                rendered = html.unescape(path.read_text())
                for field in API_SEMANTIC_FIELDS:
                    self.assertIn(field, rendered, f"{page['path']} lacks {field}")
                for symbol in page["symbols"]:
                    self.assertIn(symbol, rendered, f"{page['path']} lacks {symbol}")
                if page.get("status") == "Experimental":
                    self.assertIn("Experimental", rendered)


if __name__ == "__main__":
    unittest.main()
