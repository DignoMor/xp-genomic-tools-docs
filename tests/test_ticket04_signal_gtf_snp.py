"""Built-reference coverage for SPEC002, SPEC007, SPEC008, and SPEC009."""

from __future__ import annotations

import html
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = Path(__file__).with_name("ticket04_reference_inventory.json")


class Ticket04ReferenceArtifactTest(unittest.TestCase):
    def test_declared_entries_have_complete_built_pages_and_resolved_links(self) -> None:
        inventory = json.loads(INVENTORY.read_text())
        with tempfile.TemporaryDirectory() as directory:
            site_dir = Path(directory)
            completed = subprocess.run(
                [str(ROOT / ".venv/bin/mkdocs"), "build", "--strict", "--clean", "--site-dir", str(site_dir)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            for entry in inventory["entries"]:
                page = site_dir / entry["path"] / "index.html"
                self.assertTrue(page.is_file(), f"missing built page for {entry['symbols']}")
                rendered = html.unescape(page.read_text())
                for field in inventory["required_fields"]:
                    self.assertIn(f">{field}<", rendered, f"{page} lacks {field}")
                for symbol in entry["symbols"]:
                    self.assertIn(symbol, rendered, f"{page} lacks {symbol}")
                if "format" in entry:
                    format_page = site_dir / entry["format"] / "index.html"
                    self.assertTrue(format_page.is_file(), f"missing format target {entry['format']}")
                    self.assertIn(entry["format"].split("/")[-2], rendered.lower())
                self.assertNotRegex(rendered.lower(), r"/specs/|delivery-spec|spec00[2789]")


if __name__ == "__main__":
    unittest.main()
