"""Load, validate, and render per-tool CLI inventories."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from cli_page_registry import (
    ALL_TOOLS,
    GENOMIC_ELEMENT_TOOLS,
    ToolRegistry,
    parser_path_to_slug,
)


DOCS_ROOT = Path(__file__).resolve().parents[1]
CLI_REFERENCE = DOCS_ROOT / "docs/reference/cli"
SITE_INVENTORY_PATH = CLI_REFERENCE / "inventory.json"
GROUPED_INDEX_PATH = CLI_REFERENCE / "index.md"
EXACT_PATH_INDEX_PATH = CLI_REFERENCE / "exact-path-index.md"
GENERATED_INDEX_PATHS = {
    GROUPED_INDEX_PATH.relative_to(DOCS_ROOT / "docs").as_posix().removesuffix(".md"),
    EXACT_PATH_INDEX_PATH.relative_to(DOCS_ROOT / "docs")
    .as_posix()
    .removesuffix(".md"),
}


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


def load_site_inventory(path: Path = SITE_INVENTORY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text())


def _tool_registry(console_name: str) -> ToolRegistry:
    for tool in ALL_TOOLS:
        if tool.console_name == console_name:
            return tool
    raise RuntimeError(f"Unknown CLI console name: {console_name}")


def site_index_entries(inventory: dict[str, Any]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for tool_meta in inventory["tools"]:
        tool = _tool_registry(tool_meta["console_name"])
        for parser_path in sorted(tool.invocable_paths | tool.group_paths):
            entries.append(
                {
                    "console_name": tool.console_name,
                    "command_path": parser_path,
                    "qualified_path": f"{tool.console_name} {parser_path}",
                    "page": tool.page_for(parser_path).removesuffix(".md"),
                }
            )
    return entries


def validate_site_inventory(inventory: dict[str, Any]) -> None:
    declared = {tool["console_name"] for tool in inventory["tools"]}
    expected = {tool.console_name for tool in ALL_TOOLS}
    if declared != expected:
        raise RuntimeError(
            "Site CLI inventory tool drift: "
            f"missing={sorted(expected - declared)} extra={sorted(declared - expected)}"
        )

    seen_ids: set[str] = set()
    seen_landings: set[str] = set()
    for tool_meta in inventory["tools"]:
        for key in ("id", "console_name", "ownership", "description", "landing"):
            if key not in tool_meta:
                raise RuntimeError(f"Site CLI inventory tool lacks {key!r}")
        if tool_meta["id"] in seen_ids:
            raise RuntimeError(f"Duplicate site CLI inventory tool id: {tool_meta['id']}")
        seen_ids.add(tool_meta["id"])
        landing = tool_meta["landing"]
        if landing in seen_landings:
            raise RuntimeError(f"Duplicate site CLI inventory landing: {landing}")
        seen_landings.add(landing)
        tool = _tool_registry(tool_meta["console_name"])
        if landing != f"reference/cli/{tool.slug}":
            raise RuntimeError(
                f"Site CLI inventory landing mismatch for {tool_meta['console_name']}"
            )

    entries = site_index_entries(inventory)
    qualified = [entry["qualified_path"] for entry in entries]
    if len(qualified) != len(set(qualified)):
        duplicates = sorted(
            name for name in set(qualified) if qualified.count(name) > 1
        )
        raise RuntimeError(
            "Site CLI inventory has duplicate qualified paths: "
            + ", ".join(duplicates)
        )

    for tool in ALL_TOOLS:
        validate_tool_inventory(tool, load_tool_inventory(tool))


def _relative_page_link(page_path: str) -> str:
    relative = Path(page_path).relative_to("reference/cli")
    if len(relative.parts) == 1:
        return f"{relative.as_posix()}/index.md"
    return f"{relative.as_posix()}.md"


def render_grouped_cli_index(inventory: dict[str, Any]) -> str:
    lines = [
        "# CLI command grouped index",
        "",
        f"Supported release `{inventory['release']}`. Three installed console scripts "
        "own distinct genomic workflows. Browse by ownership, then open a tool "
        "landing for task-oriented groupings and per-command semantics.",
        "",
    ]
    for tool_meta in inventory["tools"]:
        tool = _tool_registry(tool_meta["console_name"])
        lines.extend(
            [
                f"## {tool_meta['ownership']}: `{tool_meta['console_name']}`",
                "",
                tool_meta["description"],
                "",
                f"- Canonical landing: [`{tool_meta['console_name']}`]({_relative_page_link(tool_meta['landing'])})",
                f"- Search terms: `{tool_meta['console_name']}`, `{tool.slug}`",
            ]
        )
        if tool.intent_groups:
            lines.append("- Browse by task on the tool landing:")
            for group in tool.intent_groups:
                lines.append(f"  - {group.title}")
        else:
            top_level = sorted(
                {
                    path.split()[0]
                    for path in tool.documented_paths
                    if path != "(root)"
                }
            )
            if top_level:
                group_text = ", ".join(f"`{name}`" for name in top_level)
                lines.append(f"- Top-level command groups: {group_text}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_site_exact_path_index(inventory: dict[str, Any]) -> str:
    entries = site_index_entries(inventory)
    lines = [
        "# CLI exact command-path index",
        "",
        "Every installed console script, invocable command path, and non-invocable "
        "command group appears exactly once with its canonical page.",
        "",
        "| Executable and command path | Canonical page |",
        "| --- | --- |",
    ]
    for entry in sorted(entries, key=lambda item: item["qualified_path"].lower()):
        page_name = entry["command_path"]
        lines.append(
            f"| `{entry['qualified_path']}` | "
            f"[{page_name}]({_relative_page_link(entry['page'])}) |"
        )
    lines.append("")
    return "\n".join(lines)


def write_generated_cli_indexes(inventory: dict[str, Any] | None = None) -> None:
    payload = inventory or load_site_inventory()
    validate_site_inventory(payload)
    GROUPED_INDEX_PATH.write_text(render_grouped_cli_index(payload))
    EXACT_PATH_INDEX_PATH.write_text(render_site_exact_path_index(payload))


def validate_retired_generated_references() -> None:
    authored_roots = [
        DOCS_ROOT / tool.authored_path("(root)") for tool in ALL_TOOLS
    ]
    for path in authored_roots:
        if "generated/" in path.read_text():
            raise RuntimeError(
                f"{path.relative_to(DOCS_ROOT)} still links to generated parser snapshots"
            )
    for relative in (
        "docs/cli/MotifTools.md",
        "docs/cli/GenomicElementTools.md",
        "docs/cli/ExogenousSequenceTools.md",
    ):
        path = DOCS_ROOT / relative
        if path.is_file() and "reference/cli/generated/" in path.read_text():
            raise RuntimeError(
                f"{relative} still links to generated parser snapshots as canonical reference"
            )


def validate_built_cli_indexes(site_dir: Path, inventory: dict[str, Any]) -> None:
    grouped_page = _site_page(site_dir, "reference/cli/index")
    exact_page = _site_page(site_dir, "reference/cli/exact-path-index")
    for path in (grouped_page, exact_page):
        if not path.is_file():
            raise RuntimeError(f"Missing built CLI index page: {path}")

    grouped_html = html.unescape(_article_html(grouped_page.read_text()))
    exact_html = html.unescape(_article_html(exact_page.read_text()))
    entries = site_index_entries(inventory)

    for tool_meta in inventory["tools"]:
        console_name = tool_meta["console_name"]
        ownership = tool_meta["ownership"]
        if ownership not in grouped_html:
            raise RuntimeError(f"Grouped CLI index lacks ownership {ownership!r}")
        if console_name not in grouped_html:
            raise RuntimeError(
                f"Grouped CLI index lacks console name {console_name!r}"
            )
        if tool_meta["description"] not in grouped_html:
            raise RuntimeError(
                f"Grouped CLI index lacks description for {console_name!r}"
            )

    qualified_counts: dict[str, int] = {}
    for entry in entries:
        qualified = entry["qualified_path"]
        qualified_counts[qualified] = qualified_counts.get(qualified, 0) + 1
        if qualified not in exact_html:
            raise RuntimeError(
                f"Exact-path CLI index lacks qualified path {qualified!r}"
            )
        if entry["command_path"] not in exact_html:
            raise RuntimeError(
                f"Exact-path CLI index lacks parser path {entry['command_path']!r}"
            )
        built = _site_page(site_dir, entry["page"])
        if not built.is_file():
            raise RuntimeError(f"CLI index entry has no built page: {entry['page']}")

    duplicates = sorted(name for name, count in qualified_counts.items() if count > 1)
    if duplicates:
        raise RuntimeError(
            "Exact-path CLI index has duplicate qualified paths: "
            + ", ".join(duplicates)
        )
    if len(entries) != len(qualified_counts):
        raise RuntimeError("Exact-path CLI index entry count mismatch")


def validate_built_tool_landing_no_generated_links(site_dir: Path, tool: ToolRegistry) -> None:
    landing = _site_page(site_dir, f"reference/cli/{tool.slug}")
    content = landing.read_text()
    if "reference/cli/generated/" in content or "../generated/" in content:
        raise RuntimeError(
            f"{tool.console_name} landing still links to generated parser snapshots"
        )


def validate_all_tool_inventories() -> None:
    for tool in ALL_TOOLS:
        validate_tool_inventory(tool, load_tool_inventory(tool))
