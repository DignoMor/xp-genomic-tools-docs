"""Built-artifact acceptance for MotifTools CLI and MotifGeneration docs."""

from __future__ import annotations

import html
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "docs/reference/cli/motif-tools"


class Ticket07MotifToolsReferenceTest(unittest.TestCase):
    def test_inventory_covers_every_command_path(self) -> None:
        inventory = json.loads((REFERENCE / "inventory.json").read_text())
        expected = {"anti_motif", "random_seq", "pwm_seq", "barcodes"}
        self.assertEqual(set(inventory["commands"]), expected)
        self.assertEqual(inventory["parser_reference"], "../generated/motif-tools.md")

    def test_semantic_reference_documents_anti_motif_provenance(self) -> None:
        text = (REFERENCE / "anti-motif.md").read_text()
        for phrase in (
            "anti_motif",
            "provenance",
            "nsites",
            "E-value",
            "never mutated",
            "normalize(PWM * nsites + 1)",
        ):
            self.assertIn(phrase, text)

    def test_built_artifact_has_complete_cli_and_api_pages(self) -> None:
        inventory = json.loads((ROOT / "tests/ticket07_motif_tools_reference_inventory.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    str(ROOT / ".venv/bin/mkdocs"),
                    "build",
                    "--strict",
                    "--clean",
                    "--site-dir",
                    directory,
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            site = Path(directory)
            required = inventory["required_fields"]
            cli_html = html.unescape((site / "reference/cli/motif-tools/index.html").read_text())
            anti_html = html.unescape((site / "reference/cli/motif-tools/anti-motif/index.html").read_text())
            for field in required:
                self.assertIn(field, cli_html)
                self.assertIn(field, anti_html)
            for symbol in inventory["entries"][0]["symbols"]:
                self.assertIn(symbol, cli_html)
            for phrase in ("provenance", "nsites", "E-value", "never mutated"):
                self.assertIn(phrase, anti_html)
            api_page = site / "reference/python/motifs/motif-generation/index.html"
            self.assertTrue(api_page.is_file(), api_page)
            api_html = html.unescape(api_page.read_text())
            api_fields = (
                "Status", "Purpose", "Canonical import", "Signature", "Example",
            )
            for field in api_fields:
                self.assertIn(field, api_html)
            for symbol in inventory["entries"][-1]["symbols"]:
                self.assertIn(symbol, api_html)
            generated = site / "reference/cli/generated/motif-tools/index.html"
            self.assertTrue(generated.is_file(), generated)
            self.assertIn("anti_motif", generated.read_text())


if __name__ == "__main__":
    unittest.main()
