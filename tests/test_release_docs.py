from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from release_test_helpers import preserve_agent_resources, stage_docs_revision


DOCS_ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = DOCS_ROOT.parent / "code"


class ReleaseDocumentationAcceptanceTest(unittest.TestCase):
    def _run_release_build(self, directory: str) -> subprocess.CompletedProcess[str]:
        staged_root = Path(directory) / "staged-docs"
        staged_root.mkdir()
        docs_revision = stage_docs_revision(DOCS_ROOT, staged_root)
        with preserve_agent_resources(DOCS_ROOT):
            return subprocess.run(
                [
                    sys.executable,
                    "scripts/build_release_docs.py",
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

    def test_representative_reference_builds_as_a_release_artifact(self) -> None:
        """SPEC001: the release command proves the representative built-site seam."""
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)

        self.assertEqual(
            completed.returncode,
            0,
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )

    def test_release_rejects_method_in_element_collections_library_section(
        self,
    ) -> None:
        """SPEC001: Element collections is class-only in the Library article."""
        library_path = DOCS_ROOT / "docs/library.md"
        original = library_path.read_text()
        collection_only = (
            "- [GeneralElements, GenomicElements, and ExogeneousSequences]"
            "(reference/python/elements/index.md)\n"
        )
        with_method = (
            "- [GeneralElements, GenomicElements, and ExogeneousSequences]"
            "(reference/python/elements/index.md)\n"
            "    - [`GeneralElements.load_mask_from_arr`]"
            "(reference/python/general-elements/load-mask-from-arr.md)\n"
        )
        self.assertIn(collection_only, original)

        try:
            library_path.write_text(original.replace(collection_only, with_method))
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            library_path.write_text(original)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("Element collections Library section", completed.stderr)

    def test_release_rejects_unmarked_method_navigation_label(self) -> None:
        """SPEC001: method pages are labeled as methods in Python navigation."""
        config_path = DOCS_ROOT / "mkdocs.yml"
        original_config = config_path.read_text()
        method_label = (
            "              - GeneralElements.load_mask_from_arr(): "
            "reference/python/general-elements/load-mask-from-arr.md\n"
        )
        unmarked_label = (
            "              - GeneralElements.load_mask_from_arr: "
            "reference/python/general-elements/load-mask-from-arr.md\n"
        )
        self.assertIn(method_label, original_config)

        try:
            config_path.write_text(
                original_config.replace(method_label, unmarked_label)
            )
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            config_path.write_text(original_config)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("presented as a method", completed.stderr)

    def test_release_rejects_method_inside_element_collections_nav_group(self) -> None:
        """SPEC001: Element collections is class-only in Python navigation."""
        config_path = DOCS_ROOT / "mkdocs.yml"
        original_config = config_path.read_text()
        correct_navigation = """          - Element collections:
              - Overview: reference/python/elements/index.md
              - GenomicElements: reference/python/elements/genomic-elements.md
          - Operations:
              - GeneralElements.load_mask_from_arr(): reference/python/general-elements/load-mask-from-arr.md
          - MemeMotif: reference/python/motifs/meme-motif.md
"""
        wrong_navigation = """          - Element collections:
              - Overview: reference/python/elements/index.md
              - GenomicElements: reference/python/elements/genomic-elements.md
              - GeneralElements.load_mask_from_arr(): reference/python/general-elements/load-mask-from-arr.md
          - MemeMotif: reference/python/motifs/meme-motif.md
"""
        self.assertIn(correct_navigation, original_config)

        try:
            config_path.write_text(original_config.replace(correct_navigation, wrong_navigation))
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            config_path.write_text(original_config)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("class-only Element collections navigation group", completed.stderr)

    def test_release_rejects_method_as_peer_of_reference_areas(self) -> None:
        """SPEC001: operation pages are not peers of classes or reference areas."""
        config_path = DOCS_ROOT / "mkdocs.yml"
        original_config = config_path.read_text()
        grouped = """          - Operations:
              - GeneralElements.load_mask_from_arr(): reference/python/general-elements/load-mask-from-arr.md
"""
        peer = """          - GeneralElements.load_mask_from_arr(): reference/python/general-elements/load-mask-from-arr.md
"""
        self.assertIn(grouped, original_config)

        try:
            config_path.write_text(original_config.replace(grouped, peer))
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            config_path.write_text(original_config)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("explicit Operations grouping", completed.stderr)


if __name__ == "__main__":
    unittest.main()
