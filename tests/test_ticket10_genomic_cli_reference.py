"""Built-artifact acceptance for complete GenomicElementTools CLI reference."""

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
INVENTORY = DOCS_ROOT / "docs/reference/cli/genomic-element-tools/inventory.json"
BUILD_SCRIPT = DOCS_ROOT / "scripts/build_release_docs.py"
SCRIPTS_ROOT = DOCS_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from cli_inventory import (  # noqa: E402
    load_tool_inventory,
    validate_built_tool_landing,
    validate_genomic_element_tools_inventory,
    validate_tool_inventory,
)
from cli_page_registry import GENOMIC_ELEMENT_TOOLS  # noqa: E402


class GenomicCliReferenceAcceptanceTest(unittest.TestCase):
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

    def test_inventory_maps_every_parser_path_to_one_page(self) -> None:
        inventory = load_tool_inventory(GENOMIC_ELEMENT_TOOLS)
        validate_tool_inventory(GENOMIC_ELEMENT_TOOLS, inventory)
        self.assertEqual(len(inventory["commands"]), 28)
        self.assertEqual(len(inventory["entries"]), 33)

    def test_landing_source_has_intent_grouping_and_exact_path_index(self) -> None:
        landing = (
            DOCS_ROOT / "docs/reference/cli/genomic-element-tools/index.md"
        ).read_text()
        for title in (
            "Region and signal",
            "Sequence and motif",
            "Exact command paths",
            "Legacy heading anchors",
        ):
            self.assertIn(title, landing)
        for path in ("select_tss_relative_track", "export CountTable", "mask_op"):
            self.assertIn(path, landing)

    def test_release_build_validates_genomic_landing_indexes_and_anchors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            site = Path(directory)
            inventory = json.loads(INVENTORY.read_text())
            validate_built_tool_landing(site, GENOMIC_ELEMENT_TOOLS, inventory)
            landing = html.unescape(
                (site / "reference/cli/genomic-element-tools/index.html").read_text()
            )
            for entry in inventory["entries"]:
                page = site / entry["path"] / "index.html"
                self.assertTrue(page.is_file(), page)
                rendered = html.unescape(page.read_text())
                for field in inventory["required_fields"]:
                    self.assertIn(field, rendered, f"{page} lacks {field}")
                for symbol in entry["symbols"]:
                    self.assertIn(symbol, rendered, f"{page} lacks {symbol}")
            self.assertIn('id="select_tss_relative_track"', landing)
            self.assertIn('id="tss_relative_mutagenesis"', landing)

    def test_release_rejects_inventory_command_drift(self) -> None:
        original = INVENTORY.read_text()
        patched = json.loads(original)
        patched["commands"] = patched["commands"][:-1]
        try:
            INVENTORY.write_text(json.dumps(patched, indent=2) + "\n")
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            INVENTORY.write_text(original)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("inventory commands drift", completed.stderr)


if __name__ == "__main__":
    unittest.main()
