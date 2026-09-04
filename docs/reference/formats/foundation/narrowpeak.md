# `narrowPeak` format

## Purpose

Represent a BED6 interval with four peak annotation columns.

## Availability

Supported in the current reference release (`0.4.0a1`).

Available since `0.1.0a2`.

## Inputs

Headerless rows: BED6 followed by `signalValue`, `pValue`, `qValue`, `peak`.

## Types

The first six fields use BED6 types; the three values are floats and `peak` is integer.

## Shapes

Exactly ten columns; coordinates are BED `[start,end)`.

## Dtypes

String, integer, and floating-point columns are forced to the declared schema.

## Defaults

Sorting follows configured BedTable behavior, lexicographically by `(chrom,start,end)` when enabled.

## Choices

The key is `narrowPeak`; ENCODE peak conventions are not separately selected.

## Constraints

This release enforces columns only. It does not validate ENCODE peak semantics or ranges.

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
- [`GenomicElementTools`](../../cli/genomic-element-tools/index.md)
