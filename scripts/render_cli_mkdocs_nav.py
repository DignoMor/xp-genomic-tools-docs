"""Emit Reference → CLI navigation blocks for mkdocs.yml."""

from __future__ import annotations

from cli_page_registry import EXOGENEOUS_SEQUENCE_TOOLS, GENOMIC_ELEMENT_TOOLS, MOTIF_TOOLS, ToolRegistry


def _page_ref(tool: ToolRegistry, parser_path: str) -> str:
    return tool.page_for(parser_path).removeprefix("reference/cli/")


def genomic_nav() -> str:
    tool = GENOMIC_ELEMENT_TOOLS
    lines = [
        "          - GenomicElementTools:",
        "              - Overview: reference/cli/genomic-element-tools/index.md",
        "              - Region and signal:",
    ]
    for path in (
        "bed2tssbed",
        "count_paired_bw",
        "count_single_bw",
        "pad_region",
        "get_context_ge nearest",
        "get_context_ge windowed_argmax",
        "track2tss_bed",
        "select_tss_relative_track",
    ):
        lines.append(f"                  - {path}: reference/cli/{_page_ref(tool, path)}")
    lines.append("              - Sequence and motif:")
    for path in ("onehot", "motif_search", "filter_motif_score", "tss_relative_mutagenesis"):
        lines.append(f"                  - {path}: reference/cli/{_page_ref(tool, path)}")
    for group in ("import", "export", "mask_op", "get_context_ge"):
        lines.append(f"              - {group}:")
        lines.append(f"                  - Overview: reference/cli/{_page_ref(tool, group)}")
        for path in sorted(p for p in tool.invocable_paths if p.startswith(group + " ")):
            lines.append(f"                  - {path}: reference/cli/{_page_ref(tool, path)}")
    return "\n".join(lines)


def exogeneous_nav() -> str:
    tool = EXOGENEOUS_SEQUENCE_TOOLS
    lines = [
        "          - ExogeneousSequenceTools:",
        "              - Overview: reference/cli/exogeneous-sequence-tools/index.md",
    ]
    for group in ("assemble", "gen_track", "track_dim_reduction"):
        lines.append(f"              - {group}:")
        lines.append(f"                  - Overview: reference/cli/{_page_ref(tool, group)}")
        for path in sorted(p for p in tool.invocable_paths if p.startswith(group + " ")):
            lines.append(f"                  - {path}: reference/cli/{_page_ref(tool, path)}")
    for path in ("mutagenesis", "print_stat", "motif_search", "onehot"):
        lines.append(f"              - {path}: reference/cli/{_page_ref(tool, path)}")
    return "\n".join(lines)


def motif_nav() -> str:
    tool = MOTIF_TOOLS
    lines = [
        "          - MotifTools:",
        "              - Overview: reference/cli/motif-tools/index.md",
    ]
    for path in sorted(tool.invocable_paths):
        lines.append(f"              - {path}: reference/cli/{_page_ref(tool, path)}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(genomic_nav())
    print(exogeneous_nav())
    print(motif_nav())
