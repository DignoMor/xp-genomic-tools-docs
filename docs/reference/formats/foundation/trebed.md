# `TREbed` format

## Purpose

Represent a BED3 interval with a name and forward/reverse TSS columns using the
PINTS-compatible six-column TSS-annotated BED serialization.

## Availability

Supported in the current reference release (`0.3.0a4`).

Available since `0.3.0a3`.

## Inputs

Headerless rows: `chrom`, `start`, `end`, `name`, `fwdTSS`, `revTSS`.

## Types

Chromosome/name are strings; interval and TSS coordinates are integers.

## Shapes

Exactly six columns; interval coordinates use BED `[start,end)`.

## Dtypes

String and integer columns are forced to the declared schema.

## Defaults

Sorting follows configured BedTable behavior, lexicographically by `(chrom,start,end)` when enabled.

## Choices

The key is `TREbed`.

## Constraints

- Each of `fwdTSS` and `revTSS` is either `-1` (missing TSS on that strand) or a
  nonnegative genomic position.
- Equal forward and reverse TSS values, and both fields missing, are readable.
- Format-level readability is not operation-level indexability: the format
  reader does not require a nonmissing TSS to lie inside `[start,end)`.
  Operations that index from a selected TSS (for example
  `GenomicElementTools select_tss_relative_track` and
  `GenomicElementTools tss_relative_mutagenesis`) enforce interval membership
  and complete scored-window availability themselves.

## Outputs

Typed Plus-table rows; output is headerless tab-separated text with missing values as `.`.

## Ordering

Source order or configured table sort order.

## Side effects

Read/write operations perform file or standard-stream I/O.

## Failures

Schema mismatch raises `BedTableLoadException`; conversion and I/O failures propagate.

## Related API and CLI

- [`GenomicElements`](../../python/elements/genomic-elements.md)
- [`GenomicElementTools select_tss_relative_track`](../../cli/genomic-element-tools/select-tss-relative-track.md)
- [`GenomicElementTools tss_relative_mutagenesis`](../../cli/genomic-element-tools/tss-relative-mutagenesis.md)
