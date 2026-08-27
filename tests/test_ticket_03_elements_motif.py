"""Built-reference contract coverage for element, motif, and TSS APIs."""

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
ELEMENT_MOTIF_PREFIXES = (
    "reference/python/general-elements/",
    "reference/python/elements/",
    "reference/python/motifs/",
)
INTERNAL_SYMBOLS = (
    "set_parser_genome",
    "set_parser_genomic_element_region",
    "set_parser_exogenous_sequences",
)


class Ticket03ReferenceAcceptance(unittest.TestCase):
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

    def test_declared_element_motif_and_tss_pages_are_complete(self) -> None:
        inventory = json.loads(INVENTORY.read_text())
        pages = [
            page
            for page in inventory["pages"]
            if any(page["path"].startswith(prefix) for prefix in ELEMENT_MOTIF_PREFIXES)
            and page.get("kind") != "method"
        ]
        self.assertTrue(pages)
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
            llms_full = (site / "llms-full.txt").read_text()
            for internal in INTERNAL_SYMBOLS:
                self.assertNotIn(internal, llms_full)
            format_pages = [
                site / "reference/formats/elements/annotation-arrays/index.html",
                site / "reference/formats/elements/fasta/index.html",
                site / "reference/formats/motifs/meme/index.html",
            ]
            for format_page in format_pages:
                self.assertTrue(format_page.is_file(), format_page)


if __name__ == "__main__":
    unittest.main()
