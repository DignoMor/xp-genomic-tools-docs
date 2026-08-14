# `bed3` format

## Purpose

Represent one genomic interval with the BED3 schema.

## Availability

Supported in release `0.1.0a2` as the canonical `BedTable3` region type.

## Inputs

Headerless tab-separated rows with `chrom`, `start`, and `end`.

## Types

`chrom`: string; `start`, `end`: integer.

## Shapes

Exactly three columns per row; coordinates are `[start,end)`.

## Dtypes

String chromosome and integer coordinates; missing disk values are `.`.

## Defaults

BedTable sorting is lexicographic by `(chrom,start,end)` when enabled.

## Choices

The type key is `bed3`, not a filename extension.

## Constraints

No header is permitted; row order is preserved when sorting is disabled.

## Outputs

BED3 tables serialize as tab-separated rows without a header.

## Ordering

Rows follow source order or the table's configured sort order.

## Side effects

Read/write operations perform file or standard-stream I/O.

## Failures

Wrong column count raises `BedTableLoadException`; I/O failures propagate.
