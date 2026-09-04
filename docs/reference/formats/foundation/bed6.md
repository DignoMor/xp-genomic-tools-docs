# `bed6` format

## Purpose

Represent intervals with BED3 coordinates plus name, score, and strand.

## Availability

Supported in the current reference release (`0.4.0a1`).

Available since `0.1.0a2`.

## Inputs

Headerless tab-separated rows: `chrom`, `start`, `end`, `name`, `score`, `strand`.

## Types

Chromosome/name/strand are strings; coordinates are integers; score is float.

## Shapes

Exactly six columns per row; coordinates are `[start,end)`.

## Dtypes

Columns are converted to the declared string, integer, and floating-point types.

## Defaults

BedTable sorting is lexicographic by `(chrom,start,end)` when enabled.

## Choices

The type key is `bed6`; strand values are carried as strings and are not semantically restricted by this format loader.

## Constraints

No header is permitted; missing values are represented by `.` on disk.

## Outputs

BED6 tables serialize as tab-separated rows without a header.

## Ordering

Rows follow source order or configured table sorting.

## Side effects

Read/write operations perform file or standard-stream I/O.

## Failures

Wrong column count raises `BedTableLoadException`; conversion and I/O failures propagate.

## Related API and CLI

- [`BedTable6`](../../python/bedtable/bed-table6.md)
- [`GenomicElements`](../../python/elements/genomic-elements.md)
- [`GenomicElementTools`](../../cli/genomic-element-tools/index.md)
