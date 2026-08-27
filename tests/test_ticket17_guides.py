"""Built-reference and execution acceptance for ticket 17 workflow guides."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from release_test_helpers import preserve_agent_resources, stage_docs_revision


DOCS_ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = DOCS_ROOT.parent / "code"
BUILD_SCRIPT = DOCS_ROOT / "scripts/build_release_docs.py"
INVENTORY = DOCS_ROOT / "tests/ticket17_reference_inventory.json"
QUICKSTART_REGIONS = DOCS_ROOT / "docs/get-started/assets/quickstart-synthetic-regions.bed3"
QUICKSTART_GENOME = DOCS_ROOT / "docs/get-started/assets/quickstart-synthetic-genome.fa"


class Ticket17GuidesTest(unittest.TestCase):
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

    def test_genomic_elements_guide_example_executes(self) -> None:
        from RGTools import GenomicElements

        ge = GenomicElements(
            str(QUICKSTART_REGIONS),
            "bed3",
            str(QUICKSTART_GENOME),
        )
        try:
            self.assertEqual(ge.get_num_regions(), 2)
            self.assertEqual(ge.get_all_region_seqs(), ["GGGC", "ACGT"])
            with tempfile.TemporaryDirectory() as directory:
                export_path = Path(directory) / "exported.fa"
                ge.export_exogeneous_sequences(str(export_path))
                self.assertIn(">chrB:1-5", export_path.read_text())
        finally:
            ge.close()

    def test_built_guides_link_references_and_use_canonical_language(self) -> None:
        release = self.inventory["release"]
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            site = Path(directory)

            for guide in self.inventory["guides"]:
                built = site / guide["path"] / "index.html"
                self.assertTrue(built.is_file(), built)
                rendered = html.unescape(built.read_text())
                self.assertIn(release, rendered)
                self.assertIn(guide["title"], rendered)
                for link in guide["reference_links"]:
                    self.assertIn(Path(link).name, rendered, link)
                rendered_lower = rendered.lower()
                self.assertNotRegex(
                    rendered_lower,
                    r"/specs/|delivery-spec|spec00[245]",
                    f"{guide['path']} leaked private specification material",
                )

            genomic = html.unescape(
                (site / "guides/genomic-elements/index.html").read_text()
            )
            for term in self.inventory["guides"][0]["required_terms"]:
                self.assertIn(term, genomic, term)
            self.assertIn("exogenous", genomic.lower())

            tss = html.unescape(
                (site / "guides/tss-relative-mutagenesis/index.html").read_text()
            )
            tss_article = tss.split("<article", 1)[1].split("</article>", 1)[0]
            tss_text = re.sub(r"<[^>]+>", " ", tss_article)
            tss_text = re.sub(r"\s+", " ", tss_text)
            for term in self.inventory["guides"][1]["canonical_terms"]:
                self.assertIn(term, tss_text, term)
            for marker in self.inventory["guides"][1]["missingness_markers"]:
                self.assertIn(marker, tss_text, marker)
            self.assertNotIn("index.md#tss_relative_mutagenesis", tss_text)
            self.assertNotIn("index.md#select_tss_relative_track", tss_text)


if __name__ == "__main__":
    unittest.main()
