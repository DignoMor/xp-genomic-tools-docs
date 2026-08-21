from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse


DOCS_ROOT = Path(__file__).resolve().parents[1]
GENERATED_REFERENCE = DOCS_ROOT / "docs/reference/cli/mask-op-intersect.md"
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
RELEASE = "0.1.0a2"
PAGES_BASE = "https://dignomor.github.io/xp-genomic-tools-docs/"
DOCS_RAW_BASE = "https://raw.githubusercontent.com/DignoMor/xp-genomic-tools-docs"
PRIVATE_MARKERS = re.compile(
    r"(?:/specs/|delivery-specs?|pipeline[-_ ]contracts?|\.scratch/|private/|\bSPEC\d{3}\b)",
    re.IGNORECASE,
)


def _library_target(href: str) -> str:
    return urlparse(urljoin("https://docs.invalid/library/", href)).path.lstrip("/")


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


def _load_inventories() -> list[dict[str, Any]]:
    inventories = [
        DOCS_ROOT / "docs/reference/python/elements/inventory.json",
        DOCS_ROOT / "docs/reference/foundation-bedtable-inventory.json",
        DOCS_ROOT / "tests/ticket04_reference_inventory.json",
        DOCS_ROOT / "tests/ticket05_reference_inventory.json",
        DOCS_ROOT / "tests/ticket06_reference_inventory.json",
        DOCS_ROOT / "tests/ticket07_motif_tools_reference_inventory.json",
    ]
    entries: list[dict[str, Any]] = []
    for inventory_path in inventories:
        payload = json.loads(inventory_path.read_text())
        entries.extend(payload.get("entries", []))
        for format_name in payload.get("formats", []):
            format_paths = {
                "fasta": "reference/formats/elements/fasta",
                "annotation-arrays": "reference/formats/elements/annotation-arrays",
                "meme": "reference/formats/motifs/meme",
            }
            if format_name in format_paths:
                entries.append({"path": format_paths[format_name], "symbols": [format_name]})
        for qualified_name, members in payload.get("classes", {}).items():
            class_path = (
                "reference/python/motifs/meme-motif"
                if qualified_name == "MemeMotif"
                else "reference/python/elements/index"
            )
            entries.append(
                {
                    "path": class_path,
                    "symbols": [qualified_name, *members],
                }
            )
    return entries


def _render_agent_resources(code_revision: str, docs_revision: str) -> None:
    raw_base = f"{DOCS_RAW_BASE}/{docs_revision}/docs"
    canonical = PAGES_BASE
    links = [
        ("Reference conventions", "reference/conventions/", "reference/conventions.md"),
        ("Python reference", "reference/python/elements/", "reference/python/elements/index.md"),
        ("BedTable reference", "reference/python/bedtable/bed-table3/", "reference/python/bedtable/bed-table3.md"),
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
        if "generated" not in path.parts or path.name.endswith(".md")
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

Supported in release `0.1.0a2`. This page is generated from the installed
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

Supported in `GenomicElementTools` for release `0.1.0a2`. Invoke it through the
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
"""


def _validate_built_artifact(
    site_dir: Path, code_root: Path, code_revision: str, docs_revision: str
) -> None:
    pages = {
        "python": site_dir / "reference/python/general-elements/load-mask-from-arr/index.html",
        "format": site_dir / "reference/formats/boolean-mask/index.html",
        "cli": site_dir / "reference/cli/mask-op-intersect/index.html",
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
        _site_path(entry["path"]).removesuffix("index.html")
        for entry in _load_inventories()
        if entry["path"].startswith("reference/python/")
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

    navigation = NavigationAncestryParser()
    navigation.feed(library_html)
    method_ancestors = navigation.ancestors[method_target]
    if not method_ancestors:
        raise RuntimeError(
            "GeneralElements.load_mask_from_arr must remain reachable in built "
            "navigation"
        )
    # Class/reference-area groupings list types, not operations. The operation
    # page belongs only under the explicit Operations grouping.
    for groups in method_ancestors:
        if "Element collections" in groups:
            raise RuntimeError(
                "GeneralElements.load_mask_from_arr must not occupy the "
                "class-only Element collections navigation group"
            )
        if not groups or groups[-1] != "Operations":
            raise RuntimeError(
                "GeneralElements.load_mask_from_arr must appear under the "
                "explicit Operations grouping, not as a peer of classes, "
                "modules, or reference areas"
            )
    method_titles = navigation.titles[method_target]
    if not method_titles or any("()" not in title for title in method_titles):
        raise RuntimeError(
            "GeneralElements.load_mask_from_arr must be presented as a method "
            "in built navigation"
        )

    for name in ("python", "cli"):
        rendered = html.unescape(pages[name].read_text())
        missing = [field for field in REFERENCE_FIELDS if f">{field}<" not in rendered]
        if missing:
            raise RuntimeError(f"Built {name} reference lacks fields: {missing}")

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
        expected = _extract_cli_tree(code_root, tool)
        generated = (DOCS_ROOT / "docs/reference/cli/generated" / filename).read_text()
        if json.dumps(expected, sort_keys=True, separators=(",", ":")) not in generated:
            raise RuntimeError(f"Generated {tool} parser inventory drifted from code")

    for path in (*pages.values(), llms_path, full_path):
        content = path.read_text()
        if PRIVATE_MARKERS.search(content):
            raise RuntimeError(f"Private specification material leaked into {path}")
    for path in site_dir.rglob("*.html"):
        content = path.read_text()
        if PRIVATE_MARKERS.search(content):
            raise RuntimeError(f"Private specification material leaked into {path}")


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
    _validate_raw_source_revision(raw_source_root, args.docs_revision, args.code_revision)
    reference = _extract_parser_reference(code_root)
    GENERATED_REFERENCE.parent.mkdir(parents=True, exist_ok=True)
    GENERATED_REFERENCE.write_text(_render_cli_reference(reference))
    GENERATED_CLI_DIRECTORY.mkdir(parents=True, exist_ok=True)
    for tool, filename in (
        ("GenomicElementTools", "genomic-element-tools.md"),
        ("ExogeneousSequenceTools", "exogeneous-sequence-tools.md"),
        ("MotifTools", "motif-tools.md"),
    ):
        records = _extract_cli_tree(code_root, tool)
        generated_path = GENERATED_CLI_DIRECTORY / filename
        expected_inventory = json.dumps(records, sort_keys=True, separators=(",", ":"))
        existing_inventory = _parser_inventory_in_page(generated_path)
        if existing_inventory is not None and existing_inventory != expected_inventory and not args.update_generated:
            raise RuntimeError(
                f"{filename} is stale; rerun with --update-generated, review, and rerun acceptance"
            )
        if existing_inventory is None and generated_path.exists() and not args.update_generated:
            raise RuntimeError(f"{filename} lacks a parser inventory; rerun with --update-generated")
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
    _validate_built_artifact(args.site_dir.resolve(), code_root, args.code_revision, args.docs_revision)
    print(f"Verified release documentation artifact at {args.site_dir.resolve()}")


if __name__ == "__main__":
    main()
