# `bed3gene` format

## Purpose

Represent BED3 intervals with one caller-provided gene symbol column.

## Availability

Supported in release `0.1.0a2` through the GenomicElements region-type registry.

## Inputs

Headerless tab-separated rows: `chrom`, `start`, `end`, `gene_symbol`.

## Types

Chromosome and `gene_symbol` are strings; coordinates are integers.

## Shapes

Exactly four columns; coordinates are BED `[start,end)`.

## Dtypes

String fields and integer coordinates; missing values write as `.`.

## Defaults

Sorting is lexicographic by `(chrom,start,end)` unless the consuming collection preserves order.

## Choices

The type key is `bed3gene`; no gene ontology is inferred or validated.

## Constraints

The schema defines a column only; gene identifier semantics are not enforced.

## Outputs

Typed Plus-table rows, serialized headerless and tab-separated.

## Ordering

Source order or configured table sort order.

## Side effects

Read/write operations perform file or standard-stream I/O.

## Failures

Schema mismatch raises `BedTableLoadException`; I/O failures propagate.
