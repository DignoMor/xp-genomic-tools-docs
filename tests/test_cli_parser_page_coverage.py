"""Parser-to-page coverage for CLI reference tickets 07-09, 11-12."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


DOCS_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = DOCS_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from cli_page_registry import ALL_TOOLS, REFERENCE_FIELDS, validate_registry_against_records  # noqa: E402

CODE_ROOT = DOCS_ROOT.parent / "code"


class CliParserPageCoverageTest(unittest.TestCase):
    def test_registry_matches_installed_parsers(self) -> None:
        for tool in ALL_TOOLS:
            records = json.loads(
                subprocess.check_output(
                    [
                        str(CODE_ROOT / ".venv/bin/python"),
                        str(SCRIPTS_ROOT / "extract_cli_reference.py"),
                        "--code-root",
                        str(CODE_ROOT),
                        "--tool",
                        tool.console_name,
                    ],
                    text=True,
                )
            )
            validate_registry_against_records(tool, records)

    def test_every_command_page_declares_parser_inventory(self) -> None:
        for tool in ALL_TOOLS:
            inventory_path = DOCS_ROOT / f"docs/reference/cli/{tool.slug}/inventory.json"
            payload = json.loads(inventory_path.read_text())
            self.assertEqual(set(payload["commands"]), set(tool.invocable_paths))
            for entry in payload["entries"]:
                if not entry["path"].startswith("reference/cli/"):
                    continue
                page = DOCS_ROOT / "docs" / f"{entry['path']}.md"
                if not page.is_file():
                    page = DOCS_ROOT / "docs" / entry["path"] / "index.md"
                self.assertTrue(page.is_file(), page)
                text = page.read_text()
                for field in REFERENCE_FIELDS:
                    self.assertIn(f"## {field}", text, f"{page} lacks {field}")
                self.assertIn("## Example", text, f"{page} lacks Example")
                if entry["path"].count("/") >= 4:
                    self.assertIn("Parser inventory:", text)


if __name__ == "__main__":
    unittest.main()
