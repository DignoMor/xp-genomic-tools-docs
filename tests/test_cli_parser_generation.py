"""Built-artifact argparse coverage for SPEC010 and SPEC016."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


DOCS_ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = DOCS_ROOT.parent / "code"
GENERATED = DOCS_ROOT / "docs/reference/cli/generated"


class CliParserGenerationAcceptanceTest(unittest.TestCase):
    def test_built_references_cover_the_real_parser_trees(self) -> None:
        """The generated CLI pages are a complete release parser snapshot."""
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_release_docs.py",
                    "--code-root",
                    str(CODE_ROOT),
                    "--site-dir",
                    directory,
                ],
                cwd=DOCS_ROOT,
                capture_output=True,
                text=True,
            )
        self.assertEqual(
            completed.returncode,
            0,
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        for tool in ("genomic-element-tools", "exogeneous-sequence-tools"):
            page = GENERATED / f"{tool}.md"
            self.assertTrue(page.is_file(), page)
            text = page.read_text()
            self.assertIn("<!-- Parser inventory:", text)
            inventory = text.split("<!-- Parser inventory: ", 1)[1].split(" -->", 1)[0]
            records = json.loads(inventory)
            self.assertTrue(records)
            parser_tool = (
                "GenomicElementTools"
                if tool == "genomic-element-tools"
                else "ExogeneousSequenceTools"
            )
            extracted = json.loads(
                subprocess.check_output(
                    [
                        str(CODE_ROOT / ".venv/bin/python"),
                        str(DOCS_ROOT / "scripts/extract_cli_reference.py"),
                        "--code-root",
                        str(CODE_ROOT),
                        "--tool",
                        parser_tool,
                    ],
                    text=True,
                )
            )
            self.assertEqual(records, extracted)
            for record in records:
                self.assertIn(record["path"], text)
                for argument in record["arguments"]:
                    self.assertIn(argument["flags"], text)


if __name__ == "__main__":
    unittest.main()
