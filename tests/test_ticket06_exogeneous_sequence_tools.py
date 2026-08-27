"""Built-artifact acceptance for SPEC016 through SPEC020."""

from __future__ import annotations

import json
import html
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "docs/reference/cli/exogeneous-sequence-tools"


class Ticket06ExogeneousSequenceToolsReferenceTest(unittest.TestCase):
    def test_inventory_covers_every_command_path(self) -> None:
        inventory = json.loads((REFERENCE / "inventory.json").read_text())
        expected = {
            "assemble add_adapter", "assemble concat", "assemble barcode",
            "mutagenesis", "gen_track single_loc",
            "track_dim_reduction max", "track_dim_reduction argmax",
            "track_dim_reduction min", "track_dim_reduction argmin",
            "print_stat", "motif_search", "onehot",
        }
        self.assertEqual(set(inventory["commands"]), expected)
        self.assertEqual(inventory["parser_reference"], "../generated/exogeneous-sequence-tools.md")

    def test_semantic_reference_links_reusable_formats(self) -> None:
        root = ROOT / "docs/reference/cli/exogeneous-sequence-tools"
        combined = "\n".join(path.read_text() for path in root.rglob("*.md"))
        for page in ("exogenous-fasta.md", "assembly-outputs.md",
                     "mutagenesis.md", "track-stat-arrays.md",
                     "motif-outputs.md", "onehot-outputs.md"):
            self.assertTrue((ROOT / "docs/reference/formats/cli/exogeneous-sequence-tools" / page).is_file())
            self.assertIn(page.replace(".md", ""), combined)

    def test_built_artifact_has_complete_cli_and_format_pages(self) -> None:
        inventory = json.loads((ROOT / "tests/ticket06_reference_inventory.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [str(ROOT / ".venv/bin/mkdocs"), "build", "--strict", "--clean",
                 "--site-dir", directory], cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            site = Path(directory)
            required = inventory["required_fields"]
            cli_html = html.unescape((site / "reference/cli/exogeneous-sequence-tools/index.html").read_text())
            for field in required:
                self.assertIn(field, cli_html)
            for symbol in inventory["entries"][0]["symbols"]:
                self.assertIn(symbol, cli_html)
            for link in ("exogenous-fasta", "assembly-outputs", "mutagenesis",
                         "track-stat-arrays", "motif-outputs", "onehot-outputs"):
                self.assertIn(link, cli_html)
            for entry in inventory["entries"][1:]:
                page = site / entry["path"] / "index.html"
                self.assertTrue(page.is_file(), page)
                rendered = html.unescape(page.read_text())
                for field in required:
                    self.assertIn(field, rendered, f"{page} lacks {field}")
                for symbol in entry["symbols"]:
                    self.assertIn(symbol, rendered, f"{page} lacks {symbol}")


if __name__ == "__main__":
    unittest.main()
