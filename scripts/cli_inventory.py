"""Load, validate, and render per-tool CLI inventories."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from cli_page_registry import (
    GENOMIC_ELEMENT_TOOLS,
    ToolRegistry,
    parser_path_to_slug,
)


DOCS_ROOT = Path(__file__).resolve().parents[1]


def inventory_path(tool: ToolRegistry) -> Path:
    return DOCS_ROOT / "docs/reference/cli" / tool.slug / "inventory.json"


def load_tool_inventory(tool: ToolRegistry) -> dict[str, Any]:
    return json.loads(inventory_path(tool).read_text())


def _page_link(parser_path: str) -> str:
    slug = parser_path_to_slug(parser_path)
    if slug == "index":
        return "index.md"
    return f"{slug}.md"


def _legacy_anchor_id(parser_path: str) -> str:
    return parser_path.replace(" ", "_")


def render_browse_by_task(tool: ToolRegistry) -> str:
    if not tool.intent_groups:
        return ""
    lines = ["## Browse by task", ""]
    for group in tool.intent_groups:
        lines.extend([f"### {group.title}", ""])
        if group.group_path is not None:
            lines.append(
                f"Group landing: [`{group.group_path}`]({_page_link(group.group_path)})."
            )
            lines.append("")
        for parser_path in group.paths:
            lines.append(f"- [`{parser_path}`]({_page_link(parser_path)})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_exact_path_index(tool: ToolRegistry) -> str:
    paths = sorted(tool.invocable_paths | tool.group_paths)
    lines = [
        "## Exact command paths",
        "",
        "Every invocable command path and non-invocable command group appears "
        "exactly once for direct lookup.",
        "",
        "| Command path | Canonical page |",
        "| --- | --- |",
    ]
    for parser_path in paths:
        lines.append(
            f"| `{parser_path}` | [`{parser_path}`]({_page_link(parser_path)}) |"
        )
    lines.append("")
    return "\n".join(lines)


def render_legacy_anchors(tool: ToolRegistry) -> str:
    lines = [
        "## Legacy heading anchors",
        "",
        "Former consolidated-page fragment links resolve to the canonical pages "
        "below.",
        "",
    ]
    for parser_path in sorted(tool.invocable_paths):
        anchor = _legacy_anchor_id(parser_path)
        lines.extend(
            [
                f'<span id="{anchor}"></span>',
                "",
                f"### `{parser_path}`",
                "",
                f"Canonical reference: [`{parser_path}`]({_page_link(parser_path)}).",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def validate_tool_inventory(tool: ToolRegistry, inventory: dict[str, Any]) -> None:
    commands = set(inventory.get("commands", []))
    if commands != tool.invocable_paths:
        raise RuntimeError(
            f"{tool.console_name} inventory commands drift: "
            f"missing={sorted(tool.invocable_paths - commands)} "
            f"extra={sorted(commands - tool.invocable_paths)}"
        )

    expected_paths: set[str] = {tool.slug}
    for parser_path in sorted(tool.group_paths | tool.invocable_paths):
        expected_paths.add(f"{tool.slug}/{parser_path_to_slug(parser_path)}")
    normalized_entries = set()
    for entry in inventory.get("entries", []):
        path = entry["path"]
        if path == f"reference/cli/{tool.slug}":
            normalized_entries.add(tool.slug)
            continue
        normalized_entries.add(path.removeprefix("reference/cli/"))

    if normalized_entries != expected_paths:
        raise RuntimeError(
            f"{tool.console_name} inventory entry drift: "
            f"missing={sorted(expected_paths - normalized_entries)} "
            f"extra={sorted(normalized_entries - expected_paths)}"
        )

    if tool.intent_groups:
        listed = {path for group in tool.intent_groups for path in group.paths}
        if listed != tool.invocable_paths:
            raise RuntimeError(
                f"{tool.console_name} intent groups drift: "
                f"missing={sorted(tool.invocable_paths - listed)} "
                f"extra={sorted(listed - tool.invocable_paths)}"
            )


def _site_page(site_dir: Path, page_path: str) -> Path:
    clean = page_path.rstrip("/")
    if clean.endswith("/index"):
        return site_dir / f"{clean}.html"
    return site_dir / f"{clean}/index.html"


def _article_html(page_html: str) -> str:
    if "<article" not in page_html:
        raise RuntimeError("Built page lacks article body")
    return page_html.split("<article", 1)[1].split("</article>", 1)[0]


def validate_built_tool_landing(
    site_dir: Path, tool: ToolRegistry, inventory: dict[str, Any]
) -> None:
    landing = _site_page(site_dir, f"reference/cli/{tool.slug}")
    if not landing.is_file():
        raise RuntimeError(f"Missing built CLI landing page: {landing}")
    rendered = html.unescape(_article_html(landing.read_text()))

    if tool.intent_groups:
        if "Browse by task" not in rendered:
            raise RuntimeError(f"{tool.console_name} landing lacks Browse by task")
        for group in tool.intent_groups:
            if group.title not in rendered:
                raise RuntimeError(
                    f"{tool.console_name} landing lacks intent group {group.title!r}"
                )

    if "Exact command paths" not in rendered:
        raise RuntimeError(f"{tool.console_name} landing lacks Exact command paths")

    for parser_path in sorted(tool.invocable_paths | tool.group_paths):
        if parser_path not in rendered:
            raise RuntimeError(
                f"{tool.console_name} landing lacks exact-path entry {parser_path!r}"
            )

    if tool is GENOMIC_ELEMENT_TOOLS:
        for anchor in ("select_tss_relative_track", "tss_relative_mutagenesis"):
            if f'id="{anchor}"' not in landing.read_text():
                raise RuntimeError(
                    f"{tool.console_name} landing lacks legacy anchor {anchor!r}"
                )
            if parser_path_to_slug(anchor) not in rendered:
                raise RuntimeError(
                    f"{tool.console_name} legacy anchor {anchor!r} lacks canonical link"
                )


def validate_genomic_element_tools_inventory() -> None:
    inventory = load_tool_inventory(GENOMIC_ELEMENT_TOOLS)
    validate_tool_inventory(GENOMIC_ELEMENT_TOOLS, inventory)
