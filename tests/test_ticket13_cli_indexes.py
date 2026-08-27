"""Built-reference coverage for consolidated CLI indexes."""

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
CODE_ROOT = DOCS_ROOT.parent / "code"
INVENTORY = DOCS_ROOT / "docs/reference/cli/inventory.json"
GROUPED_INDEX = DOCS_ROOT / "docs/reference/cli/index.md"
EXACT_PATH_INDEX = DOCS_ROOT / "docs/reference/cli/exact-path-index.md"
BUILD_SCRIPT = DOCS_ROOT / "scripts/build_release_docs.py"
SCRIPTS_ROOT = DOCS_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from cli_inventory import (  # noqa: E402
    load_site_inventory,
    site_index_entries,
    validate_site_inventory,
    write_generated_cli_indexes,
)
from cli_page_registry import ALL_TOOLS  # noqa: E402


class CliIndexAcceptanceTest(unittest.TestCase):
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

    def test_site_inventory_declares_three_distinct_tool_owners(self) -> None:
        """US42-US44: grouped landing explains element, exogenous, and motif ownership."""
        inventory = json.loads(INVENTORY.read_text())
        validate_site_inventory(inventory)
        ownerships = {tool["ownership"] for tool in inventory["tools"]}
        self.assertEqual(
            ownerships,
            {
                "Genomic-element-centric",
                "Exogenous-sequence-centric",
                "Motif-centric",
            },
        )

    def test_grouped_and_exact_path_indexes_cover_every_parser_path(self) -> None:
        """US19-US20: grouped and exact-path indexes expose every declared entry."""
        inventory = load_site_inventory()
        grouped = GROUPED_INDEX.read_text()
        exact = EXACT_PATH_INDEX.read_text()
        for tool_meta in inventory["tools"]:
            self.assertIn(tool_meta["console_name"], grouped)
            self.assertIn(tool_meta["ownership"], grouped)
            self.assertIn(tool_meta["description"], grouped)
        for entry in site_index_entries(inventory):
            self.assertIn(entry["qualified_path"], exact)
            self.assertIn(entry["command_path"], exact)
        self.assertEqual(len(site_index_entries(inventory)), 51)

    def test_release_build_validates_cli_indexes_and_retires_generated_links(self) -> None:
        """US53-US55: strict build proves indexes and canonical landings."""
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            site = Path(directory)
            inventory = load_site_inventory()
            grouped = html.unescape(
                (site / "reference/cli/index.html").read_text()
            )
            exact = html.unescape(
                (site / "reference/cli/exact-path-index/index.html").read_text()
            )
            for tool_meta in inventory["tools"]:
                self.assertIn(tool_meta["console_name"], grouped)
                landing = site / tool_meta["landing"] / "index.html"
                self.assertTrue(landing.is_file(), landing)
                landing_html = landing.read_text()
                self.assertNotIn("reference/cli/generated/", landing_html)
                self.assertNotIn("../generated/", landing_html)
            for entry in site_index_entries(inventory):
                self.assertIn(entry["qualified_path"], exact)
                page = site / entry["page"] / "index.html"
                self.assertTrue(page.is_file(), page)

    def test_release_rejects_extra_cli_index_entry(self) -> None:
        """Strict build fails when the exact-path inventory gains a stale entry."""
        original = INVENTORY.read_text()
        patched = json.loads(original)
        patched["tools"].append(
            {
                "id": "extra-tools",
                "console_name": "ExtraTools",
                "ownership": "Extra-centric",
                "description": "Stale tool entry.",
                "landing": "reference/cli/motif-tools",
            }
        )
        try:
            INVENTORY.write_text(json.dumps(patched, indent=2) + "\n")
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            INVENTORY.write_text(original)
            write_generated_cli_indexes(load_site_inventory())
            restore_golden_docs(DOCS_ROOT)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("tool drift", completed.stderr.lower())

    def test_release_rejects_generated_snapshot_as_canonical_landing_link(self) -> None:
        """US53: strict build fails when a tool landing links to generated snapshots."""
        landing = DOCS_ROOT / "docs/reference/cli/authored/motif-tools/_landing.md"
        original = landing.read_text()
        patched = original.replace(
            "site-wide exact-path index",
            "[generated snapshot](../generated/motif-tools.md) and site-wide exact-path index",
        )
        try:
            landing.write_text(patched)
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            landing.write_text(original)
            restore_golden_docs(DOCS_ROOT)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("generated parser snapshots", completed.stderr.lower())


if __name__ == "__main__":
    unittest.main()
