# Concepts

## Genomic elements vs exogenous sequences

**Genomic elements** are regions on a reference genome. A typical dataset is:

- a region table (BED-like TSV with a declared type key)
- an optional genome FASTA (chromosome IDs must match region `chrom` strings)
- optional per-region annotations (arrays aligned row-for-row with the regions)

**Exogenous sequences** are FASTA sequences that are *not* tied to a reference
genome (for example MPRA inserts or allele-expanded oligo sets). Internally they
are treated as synthetic intervals (`chrom=id`, `start=0`, `end=length`) so the
same annotation machinery can apply.

## Coordinates

Default genomic coordinates are **BED: 0-based, half-open** (`start` inclusive,
`end` exclusive). Use this convention for region tables, sequence slicing, and
BigWig queries.

## Region type keys

Region files are not typed by file extension. You pass an explicit
`--region_file_type` (or equivalent) such as `bed3`, `bed6`, `narrowPeak`, or
`TREbed`. See [Data formats](formats.md).

## Annotations

Annotation files (`.npy` / `.npz`) are **sidecar arrays**. Row `i` of an
annotation corresponds to region `i` in the current region-table order. Region
order is preserved when loading genomic elements so annotations stay aligned.

Common annotation roles:

| Role | Typical use |
| --- | --- |
| **stat** | Per-region scalar or vector summary |
| **track** | Per-base (or dense) signal along each region |
| **mask** | Boolean / logical mask over regions |

## Shared CLI inputs

- **GenomicElementTools** usually takes `--region_file_path`,
  `--region_file_type`, and often `--fasta_path` for the genome.
- **ExogenousSequenceTools** usually takes `--fasta` for the sequence set.

Exact required flags differ by subcommand; use `--help` on the command you are
running.

## TSS-relative regulatory terminology

These terms appear in TREbed workflows, TSS-relative track selection, and
`tss_relative_mutagenesis`. They are distinct concepts:

| Term | Meaning |
| --- | --- |
| **Transcription regulatory element (TRE)** | A named genomic interval modeled with forward and reverse transcription start site (TSS) annotations. In XP Genomic Tools this is usually one row in a TREbed collection. |
| **TREbed** | The six-column region format (`chrom`, `start`, `end`, `name`, `fwdTSS`, `revTSS`) for TRE rows. Format-level readability does not guarantee that a selected TSS is usable for indexing; element-centric commands enforce stricter rules. |
| **TSS-relative coordinate** | A signed, no-zero offset from a selected TSS base: `+1` is the TSS, positive values are downstream, negative values are upstream, and zero is invalid. Selection may emit `0` as a no-match sentinel; mutagenesis rejects it. |
| **Mutation target group** | The cross-round trajectory for one target FASTA record ID. Regions expand across target groups before the first round; all rounds must share the same ID set, joined by ID rather than file order. |
| **Mutation round** | One manifest row: one coordinate stat, one target FASTA, and one strand applied sequentially to every derived sequence. Later rounds see the results of earlier rounds. |
| **Replaced window** | The exact sequence segment removed immediately before a round inserts its target. Optional `replaced/<round_id>.fasta` audit files capture these windows using the same IDs and order as the final output. |

See the [TSS-relative mutagenesis workflow](guides/tss-relative-mutagenesis.md) for
a composed CLI example.
