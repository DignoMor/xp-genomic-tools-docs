# FASTA profiles

## Purpose

Sequence interchange for genome-anchored (`GenomicElements`) and exogenous
(`ExogenousSequences`) collections, plus exported region FASTA.

## Availability

Supported in the current reference release (`0.4.0a1`).

Available since `0.1.0a2`.

## Inputs

Multi-FASTA files. Genome record IDs must match region `chrom` strings exactly.
Exogenous records use standard `>id` headers with sequence text. BED extraction
uses 0-based, half-open `[start,end)` coordinates.

## Types

Record IDs and sequences are strings; coordinates are integers.

## Shapes

One sequence per record. Genome extraction length is `end - start`. Exogenous
synthetic regions are BED3 `(id, 0, len)`.

## Dtypes

Sequence text has no NumPy dtype; coordinates are integer.

## Defaults

Start inclusive, end exclusive. No alphabet normalization or line-wrapping promise.

## Choices

Genome FASTA, exogenous FASTA, or exported-region FASTA profiles.

## Constraints

Genome record IDs must match `chrom` exactly. Annotation row `i` aligns with
FASTA record `i`. Genomic export defaults to `chrom:start-end` headers and may
optionally use row-level names; selected IDs must be unique. Sequences default
to genomic-forward orientation and may optionally use region-strand orientation
when the region schema exposes strand. Export refuses overwrite of an existing
path. Every exported genomic interval must satisfy BED half-open containment
`0 <= start < end <= chromosome_length`.

## Outputs

String slices, synthetic BED3 regions, or FASTA files on disk.

## Ordering

Source FASTA order; region-table order for genomic extraction.

## Side effects

Indexing reads FASTA; writers create files; export refuses existing destinations
and does not create or replace a destination when any interval fails validation.

## Failures

Missing chromosomes return `None` for single-region getters and raise during bulk
extraction or export. Genomic export also raises when an interval has
`start < 0`, `start >= end`, or `end` beyond the chromosome length. Malformed
FASTA and existing export paths fail as stated in the governing APIs.

## Genome FASTA profile

Sequence source for `GenomicElements`. Genome FASTA is read/indexed, not written
by this API.

## Exogenous and exported FASTA profile

`ExogenousSequences` reads all records in file order and exposes synthetic
BED3 `(id,0,len)` regions. `write_sequences_to_fasta` and genomic export write
standard `>id` records.

## Related API and CLI

- [`GenomicElements`](../../python/elements/genomic-elements.md)
- [`ExogenousSequences`](../../python/elements/exogenous-sequences.md)
- [`GenomicElementTools`](../../cli/genomic-element-tools/index.md)
- [`ExogenousSequenceTools`](../../cli/exogenous-sequence-tools/index.md)
