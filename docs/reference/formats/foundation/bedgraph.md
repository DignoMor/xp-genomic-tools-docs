# `bedGraph` format

## Purpose

Represent a BED3 interval with one numeric `dataValue` signal column.

## Availability

Supported in release `0.1.0a2` as a GenomicElements region type.

## Inputs

Headerless rows: `chrom`, `start`, `end`, `dataValue`.

## Types

Chromosome is string; coordinates are integers; `dataValue` is float.

## Shapes

Exactly four columns; coordinates are BED `[start,end)`.

## Dtypes

String, integer, and floating-point columns are forced to the declared schema.

## Defaults

Sorting follows configured BedTable behavior, lexicographically by `(chrom,start,end)` when enabled.

## Choices

The key is `bedGraph`; track headers are not part of this profile.

## Constraints

This contract documents columns only and does not add bedGraph track-header semantics.

## Outputs

Typed Plus-table rows; output is headerless tab-separated text with missing values as `.`.

## Ordering

Source order or configured table sort order.

## Side effects

Read/write operations perform file or standard-stream I/O.

## Failures

Schema mismatch raises `BedTableLoadException`; conversion and I/O failures propagate.
