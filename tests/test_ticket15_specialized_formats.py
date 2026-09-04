"""Built-reference coverage for ticket 15 specialized data formats."""

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
INVENTORY = DOCS_ROOT / "tests/ticket15_reference_inventory.json"
BUILD_SCRIPT = DOCS_ROOT / "scripts/build_release_docs.py"
RELEASE = "0.4.0a1"
LIVE_NETWORK_MARKERS = (
    "requests.get(",
    "EnsemblRestSearch(",
    "get_rsid_from_location",
    "live network",
)


class Ticket15SpecializedFormatsTest(unittest.TestCase):
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

    def test_specialized_format_pages_without_live_service_calls(self) -> None:
        inventory = json.loads(INVENTORY.read_text())
        self.assertEqual(inventory["release"], RELEASE)
        required_fields = inventory["required_fields"]
        link_heading = inventory["link_heading"]
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            site = Path(directory)
            for entry in inventory["entries"]:
                format_path = entry["path"]
                built = site / format_path / "index.html"
                self.assertTrue(built.is_file(), format_path)
                rendered = html.unescape(built.read_text())
                source = (DOCS_ROOT / "docs" / format_path).with_suffix(".md").read_text()
                for field in required_fields:
                    self.assertIn(field, rendered, f"{format_path} lacks {field}")
                for symbol in entry["symbols"]:
                    self.assertIn(symbol, rendered, f"{format_path} lacks {symbol}")
                self.assertIn(RELEASE, rendered, f"{format_path} lacks release binding")
                self.assertIn("Available since", rendered, f"{format_path} lacks introduction history")
                self.assertIn(link_heading, rendered, f"{format_path} lacks link section")
                for api_path in entry.get("related_api", []):
                    api_slug = Path(api_path).name
                    self.assertIn(api_slug, rendered, f"{format_path} missing API link to {api_path}")
                for cli_path in entry.get("related_cli", []):
                    cli_slug = Path(cli_path).name
                    self.assertIn(cli_slug, rendered, f"{format_path} missing CLI link to {cli_path}")
                for back_api in entry.get("backlink_api", []):
                    back_built = site / back_api / "index.html"
                    self.assertTrue(back_built.is_file(), back_api)
                    back_rendered = html.unescape(back_built.read_text())
                    slug = Path(format_path).name
                    self.assertIn(
                        slug,
                        back_rendered,
                        f"{back_api} does not link back to {format_path}",
                    )
                for back_cli in entry.get("backlink_cli", []):
                    back_built = site / back_cli / "index.html"
                    self.assertTrue(back_built.is_file(), back_cli)
                    back_rendered = html.unescape(back_built.read_text())
                    slug = Path(format_path).name
                    self.assertIn(
                        slug,
                        back_rendered,
                        f"{back_cli} does not link back to {format_path}",
                    )
                self.assertNotRegex(
                    rendered.lower(),
                    r"/specs/|delivery-spec|spec00[6789]",
                    f"{format_path} leaked private specification material",
                )
                for marker in LIVE_NETWORK_MARKERS:
                    self.assertNotIn(marker, source, f"{format_path} test source invokes live network: {marker}")

    def test_meme_bigwig_gtf_and_snp_semantics_are_explicit(self) -> None:
        meme = (DOCS_ROOT / "docs/reference/formats/motifs/meme.md").read_text()
        bigwig = (DOCS_ROOT / "docs/reference/formats/signal/bigwig.md").read_text()
        gtf = (DOCS_ROOT / "docs/reference/formats/gtf/gencode.md").read_text()
        snp = (DOCS_ROOT / "docs/reference/formats/snp/ensembl-simple-info.md").read_text()
        self.assertIn("ALPHABET", meme)
        self.assertIn("letter-probability matrix", meme)
        self.assertIn("strands", meme.lower())
        self.assertIn("log-odds", meme.lower())
        self.assertIn("pyBigWig", bigwig)
        self.assertIn("raw_count", bigwig)
        self.assertIn("PairedBwTrack", bigwig)
        self.assertIn("nine", gtf.lower())
        self.assertIn("1-based", gtf)
        self.assertIn("feature_type", gtf)
        self.assertIn("BED 0-based", snp)
        self.assertIn("HTTP", snp)


if __name__ == "__main__":
    unittest.main()
