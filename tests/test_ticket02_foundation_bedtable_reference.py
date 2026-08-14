"""Built-reference contract coverage for SPEC002, SPEC003, and SPEC004."""

from __future__ import annotations

import html
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


DOCS_ROOT = Path(__file__).resolve().parents[1]
INVENTORY = DOCS_ROOT / "docs/reference/foundation-bedtable-inventory.json"
REQUIRED_FIELDS = (
    "Purpose", "Availability", "Inputs", "Types", "Shapes", "Dtypes",
    "Defaults", "Choices", "Constraints", "Outputs", "Ordering",
    "Side effects", "Failures",
)


class FoundationBedTableArtifactTest(unittest.TestCase):
    def test_declared_ticket02_entries_are_complete_in_built_artifact(self) -> None:
        inventory = json.loads(INVENTORY.read_text())
        self.assertTrue(inventory["entries"])
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-m", "mkdocs", "build", "--strict", "--clean", "--site-dir", directory],
                cwd=DOCS_ROOT, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            site = Path(directory)
            for entry in inventory["entries"]:
                path = site / entry["path"] / "index.html"
                self.assertTrue(path.is_file(), f"missing declared entry: {entry['qualified_name']}")
                rendered = html.unescape(path.read_text())
                for field in REQUIRED_FIELDS:
                    self.assertIn(f">{field}<", rendered, f"{entry['qualified_name']} lacks {field}")
                for member in entry.get("members", []):
                    self.assertIn(member, rendered, f"{entry['qualified_name']} lacks member {member}")


if __name__ == "__main__":
    unittest.main()
