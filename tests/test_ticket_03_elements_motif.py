"""Built-reference contract coverage for SPEC002, SPEC005, and SPEC006."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "docs/reference/python/elements/inventory.json"
FIELDS = ("Purpose", "Availability", "Inputs", "Types", "Shapes", "Dtypes",
          "Defaults", "Choices", "Constraints", "Outputs", "Ordering",
          "Side effects", "Failures")


class Ticket03ReferenceAcceptance(unittest.TestCase):
    def test_declared_entries_and_formats_exist_in_built_artifact(self):
        inventory = json.loads(INVENTORY.read_text())
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [str(ROOT / ".venv/bin/mkdocs"), "build", "--strict", "--clean",
                 "--site-dir", directory], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            site = Path(directory)
            pages = [site / "reference/python/elements/index.html",
                     site / "reference/python/elements/genomic-elements/index.html",
                     site / "reference/python/motifs/meme-motif/index.html",
                     site / "reference/formats/elements/annotation-arrays/index.html",
                     site / "reference/formats/elements/fasta/index.html",
                     site / "reference/formats/motifs/meme/index.html"]
            for page in (pages[0], pages[1], pages[2], pages[3], pages[4], pages[5]):
                self.assertTrue(page.is_file(), page)
            page_for_class = {
                "MemeMotif": site / "reference/python/motifs/meme-motif/index.html",
                "GenomicElements": site / "reference/python/elements/genomic-elements/index.html",
            }
            for cls, members in inventory["classes"].items():
                html = page_for_class.get(cls, pages[0]).read_text()
                self.assertIn(cls, html)
                for member in members:
                    self.assertIn(member, html, f"missing declared entry {cls}.{member}")
            for page in (pages[0], pages[2], pages[3], pages[4], pages[5]):
                html = page.read_text()
                for field in FIELDS:
                    self.assertIn(field, html, f"{page} lacks required field {field}")
            self.assertIn("numpy.bool_", pages[3].read_text())
            self.assertIn("first dimension", pages[3].read_text())
            self.assertIn("exactly one array", pages[3].read_text())


if __name__ == "__main__":
    unittest.main()
