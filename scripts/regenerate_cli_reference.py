"""Bootstrap authored semantics (if needed) and assemble CLI reference pages."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

SCRIPTS_ROOT = Path(__file__).resolve().parent
DOCS_ROOT = SCRIPTS_ROOT.parent
sys.path.insert(0, str(SCRIPTS_ROOT))

from assemble_cli_pages import assemble_all_tools, validate_authored_coverage, write_pages  # noqa: E402
from bootstrap_cli_authored import main as bootstrap_authored  # noqa: E402
from cli_page_registry import ALL_TOOLS  # noqa: E402


def _code_root(override: Path | None) -> Path:
    if override is not None:
        return override
    env_root = os.environ.get("XP_GENOMIC_TOOLS_CODE_ROOT")
    if env_root:
        return Path(env_root)
    return DOCS_ROOT.parent / "code"


def _venv_python(code_root: Path) -> Path:
    local = code_root / ".venv/bin/python"
    if local.is_file():
        return local
    return Path(sys.executable)


def _parser_records(code_root: Path) -> dict[str, list[dict]]:
    records: dict[str, list[dict]] = {}
    python = str(_venv_python(code_root))
    for tool in ALL_TOOLS:
        records[tool.console_name] = json.loads(
            subprocess.check_output(
                [
                    python,
                    str(SCRIPTS_ROOT / "extract_cli_reference.py"),
                    "--code-root",
                    str(code_root),
                    "--tool",
                    tool.console_name,
                ],
                text=True,
            )
        )
    return records


LEGACY_SOURCE_COMMIT = "5d90c9c"
LEGACY_INDEX_PATHS = (
    "docs/reference/cli/genomic-element-tools/index.md",
    "docs/reference/cli/exogenous-sequence-tools/index.md",
    "docs/reference/cli/motif-tools/index.md",
)


def _restore_legacy_bootstrap_sources() -> None:
    for relative in LEGACY_INDEX_PATHS:
        target = DOCS_ROOT / relative
        completed = subprocess.run(
            ["git", "-C", str(DOCS_ROOT), "show", f"{LEGACY_SOURCE_COMMIT}:{relative}"],
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(completed.stdout)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--code-root",
        type=Path,
        default=None,
        help="Code checkout used to extract parser inventory.",
    )
    args = parser.parse_args(argv)
    code_root = _code_root(args.code_root)
    try:
        validate_authored_coverage()
    except RuntimeError:
        _restore_legacy_bootstrap_sources()
        bootstrap_authored()
        validate_authored_coverage()
    write_pages(assemble_all_tools(_parser_records(code_root), version("RGTools")))
    legacy_mask = DOCS_ROOT / "docs/reference/cli/mask-op-intersect.md"
    if legacy_mask.is_file():
        legacy_mask.unlink()


if __name__ == "__main__":
    main()
