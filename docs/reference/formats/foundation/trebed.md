# `TREbed` format

## Purpose

Represent a BED3 interval with a name and forward/reverse TSS columns.

## Availability

Supported in release `0.1.0a2` as a GenomicElements region type.

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

This release specifies the columns only; the TSS coordinate base, ordering, and relationship to the interval remain unspecified and are not validated.

## Outputs

Typed Plus-table rows; output is headerless tab-separated text with missing values as `.`.

## Ordering

Source order or configured table sort order.

## Side effects

Read/write operations perform file or standard-stream I/O.

## Failures

Schema mismatch raises `BedTableLoadException`; conversion and I/O failures propagate.
