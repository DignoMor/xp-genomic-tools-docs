"""Built-artifact argparse coverage for SPEC010 and SPEC016."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from release_test_helpers import preserve_agent_resources, stage_docs_revision


DOCS_ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = DOCS_ROOT.parent / "code"
GENERATED = DOCS_ROOT / "docs/reference/cli/generated"


class CliParserGenerationAcceptanceTest(unittest.TestCase):
    def test_stale_generated_snapshot_is_detectable_before_regeneration(self) -> None:
        """SPEC010/SPEC016: an existing parser inventory is compared before overwrite."""
        with tempfile.TemporaryDirectory() as directory:
            staged_root = Path(directory) / "staged-docs"
            page = GENERATED / "genomic-element-tools.md"
            original = page.read_text()
            stale = re.sub(
                r"<!-- Parser inventory: .*? -->",
                '<!-- Parser inventory: [{"path":"stale"}] -->',
                original,
                count=1,
            )
            page.write_text(stale)
            try:
                staged_root.mkdir()
                docs_revision = stage_docs_revision(DOCS_ROOT, staged_root)
                completed = subprocess.run(
                    [
                        sys.executable,
                        "scripts/build_release_docs.py",
                        "--code-root",
                        str(CODE_ROOT),
                        "--site-dir",
                        str(Path(directory) / "site"),
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
            finally:
                page.write_text(original)
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("is stale", completed.stderr)

    def test_built_references_cover_the_real_parser_trees(self) -> None:
        """The generated CLI pages are a complete release parser snapshot."""
        with tempfile.TemporaryDirectory() as directory:
            staged_root = Path(directory) / "staged-docs"
            staged_root.mkdir()
            docs_revision = stage_docs_revision(DOCS_ROOT, staged_root)
            with preserve_agent_resources(DOCS_ROOT):
                completed = subprocess.run(
                    [
                    sys.executable,
                    "scripts/build_release_docs.py",
                    "--code-root",
                    str(CODE_ROOT),
                    "--site-dir",
                    directory,
                    "--code-revision",
                    subprocess.check_output(["git", "-C", str(CODE_ROOT), "rev-parse", "HEAD"], text=True).strip(),
                    "--docs-revision",
                    docs_revision,
                    "--raw-source-root",
                    str(staged_root),
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
        for tool in ("genomic-element-tools", "exogenous-sequence-tools", "motif-tools"):
            page = GENERATED / f"{tool}.md"
            self.assertTrue(page.is_file(), page)
            text = page.read_text()
            self.assertIn("<!-- Parser inventory:", text)
            inventory = text.split("<!-- Parser inventory: ", 1)[1].split(" -->", 1)[0]
            records = json.loads(inventory)
            self.assertTrue(records)
            parser_tool = {
                "genomic-element-tools": "GenomicElementTools",
                "exogenous-sequence-tools": "ExogenousSequenceTools",
                "motif-tools": "MotifTools",
            }[tool]
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
