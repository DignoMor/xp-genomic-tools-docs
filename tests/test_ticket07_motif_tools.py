"""Built-artifact acceptance for MotifTools CLI and MotifGeneration docs."""

from __future__ import annotations

import html
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "docs/reference/cli/motif-tools"
OVERVIEW = ROOT / "docs/cli/MotifTools.md"
LANDING = ROOT / "docs/reference/cli/authored/motif-tools/_landing.md"
PRIMARY_MOTIFTOOLS = Path(
    "/local/storage/xp76/projects/xp-genomic-tools/code/.venv/bin/MotifTools"
)


def _review_code_root() -> Path:
    env = os.environ.get("XP_GENOMIC_TOOLS_CODE_ROOT")
    if env:
        return Path(env)
    for candidate in (ROOT.parent / "code-review", ROOT.parent / "code"):
        if (candidate / "src" / "MotifTools").is_dir():
            return candidate
    raise FileNotFoundError("MotifTools source root for documentation CLI checks")


def _run_documented_motiftools(*args: str) -> subprocess.CompletedProcess[str]:
    code_root = _review_code_root()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(code_root / "src")
    for executable in (
        PRIMARY_MOTIFTOOLS,
        ROOT.parent / "code" / ".venv/bin/MotifTools",
        code_root / ".venv/bin/MotifTools",
    ):
        if executable.is_file():
            command = [str(executable), *args]
            break
    else:
        raise FileNotFoundError("MotifTools executable for documentation CLI checks")
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def _documented_meme(page: str, motif_name: str) -> str:
    marker = f"MOTIF {motif_name}\n"
    for body in re.findall(r"cat > \S+ <<'EOF'\n(.*?)(?:\n)EOF", page, re.S):
        if marker in body:
            return body if body.endswith("\n") else f"{body}\n"
    raise AssertionError(f"documented MEME for {motif_name} not found")


def _documented_fasta(page: str, motif_name: str) -> str:
    match = re.search(
        rf"(>dinucleotide_transversion_{re.escape(motif_name)}\n[ACGT]+\n)",
        page,
    )
    if match is None:
        raise AssertionError(f"documented FASTA for {motif_name} not found")
    return match.group(1)


def _documented_warning(page: str, motif_name: str) -> str:
    match = re.search(
        rf"(Warning: motif {re.escape(motif_name)} scores [^\n]+)\n",
        page,
    )
    if match is None:
        return ""
    return f"{match.group(1)}\n"


class Ticket07MotifToolsReferenceTest(unittest.TestCase):
    def test_inventory_covers_every_command_path(self) -> None:
        inventory = json.loads((REFERENCE / "inventory.json").read_text())
        expected = {
            "anti_motif",
            "random_seq",
            "pwm_seq",
            "barcodes",
            "dinucleotide_transversion",
        }
        self.assertEqual(set(inventory["commands"]), expected)
        self.assertNotIn("parser_reference", inventory)

    def test_semantic_reference_documents_anti_motif_provenance(self) -> None:
        text = (REFERENCE / "anti-motif.md").read_text()
        for phrase in (
            "anti_motif",
            "provenance",
            "nsites",
            "E-value",
            "never mutated",
            "normalize(PWM * nsites + 1)",
        ):
            self.assertIn(phrase, text)

    def test_semantic_reference_documents_dinucleotide_warning_and_composition(self) -> None:
        text = (REFERENCE / "dinucleotide-transversion.md").read_text()
        for phrase in (
            "warn_score_cutoff",
            "stderr",
            "heuristic",
            "p-value",
            "nsites",
            "knockout",
            "original PWM orientation",
            "ExogenousSequenceTools mutagenesis",
            "reverse-complement",
        ):
            self.assertIn(phrase, text)

    def test_overview_documents_dinucleotide_stderr_exception(self) -> None:
        overview = OVERVIEW.read_text()
        landing = LANDING.read_text()
        assembled = (REFERENCE / "index.md").read_text()
        self.assertNotRegex(overview, r"Successful path commands are silent\.")
        self.assertNotIn(
            "Successful path commands produce no stdout or stderr.",
            landing,
        )
        self.assertNotIn(
            "Successful path commands produce no stdout or stderr.",
            assembled,
        )
        for text in (overview, landing, assembled):
            self.assertIn("dinucleotide_transversion", text)
            self.assertIn("stderr", text)
            self.assertIn("warn_score_cutoff", text)
            self.assertIn("heuristic", text)
            self.assertIn("p-value", text)
            self.assertIn("knockout", text)
            self.assertIn("mutagenesis", text)
            self.assertRegex(text, r"minus[- ]strand")

    def test_documented_dinucleotide_examples_match_generated_cli_bytes(self) -> None:
        page = (REFERENCE / "dinucleotide-transversion.md").read_text()
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            for motif_name in ("EVEN2", "TIED"):
                meme = work / f"{motif_name}.meme"
                meme.write_text(_documented_meme(page, motif_name), encoding="utf-8")
                out = work / f"{motif_name}.fasta"
                completed = _run_documented_motiftools(
                    "dinucleotide_transversion",
                    "--motif_file",
                    str(meme),
                    "--motif_name",
                    motif_name,
                    "--output",
                    str(out),
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(completed.stdout, "")
                self.assertEqual(
                    completed.stderr,
                    _documented_warning(page, motif_name),
                )
                self.assertEqual(
                    out.read_text(encoding="utf-8"),
                    _documented_fasta(page, motif_name),
                )
            meme = work / "FWD0.meme"
            meme.write_text(_documented_meme(page, "FWD0"), encoding="utf-8")
            completed = _run_documented_motiftools(
                "dinucleotide_transversion",
                "--motif_file",
                str(meme),
                "--motif_name",
                "FWD0",
                "--output",
                "-",
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(completed.stdout, _documented_fasta(page, "FWD0"))
            self.assertEqual(completed.stderr, _documented_warning(page, "FWD0"))
            self.assertTrue(completed.stderr.startswith("Warning: motif FWD0 "))

    def test_built_artifact_has_complete_cli_and_api_pages(self) -> None:
        inventory = json.loads((ROOT / "tests/ticket07_motif_tools_reference_inventory.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    str(ROOT / ".venv/bin/mkdocs"),
                    "build",
                    "--strict",
                    "--clean",
                    "--site-dir",
                    directory,
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            site = Path(directory)
            required = inventory["required_fields"]
            cli_html = html.unescape((site / "reference/cli/motif-tools/index.html").read_text())
            anti_html = html.unescape((site / "reference/cli/motif-tools/anti-motif/index.html").read_text())
            for field in required:
                self.assertIn(field, cli_html)
                self.assertIn(field, anti_html)
            for symbol in inventory["entries"][0]["symbols"]:
                self.assertIn(symbol, cli_html)
            for phrase in ("provenance", "nsites", "E-value", "never mutated"):
                self.assertIn(phrase, anti_html)
            api_page = site / "reference/python/motifs/motif-generation/index.html"
            self.assertTrue(api_page.is_file(), api_page)
            api_html = html.unescape(api_page.read_text())
            api_fields = (
                "Status", "Purpose", "Canonical import", "Signature", "Example",
            )
            for field in api_fields:
                self.assertIn(field, api_html)
            for symbol in inventory["entries"][-1]["symbols"]:
                self.assertIn(symbol, api_html)
            generated = site / "reference/cli/generated/motif-tools/index.html"
            self.assertTrue(generated.is_file(), generated)
            redirect_content = generated.read_text()
            self.assertRegex(
                redirect_content,
                r"(window\.location\.replace|http-equiv=.refresh|location\.href)",
                msg="generated MotifTools URL must redirect to the canonical landing",
            )
            self.assertIn("motif-tools", redirect_content)


if __name__ == "__main__":
    unittest.main()
