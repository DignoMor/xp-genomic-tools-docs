"""Ticket 01: prove the reference pipeline end to end."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import tempfile
import unittest
from importlib.metadata import version
from pathlib import Path

from release_test_helpers import preserve_agent_resources, stage_docs_revision


DOCS_ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = DOCS_ROOT.parent / "code"
INVENTORY = DOCS_ROOT / "docs/reference/python/inventory.json"
GENOMIC_ELEMENTS_PAGE = DOCS_ROOT / "docs/reference/python/elements/genomic-elements.md"
AUTHORED_MASK_INTERSECT = (
    DOCS_ROOT / "docs/reference/cli/authored/genomic-element-tools/mask-op/intersect.md"
)
MKDOCS_CONFIG = DOCS_ROOT / "mkdocs.yml"
BUILD_SCRIPT = DOCS_ROOT / "scripts/build_release_docs.py"
TARGET_RELEASE = "0.3.0a4"

API_SEMANTIC_FIELDS = (
    "Status",
    "Purpose",
    "Canonical import",
    "Signature",
    "Parameters",
    "Return or yield behavior",
    "Raised exceptions",
    "Constraints",
    "Ordering",
    "Side effects",
    "Lifecycle behavior",
    "Supported protocols and inheritance",
    "Example",
    "Related formats or commands",
)

CURATED_GENOMIC_ELEMENTS_MEMBERS = (
    "__init__",
    "fasta_path",
    "region_file_type",
    "region_file_path",
    "get_num_regions",
    "get_region_file_suffix2class_dict",
    "BedTable6Gene",
    "BedTable3Gene",
    "BedTableNarrowPeak",
    "BedTableBedGraph",
    "BedTableTREBed",
    "merge_genomic_elements",
    "export_exogeneous_sequences",
    "get_all_region_seqs",
    "get_region_bed_table",
    "apply_logical_filter",
)

EXCLUDED_INTERNAL_MARKERS = (
    "set_parser_genome",
    "set_parser_genomic_element_region",
)

REDIRECT_SOURCE = "reference/cli/generated/genomic-element-tools"
REDIRECT_TARGET = "reference/cli/genomic-element-tools/"
MASK_REDIRECT_SOURCE = "reference/cli/mask-op-intersect"
MASK_CANONICAL = "reference/cli/genomic-element-tools/mask-op/intersect"
MASK_REDIRECT_SOURCE = "reference/cli/mask-op-intersect"
MASK_CANONICAL = "reference/cli/genomic-element-tools/mask-op/intersect"


class Ticket01ReferencePipelineTest(unittest.TestCase):
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

    def test_canonical_release_version_is_0_3_0a4(self) -> None:
        self.assertEqual(version("RGTools"), TARGET_RELEASE)
        build_source = BUILD_SCRIPT.read_text()
        self.assertNotIn('RELEASE = "0.3.0a3"', build_source)
        self.assertIn("importlib.metadata", build_source)

    def test_genomic_elements_page_exists_with_curated_members(self) -> None:
        inventory = json.loads(INVENTORY.read_text())
        genomic_members = [
            symbol
            for symbol in next(
                page["symbols"]
                for page in inventory["pages"]
                if page["path"] == "reference/python/elements/genomic-elements"
            )
            if symbol != "GenomicElements"
        ]
        self.assertEqual(set(genomic_members), set(CURATED_GENOMIC_ELEMENTS_MEMBERS))
        self.assertTrue(GENOMIC_ELEMENTS_PAGE.is_file())

        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)

            page = Path(directory) / "reference/python/elements/genomic-elements/index.html"
            self.assertTrue(page.is_file(), page)
            rendered = html.unescape(page.read_text())
            self.assertIn("GenomicElements", rendered)
            self.assertIn("region_file_path", rendered)
            self.assertIn("region_file_type", rendered)
            self.assertIn("fasta_path", rendered)
            for member in CURATED_GENOMIC_ELEMENTS_MEMBERS:
                self.assertIn(member, rendered, f"missing curated member {member}")
            for marker in EXCLUDED_INTERNAL_MARKERS:
                self.assertNotIn(marker, rendered, f"internal marker leaked: {marker}")

    def test_genomic_elements_page_has_required_semantic_sections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            rendered = html.unescape(
                (
                    Path(directory)
                    / "reference/python/elements/genomic-elements/index.html"
                ).read_text()
            )
            rendered_text = re.sub(r"<[^>]+>", " ", rendered)
            rendered_text = re.sub(r"\s+", " ", rendered_text)
            for field in API_SEMANTIC_FIELDS:
                self.assertIn(field, rendered, f"missing semantic section {field}")
            self.assertIn("from RGTools import GenomicElements", rendered_text)

    def test_mask_op_intersect_has_example_section(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            rendered = html.unescape(
                (
                    Path(directory)
                    / "reference/cli/mask-op-intersect/index.html"
                ).read_text()
            )
            self.assertIn("Example", rendered)
            self.assertIn("mask_op intersect", rendered)

    def test_superseded_cli_url_redirects_to_canonical_landing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            redirect_page = (
                Path(directory) / REDIRECT_SOURCE / "index.html"
            )
            self.assertTrue(redirect_page.is_file(), redirect_page)
            content = redirect_page.read_text()
            self.assertRegex(
                content,
                r"(window\.location\.replace|http-equiv=.refresh|location\.href)",
                msg="redirect page lacks redirect mechanism",
            )
            self.assertIn(REDIRECT_TARGET.rstrip("/").split("/")[-1], content)

    def test_release_rejects_missing_genomic_elements_page(self) -> None:
        original = GENOMIC_ELEMENTS_PAGE.read_text()
        try:
            GENOMIC_ELEMENTS_PAGE.write_text("# placeholder\n")
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            GENOMIC_ELEMENTS_PAGE.write_text(original)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("GenomicElements", completed.stderr)

    def test_release_rejects_missing_mask_example_section(self) -> None:
        original = AUTHORED_MASK_INTERSECT.read_text()
        if "## Example\n" not in original:
            original = original.replace("## Examples removed\n", "## Example\n", 1)
        patched = original.replace("## Example\n", "## Examples removed\n", 1)
        self.assertNotEqual(original, patched)
        try:
            AUTHORED_MASK_INTERSECT.write_text(patched)
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            AUTHORED_MASK_INTERSECT.write_text(original)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("Example", completed.stderr)

    def test_release_rejects_missing_redirect_mapping(self) -> None:
        original = MKDOCS_CONFIG.read_text()
        redirect_lines = (
            f"        {REDIRECT_SOURCE}.md: {REDIRECT_TARGET}index.md\n",
            "        reference/cli/mask-op-intersect.md: "
            "reference/cli/genomic-element-tools/mask-op/intersect.md\n",
        )
        for redirect_line in redirect_lines:
            self.assertIn(redirect_line, original)
        try:
            patched = original
            for redirect_line in redirect_lines:
                patched = patched.replace(redirect_line, "")
            MKDOCS_CONFIG.write_text(patched)
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            MKDOCS_CONFIG.write_text(original)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("redirect", completed.stderr.lower())

    def test_release_rejects_missing_genomic_elements_semantic_section(self) -> None:
        original = GENOMIC_ELEMENTS_PAGE.read_text()
        patched = original.replace("## Example\n", "## Example removed\n", 1)
        self.assertNotEqual(original, patched)
        try:
            GENOMIC_ELEMENTS_PAGE.write_text(patched)
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            GENOMIC_ELEMENTS_PAGE.write_text(original)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("Example", completed.stderr)


if __name__ == "__main__":
    unittest.main()
