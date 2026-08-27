"""Failing-closed documentation acceptance for the exogenous identifier cutover."""

from __future__ import annotations

import re
import subprocess
import tempfile
import unittest
from pathlib import Path

DOCS_ROOT = Path(__file__).resolve().parents[1]
MKDOCS_CONFIG = DOCS_ROOT / "mkdocs.yml"
SPELLING_RE = re.compile(r"exogeneous", re.IGNORECASE)

# Canonical renamed paths that must exist in the built site.
NEW_SITE_PATHS = (
    "reference/cli/exogenous-sequence-tools",
    "reference/python/elements/exogenous-sequences",
    "reference/cli/genomic-element-tools/export/exogenous-sequences",
    "reference/formats/cli/exogenous-sequence-tools/exogenous-fasta",
    "cli/ExogenousSequenceTools",
)

# Representative old public paths that must not exist in the built site (404/absence).
OLD_SITE_PATHS = (
    "reference/cli/exogeneous-sequence-tools",
    "reference/python/elements/exogeneous-sequences",
    "reference/cli/genomic-element-tools/export/exogeneous-sequences",
    "reference/formats/cli/exogeneous-sequence-tools/exogenous-fasta",
    "reference/formats/cli/exogeneous-sequence-tools",
    "cli/ExogeneousSequenceTools",
    "reference/cli/generated/exogeneous-sequence-tools",
)

# Old redirect source keys that must not appear in mkdocs redirect_maps.
OLD_REDIRECT_SOURCE_KEYS = (
    "reference/cli/generated/exogeneous-sequence-tools.md",
    "cli/ExogeneousSequenceTools.md",
)


class ExogenousIdentifierDocumentationCutoverTest(unittest.TestCase):
    def _build_site(self, site_dir: str) -> subprocess.CompletedProcess[str]:
        mkdocs = DOCS_ROOT / ".venv" / "bin" / "mkdocs"
        return subprocess.run(
            [
                str(mkdocs),
                "build",
                "--strict",
                "--clean",
                "--site-dir",
                site_dir,
            ],
            cwd=DOCS_ROOT,
            capture_output=True,
            text=True,
        )

    def test_canonical_renamed_paths_exist_in_built_site(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            completed = self._build_site(directory)
            self.assertEqual(
                completed.returncode,
                0,
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            site = Path(directory)
            for rel_path in NEW_SITE_PATHS:
                candidates = (
                    site / f"{rel_path}/index.html",
                    site / f"{rel_path}.html",
                )
                self.assertTrue(
                    any(candidate.is_file() for candidate in candidates),
                    f"canonical path missing from built site: {rel_path}",
                )

    def test_old_misspelled_paths_absent_from_built_site(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            completed = self._build_site(directory)
            self.assertEqual(
                completed.returncode,
                0,
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            site = Path(directory)
            for rel_path in OLD_SITE_PATHS:
                candidates = (
                    site / f"{rel_path}/index.html",
                    site / f"{rel_path}.html",
                    site / f"{rel_path}/index.md",
                    site / f"{rel_path}.md",
                )
                for candidate in candidates:
                    self.assertFalse(
                        candidate.exists(),
                        f"old misspelled path must be absent, found {candidate}",
                    )

    def test_built_site_has_no_misspelled_path_segments(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            completed = self._build_site(directory)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            site = Path(directory)
            for path in site.rglob("*"):
                if not path.is_file():
                    continue
                rel = path.relative_to(site).as_posix()
                self.assertNotRegex(
                    rel,
                    SPELLING_RE,
                    f"built artifact path contains forbidden spelling: {rel}",
                )

    def test_redirect_maps_have_no_misspelled_source_keys(self) -> None:
        config = MKDOCS_CONFIG.read_text()
        in_redirect_maps = False
        for line in config.splitlines():
            stripped = line.strip()
            if stripped == "redirect_maps:":
                in_redirect_maps = True
                continue
            if in_redirect_maps:
                if stripped and not stripped.startswith("#") and not line.startswith(" "):
                    break
                if ":" not in stripped or stripped.startswith("#"):
                    continue
                source_key = stripped.split(":", 1)[0].strip()
                self.assertNotRegex(
                    source_key,
                    SPELLING_RE,
                    f"redirect source key must not use old spelling: {source_key}",
                )

    def test_enumerated_old_redirect_sources_are_not_configured(self) -> None:
        config = MKDOCS_CONFIG.read_text()
        for source_key in OLD_REDIRECT_SOURCE_KEYS:
            self.assertNotIn(
                source_key,
                config,
                f"old redirect source must not be configured: {source_key}",
            )


if __name__ == "__main__":
    unittest.main()
