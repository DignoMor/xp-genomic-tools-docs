"""Release-build and execution acceptance for ticket 16 quickstarts."""

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
BUILD_SCRIPT = DOCS_ROOT / "scripts/build_release_docs.py"
INVENTORY = DOCS_ROOT / "tests/ticket16_reference_inventory.json"


class Ticket16QuickstartsTest(unittest.TestCase):
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

    def test_synthetic_assets_exist_with_deliberate_names(self) -> None:
        for asset in self.inventory["assets"]:
            source = DOCS_ROOT / asset["source_path"]
            self.assertTrue(source.is_file(), source)
            self.assertIn("quickstart-synthetic", source.name)
            self.assertNotIn("fixtures", source.as_posix())
            self.assertNotIn("tests/", source.as_posix())

    def test_python_quickstart_executes_in_aligned_environment(self) -> None:
        from RGTools import GenomicElements

        regions = DOCS_ROOT / self.inventory["assets"][0]["source_path"]
        genome = DOCS_ROOT / self.inventory["assets"][1]["source_path"]
        expectations = self.inventory["python_expectations"]

        ge = GenomicElements(str(regions), "bed3", str(genome))
        try:
            self.assertEqual(ge.get_num_regions(), expectations["num_regions"])
            self.assertEqual(ge.get_all_region_seqs(), expectations["sequences"])
            one_hot = ge.get_all_region_one_hot()
            self.assertEqual(list(one_hot.shape), expectations["one_hot_shape"])
            chrom_order = ge.get_region_bed_table().get_chrom_names().tolist()
            self.assertEqual(chrom_order, expectations["chrom_order"])
        finally:
            ge.close()

    def test_cli_quickstart_commands_execute_with_expected_outputs(self) -> None:
        regions = DOCS_ROOT / self.inventory["assets"][0]["source_path"]
        genome = DOCS_ROOT / self.inventory["assets"][1]["source_path"]
        motif_tools = CODE_ROOT / ".venv/bin/MotifTools"
        genomic_tools = CODE_ROOT / ".venv/bin/GenomicElementTools"

        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            smoke_output = work / "random.fasta"
            smoke_cmd = [
                str(motif_tools),
                *self.inventory["cli_smoke"]["command"][1:],
            ]
            smoke_cmd[-1] = str(smoke_output)
            completed = subprocess.run(smoke_cmd, capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                smoke_output.read_text(),
                self.inventory["cli_smoke"]["expected_fasta"],
            )

            export_output = work / "exported.fa"
            export_cmd = [
                str(genomic_tools),
                *self.inventory["cli_export"]["command"][1:],
            ]
            export_cmd[export_cmd.index("{genome}")] = str(genome)
            export_cmd[export_cmd.index("{regions}")] = str(regions)
            export_cmd[export_cmd.index("{output}")] = str(export_output)
            completed = subprocess.run(export_cmd, capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                export_output.read_text(),
                self.inventory["cli_export"]["expected_fasta"],
            )

    def _built_page(self, site: Path, page_path: str) -> Path:
        if page_path.endswith("/index") or page_path == "get-started":
            # MkDocs serves index.md at the directory URL without an extra segment.
            if page_path == "get-started":
                return site / "get-started" / "index.html"
            stem = page_path.removesuffix("/index")
            return site / stem / "index.html"
        return site / page_path / "index.html"

    def test_built_quickstarts_serve_assets_and_route_python_vs_cli(self) -> None:
        release = self.inventory["release"]
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            site = Path(directory)

            for page_key in (
                "landing_path",
                "python_quickstart_path",
                "cli_quickstart_path",
            ):
                built = self._built_page(site, self.inventory[page_key])
                self.assertTrue(built.is_file(), built)
                rendered = html.unescape(built.read_text()).lower()
                self.assertIn(release, rendered)
                self.assertNotRegex(
                    rendered,
                    r"/specs/|delivery-spec|spec00[245]",
                    f"{page_key} leaked private specification material",
                )

            landing = html.unescape(
                self._built_page(site, self.inventory["landing_path"]).read_text()
            ).lower()
            for link in self.inventory["landing_links"]:
                self.assertIn(link, landing, f"landing page missing route to {link}")

            for asset in self.inventory["assets"]:
                built_asset = site / asset["site_path"]
                self.assertTrue(built_asset.is_file(), built_asset)
                source = (DOCS_ROOT / asset["source_path"]).read_text()
                self.assertEqual(built_asset.read_text(), source)

            python_page = html.unescape(
                self._built_page(site, self.inventory["python_quickstart_path"]).read_text()
            )
            cli_page = html.unescape(
                self._built_page(site, self.inventory["cli_quickstart_path"]).read_text()
            )
            for marker in self.inventory["synthetic_markers"]:
                self.assertIn(marker, python_page.lower())
                self.assertIn(marker, cli_page.lower())

            for path in self.inventory["reference_links"]["python"]:
                self.assertIn(Path(path).name, python_page, path)
            for path in self.inventory["reference_links"]["cli"]:
                self.assertIn(Path(path).name, cli_page, path)

            self.assertIn("exogenous", python_page.lower())
            self.assertIn("ExogeneousSequences", python_page)
            self.assertIn("exogenous", cli_page.lower())
            self.assertIn("export ExogeneousSequences", cli_page)

            compact = (site / "llms.txt").read_text()
            self.assertIn("get-started", compact)


if __name__ == "__main__":
    unittest.main()
