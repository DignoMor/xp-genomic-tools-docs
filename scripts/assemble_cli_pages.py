"""Assemble CLI reference pages from authored semantics and parser fragments."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from cli_page_registry import (
    ALL_TOOLS,
    REFERENCE_FIELDS,
    ToolRegistry,
    parser_path_to_slug,
    validate_registry_against_records,
)


DOCS_ROOT = Path(__file__).resolve().parents[1]
FRAGMENT_ROOT = DOCS_ROOT / "docs/reference/cli/fragments"


def _render_options_table(arguments: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for argument in arguments:
        if argument["dest"] == "help":
            continue
        choices = ", ".join(f"`{choice}`" for choice in argument["choices"])
        rows.append(
            "| {flags} | {required} | {value_type} | {choices} | {default} | "
            "{repeatable} | {help_text} |".format(
                flags=f"`{argument['flags']}`",
                required="yes" if argument["required"] else "no",
                value_type=f"`{argument['type']}`",
                choices=choices or "inapplicable",
                default=f"`{argument['default']}`",
                repeatable="yes" if argument["repeatable"] else "no",
                help_text=argument["help"],
            )
        )
    header = (
        "| Flags | Required | Type | Choices | Default | Repeatable | Parser help |\n"
        "| --- | --- | --- | --- | --- | --- | --- |"
    )
    return header + ("\n" + "\n".join(rows) if rows else "")


def render_syntax_fragment(tool: ToolRegistry, record: dict[str, Any]) -> str:
    parser_path = record["path"]
    title = (
        f"`{tool.console_name}`"
        if parser_path == "(root)"
        else f"`{tool.console_name} {parser_path}`"
    )
    return (
        f"## Syntax\n\nParser-derived invocation for {title}:\n\n"
        f"```text\n{record['usage']}\n```\n\n"
        f"### Options\n\n{_render_options_table(record['arguments'])}\n"
    )


def _required_field_note(record: dict[str, Any]) -> str:
    notes: list[str] = []
    for argument in record["arguments"]:
        if argument["dest"] == "help":
            continue
        if argument["required"] and argument["default"] not in ("inapplicable", "none"):
            notes.append(
                f"Although argparse exposes `{argument['default']}` as the "
                f"`{argument['flags']}` default, the flag is required, so omission "
                "is an argparse error rather than use of that default."
            )
    return "\n\n".join(notes)


def _load_authored(tool: ToolRegistry, parser_path: str) -> str:
    authored_path = DOCS_ROOT / tool.authored_path(parser_path)
    if not authored_path.is_file():
        raise RuntimeError(f"Missing authored semantics: {authored_path}")
    text = authored_path.read_text().strip()
    if not text.startswith("#"):
        raise ValueError(f"{authored_path} must start with a heading")
    return text + "\n"


def _rel_link(tool: ToolRegistry, page_slug: str, target: str) -> str:
    source_dir = Path("reference/cli") / tool.slug / Path(page_slug).parent
    return os.path.relpath(target, source_dir).replace(os.sep, "/")


def _repair_links(body: str, tool: ToolRegistry, page_slug: str) -> str:
    source_dir = Path("reference/cli") / tool.slug / Path(page_slug).parent

    def rel(target: str) -> str:
        return os.path.relpath(target, source_dir).replace(os.sep, "/")

    def fix_href(match: re.Match[str]) -> str:
        href = match.group(1)
        if href.startswith("#"):
            anchor_map = {
                "#select_tss_relative_track": rel(
                    f"reference/cli/{tool.slug}/select-tss-relative-track.md"
                ),
                "#mask_op-intersect": rel(
                    f"reference/cli/{tool.slug}/mask-op/intersect.md"
                ),
                "#export-maskedge": rel(
                    f"reference/cli/{tool.slug}/export/masked-ge.md"
                ),
                "#export MaskedGE": rel(
                    f"reference/cli/{tool.slug}/export/masked-ge.md"
                ),
            }
            return f"]({anchor_map.get(href, href)})"
        normalized = href
        while normalized.startswith("../"):
            normalized = normalized[3:]
        if normalized.startswith("guides/"):
            return f"]({rel(normalized)})"
        if normalized.startswith("formats/"):
            return f"]({rel('reference/' + normalized)})"
        if normalized.endswith("index.md") and "cli/" in normalized:
            return f"]({rel(f'reference/cli/{tool.slug}/index.md')})"
        if href == "../../cli/mask-op-intersect.md":
            return f"]({rel(f'reference/cli/{tool.slug}/mask-op/intersect.md')})"
        if href in ("../index.md", "index.md"):
            return f"]({rel(f'reference/cli/{tool.slug}/index.md')})"
        return match.group(0)

    return re.sub(r"\]\(([^)]+)\)", fix_href, body)


def _ensure_required_sections(body: str, tool_name: str, parser_path: str) -> str:
    for field in REFERENCE_FIELDS:
        if f"## {field}" not in body:
            filler = {
                "Availability": (
                    f"Supported in `{tool_name}` for release `{{release}}`. Invoke through "
                    f"the installed `{tool_name}` console script."
                ),
                "Inputs": "See Purpose and the parser-derived options table.",
                "Types": "Paths and schema keys are strings unless noted in Purpose.",
                "Shapes": "Annotation arrays align by first dimension with region or sequence order.",
                "Dtypes": "See linked format references and Purpose.",
                "Defaults": "Parser defaults appear in the generated options table.",
                "Choices": "Parser choices appear in the generated options table.",
                "Constraints": "See Purpose and linked format references.",
                "Outputs": "See Purpose for the serialized output contract.",
                "Ordering": "Output rows retain input order unless stated otherwise in Purpose.",
                "Side effects": "Reads declared inputs and writes declared outputs; inputs are not mutated.",
                "Failures": "Argparse exits for missing required flags or invalid choices; runtime validation errors propagate from the implementation.",
                "Example": (
                    f"Run `{tool_name} {parser_path} --help` after installation to inspect "
                    "required flags, then supply tiny synthetic inputs aligned with the linked format pages."
                ),
            }.get(field, "See Purpose.")
            body = f"{body.rstrip()}\n\n## {field}\n\n{filler}\n"
    if "## Example" not in body:
        body = f"{body.rstrip()}\n\n## Example\n\nSee linked format references and the tool landing page.\n"
    return body


def _group_child_links(tool: ToolRegistry, group_path: str) -> str:
    children = sorted(
        path for path in tool.documented_paths if path.startswith(group_path + " ")
    )
    return "\n".join(
        f"- [`{child}`]({parser_path_to_slug(child)}.md)" for child in children
    )


def _finalize_body(
    body: str, tool: ToolRegistry, page_slug: str, release: str
) -> str:
    body = _repair_links(body, tool, page_slug)
    return (
        body.replace("{release}", release)
        .replace("0.3.0a3", release)
        .replace("0.2.0a2", release)
        .replace("0.1.0a2", release)
    )


def _assemble_command_page(
    tool: ToolRegistry, record: dict[str, Any], release: str
) -> str:
    parser_path = record["path"]
    page_slug = parser_path_to_slug(parser_path)
    body = _ensure_required_sections(
        _load_authored(tool, parser_path), tool.console_name, parser_path
    )
    if "## Syntax" not in body:
        body = f"{body.rstrip()}\n\n{render_syntax_fragment(tool, record).rstrip()}\n"
    note = _required_field_note(record)
    if note and note not in body:
        body = f"{body.rstrip()}\n\n{note}\n"
    body = _finalize_body(body, tool, page_slug, release)
    inventory = json.dumps([record], sort_keys=True, separators=(",", ":"))
    return (
        "<!-- Generated by scripts/assemble_cli_pages.py; do not edit directly. -->\n"
        f"<!-- Parser inventory: {inventory} -->\n\n{body}"
    )


def _assemble_landing_page(
    tool: ToolRegistry, records: list[dict[str, Any]], release: str
) -> str:
    body = _ensure_required_sections(
        _load_authored(tool, "(root)"), tool.console_name, "(root)"
    )
    top_level = sorted(
        {path.split()[0] for path in tool.documented_paths if path != "(root)"}
    )
    if "## Command index" not in body:
        lines = ["## Command index", ""]
        for command in top_level:
            if command in tool.group_paths:
                lines.extend(
                    [
                        f"### `{command}`",
                        "",
                        f"Group landing: [{command}]({parser_path_to_slug(command)}.md).",
                        "",
                        _group_child_links(tool, command),
                        "",
                    ]
                )
            else:
                lines.append(f"- [`{command}`]({parser_path_to_slug(command)}.md)")
        body = f"{body.rstrip()}\n\n" + "\n".join(lines).rstrip() + "\n"
    if "## Syntax" not in body:
        root = next(record for record in records if record["path"] == "(root)")
        body = f"{body.rstrip()}\n\n{render_syntax_fragment(tool, root).rstrip()}\n"
    body = _finalize_body(body, tool, "index", release)
    inventory = json.dumps(records, sort_keys=True, separators=(",", ":"))
    return (
        "<!-- Generated by scripts/assemble_cli_pages.py; do not edit directly. -->\n"
        f"<!-- Parser inventory: {inventory} -->\n\n{body}"
    )


def _assemble_group_page(
    tool: ToolRegistry, group_path: str, record: dict[str, Any], release: str
) -> str:
    page_slug = parser_path_to_slug(group_path)
    body = _ensure_required_sections(
        _load_authored(tool, group_path), tool.console_name, group_path
    )
    child_links = _group_child_links(tool, group_path)
    if child_links and "## Nested commands" not in body:
        body = f"{body.rstrip()}\n\n## Nested commands\n\n{child_links}\n"
    if "## Syntax" not in body:
        body = f"{body.rstrip()}\n\n{render_syntax_fragment(tool, record).rstrip()}\n"
    body = _finalize_body(body, tool, page_slug, release)
    inventory = json.dumps([record], sort_keys=True, separators=(",", ":"))
    return (
        "<!-- Generated by scripts/assemble_cli_pages.py; do not edit directly. -->\n"
        f"<!-- Parser inventory: {inventory} -->\n\n{body}"
    )


def assemble_tool_pages(
    tool: ToolRegistry, records: list[dict[str, Any]], release: str
) -> dict[str, str]:
    validate_registry_against_records(tool, records)
    pages: dict[str, str] = {}
    record_by_path = {record["path"]: record for record in records}
    pages[tool.page_for("(root)")] = _assemble_landing_page(tool, records, release)
    for group_path in sorted(tool.group_paths):
        pages[tool.page_for(group_path)] = _assemble_group_page(
            tool, group_path, record_by_path[group_path], release
        )
    for parser_path in sorted(tool.invocable_paths):
        pages[tool.page_for(parser_path)] = _assemble_command_page(
            tool, record_by_path[parser_path], release
        )
    return pages


def write_fragment_snapshots(tool: ToolRegistry, records: list[dict[str, Any]]) -> None:
    for record in records:
        if record["path"] == "(root)":
            continue
        slug = parser_path_to_slug(record["path"])
        fragment_path = FRAGMENT_ROOT / tool.slug / f"{slug}.syntax.md"
        fragment_path.parent.mkdir(parents=True, exist_ok=True)
        fragment_path.write_text(render_syntax_fragment(tool, record))


def assemble_all_tools(
    parser_records: dict[str, list[dict[str, Any]]], release: str
) -> dict[str, str]:
    pages: dict[str, str] = {}
    for tool in ALL_TOOLS:
        records = parser_records[tool.console_name]
        write_fragment_snapshots(tool, records)
        pages.update(assemble_tool_pages(tool, records, release))
    return pages


def write_pages(pages: dict[str, str]) -> None:
    for relative, content in pages.items():
        target = DOCS_ROOT / "docs" / relative.removeprefix("docs/")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)


def validate_authored_coverage() -> None:
    missing = [
        str((DOCS_ROOT / tool.authored_path(parser_path)).relative_to(DOCS_ROOT))
        for tool in ALL_TOOLS
        for parser_path in tool.documented_paths
        if not (DOCS_ROOT / tool.authored_path(parser_path)).is_file()
    ]
    if missing:
        raise RuntimeError(
            "Missing authored CLI semantics:\n" + "\n".join(sorted(missing))
        )
