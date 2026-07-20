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
`TREbed`. See [Formats](formats.md).

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
- **ExogeneousSequenceTools** usually takes `--fasta` for the sequence set.

Exact required flags differ by subcommand; use `--help` on the command you are
running.
