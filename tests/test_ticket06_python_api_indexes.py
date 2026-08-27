"""Built-reference coverage for consolidated Python API indexes."""

from __future__ import annotations

import html
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from release_test_helpers import preserve_agent_resources, restore_golden_docs, stage_docs_revision


DOCS_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DOCS_ROOT / "scripts"))
from python_api_inventory import load_inventory, write_generated_indexes  # noqa: E402

CODE_ROOT = DOCS_ROOT.parent / "code"
INVENTORY = DOCS_ROOT / "docs/reference/python/inventory.json"
BUILD_SCRIPT = DOCS_ROOT / "scripts/build_release_docs.py"
GROUPED_INDEX = DOCS_ROOT / "docs/reference/python/index.md"
ALPHABETICAL_INDEX = DOCS_ROOT / "docs/reference/python/alphabetical-index.md"


class PythonApiIndexAcceptanceTest(unittest.TestCase):
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

    def test_consolidated_inventory_declares_every_supported_page(self) -> None:
        """SPEC003-SPEC009: one inventory lists every supported Python page."""
        inventory = json.loads(INVENTORY.read_text())
        paths = {page["path"] for page in inventory["pages"]}
        self.assertIn("reference/python/general-elements/load-mask-from-arr", paths)
        self.assertEqual(len(paths), 20)

    def test_grouped_and_alphabetical_indexes_cover_inventory(self) -> None:
        """US19-US20: grouped and alphabetical indexes expose every declared entry."""
        inventory = json.loads(INVENTORY.read_text())
        grouped = GROUPED_INDEX.read_text()
        alphabetical = ALPHABETICAL_INDEX.read_text()
        for page in inventory["pages"]:
            self.assertIn(page["qualified_name"], grouped)
            for alias in page.get("aliases", []):
                self.assertIn(alias, grouped)
            for entry in page.get("index_entries", [{"qualified_name": page["qualified_name"]}]):
                self.assertIn(entry["qualified_name"], alphabetical)

    def test_release_build_validates_indexes_and_member_anchors(self) -> None:
        """US67-US71: strict build proves inventory, indexes, and anchors."""
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            site = Path(directory)
            inventory = json.loads(INVENTORY.read_text())
            grouped = html.unescape(
                (site / "reference/python/index.html").read_text()
            )
            alphabetical = html.unescape(
                (site / "reference/python/alphabetical-index/index.html").read_text()
            )
            for page in inventory["pages"]:
                self.assertIn(page["qualified_name"], grouped)
                built = site / page["path"] / "index.html"
                self.assertTrue(built.is_file(), built)
                rendered = html.unescape(built.read_text())
                for symbol in page["symbols"]:
                    self.assertIn(symbol, rendered, f"{page['path']} lacks {symbol}")
                for entry in page.get(
                    "index_entries", [{"qualified_name": page["qualified_name"]}]
                ):
                    self.assertIn(entry["qualified_name"], alphabetical)
            for internal in inventory["internal_symbols"]:
                self.assertNotIn(internal, grouped)
                self.assertNotIn(internal, alphabetical)

    def test_release_rejects_undeclared_python_reference_page(self) -> None:
        """US71: strict build fails when an extra public Python page appears."""
        extra = DOCS_ROOT / "docs/reference/python/foundation/extra-api.md"
        try:
            extra.write_text("# Extra\n\n## Status\nx\n## Purpose\nx\n")
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            extra.unlink(missing_ok=True)
            restore_golden_docs(DOCS_ROOT)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("Undeclared Python reference page", completed.stderr)

    def test_release_rejects_internal_symbol_in_inventory(self) -> None:
        """US69: strict build fails when inventory declares an internal symbol."""
        original = INVENTORY.read_text()
        patched = json.loads(original)
        patched["pages"][0]["symbols"].append("set_parser_genome")
        try:
            INVENTORY.write_text(json.dumps(patched, indent=2) + "\n")
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            INVENTORY.write_text(original)
            write_generated_indexes(load_inventory())
            restore_golden_docs(DOCS_ROOT)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("internal symbols", completed.stderr.lower())


if __name__ == "__main__":
    unittest.main()
