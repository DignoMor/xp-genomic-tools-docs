# Formats

Short reference for inputs and outputs used by `RGTools` and the CLIs.

## Region tables (BedTable family)

- Tab-separated, **no header**
- Missing values on disk are encoded as `.`
- Type is declared by a **region type key**, not by the filename suffix

| Type key | Columns (summary) |
| --- | --- |
| `bed3` | `chrom`, `start`, `end` |
| `bed6` | BED3 + `name`, `score`, `strand` |
| `bed3gene` | BED3 + `gene_symbol` |
| `bed6gene` | BED6 + `gene_symbol` |
| `narrowPeak` | BED6 + `signalValue`, `pValue`, `qValue`, `peak` |
| `TREbed` | BED3 + `name`, `fwdTSS`, `revTSS` |
| `bedGraph` | BED3 + `dataValue` |

Coordinates: **0-based, half-open** unless a format is explicitly otherwise
(GTF / Ensembl wire formats use their own conventions and are converted when
needed).

## FASTA

- **Genome FASTA**: chromosome (or contig) records; IDs must match region `chrom`
- **Exogenous FASTA**: one record per sequence; used by
  `ExogeneousSequenceTools` and some export/import paths

## Annotations (`.npy` / `.npz`)

Per-region arrays written beside region tables. Row order must match the region
table order. Used as stats, tracks, or masks depending on the command. Masks
have a stricter representation; see the [boolean mask reference](reference/formats/boolean-mask.md).

## MEME motifs

MEME-format motif text (subset supported by `MemeMotif`). Used by
`motif_search` on both CLIs.

## BigWig

Read-only signal tracks via pyBigWig. Consumed by counting commands
(`count_single_bw`, `count_paired_bw`) and related exports.

## ListFile

One item per line. Used for simple lists (for example importing a stat list into
a region-aligned annotation).
