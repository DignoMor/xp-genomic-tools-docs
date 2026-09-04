"""Parser-path to canonical CLI reference page registry."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


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


def token_to_kebab(token: str) -> str:
    if token == token.lower():
        return token.replace("_", "-")
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", token)
    return spaced.lower().replace("_", "-")


def parser_path_to_slug(parser_path: str) -> str:
    if parser_path == "(root)":
        return "index"
    return "/".join(token_to_kebab(part) for part in parser_path.split())


def parser_path_to_page(tool_slug: str, parser_path: str) -> str:
    slug = parser_path_to_slug(parser_path)
    if slug == "index":
        return f"reference/cli/{tool_slug}/index.md"
    return f"reference/cli/{tool_slug}/{slug}.md"


@dataclass(frozen=True)
class IntentGroup:
    title: str
    paths: tuple[str, ...]
    group_path: str | None = None


@dataclass(frozen=True)
class ToolRegistry:
    console_name: str
    slug: str
    group_paths: frozenset[str]
    invocable_paths: frozenset[str]
    intent_groups: tuple[IntentGroup, ...] = field(default_factory=tuple)

    @property
    def documented_paths(self) -> frozenset[str]:
        return frozenset({"(root)"}) | self.group_paths | self.invocable_paths

    def page_for(self, parser_path: str) -> str:
        return parser_path_to_page(self.slug, parser_path)

    def authored_path(self, parser_path: str) -> str:
        slug = parser_path_to_slug(parser_path)
        if slug == "index":
            return f"docs/reference/cli/authored/{self.slug}/_landing.md"
        return f"docs/reference/cli/authored/{self.slug}/{slug}.md"


GENOMIC_ELEMENT_INTENT_GROUPS: tuple[IntentGroup, ...] = (
    IntentGroup(
        title="Region and signal",
        paths=(
            "bed2tssbed",
            "count_paired_bw",
            "count_single_bw",
            "pad_region",
            "get_context_ge nearest",
            "get_context_ge windowed_argmax",
            "track2tss_bed",
            "select_tss_relative_track",
        ),
    ),
    IntentGroup(
        title="Sequence and motif",
        paths=(
            "onehot",
            "motif_search",
            "filter_motif_score",
            "tss_relative_mutagenesis",
        ),
    ),
    IntentGroup(
        title="import",
        group_path="import",
        paths=("import stat_list", "import allele_expanded_ES"),
    ),
    IntentGroup(
        title="export",
        group_path="export",
        paths=(
            "export ChromFilteredGE",
            "export CountTable",
            "export ExogenousSequences",
            "export Heatmap",
            "export MaskedGE",
            "export MergedGE",
            "export TREbed",
            "export WTES",
            "export allele_expanded_ES",
            "export bed6poly",
            "export stat_list",
        ),
    ),
    IntentGroup(
        title="mask_op",
        group_path="mask_op",
        paths=("mask_op intersect", "mask_op opposite", "mask_op union"),
    ),
    IntentGroup(
        title="get_context_ge",
        group_path="get_context_ge",
        paths=("get_context_ge nearest", "get_context_ge windowed_argmax"),
    ),
)

GENOMIC_ELEMENT_TOOLS = ToolRegistry(
    console_name="GenomicElementTools",
    slug="genomic-element-tools",
    group_paths=frozenset({"export", "import", "mask_op", "get_context_ge"}),
    invocable_paths=frozenset(
        {
            "bed2tssbed",
            "count_paired_bw",
            "count_single_bw",
            "pad_region",
            "onehot",
            "motif_search",
            "track2tss_bed",
            "filter_motif_score",
            "select_tss_relative_track",
            "tss_relative_mutagenesis",
            "get_context_ge nearest",
            "get_context_ge windowed_argmax",
            "mask_op intersect",
            "mask_op union",
            "mask_op opposite",
            "import stat_list",
            "import allele_expanded_ES",
            "export stat_list",
            "export ExogenousSequences",
            "export WTES",
            "export allele_expanded_ES",
            "export CountTable",
            "export Heatmap",
            "export ChromFilteredGE",
            "export MaskedGE",
            "export TREbed",
            "export MergedGE",
            "export bed6poly",
        }
    ),
    intent_groups=GENOMIC_ELEMENT_INTENT_GROUPS,
)

EXOGENOUS_SEQUENCE_TOOLS = ToolRegistry(
    console_name="ExogenousSequenceTools",
    slug="exogenous-sequence-tools",
    group_paths=frozenset({"assemble", "track_dim_reduction", "gen_track"}),
    invocable_paths=frozenset(
        {
            "assemble add_adapter",
            "assemble concat",
            "assemble barcode",
            "mutagenesis",
            "gen_track single_loc",
            "track_dim_reduction max",
            "track_dim_reduction argmax",
            "track_dim_reduction min",
            "track_dim_reduction argmin",
            "print_stat",
            "motif_search",
            "onehot",
        }
    ),
)

MOTIF_TOOLS = ToolRegistry(
    console_name="MotifTools",
    slug="motif-tools",
    group_paths=frozenset(),
    invocable_paths=frozenset({"anti_motif", "random_seq", "pwm_seq", "barcodes"}),
)

ALL_TOOLS: tuple[ToolRegistry, ...] = (
    GENOMIC_ELEMENT_TOOLS,
    EXOGENOUS_SEQUENCE_TOOLS,
    MOTIF_TOOLS,
)

REDIRECTS = {
    "reference/cli/generated/genomic-element-tools.md": "reference/cli/genomic-element-tools/index.md",
    "reference/cli/generated/exogenous-sequence-tools.md": "reference/cli/exogenous-sequence-tools/index.md",
    "reference/cli/generated/motif-tools.md": "reference/cli/motif-tools/index.md",
    "reference/cli/mask-op-intersect.md": "reference/cli/genomic-element-tools/mask-op/intersect.md",
    "cli/index.md": "reference/cli/index.md",
    "cli/GenomicElementTools.md": "reference/cli/genomic-element-tools/index.md",
    "cli/ExogenousSequenceTools.md": "reference/cli/exogenous-sequence-tools/index.md",
    "cli/MotifTools.md": "reference/cli/motif-tools/index.md",
}


def invocable_paths_from_records(records: list[dict]) -> set[str]:
    paths = {record["path"] for record in records}
    groups = {
        record["path"]
        for record in records
        if record["path"] != "(root)"
        and any(
            other.startswith(record["path"] + " ")
            for other in paths
        )
    }
    return {path for path in paths if path != "(root)" and path not in groups}


def validate_registry_against_records(tool: ToolRegistry, records: list[dict]) -> None:
    discovered = invocable_paths_from_records(records)
    paths = {record["path"] for record in records}
    groups = {
        record["path"]
        for record in records
        if record["path"] != "(root)"
        and any(other.startswith(record["path"] + " ") for other in paths)
    }
    if discovered != tool.invocable_paths:
        raise RuntimeError(
            f"{tool.console_name} invocable drift: "
            f"missing={sorted(tool.invocable_paths - discovered)} "
            f"extra={sorted(discovered - tool.invocable_paths)}"
        )
    if groups != tool.group_paths:
        raise RuntimeError(
            f"{tool.console_name} group drift: "
            f"missing={sorted(tool.group_paths - groups)} "
            f"extra={sorted(groups - tool.group_paths)}"
        )
