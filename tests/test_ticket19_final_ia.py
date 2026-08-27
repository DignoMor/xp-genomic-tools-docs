"""Built-reference acceptance for ticket 19 final information architecture."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from release_test_helpers import preserve_agent_resources, restore_golden_docs, stage_docs_revision


DOCS_ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = DOCS_ROOT.parent / "code"
BUILD_SCRIPT = DOCS_ROOT / "scripts/build_release_docs.py"
MKDOCS_CONFIG = DOCS_ROOT / "mkdocs.yml"
INVENTORY = DOCS_ROOT / "tests/ticket19_reference_inventory.json"


class Ticket19FinalInformationArchitectureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = json.loads(INVENTORY.read_text())

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

    def _extract_top_level_nav_labels(self, config_text: str) -> list[str]:
        nav_section = config_text.split("nav:", 1)[1]
        labels: list[str] = []
        for line in nav_section.splitlines():
            if line.startswith("  - ") and not line.startswith("    "):
                labels.append(line[4:].split(":")[0].strip())
        return labels

    def test_mkdocs_declares_seven_top_level_destinations(self) -> None:
        labels = self._extract_top_level_nav_labels(MKDOCS_CONFIG.read_text())
        self.assertEqual(labels, self.inventory["top_level_nav"])

    def test_release_build_exposes_final_information_architecture(self) -> None:
        release = self.inventory["release"]
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            site = Path(directory)

            nav_html = html.unescape((site / "index.html").read_text())
            for destination in self.inventory["top_level_nav"]:
                self.assertIn(destination, nav_html, destination)

            for key, path in self.inventory["landing_paths"].items():
                built = site / path / "index.html"
                self.assertTrue(built.is_file(), f"{key} landing missing: {built}")
                rendered = html.unescape(built.read_text())
                self.assertIn(release, rendered)

            for guide in self.inventory["guide_topics"]:
                built = site / "guides" / guide / "index.html"
                self.assertTrue(built.is_file(), built)

            compact = (site / "llms.txt").read_text()
            exhaustive = (site / "llms-full.txt").read_text()
            for segment in self.inventory["llms_full_required_segments"]:
                self.assertIn(segment, exhaustive, segment)
            for link in self.inventory["llms_compact_required_links"]:
                self.assertIn(link, compact, link)

            random_seq = html.unescape(
                (
                    site
                    / self.inventory["random_seq_example"]["path"]
                    / "index.html"
                ).read_text()
            )
            self.assertIn(
                self.inventory["random_seq_example"]["expected_sequence"],
                random_seq,
            )

            for redirect in self.inventory["legacy_cli_redirects"]:
                source = redirect["source"]
                if source == "cli/index":
                    redirect_page = site / "cli" / "index.html"
                else:
                    redirect_page = site / source / "index.html"
                self.assertTrue(redirect_page.is_file(), redirect_page)
                content = redirect_page.read_text()
                self.assertRegex(
                    content,
                    r"(window\.location\.replace|http-equiv=.refresh|location\.href)",
                    msg=f"{redirect['source']} lacks redirect mechanism",
                )
                self.assertIn(redirect["target_slug"], content)

    def test_release_rejects_stale_top_level_navigation(self) -> None:
        original = MKDOCS_CONFIG.read_text()
        patched = original.replace(
            "  - Python API:",
            "  - Library (RGTools):",
            1,
        )
        self.assertNotEqual(original, patched)
        try:
            MKDOCS_CONFIG.write_text(patched)
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            restore_golden_docs(DOCS_ROOT)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("Top-level navigation", completed.stderr)


if __name__ == "__main__":
    unittest.main()
