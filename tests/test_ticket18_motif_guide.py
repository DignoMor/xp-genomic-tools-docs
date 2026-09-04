"""Release-build and execution acceptance for ticket 18 motif guide."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

from release_test_helpers import preserve_agent_resources, stage_docs_revision


DOCS_ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = DOCS_ROOT.parent / "code"
BUILD_SCRIPT = DOCS_ROOT / "scripts/build_release_docs.py"
INVENTORY = DOCS_ROOT / "tests/ticket18_reference_inventory.json"
MEME_ASSET = DOCS_ROOT / "docs/get-started/assets/quickstart-synthetic-motif.meme"
REGIONS = DOCS_ROOT / "docs/get-started/assets/quickstart-synthetic-regions.bed3"
GENOME = DOCS_ROOT / "docs/get-started/assets/quickstart-synthetic-genome.fa"


class Ticket18MotifGuideTest(unittest.TestCase):
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

    def test_pwm_generation_and_searches_execute_deterministically(self) -> None:
        motif_tools = CODE_ROOT / ".venv/bin/MotifTools"
        exo_tools = CODE_ROOT / ".venv/bin/ExogenousSequenceTools"
        genomic_tools = CODE_ROOT / ".venv/bin/GenomicElementTools"
        meme = DOCS_ROOT / self.inventory["synthetic_asset"]

        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            pwm_output = work / "pwm.fasta"
            pwm_cmd = [
                str(motif_tools),
                *self.inventory["pwm_example"]["command"][1:],
            ]
            pwm_cmd[pwm_cmd.index("{meme}")] = str(meme)
            pwm_cmd[pwm_cmd.index("{output}")] = str(pwm_output)
            completed = subprocess.run(pwm_cmd, capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                pwm_output.read_text(),
                self.inventory["pwm_example"]["expected_fasta"],
            )

            exo_cmd = [
                str(exo_tools),
                *self.inventory["exogenous_search"]["command"][1:],
            ]
            exo_cmd[exo_cmd.index("{fasta}")] = str(pwm_output)
            exo_cmd[exo_cmd.index("{meme}")] = str(meme)
            completed = subprocess.run(exo_cmd, capture_output=True, text=True, cwd=work)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            exo_track = work / "es_scores.QUICKSTART_MOTIF.npy"
            self.assertTrue(exo_track.is_file(), exo_track)
            self.assertEqual(
                list(np.load(exo_track).shape),
                self.inventory["exogenous_search"]["expected_shape"],
            )

            geo_cmd = [
                str(genomic_tools),
                *self.inventory["genomic_search"]["command"][1:],
            ]
            geo_cmd[geo_cmd.index("{genome}")] = str(GENOME)
            geo_cmd[geo_cmd.index("{regions}")] = str(REGIONS)
            geo_cmd[geo_cmd.index("{meme}")] = str(meme)
            completed = subprocess.run(geo_cmd, capture_output=True, text=True, cwd=work)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            geo_track = work / "ge_scores.QUICKSTART_MOTIF.npy"
            self.assertTrue(geo_track.is_file(), geo_track)
            self.assertEqual(
                list(np.load(geo_track).shape),
                self.inventory["genomic_search"]["expected_shape"],
            )

    def test_built_motif_guide_links_references_and_preserves_ownership(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            built = Path(directory) / self.inventory["guide_path"] / "index.html"
            self.assertTrue(built.is_file(), built)
            rendered = html.unescape(built.read_text())
            article = rendered.split("<article", 1)[1].split("</article>", 1)[0]
            text = re.sub(r"<[^>]+>", " ", article)
            text = re.sub(r"\s+", " ", text)

            self.assertIn(self.inventory["title"], text)
            self.assertIn(self.inventory["release"], rendered)
            for term in self.inventory["ownership_terms"]:
                self.assertIn(term, text, term)
            for link in self.inventory["reference_links"]:
                self.assertIn(Path(link).name, rendered, link)
            for marker in self.inventory["task_markers"]:
                self.assertIn(marker, text, marker)
            self.assertIn("exogenous", text.lower())
            self.assertIn("ExogenousSequenceTools", text)
            self.assertNotRegex(
                text.lower(),
                r"/specs/|delivery-spec|spec00[245]",
                "motif guide leaked private specification material",
            )

            asset_built = (
                Path(directory)
                / "get-started/assets/quickstart-synthetic-motif.meme"
            )
            self.assertTrue(asset_built.is_file(), asset_built)
            self.assertEqual(
                asset_built.read_text(),
                MEME_ASSET.read_text(),
            )


if __name__ == "__main__":
    unittest.main()
