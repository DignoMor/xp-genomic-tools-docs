"""Built-site acceptance for HTML agent-reference peer of llms.txt (docs#6)."""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from release_test_helpers import preserve_agent_resources, restore_golden_docs, stage_docs_revision


DOCS_ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = DOCS_ROOT.parent / "code"
BUILD_SCRIPT = DOCS_ROOT / "scripts/build_release_docs.py"
PAGES_BASE = "https://dignomor.github.io/xp-genomic-tools-docs/"
INDEX_SOURCE = DOCS_ROOT / "docs/index.md"


def _destination_labels(compact: str) -> list[str]:
    labels: list[str] = []
    for line in compact.splitlines():
        match = re.match(r"^- ([^:]+): https://", line)
        if match is None:
            continue
        label = match.group(1)
        if label == "HTML agent reference":
            continue
        labels.append(label)
    return labels


def _html_destination_labels(article: str) -> list[str]:
    labels: list[str] = []
    peer_labels = {"Compact plaintext index", "Exhaustive plaintext reference"}
    for match in re.finditer(r"<li>(.*?)</li>", article, flags=re.DOTALL):
        item = re.sub(r"<[^>]+>", " ", match.group(1))
        item = " ".join(item.split())
        if ":" not in item:
            continue
        label = item.split(":", 1)[0].strip()
        if label in peer_labels:
            continue
        labels.append(label)
    return labels


class Issue06AgentReferenceTest(unittest.TestCase):
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

    def test_release_build_publishes_html_agent_reference_peer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            completed = self._run_release_build(directory)
            self.assertEqual(
                completed.returncode,
                0,
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            site = Path(directory)
            agent_page = site / "agent-reference" / "index.html"
            self.assertTrue(agent_page.is_file(), agent_page)
            rendered = html.unescape(agent_page.read_text())
            self.assertIn("Agent reference", rendered)
            self.assertRegex(rendered, r"<h1[^>]*>\s*Agent reference\b")
            self.assertIn("Agent reference", rendered.split("<title>", 1)[1].split("</title>", 1)[0])

            compact = (site / "llms.txt").read_text()
            article = rendered.split("<article", 1)[1].split("</article>", 1)[0]
            code_match = re.search(r"Code revision:\s*`([0-9a-f]{40})`", compact)
            self.assertIsNotNone(code_match)
            code_revision = code_match.group(1)
            self.assertIn(code_revision, article)
            release_match = re.search(
                r"xp-genomic-tools public reference \(([^)]+)\)", compact
            )
            self.assertIsNotNone(release_match)
            self.assertIn(release_match.group(1), article)

            compact_labels = _destination_labels(compact)
            html_labels = _html_destination_labels(article)
            self.assertEqual(compact_labels, html_labels)
            self.assertIn("Exhaustive plain-text reference", compact_labels)
            self.assertIn("FAQ", compact_labels)

            self.assertIn(f"{PAGES_BASE}agent-reference/", compact)
            self.assertIn(f"{PAGES_BASE}llms.txt", article)
            self.assertIn(f"{PAGES_BASE}llms-full.txt", article)

            homepage = html.unescape((site / "index.html").read_text())
            self.assertIn("agent-reference", homepage)

            sitemap = (site / "sitemap.xml").read_text()
            self.assertIn(f"{PAGES_BASE}agent-reference/", sitemap)

    def test_source_overview_links_agent_reference(self) -> None:
        self.assertIn("agent-reference", INDEX_SOURCE.read_text())

    def test_release_rejects_missing_homepage_agent_reference_link(self) -> None:
        original = INDEX_SOURCE.read_text()
        line = (
            "5. Agents: start from the [Agent reference](agent-reference.md) "
            "HTML index or the compact [`llms.txt`](llms.txt) peer\n"
        )
        self.assertIn(line, original)
        try:
            INDEX_SOURCE.write_text(original.replace(line, ""))
            with tempfile.TemporaryDirectory() as directory:
                completed = self._run_release_build(directory)
        finally:
            INDEX_SOURCE.write_text(original)
            restore_golden_docs(DOCS_ROOT)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("agent-reference", completed.stderr)


if __name__ == "__main__":
    unittest.main()
