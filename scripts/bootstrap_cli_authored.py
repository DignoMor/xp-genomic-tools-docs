"""One-time/bootstrap helper: split legacy CLI landing pages into authored semantics."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from cli_page_registry import ALL_TOOLS, parser_path_to_slug


DOCS_ROOT = Path(__file__).resolve().parents[1]
AUTHORED_ROOT = DOCS_ROOT / "docs/reference/cli/authored"

SECTION_RE = re.compile(r"^### `([^`]+)`\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^## ([^\n]+)\s*$", re.MULTILINE)


def _split_genomic_sections(text: str) -> dict[str, str]:
    matches = list(SECTION_RE.finditer(text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        path = match.group(1)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        sections[path] = body
    return sections


def _landing_intro(text: str) -> str:
    marker = "## Shared contract"
    if marker not in text:
        marker = "## Command paths"
    return text.split(marker, 1)[0].strip()


def _wrap_command_page(tool_name: str, parser_path: str, body: str, release: str) -> str:
    title = f"{tool_name} {parser_path}" if parser_path != "(root)" else tool_name
    lines = [f"# `{title}`", ""]
    if "## Purpose" not in body:
        lines.extend(["## Purpose", "", body.split("\n\n", 1)[0], ""])
        remainder = body.split("\n\n", 1)[1] if "\n\n" in body else ""
        body = remainder
    field_map = {
        "Purpose / Inputs.": "Purpose",
        "Purpose / Inputs": "Purpose",
        "Types / shapes / dtypes.": "Types",
        "Types / shapes / dtypes": "Types",
        "Defaults / constraints.": "Defaults",
        "Defaults / choices / constraints.": "Defaults",
        "Outputs / side effects / failures.": "Outputs",
        "Outputs / ordering / failures.": "Outputs",
        "Outputs / ordering / constraints.": "Outputs",
        "Outputs / constraints.": "Outputs",
        "Constraints / outputs.": "Constraints",
        "Shapes / dtypes / outputs.": "Shapes",
        "Behavior.": "Constraints",
        "Inputs.": "Inputs",
        "Outputs.": "Outputs",
        "Failures.": "Failures",
    }
    paragraphs = [part.strip() for part in re.split(r"\n\n+", body) if part.strip()]
    current_field = "Constraints"
    field_sections: dict[str, list[str]] = {}
    for paragraph in paragraphs:
        matched = False
        for prefix, field in field_map.items():
            if paragraph.startswith(f"**{prefix}**"):
                current_field = field
                content = paragraph.removeprefix(f"**{prefix}**").strip()
                field_sections.setdefault(current_field, []).append(content)
                matched = True
                break
        if not matched:
            field_sections.setdefault(current_field, []).append(paragraph)
    standard_fields = (
        "Purpose",
        "Availability",
        "Inputs",
        "Types",
        "Shapes",
        "Dtypes",
        "Defaults",
        "Choices",
        "Constraints",
        "Outputs",
        "Ordering",
        "Side effects",
        "Failures",
        "Example",
    )
    if "Purpose" not in field_sections and body:
        field_sections["Purpose"] = [body.split("\n\n", 1)[0]]
    for field in standard_fields:
        if field in field_sections:
            lines.extend([f"## {field}", ""])
            lines.append("\n\n".join(field_sections[field]))
            lines.append("")
    if "Example" not in field_sections:
        lines.extend(
            [
                "## Example",
                "",
                f"See the [`{tool_name}` landing page](../index.md) worked examples "
                f"and linked format references for `{parser_path}`.",
                "",
            ]
        )
    if "## Availability" not in "\n".join(lines):
        lines[2:2] = [
            "## Availability",
            "",
            f"Supported in `{tool_name}` for release `{release}`. Invoke through the "
            f"installed `{tool_name}` console script.",
            "",
        ]
    return "\n".join(lines).rstrip() + "\n"


def bootstrap_genomic_element_tools() -> None:
    source = DOCS_ROOT / "docs/reference/cli/genomic-element-tools/index.md"
    text = source.read_text()
    intro = _landing_intro(text)
    sections = _split_genomic_sections(text)
    tool_dir = AUTHORED_ROOT / "genomic-element-tools"
    tool_dir.mkdir(parents=True, exist_ok=True)
    (tool_dir / "_landing.md").write_text(
        intro.replace("0.3.0a3", "0.3.0a4")
        + "\n\n## Availability\n\nSupported in release `0.3.0a4`.\n"
    )
    for parser_path, body in sections.items():
        slug = parser_path_to_slug(parser_path)
        target = tool_dir / f"{slug}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        if parser_path == "mask_op intersect":
            mask_source = DOCS_ROOT / "docs/reference/cli/mask-op-intersect.md"
            authored = mask_source.read_text()
            authored = re.sub(
                r"<!-- Generated by scripts/build_release_docs.py; do not edit directly\. -->\n",
                "",
                authored,
            )
            authored = re.sub(
                r"<!-- Parser inventory: .*? -->\n\n",
                "",
                authored,
                count=1,
            )
            authored = re.sub(
                r"## Syntax\n.*?## Inputs\n",
                "## Inputs\n",
                authored,
                count=1,
                flags=re.DOTALL,
            )
            target.write_text(authored)
            continue
        target.write_text(
            _wrap_command_page("GenomicElementTools", parser_path, body, "0.3.0a4")
        )
    for group in ("export", "import", "mask_op", "get_context_ge"):
        slug = parser_path_to_slug(group)
        target = tool_dir / f"{slug}.md"
        if not target.is_file():
            target.write_text(
                f"# `{group}`\n\n"
                f"## Purpose\n\n"
                f"Group landing for `{group}` nested commands in `GenomicElementTools`.\n\n"
                f"## Availability\n\nSupported in release `0.3.0a4`.\n\n"
                f"## Inputs\n\nSee nested command pages.\n\n"
                f"## Types\n\nSee nested command pages.\n\n"
                f"## Shapes\n\nSee nested command pages.\n\n"
                f"## Dtypes\n\nSee nested command pages.\n\n"
                f"## Defaults\n\nSee nested command pages.\n\n"
                f"## Choices\n\nSee nested command pages.\n\n"
                f"## Constraints\n\nSee nested command pages.\n\n"
                f"## Outputs\n\nSee nested command pages.\n\n"
                f"## Ordering\n\nSee nested command pages.\n\n"
                f"## Side effects\n\nSee nested command pages.\n\n"
                f"## Failures\n\nSee nested command pages.\n\n"
            )


def bootstrap_exogenous_sequence_tools() -> None:
    source = DOCS_ROOT / "docs/reference/cli/exogenous-sequence-tools/index.md"
    text = source.read_text()
    tool_dir = AUTHORED_ROOT / "exogenous-sequence-tools"
    tool_dir.mkdir(parents=True, exist_ok=True)
    intro = text.split("## `assemble`", 1)[0].strip()
    (tool_dir / "_landing.md").write_text(
        intro.replace("0.1.0a2", "0.3.0a4")
    )
    command_blocks = re.split(r"^## `([^`]+)`\s*$", text, flags=re.MULTILINE)[1:]
    for index in range(0, len(command_blocks), 2):
        heading = command_blocks[index].strip()
        body = command_blocks[index + 1].strip()
        if heading == "assemble":
            for subheading in ("add_adapter", "concat", "barcode"):
                match = re.search(
                    rf"^### `assemble {subheading}`\s*$([\s\S]*?)(?=^### `|^## `|\Z)",
                    body,
                    flags=re.MULTILINE,
                )
                if not match:
                    continue
                slug = parser_path_to_slug(f"assemble {subheading}")
                target = tool_dir / f"{slug}.md"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    _wrap_command_page(
                        "ExogenousSequenceTools",
                        f"assemble {subheading}",
                        match.group(1).strip(),
                        "0.3.0a4",
                    )
                )
            (tool_dir / "assemble.md").write_text(
                "# `assemble`\n\n## Purpose\n\nAssemble exogenous sequences.\n\n"
                "## Availability\n\nSupported in release `0.3.0a4`.\n\n"
                "## Inputs\n\nSee nested commands.\n\n## Types\n\nSee nested commands.\n\n"
                "## Shapes\n\nSee nested commands.\n\n## Dtypes\n\nSee nested commands.\n\n"
                "## Defaults\n\nSee nested commands.\n\n## Choices\n\nSee nested commands.\n\n"
                "## Constraints\n\nSee nested commands.\n\n## Outputs\n\nSee nested commands.\n\n"
                "## Ordering\n\nSee nested commands.\n\n## Side effects\n\nSee nested commands.\n\n"
                "## Failures\n\nSee nested commands.\n\n"
            )
            continue
        if heading.startswith("gen_track"):
            match = re.search(
                r"^### `gen_track single_loc`\s*$([\s\S]*?)(?=^## `|\Z)",
                text,
                flags=re.MULTILINE,
            )
            if match:
                (tool_dir / "gen-track/single-loc.md").parent.mkdir(parents=True, exist_ok=True)
                (tool_dir / "gen-track/single-loc.md").write_text(
                    _wrap_command_page(
                        "ExogenousSequenceTools",
                        "gen_track single_loc",
                        match.group(1).strip(),
                        "0.3.0a4",
                    )
                )
            (tool_dir / "gen-track.md").write_text(
                "# `gen_track`\n\n## Purpose\n\nGenerate track annotations from exogenous FASTA.\n\n"
                "## Availability\n\nSupported in release `0.3.0a4`.\n\n"
                "## Inputs\n\nSee nested commands.\n\n## Types\n\nSee nested commands.\n\n"
                "## Shapes\n\nSee nested commands.\n\n## Dtypes\n\nSee nested commands.\n\n"
                "## Defaults\n\nSee nested commands.\n\n## Choices\n\nSee nested commands.\n\n"
                "## Constraints\n\nSee nested commands.\n\n## Outputs\n\nSee nested commands.\n\n"
                "## Ordering\n\nSee nested commands.\n\n## Side effects\n\nSee nested commands.\n\n"
                "## Failures\n\nSee nested commands.\n\n"
            )
            continue
        if heading.startswith("track_dim_reduction"):
            for operation in ("max", "argmax", "min", "argmin"):
                match = re.search(
                    rf"^### `track_dim_reduction {operation}`\s*$([\s\S]*?)(?=^### `|^## `|\Z)",
                    text,
                    flags=re.MULTILINE,
                )
                if not match:
                    continue
                slug = parser_path_to_slug(f"track_dim_reduction {operation}")
                (tool_dir / f"{slug}.md").parent.mkdir(parents=True, exist_ok=True)
                (tool_dir / f"{slug}.md").write_text(
                    _wrap_command_page(
                        "ExogenousSequenceTools",
                        f"track_dim_reduction {operation}",
                        match.group(1).strip(),
                        "0.3.0a4",
                    )
                )
            (tool_dir / "track-dim-reduction.md").write_text(
                "# `track_dim_reduction`\n\n## Purpose\n\nReduce track annotations along sequence positions.\n\n"
                "## Availability\n\nSupported in release `0.3.0a4`.\n\n"
                "## Inputs\n\nSee nested commands.\n\n## Types\n\nSee nested commands.\n\n"
                "## Shapes\n\nSee nested commands.\n\n## Dtypes\n\nSee nested commands.\n\n"
                "## Defaults\n\nSee nested commands.\n\n## Choices\n\nSee nested commands.\n\n"
                "## Constraints\n\nSee nested commands.\n\n## Outputs\n\nSee nested commands.\n\n"
                "## Ordering\n\nSee nested commands.\n\n## Side effects\n\nSee nested commands.\n\n"
                "## Failures\n\nSee nested commands.\n\n"
            )
            continue
        slug = parser_path_to_slug(heading)
        target = tool_dir / f"{slug}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            _wrap_command_page("ExogenousSequenceTools", heading, body, "0.3.0a4")
        )


def bootstrap_motif_tools() -> None:
    source = DOCS_ROOT / "docs/reference/cli/motif-tools/index.md"
    text = source.read_text()
    tool_dir = AUTHORED_ROOT / "motif-tools"
    tool_dir.mkdir(parents=True, exist_ok=True)
    intro = text.split("## `anti_motif`", 1)[0].strip()
    (tool_dir / "_landing.md").write_text(
        intro.replace("0.2.0a2", "0.3.0a4")
    )
    for command in ("anti_motif", "pwm_seq", "random_seq", "barcodes"):
        match = re.search(
            rf"^## `{command}`\s*$([\s\S]*?)(?=^## `|\Z)",
            text,
            flags=re.MULTILINE,
        )
        if not match:
            continue
        body = match.group(1).strip()
        page = _wrap_command_page("MotifTools", command, body, "0.3.0a4")
        (tool_dir / f"{command.replace('_', '-')}.md").write_text(page)


def main() -> None:
    bootstrap_genomic_element_tools()
    bootstrap_exogenous_sequence_tools()
    bootstrap_motif_tools()
    print(f"Authored semantics written under {AUTHORED_ROOT}")


if __name__ == "__main__":
    main()
