from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from collections import defaultdict
from html.parser import HTMLParser
from importlib.metadata import version
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse


DOCS_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = DOCS_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from cli_inventory import (  # noqa: E402
    load_site_inventory,
    load_tool_inventory,
    validate_all_tool_inventories,
    validate_built_cli_indexes,
    validate_built_tool_landing,
    validate_built_tool_landing_no_generated_links,
    validate_genomic_element_tools_inventory,
    validate_retired_generated_references,
    validate_site_inventory,
    validate_tool_inventory,
    write_generated_cli_indexes,
)
from cli_page_registry import ALL_TOOLS, GENOMIC_ELEMENT_TOOLS, REDIRECTS  # noqa: E402
from python_api_inventory import (  # noqa: E402
    inventory_entries,
    load_inventory,
    validate_built_python_api,
    validate_inventory_schema,
    validate_inventory_sources,
    write_generated_indexes,
)
from regenerate_cli_reference import main as regenerate_cli_reference  # noqa: E402

GENERATED_CLI_DIRECTORY = DOCS_ROOT / "docs/reference/cli/generated"
REFERENCE_FIELDS = (
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
GENOMIC_ELEMENTS_PATH = "reference/python/elements/genomic-elements"
GENOMIC_ELEMENTS_SOURCE = DOCS_ROOT / "docs/reference/python/elements/genomic-elements.md"
LIBRARY_SOURCE = DOCS_ROOT / "docs/library.md"
MKDOCS_CONFIG = DOCS_ROOT / "mkdocs.yml"
MASK_AUTHORED_SOURCE = (
    DOCS_ROOT / "docs/reference/cli/authored/genomic-element-tools/mask-op/intersect.md"
)
PYTHON_INVENTORY = DOCS_ROOT / "docs/reference/python/inventory.json"
CANONICAL_MASK_INTERSECT = "reference/cli/genomic-element-tools/mask-op/intersect"
METHOD_PAGE = "reference/python/general-elements/load-mask-from-arr.md"
METHOD_NAV_LABEL = "GeneralElements.load_mask_from_arr()"
LIBRARY_COLLECTIONS_HEADER = "### Element collections"


def _release_version() -> str:
    return version("RGTools")


RELEASE = _release_version()
CLI_RELEASES = {
    "GenomicElementTools": RELEASE,
    "ExogeneousSequenceTools": RELEASE,
    "MotifTools": RELEASE,
}
PAGES_BASE = "https://dignomor.github.io/xp-genomic-tools-docs/"
DOCS_RAW_BASE = "https://raw.githubusercontent.com/DignoMor/xp-genomic-tools-docs"
PRIVATE_MARKERS = re.compile(
    r"(?:/specs/|delivery-specs?|pipeline[-_ ]contracts?|\.scratch/|private/|\bSPEC\d{3}\b)",
    re.IGNORECASE,
)


def _library_target(href: str) -> str:
    return urlparse(urljoin("https://docs.invalid/library/", href)).path.lstrip("/")


def _markdown_has_heading(text: str, heading: str) -> bool:
    return f"## {heading}\n" in text or f"## {heading}\r\n" in text


def _extract_nav_section(config_text: str, heading: str) -> str:
    match = re.search(
        rf"(?m)^(?P<indent>[ \t]*)- {re.escape(heading)}:\n"
        rf"(?P<body>(?:(?!\1- )[^\n]*\n?)*)",
        config_text,
    )
    if match is None:
        return ""
    return match.group(0)


def _validate_source_contracts() -> None:
    """Fail fast on source IA and semantic contracts before assemble mutates CLI pages."""
    genomic_text = GENOMIC_ELEMENTS_SOURCE.read_text()
    if not genomic_text.strip().startswith("# `GenomicElements`"):
        raise RuntimeError(
            "GenomicElements page is missing or placeholder content; "
            f"restore {GENOMIC_ELEMENTS_SOURCE.relative_to(DOCS_ROOT)}"
        )
    missing_api = [
        field
        for field in API_SEMANTIC_FIELDS
        if not _markdown_has_heading(genomic_text, field)
    ]
    if missing_api:
        raise RuntimeError(
            "GenomicElements page lacks semantic sections: "
            + ", ".join(missing_api)
        )

    mask_authored = MASK_AUTHORED_SOURCE.read_text()
    if not _markdown_has_heading(mask_authored, "Example"):
        raise RuntimeError(
            "Built canonical mask_op intersect page lacks Example section"
        )

    library_text = LIBRARY_SOURCE.read_text()
    collections_start = library_text.find(LIBRARY_COLLECTIONS_HEADER)
    if collections_start == -1:
        raise RuntimeError(
            f"Library page lacks {LIBRARY_COLLECTIONS_HEADER!r} section"
        )
    collections_end = library_text.find("\n### ", collections_start + 1)
    collections_section = library_text[
        collections_start : collections_end if collections_end != -1 else None
    ]
    if METHOD_PAGE in collections_section:
        raise RuntimeError(
            "The Element collections Library section is class-only; operation "
            "pages such as GeneralElements.load_mask_from_arr must not appear there"
        )

    mkdocs_text = MKDOCS_CONFIG.read_text()
    for source, target in REDIRECTS.items():
        normalized = f"{source}: {target}"
        if normalized not in mkdocs_text:
            raise RuntimeError(
                f"Missing redirect mapping for {source} -> {target}"
            )

    python_nav = _extract_nav_section(mkdocs_text, "Python")
    if not python_nav:
        raise RuntimeError(
            "GeneralElements.load_mask_from_arr must remain reachable in built "
            "navigation"
        )
    element_collections_nav = _extract_nav_section(python_nav, "Element collections")
    operations_nav = _extract_nav_section(python_nav, "Operations")
    marked_entry = f"- {METHOD_NAV_LABEL}: {METHOD_PAGE}"
    unmarked_entry = f"- GeneralElements.load_mask_from_arr: {METHOD_PAGE}"
    marked_present = marked_entry in python_nav
    unmarked_present = unmarked_entry in python_nav and not marked_present
    if unmarked_present:
        raise RuntimeError(
            "GeneralElements.load_mask_from_arr must be presented as a method "
            "in built navigation"
        )
    if METHOD_PAGE in element_collections_nav:
        raise RuntimeError(
            "GeneralElements.load_mask_from_arr must not occupy the "
            "class-only Element collections navigation group"
        )
    if (
        not marked_present
        and unmarked_entry not in operations_nav
        and METHOD_PAGE in python_nav
    ):
        raise RuntimeError(
            "GeneralElements.load_mask_from_arr must appear under the "
            "explicit Operations grouping, not as a peer of classes, "
            "modules, or reference areas"
        )
    if marked_present and marked_entry not in operations_nav:
        raise RuntimeError(
            "GeneralElements.load_mask_from_arr must appear under the "
            "explicit Operations grouping, not as a peer of classes, "
            "modules, or reference areas"
        )


class NavigationAncestryParser(HTMLParser):
    """Collect the rendered navigation groups containing each target."""

    def __init__(self) -> None:
        super().__init__()
        self.ancestors: dict[str, list[tuple[str, ...]]] = defaultdict(list)
        self.titles: dict[str, list[str]] = defaultdict(list)
        self._list_item_labels: list[str | None] = []
        self._label_index: int | None = None
        self._label_text: list[str] = []
        self._link_target: str | None = None
        self._link_text: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag == "li":
            self._list_item_labels.append(None)
            return
        attributes = dict(attrs)
        if tag == "label" and "md-nav__link" in (
            attributes.get("class") or ""
        ).split():
            self._label_index = len(self._list_item_labels) - 1
            self._label_text = []
            return
        if tag != "a":
            return
        if "md-nav__link" not in (attributes.get("class") or "").split():
            return
        href = attributes.get("href")
        if href is not None:
            target = _library_target(href)
            groups = tuple(
                label for label in self._list_item_labels[:-1] if label is not None
            )
            self.ancestors[target].append(groups)
            self._link_target = target
            self._link_text = []

    def handle_data(self, data: str) -> None:
        if self._label_index is not None:
            self._label_text.append(data)
        elif self._link_target is not None:
            self._link_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "label" and self._label_index is not None:
            label = " ".join("".join(self._label_text).split())
            self._list_item_labels[self._label_index] = label
            self._label_index = None
            self._label_text = []
        elif tag == "a" and self._link_target is not None:
            title = " ".join("".join(self._link_text).split())
            self.titles[self._link_target].append(title)
            self._link_target = None
            self._link_text = []
        elif tag == "li":
            self._list_item_labels.pop()


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=DOCS_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def _git_revision(repository: Path) -> str:
    return _run(["git", "-C", str(repository), "rev-parse", "HEAD"]).stdout.strip()


def _git_file(raw_source_root: Path, revision: str, target: Path) -> str | None:
    completed = subprocess.run(
        ["git", "-C", str(raw_source_root), "show", f"{revision}:{target}"],
        capture_output=True,
        text=True,
    )
    return completed.stdout if completed.returncode == 0 else None


def _validate_raw_source_revision(
    raw_source_root: Path, revision: str, code_revision: str
) -> None:
    targets = [
        Path("docs/llms.txt"),
        Path("docs/llms-full.txt"),
        *(
            path.relative_to(DOCS_ROOT)
            for path in (DOCS_ROOT / "docs/reference").rglob("*.md")
        ),
    ]
    missing: list[str] = []
    for target in targets:
        committed = _git_file(raw_source_root, revision, target)
        if committed is None:
            missing.append(str(target))
            continue
        if target.parts[:2] == ("docs", "reference"):
            if "authored" in target.parts or "fragments" in target.parts:
                continue
            if len(target.parts) > 2 and target.parts[2] == "cli":
                continue
            if target.as_posix() in (
                "docs/reference/python/index.md",
                "docs/reference/python/alphabetical-index.md",
                "docs/reference/cli/index.md",
                "docs/reference/cli/exact-path-index.md",
            ):
                continue
            local = DOCS_ROOT / target
            if committed != local.read_text():
                raise RuntimeError(
                    f"Immutable docs revision {revision} has stale raw content: {target}"
                )
    if missing:
        raise RuntimeError(
            f"Immutable docs revision {revision} lacks raw fallback targets: {', '.join(missing)}"
        )
    for target in (Path("docs/llms.txt"), Path("docs/llms-full.txt")):
        committed = _git_file(raw_source_root, revision, target)
        assert committed is not None
        for marker in (RELEASE, code_revision):
            if marker not in committed:
                raise RuntimeError(
                    f"Immutable {target} does not identify {marker} at {revision}"
                )


def _site_path(path: str) -> str:
    clean = path.rstrip("/")
    if clean.endswith("/index"):
        return clean.removesuffix("/index") + "/index.html"
    return clean + "/index.html"


def _load_python_inventory() -> dict[str, Any]:
    return load_inventory(PYTHON_INVENTORY)


def _load_inventories() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = list(inventory_entries(_load_python_inventory()))
    for inventory_path in (
        DOCS_ROOT / "tests/ticket05_reference_inventory.json",
        DOCS_ROOT / "tests/ticket06_reference_inventory.json",
        DOCS_ROOT / "tests/ticket07_motif_tools_reference_inventory.json",
    ):
        payload = json.loads(inventory_path.read_text())
        entries.extend(payload.get("entries", []))
    return entries


def _render_agent_resources(code_revision: str, docs_revision: str) -> None:
    raw_base = f"{DOCS_RAW_BASE}/{docs_revision}/docs"
    canonical = PAGES_BASE
    links = [
        ("Reference conventions", "reference/conventions/", "reference/conventions.md"),
        ("Python reference", "reference/python/", "reference/python/index.md"),
        ("BedTable reference", "reference/python/bedtable/bed-table3/", "reference/python/bedtable/bed-table3.md"),
        ("CLI grouped index", "reference/cli/", "reference/cli/index.md"),
        ("CLI exact-path index", "reference/cli/exact-path-index/", "reference/cli/exact-path-index.md"),
        ("GenomicElementTools CLI", "reference/cli/genomic-element-tools/", "reference/cli/genomic-element-tools/index.md"),
        ("ExogeneousSequenceTools CLI", "reference/cli/exogeneous-sequence-tools/", "reference/cli/exogeneous-sequence-tools/index.md"),
        ("MotifTools CLI", "reference/cli/motif-tools/", "reference/cli/motif-tools/index.md"),
        ("Formats", "formats/", "formats.md"),
        ("Boolean-mask dtype rule", "reference/formats/boolean-mask/#dtype", "reference/formats/boolean-mask.md#dtype"),
    ]
    compact = [
        f"# xp-genomic-tools public reference ({RELEASE})",
        "",
        f"Code revision: `{code_revision}`",
        "",
        "Canonical Pages and immutable raw-source fallbacks:",
        "",
        f"- Exhaustive plain-text reference: {canonical}llms-full.txt (raw: {raw_base}/llms-full.txt)",
    ]
    for label, link_path, raw_path in links:
        compact.append(
            f"- {label}: {canonical}{link_path} "
            f"(raw: {raw_base}/{raw_path})"
        )
    (DOCS_ROOT / "docs/llms.txt").write_text("\n".join(compact) + "\n")

    reference_files = sorted(
        path
        for path in (DOCS_ROOT / "docs/reference").rglob("*.md")
        if "authored" not in path.parts
        and ("generated" not in path.parts or path.name.endswith(".md"))
    )
    full = [
        f"# xp-genomic-tools exhaustive public reference ({RELEASE})",
        "",
        f"Code revision: `{code_revision}`",
        f"Documentation revision: `{docs_revision}`",
        "",
    ]
    for reference_path in reference_files:
        relative = reference_path.relative_to(DOCS_ROOT / "docs").as_posix()
        canonical_relative = relative.removesuffix("/index.md").removesuffix(".md")
        full.extend(
            [
                f"## `{relative}`",
                "",
                reference_path.read_text().strip(),
                "",
                f"Canonical: {canonical}{canonical_relative}/",
                f"Raw: {raw_base}/{relative}",
                "",
            ]
        )
    (DOCS_ROOT / "docs/llms-full.txt").write_text("\n".join(full))


def _extract_parser_reference(code_root: Path) -> dict[str, Any]:
    code_python = code_root / ".venv/bin/python"
    if not code_python.is_file():
        raise RuntimeError(
            f"Missing {code_python}; create code/.venv and install code/pyproject.toml"
        )
    completed = _run(
        [
            str(code_python),
            "scripts/extract_mask_op_reference.py",
            "--code-root",
            str(code_root),
        ]
    )
    return json.loads(completed.stdout)


def _extract_cli_tree(code_root: Path, tool: str) -> list[dict[str, Any]]:
    """Extract a complete parser tree using the selected code environment."""
    code_python = code_root / ".venv/bin/python"
    completed = _run(
        [
            str(code_python),
            "scripts/extract_cli_reference.py",
            "--code-root",
            str(code_root),
            "--tool",
            tool,
        ]
    )
    return json.loads(completed.stdout)


def _render_cli_tree(tool: str, records: list[dict[str, Any]]) -> str:
    inventory = json.dumps(records, sort_keys=True, separators=(",", ":"))
    sections: list[str] = []
    for record in records:
        path = record["path"]
        rows = []
        for argument in record["arguments"]:
            choices = ", ".join(f"`{choice}`" for choice in argument["choices"])
            rows.append(
                "| {flags} | {spellings} | {required} | {nargs} | {value_type} | "
                "{choices} | {default} | {repeatable} | {help_text} |".format(
                    flags=f"`{argument['flags']}`",
                    spellings=", ".join(f"`{flag}`" for flag in argument["spellings"])
                    or "positional",
                    required="yes" if argument["required"] else "no",
                    nargs=f"`{argument['nargs']}`",
                    value_type=f"`{argument['type']}`",
                    choices=choices or "inapplicable",
                    default=f"`{argument['default']}`",
                    repeatable="yes" if argument["repeatable"] else "no",
                    help_text=argument["help"],
                )
            )
        sections.append(
            f"""## `{path}`

### Syntax

```text
{record['usage']}
```

| Flags / positional | Spellings / aliases | Required | Nargs | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}

### Inputs, outputs, and behavior

The parser-derived table above is the authoritative syntax for this command.
Inputs and outputs are paths or values accepted by the listed flags; their
semantic shape, dtype, ordering, side effects, and failure behavior are
defined by the command's public operation and linked format references.
Argparse exits for missing required values and invalid choices; runtime
validation errors propagate from the command implementation.
"""
        )
    return f"""<!-- Generated by scripts/build_release_docs.py; do not edit directly. -->
<!-- Parser inventory: {inventory} -->

# `{tool}` CLI reference

Supported in release `{CLI_RELEASES[tool]}`. This page is generated from the installed
argparse tree and includes every top-level and nested command path.

## Purpose

Complete parser-derived syntax and public flag inventory for `{tool}`.

## Availability

Invoke through the installed `{tool}` console script.

## Commands

{chr(10).join(sections)}
"""


def _parser_inventory_in_page(path: Path) -> str | None:
    if not path.is_file():
        return None
    marker = "<!-- Parser inventory: "
    text = path.read_text()
    if marker not in text:
        return None
    return text.split(marker, 1)[1].split(" -->", 1)[0]


def _reject_stale_parser_inventory(
    generated_path: Path,
    records: list[dict[str, Any]],
    *,
    update_generated: bool,
) -> None:
    if update_generated:
        return
    existing_inventory = _parser_inventory_in_page(generated_path)
    if existing_inventory is None:
        return
    expected_inventory = json.dumps(records, sort_keys=True, separators=(",", ":"))
    if existing_inventory != expected_inventory:
        raise RuntimeError(
            f"{generated_path.relative_to(DOCS_ROOT)} parser inventory is stale; "
            "rerun with --update-generated after accepting parser drift"
        )


def _render_cli_reference(reference: dict[str, Any]) -> str:
    rows = []
    for argument in reference["arguments"]:
        choices = ", ".join(f"`{choice}`" for choice in argument["choices"])
        rows.append(
            "| {flags} | {required} | {value_type} | {choices} | {default} | {repeatable} | {help_text} |".format(
                flags=f"`{argument['flags']}`",
                required="yes" if argument["required"] else "no",
                value_type=f"`{argument['type']}`",
                choices=choices or "inapplicable",
                default=f"`{argument['default']}`",
                repeatable="yes" if argument["repeatable"] else "no",
                help_text=argument["help"],
            )
        )
    table = "\n".join(rows)
    return f"""<!-- Generated by scripts/build_release_docs.py; do not edit directly. -->

# `GenomicElementTools mask_op intersect`

## Purpose

Compute the element-wise logical AND across aligned boolean mask annotations.
This is boolean array algebra, not genomic interval intersection.

## Availability

Supported in `GenomicElementTools` for release `{CLI_RELEASES['GenomicElementTools']}`. Invoke it through the
installed `GenomicElementTools` console script.

## Syntax

This syntax and argument inventory are generated from the released argparse
parser during the documentation acceptance build.

```text
{reference['usage']}
```

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
{table}

Although argparse exposes `bed3` as the `--region_file_type` default, the flag
is required, so omission is an argparse error rather than use of that default.

## Inputs

- `--region_file_path`: a headerless supported BED-like region table. Its row
  count establishes mask length and alignment.
- `--region_file_type`: the region schema key shown in the generated choices.
- `--mask_npy`: a `.npy` array or `.npz` containing exactly one array. Supply
  the flag at least twice.

## Types

Paths and the region type key are strings. Each loaded mask is a NumPy array.

## Shapes

Each mask must have shape `(N,)` or `(N, 1)`, where `N` is the number of region
rows. The saved result has shape `(N, 1)`.

## Dtypes

Every input mask and the output use NumPy boolean dtype. See the
[boolean-mask format](../formats/boolean-mask.md#dtype).

## Defaults

No semantic input or output default applies: all four non-help flags are
required. The parser metadata default for `--region_file_type` is described
under Syntax because the required flag prevents that default from taking effect.

## Choices

`--region_file_type` accepts exactly the parser-derived choices in the table.
The remaining flags have no enumerated choices.

## Constraints

Provide at least two masks. All masks must have boolean dtype, an accepted
shape, and first-dimension alignment with the region table. A single-array NPZ
is accepted; a multi-array NPZ is rejected.

## Outputs

`--opath` receives a NumPy `.npy` boolean mask containing the logical AND of all
inputs. Use a `.npy` suffix; if the supplied path has no suffix, NumPy appends
`.npy`. The filename is not used to select another output format.

## Ordering

Output row `i` corresponds to region row `i`. Input mask order does not change
the result because logical AND is commutative.

## Side effects

Reads the region and mask files and writes or replaces the file at `--opath`
(or `--opath.npy` when NumPy appends the missing suffix). No region table is
modified.

## Failures

Argparse exits for missing required flags or invalid region-type choices. The
command raises `ValueError` for fewer than two masks, non-boolean masks, shape
or region-count mismatches, multi-array NPZ input, or an unsupported region
schema encountered while loading.

## Example

Intersect two boolean masks aligned to the same three-region BED3 table:

```bash
GenomicElementTools mask_op intersect \\
  --region_file_path regions.bed3 \\
  --region_file_type bed3 \\
  --mask_npy mask_a.npy \\
  --mask_npy mask_b.npy \\
  --opath intersect.npy
```

Each input mask has shape `(3,)` or `(3, 1)` with boolean dtype. The saved
`intersect.npy` contains the element-wise logical AND with shape `(3, 1)`.
"""


def _validate_built_artifact(
    site_dir: Path,
    code_root: Path,
    code_revision: str,
    docs_revision: str,
) -> None:
    pages = {
        "python": site_dir / "reference/python/general-elements/load-mask-from-arr/index.html",
        "format": site_dir / "reference/formats/boolean-mask/index.html",
        "cli": site_dir / _site_path(CANONICAL_MASK_INTERSECT.removesuffix(".md")),
        "cli_redirect": site_dir / "reference/cli/mask-op-intersect/index.html",
    }
    for name, path in pages.items():
        if not path.is_file():
            raise RuntimeError(f"Missing built {name} reference: {path}")

    library_path = site_dir / "library/index.html"
    library_html = html.unescape(library_path.read_text())
    library_article = library_html.split("<article", 1)[1].split("</article>", 1)[0]
    library_links = {
        _library_target(href)
        for href in re.findall(r'href="([^"]+)"', library_article)
    }
    expected_python_links = {
        _site_path(page["path"]).removesuffix("index.html")
        for page in _load_python_inventory()["pages"]
        if page.get("kind") != "method"
    }
    missing_library_links = expected_python_links - library_links
    if missing_library_links:
        raise RuntimeError(
            "Built Library page omits declared Python references: "
            + ", ".join(sorted(missing_library_links))
        )

    # Element collections is a class-only grouping: the representative operation
    # page must stay out of the Library article's collection listing.
    method_target = "reference/python/general-elements/load-mask-from-arr/"
    if method_target in library_links:
        raise RuntimeError(
            "The Element collections Library section is class-only; operation "
            "pages such as GeneralElements.load_mask_from_arr must not appear there"
        )

    for name in ("python", "cli"):
        rendered = html.unescape(pages[name].read_text())
        missing = [field for field in REFERENCE_FIELDS if f">{field}<" not in rendered]
        if missing:
            raise RuntimeError(f"Built {name} reference lacks fields: {missing}")

    cli_rendered = html.unescape(pages["cli"].read_text())
    if ">Example<" not in cli_rendered:
        raise RuntimeError(
            "Built canonical mask_op intersect page lacks Example section"
        )

    redirect_rendered = pages["cli_redirect"].read_text()
    if "intersect" not in redirect_rendered:
        raise RuntimeError(
            "Legacy mask-op-intersect URL does not redirect toward intersect"
        )

    for tool in ALL_TOOLS:
        for parser_path in sorted(tool.invocable_paths | tool.group_paths):
            page = site_dir / _site_path(tool.page_for(parser_path).removesuffix(".md"))
            if not page.is_file():
                raise RuntimeError(
                    f"Missing built CLI page for {tool.console_name} {parser_path}: {page}"
                )
            rendered = html.unescape(page.read_text())
            missing = [field for field in REFERENCE_FIELDS if f">{field}<" not in rendered]
            if missing:
                raise RuntimeError(
                    f"Built CLI page {tool.page_for(parser_path)} lacks fields: {missing}"
                )
            if parser_path in tool.invocable_paths and ">Example<" not in rendered:
                raise RuntimeError(
                    f"Built CLI page {tool.page_for(parser_path)} lacks Example section"
                )
            if f">{parser_path.split()[-1]}<" not in rendered and parser_path not in rendered:
                raise RuntimeError(
                    f"Built CLI page {tool.page_for(parser_path)} lacks command symbol"
                )

    genomic_page = site_dir / _site_path(GENOMIC_ELEMENTS_PATH)
    if not genomic_page.is_file():
        raise RuntimeError(f"Missing built GenomicElements page: {genomic_page}")
    genomic_html = html.unescape(genomic_page.read_text())
    if "<article" not in genomic_html:
        raise RuntimeError(f"Built GenomicElements page lacks article body: {genomic_page}")
    genomic_rendered = genomic_html.split("<article", 1)[1].split("</article>", 1)[0]
    genomic_text = re.sub(r"<[^>]+>", " ", genomic_rendered)
    genomic_text = re.sub(r"\s+", " ", genomic_text)
    missing_api = [
        field for field in API_SEMANTIC_FIELDS if f">{field}<" not in genomic_rendered
    ]
    if missing_api:
        raise RuntimeError(
            f"Built GenomicElements page lacks semantic sections: {missing_api}"
        )
    internal_symbols = _load_python_inventory().get("internal_symbols", [])
    for internal in internal_symbols:
        if internal in genomic_text:
            raise RuntimeError(
                f"GenomicElements page exposes internal member {internal!r}"
            )
    if "from RGTools import GenomicElements" not in genomic_text:
        raise RuntimeError("GenomicElements page lacks canonical import")

    for source, target in REDIRECTS.items():
        redirect_html = site_dir / _site_path(source.removesuffix(".md"))
        if not redirect_html.is_file():
            raise RuntimeError(f"Missing redirect page for {source}")
        redirect_content = redirect_html.read_text()
        target_path = target.removesuffix(".md").removesuffix("/index")
        target_slug = Path(target_path).name
        if "Parser inventory" in redirect_content:
            raise RuntimeError(
                f"Redirect source {source} still renders duplicate generated reference"
            )
        if target_slug not in redirect_content and target_path not in redirect_content:
            raise RuntimeError(
                f"Redirect from {source} does not target {target_path}"
            )
        if not re.search(
            r"(window\.location\.replace|http-equiv=.refresh|location\.href)",
            redirect_content,
        ):
            raise RuntimeError(f"Redirect page for {source} lacks redirect mechanism")

    format_html = " ".join(html.unescape(pages["format"].read_text()).split())
    for required in ("numpy.bool_", "Integer masks", "(N, 1)"):
        if required not in format_html:
            raise RuntimeError(f"Boolean-mask artifact lacks {required!r}")

    llms_path = site_dir / "llms.txt"
    full_path = site_dir / "llms-full.txt"
    if not llms_path.is_file() or not full_path.is_file():
        raise RuntimeError("Built artifact lacks llms.txt or llms-full.txt")
    dtype_url = (
        "https://dignomor.github.io/xp-genomic-tools-docs/"
        "reference/formats/boolean-mask/#dtype"
    )
    compact = llms_path.read_text()
    exhaustive = full_path.read_text()
    for marker in (RELEASE, code_revision, "raw.githubusercontent.com"):
        if marker not in compact or marker not in exhaustive:
            raise RuntimeError(f"agent resource lacks release marker {marker!r}")
    for required in ("llms-full.txt", "reference/python", "reference/cli", "reference/formats"):
        if required not in compact:
            raise RuntimeError(f"llms.txt lacks {required!r}")
    if dtype_url not in compact:
        raise RuntimeError("llms.txt does not link directly to the mask dtype rule")

    # Every declared inventory entry must resolve to a complete built page.
    for entry in _load_inventories():
        relative = entry["path"].removeprefix("reference/")
        page = site_dir / _site_path("reference/" + relative)
        if not page.is_file():
            # Inventory paths are source Markdown paths without an extension.
            page = site_dir / _site_path(entry["path"])
        if not page.is_file():
            raise RuntimeError(f"Inventory entry has no built page: {entry['path']}")
        rendered = html.unescape(page.read_text())
        for field in entry.get("required_fields", REFERENCE_FIELDS):
            if field not in rendered:
                raise RuntimeError(f"{entry['path']} lacks field {field}")
        for symbol in entry.get("symbols", entry.get("members", [])):
            if symbol not in rendered:
                raise RuntimeError(f"{entry['path']} lacks symbol {symbol}")
        for format_path in entry.get("formats", []):
            if not (site_dir / _site_path(format_path)).is_file():
                raise RuntimeError(f"Unresolved format reference: {format_path}")
        singular_format = entry.get("format")
        if singular_format and not (site_dir / _site_path(singular_format)).is_file():
            raise RuntimeError(f"Unresolved format reference: {singular_format}")

    # Generated parser snapshots must match the installed code, including all flags.
    for tool, filename in (
        ("GenomicElementTools", "genomic-element-tools.md"),
        ("ExogeneousSequenceTools", "exogeneous-sequence-tools.md"),
        ("MotifTools", "motif-tools.md"),
    ):
        expected = json.dumps(
            _extract_cli_tree(code_root, tool), sort_keys=True, separators=(",", ":")
        )
        generated = (GENERATED_CLI_DIRECTORY / filename).read_text()
        if expected not in generated:
            raise RuntimeError(f"Generated {tool} parser inventory drifted from code")

    for path in (*pages.values(), llms_path, full_path):
        content = path.read_text()
        if PRIVATE_MARKERS.search(content):
            raise RuntimeError(f"Private specification material leaked into {path}")
    for path in site_dir.rglob("*.html"):
        content = path.read_text()
        if PRIVATE_MARKERS.search(content):
            raise RuntimeError(f"Private specification material leaked into {path}")
        for internal in internal_symbols:
            if internal in content:
                raise RuntimeError(
                    f"Built page {path} exposes internal symbol {internal!r}"
                )
    for agent_path in (llms_path, full_path):
        agent_content = agent_path.read_text()
        for internal in internal_symbols:
            if internal in agent_content:
                raise RuntimeError(
                    f"Agent surface {agent_path} exposes internal symbol {internal!r}"
                )

    validate_built_python_api(site_dir, _load_python_inventory())
    cli_inventory = load_site_inventory()
    validate_site_inventory(cli_inventory)
    validate_all_tool_inventories()
    validate_retired_generated_references()
    validate_built_cli_indexes(site_dir, cli_inventory)
    validate_genomic_element_tools_inventory()
    validate_built_tool_landing(
        site_dir, GENOMIC_ELEMENT_TOOLS, load_tool_inventory(GENOMIC_ELEMENT_TOOLS)
    )
    for tool in ALL_TOOLS:
        validate_built_tool_landing_no_generated_links(site_dir, tool)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate parser-derived reference, build strictly, and verify it."
    )
    parser.add_argument("--code-root", type=Path, required=True)
    parser.add_argument("--site-dir", type=Path, required=True)
    parser.add_argument("--code-revision", required=True, help="Exact git revision used to build the release")
    parser.add_argument(
        "--docs-revision",
        required=True,
        help=(
            "Immutable docs git revision used by raw fallbacks; Ticket08 must "
            "rerun this command after committing generated llms resources"
        ),
    )
    parser.add_argument(
        "--raw-source-root",
        type=Path,
        help="Git checkout containing the immutable docs revision (defaults to this checkout)",
    )
    parser.add_argument(
        "--update-generated",
        action="store_true",
        help="Regenerate parser Markdown after intentionally accepting parser drift",
    )
    args = parser.parse_args()

    code_root = args.code_root.resolve()
    actual_code_revision = _git_revision(code_root)
    if actual_code_revision != args.code_revision:
        raise RuntimeError(
            f"Code revision mismatch: expected {args.code_revision}, found {actual_code_revision}"
        )
    if not re.fullmatch(r"[0-9a-f]{40}", args.code_revision):
        raise RuntimeError("--code-revision must be a full 40-character commit SHA")
    if not re.fullmatch(r"[0-9a-f]{40}", args.docs_revision):
        raise RuntimeError("--docs-revision must be a full 40-character commit SHA")
    raw_source_root = (args.raw_source_root or DOCS_ROOT).resolve()
    python_inventory = _load_python_inventory()
    validate_inventory_schema(python_inventory)
    validate_inventory_sources(python_inventory)
    write_generated_indexes(python_inventory)
    cli_inventory = load_site_inventory()
    validate_site_inventory(cli_inventory)
    write_generated_cli_indexes(cli_inventory)
    validate_all_tool_inventories()
    validate_retired_generated_references()
    validate_genomic_element_tools_inventory()
    _validate_source_contracts()
    _validate_raw_source_revision(raw_source_root, args.docs_revision, args.code_revision)
    regenerate_cli_reference()
    GENERATED_CLI_DIRECTORY.mkdir(parents=True, exist_ok=True)
    for tool, filename in (
        ("GenomicElementTools", "genomic-element-tools.md"),
        ("ExogeneousSequenceTools", "exogeneous-sequence-tools.md"),
        ("MotifTools", "motif-tools.md"),
    ):
        records = _extract_cli_tree(code_root, tool)
        generated_path = GENERATED_CLI_DIRECTORY / filename
        _reject_stale_parser_inventory(
            generated_path,
            records,
            update_generated=args.update_generated,
        )
        generated_path.write_text(_render_cli_tree(tool, records))

    _render_agent_resources(args.code_revision, args.docs_revision)

    _run(
        [
            str(DOCS_ROOT / ".venv/bin/mkdocs"),
            "build",
            "--strict",
            "--clean",
            "--site-dir",
            str(args.site_dir.resolve()),
        ]
    )
    _validate_built_artifact(
        args.site_dir.resolve(),
        code_root,
        args.code_revision,
        args.docs_revision,
    )
    print(f"Verified release documentation artifact at {args.site_dir.resolve()}")


if __name__ == "__main__":
    main()
