"""Built-artifact acceptance for SPEC010-SPEC015 GenomicElementTools docs."""
import html
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Ticket05ReferenceArtifactTest(unittest.TestCase):
    def test_inventory_and_serialized_formats_are_built(self):
        inventory = json.loads((ROOT / "tests/ticket05_reference_inventory.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([str(ROOT / ".venv/bin/mkdocs"), "build", "--strict", "--clean", "--site-dir", directory], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            site = Path(directory)
            for entry in inventory["entries"]:
                page = site / entry["path"] / "index.html"
                self.assertTrue(page.is_file(), page)
                rendered = html.unescape(page.read_text())
                for field in inventory["required_fields"]:
                    self.assertIn(field, rendered)
                for symbol in entry["symbols"]:
                    self.assertIn(symbol, rendered)
                for format_path in entry.get("formats", []):
                    format_page = site / format_path / "index.html"
                    self.assertTrue(format_page.is_file(), format_path)
                    format_rendered = html.unescape(format_page.read_text())
                    for field in inventory["required_fields"]:
                        self.assertIn(field, format_rendered, f"{format_path} lacks {field}")
                self.assertNotIn("CountTableTools", rendered)


if __name__ == "__main__":
    unittest.main()
