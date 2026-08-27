"""Load, validate, and render the consolidated Python API inventory."""

from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


DOCS_ROOT = Path(__file__).resolve().parents[1]
PYTHON_REFERENCE = DOCS_ROOT / "docs/reference/python"
INVENTORY_PATH = PYTHON_REFERENCE / "inventory.json"
GROUPED_INDEX_PATH = PYTHON_REFERENCE / "index.md"
ALPHABETICAL_INDEX_PATH = PYTHON_REFERENCE / "alphabetical-index.md"
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
OPERATION_SEMANTIC_FIELDS = (
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
)
FORMAT_PATHS = {
    "fasta": "reference/formats/elements/fasta",
    "annotation-arrays": "reference/formats/elements/annotation-arrays",
    "meme": "reference/formats/motifs/meme",
}
GENERATED_INDEX_PATHS = {
    GROUPED_INDEX_PATH.relative_to(DOCS_ROOT / "docs").as_posix().removesuffix(".md"),
    ALPHABETICAL_INDEX_PATH.relative_to(DOCS_ROOT / "docs").as_posix().removesuffix(".md"),
}


def load_inventory(path: Path = INVENTORY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text())


def inventory_source_path(page_path: str) -> Path:
    return DOCS_ROOT / "docs" / f"{page_path}.md"


def required_fields_for_page(page: dict[str, Any]) -> tuple[str, ...]:
    if page.get("kind") == "method":
        return OPERATION_SEMANTIC_FIELDS
    return API_SEMANTIC_FIELDS


def index_entries_for_page(page: dict[str, Any]) -> list[dict[str, str]]:
    if "index_entries" in page:
        return page["index_entries"]
    qualified_name = page["qualified_name"]
    title = page.get("title") or qualified_name.rsplit(".", 1)[-1]
    return [{"name": title, "qualified_name": qualified_name}]


def inventory_entries(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for page in inventory.get("pages", []):
        entry = {
            "path": page["path"],
            "symbols": page.get("symbols", []),
            "required_fields": required_fields_for_page(page),
        }
        if "format" in page:
            entry["format"] = page["format"]
        entries.append(entry)
    for format_name in inventory.get("formats", []):
        if format_name in FORMAT_PATHS:
            entries.append(
                {"path": FORMAT_PATHS[format_name], "symbols": [format_name]}
            )
    return entries


def validate_inventory_schema(inventory: dict[str, Any]) -> None:
    required_top = ("release", "internal_symbols", "groups", "pages")
    for key in required_top:
        if key not in inventory:
            raise RuntimeError(f"Python inventory lacks required key {key!r}")

    internal = set(inventory.get("internal_symbols", []))
    for page in inventory["pages"]:
        overlap = sorted(internal.intersection(page.get("symbols", [])))
        if overlap:
            raise RuntimeError(
                f"Inventory page {page['path']} declares internal symbols: "
                + ", ".join(overlap)
            )

    group_ids = {group["id"] for group in inventory["groups"]}
    seen_paths: set[str] = set()
    seen_qualified: set[str] = set()

    for page in inventory["pages"]:
        for key in ("path", "group", "kind", "status", "title", "qualified_name", "symbols"):
            if key not in page:
                raise RuntimeError(f"Inventory page {page.get('path', '?')} lacks {key!r}")
        if page["group"] not in group_ids:
            raise RuntimeError(
                f"Inventory page {page['path']} references unknown group {page['group']!r}"
            )
        if page["path"] in seen_paths:
            raise RuntimeError(f"Duplicate inventory page path: {page['path']}")
        seen_paths.add(page["path"])
        for entry in index_entries_for_page(page):
            qualified = entry["qualified_name"]
            if qualified in seen_qualified:
                raise RuntimeError(f"Duplicate alphabetical qualified name: {qualified}")
            seen_qualified.add(qualified)

    for landing in inventory.get("landings", []):
        if landing["path"] in seen_paths:
            raise RuntimeError(f"Duplicate inventory landing path: {landing['path']}")
        seen_paths.add(landing["path"])


def validate_inventory_sources(inventory: dict[str, Any]) -> None:
    for page in inventory["pages"]:
        source = inventory_source_path(page["path"])
        if not source.is_file():
            raise RuntimeError(f"Inventory page has no source Markdown: {page['path']}")
        text = source.read_text()
        qualified = page["qualified_name"]
        if qualified not in text:
            raise RuntimeError(
                f"{page['path']} source lacks searchable qualified name {qualified!r}"
            )
        for alias in page.get("aliases", []):
            if alias not in text:
                raise RuntimeError(
                    f"{page['path']} source lacks searchable alias {alias!r}"
                )
        for field in required_fields_for_page(page):
            if f"## {field}\n" not in text and f"## {field}\r\n" not in text:
                raise RuntimeError(f"{page['path']} source lacks section {field!r}")

    allowed_paths = {page["path"] for page in inventory["pages"]}
    allowed_paths.update(landing["path"] for landing in inventory.get("landings", []))
    allowed_paths.update(GENERATED_INDEX_PATHS)
    for markdown in PYTHON_REFERENCE.rglob("*.md"):
        relative = markdown.relative_to(DOCS_ROOT / "docs").as_posix().removesuffix(".md")
        if relative == "reference/python/inventory":
            continue
        if relative not in allowed_paths:
            raise RuntimeError(
                f"Undeclared Python reference page {relative}; add it to inventory.json"
            )


def _article_html(page_html: str) -> str:
    if "<article" not in page_html:
        raise RuntimeError("Built page lacks article body")
    return page_html.split("<article", 1)[1].split("</article>", 1)[0]


def _article_anchor_ids(article_html: str) -> set[str]:
    return set(re.findall(r'id="([^"]+)"', article_html))


def resolve_member_anchor(
    symbol: str,
    anchor_ids: set[str],
    *,
    page_heading_id: str | None = None,
) -> str | None:
    exact = [anchor_id for anchor_id in anchor_ids if anchor_id == symbol]
    if exact:
        return exact[0]
    qualified = [
        anchor_id
        for anchor_id in anchor_ids
        if anchor_id.endswith(f".{symbol}") or anchor_id.endswith(f".{symbol.lstrip('_')}")
    ]
    if qualified:
        return max(qualified, key=len)
    if page_heading_id and symbol.replace("_", "") in page_heading_id:
        return page_heading_id
    return None


def _site_page(site_dir: Path, page_path: str) -> Path:
    clean = page_path.rstrip("/")
    if clean.endswith("/index"):
        return site_dir / f"{clean}.html"
    return site_dir / f"{clean}/index.html"


def validate_built_python_api(site_dir: Path, inventory: dict[str, Any]) -> None:
    internal_symbols = inventory.get("internal_symbols", [])
    grouped_page = _site_page(site_dir, "reference/python/index")
    alphabetical_page = _site_page(site_dir, "reference/python/alphabetical-index")
    for path in (grouped_page, alphabetical_page):
        if not path.is_file():
            raise RuntimeError(f"Missing built Python index page: {path}")

    grouped_html = html.unescape(grouped_page.read_text())
    alphabetical_html = html.unescape(alphabetical_page.read_text())
    grouped_links = set(re.findall(r'href="([^"]+)"', _article_html(grouped_page.read_text())))
    alphabetical_links = set(
        re.findall(r'href="([^"]+)"', _article_html(alphabetical_page.read_text()))
    )

    for page in inventory["pages"]:
        page_link = _relative_page_link(page["path"])
        built = _site_page(site_dir, page["path"])
        if not built.is_file():
            raise RuntimeError(f"Inventory page has no built page: {page['path']}")
        article = _article_html(built.read_text())
        anchor_ids = _article_anchor_ids(article)
        heading_ids = [
            anchor_id
            for anchor_id in anchor_ids
            if not anchor_id.startswith("__") and anchor_id.islower()
        ]
        page_heading_id = heading_ids[0] if heading_ids else None
        rendered = html.unescape(built.read_text())
        for field in required_fields_for_page(page):
            if field not in rendered:
                raise RuntimeError(f"{page['path']} lacks field {field}")
        for symbol in page.get("symbols", []):
            anchor = resolve_member_anchor(symbol, anchor_ids, page_heading_id=page_heading_id)
            if anchor is None and symbol not in rendered:
                raise RuntimeError(f"{page['path']} lacks symbol anchor for {symbol}")
        for internal in internal_symbols:
            if internal in rendered:
                raise RuntimeError(
                    f"{page['path']} exposes internal symbol {internal!r}"
                )
        qualified = page["qualified_name"]
        if qualified not in grouped_html:
            raise RuntimeError(
                f"Grouped Python index lacks qualified name {qualified!r}"
            )
        for alias in page.get("aliases", []):
            if alias not in grouped_html:
                raise RuntimeError(f"Grouped Python index lacks alias {alias!r}")

        for entry in index_entries_for_page(page):
            qualified_name = entry["qualified_name"]
            if qualified_name not in alphabetical_html:
                raise RuntimeError(
                    f"Alphabetical Python index lacks entry {qualified_name!r}"
                )
            if page_link not in alphabetical_links:
                raise RuntimeError(
                    f"Alphabetical Python index lacks canonical page link for {qualified_name!r}"
                )

        singular_format = page.get("format")
        if singular_format and not _site_page(site_dir, singular_format).is_file():
            raise RuntimeError(f"Unresolved format reference: {singular_format}")

    for format_name in inventory.get("formats", []):
        format_path = FORMAT_PATHS[format_name]
        if not _site_page(site_dir, format_path).is_file():
            raise RuntimeError(f"Inventory format has no built page: {format_path}")

    if any(internal in grouped_html for internal in internal_symbols):
        raise RuntimeError("Grouped Python index exposes internal symbols")
    if any(internal in alphabetical_html for internal in internal_symbols):
        raise RuntimeError("Alphabetical Python index exposes internal symbols")

    grouped_counts = defaultdict(int)
    alphabetical_counts = defaultdict(int)
    for page in inventory["pages"]:
        grouped_counts[page["qualified_name"]] += 1
        for entry in index_entries_for_page(page):
            alphabetical_counts[entry["qualified_name"]] += 1
    duplicate_grouped = [name for name, count in grouped_counts.items() if count > 1]
    duplicate_alpha = [name for name, count in alphabetical_counts.items() if count > 1]
    if duplicate_grouped:
        raise RuntimeError(
            "Grouped Python index has duplicate qualified names: "
            + ", ".join(sorted(duplicate_grouped))
        )
    if duplicate_alpha:
        raise RuntimeError(
            "Alphabetical Python index has duplicate qualified names: "
            + ", ".join(sorted(duplicate_alpha))
        )


def _relative_page_link(page_path: str) -> str:
    relative = Path(page_path).relative_to("reference/python").as_posix()
    return f"{relative}/"


def _member_link(page_path: str, anchor: str | None) -> str:
    link = _relative_page_link(page_path)
    if anchor:
        return f"{link}#{anchor}"
    return link


def render_grouped_index(inventory: dict[str, Any]) -> str:
    groups = {group["id"]: group for group in inventory["groups"]}
    pages_by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for page in inventory["pages"]:
        pages_by_group[page["group"]].append(page)

    lines = [
        "# Python API grouped index",
        "",
        f"Supported `RGTools` release `{inventory['release']}`. Browse by API area; "
        "each entry shows the exact qualified name and links to the canonical page.",
        "",
    ]
    for group in inventory["groups"]:
        group_pages = sorted(
            pages_by_group.get(group["id"], []),
            key=lambda page: page["qualified_name"].lower(),
        )
        if not group_pages:
            continue
        lines.extend([f"## {group['title']}", ""])
        if group.get("description"):
            lines.append(group["description"])
            lines.append("")
        for page in group_pages:
            status_suffix = " (experimental)" if page["status"] == "Experimental" else ""
            lines.append(
                f"### `{page['qualified_name']}`{status_suffix}"
            )
            lines.append("")
            lines.append(
                f"- Canonical page: [`{page['title']}`]({_relative_page_link(page['path'])})"
            )
            aliases = page.get("aliases", [])
            if aliases:
                alias_text = ", ".join(f"`{alias}`" for alias in aliases)
                lines.append(f"- Aliases: {alias_text}")
            lines.append(f"- Status: {page['status']}")
            if page.get("symbols"):
                member_bits = []
                for symbol in page["symbols"]:
                    member_bits.append(f"`{symbol}`")
                lines.append("- Members: " + ", ".join(member_bits))
            search_terms = [page["qualified_name"], *aliases]
            lines.append(
                "- Search terms: "
                + ", ".join(f"`{term}`" for term in search_terms)
            )
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_alphabetical_index(inventory: dict[str, Any]) -> str:
    entries: list[tuple[str, dict[str, str], dict[str, Any]]] = []
    for page in inventory["pages"]:
        for entry in index_entries_for_page(page):
            entries.append((entry["qualified_name"].lower(), entry, page))
    entries.sort(key=lambda item: item[0])

    lines = [
        "# Python API alphabetical index",
        "",
        "Every supported class, function group, module, and standalone method page "
        "appears exactly once with its canonical page.",
        "",
        "| Qualified name | Page | Status |",
        "| --- | --- | --- |",
    ]
    for _, entry, page in entries:
        status = page["status"]
        lines.append(
            f"| `{entry['qualified_name']}` | "
            f"[{entry['name']}]({_relative_page_link(page['path'])}) | {status} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_generated_indexes(inventory: dict[str, Any]) -> None:
    GROUPED_INDEX_PATH.write_text(render_grouped_index(inventory))
    ALPHABETICAL_INDEX_PATH.write_text(render_alphabetical_index(inventory))
