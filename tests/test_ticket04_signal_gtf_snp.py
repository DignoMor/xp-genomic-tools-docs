"""Built-reference coverage for signal, GTF, and SNP APIs."""

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
SIGNAL_GTF_SNP_PREFIXES = (
    "reference/python/signal/",
    "reference/python/gtf/",
    "reference/python/snp/",
)
INTERNAL_SYMBOLS = ("_get_rsid_info", "_is_SNP")


class Ticket04ReferenceArtifactTest(unittest.TestCase):
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

    def test_declared_signal_gtf_and_snp_pages_are_complete(self) -> None:
        inventory = json.loads(INVENTORY.read_text())
        pages = [
            page
            for page in inventory["pages"]
            if any(page["path"].startswith(prefix) for prefix in SIGNAL_GTF_SNP_PREFIXES)
        ]
        self.assertEqual(len(pages), 3)
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            site = Path(directory)
            for page in pages:
                built = site / page["path"] / "index.html"
                self.assertTrue(built.is_file(), built)
                rendered = html.unescape(built.read_text())
                for field in API_SEMANTIC_FIELDS:
                    self.assertIn(field, rendered, f"{page['path']} lacks {field}")
                for symbol in page["symbols"]:
                    self.assertIn(symbol, rendered, f"{page['path']} lacks {symbol}")
                for internal in INTERNAL_SYMBOLS:
                    self.assertNotIn(internal, rendered, f"{page['path']} leaked {internal}")
                format_path = page.get("format")
                if format_path:
                    format_page = site / format_path / "index.html"
                    self.assertTrue(format_page.is_file(), format_page)
                self.assertNotRegex(rendered.lower(), r"/specs/|delivery-spec|spec00[2789]")


if __name__ == "__main__":
    unittest.main()
