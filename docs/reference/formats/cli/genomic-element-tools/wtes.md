# WTES FASTA output

## Purpose

Wild-type element sequence library emitted by `GenomicElementTools export WTES`.

## Availability

Supported in the current reference release (`0.3.0a4`).

Available since `0.1.0a2`.

## Inputs

Genome FASTA, ordered GE regions, required positive integer `--num_replicates`,
and output path `--opath`.

## Types

FASTA text with one sequence record per region replicate. Headers are strings;
sequence records contain the extracted nucleotide sequence.

## Shapes

For `N` regions and `R` replicates, output has exactly `N × R` records. Each
replicate of a region has the same sequence and the region's extracted length.

## Dtypes

FASTA sequences are uppercase nucleotide text as returned by RGTools; headers
are text. No NumPy dtype applies.

## Defaults

There is no implicit replicate count; `--num_replicates` is required and must
be at least 1.

## Choices

No format choice applies. Replicate indices are the integers `0` through
`R - 1`.

## Constraints

FASTA record IDs must match region chromosome names, and every region interval
must be valid and readable.

## Outputs

For each input region `chrom:start-end`, records are emitted with headers
`>chrom:start-end_0`, `>chrom:start-end_1`, through `>chrom:start-end_{R-1}`.

## Ordering

Region order is outermost, replicate order innermost: all replicates of region
0 precede all replicates of region 1. Replicate sequences are byte-for-byte
equal for a given region.

## Side effects

Reads genome and region files and creates or replaces the FASTA at `--opath`.

## Failures

`num_replicates < 1` raises `ValueError`; missing chromosomes, invalid regions,
unreadable inputs, and output I/O failures raise the applicable library/I/O
exception.

## Related API and CLI

- [`GenomicElementTools export WTES`](../../../cli/genomic-element-tools/export/wtes.md)
- [FASTA profiles](../../elements/fasta.md)
