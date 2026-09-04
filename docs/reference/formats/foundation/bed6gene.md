# `bed6gene` format

## Purpose

Represent BED6 intervals with one caller-provided gene symbol column.

## Availability

Supported in the current reference release (`0.4.0a1`).

Available since `0.1.0a2`.

## Inputs

Headerless tab-separated rows: BED6 fields followed by `gene_symbol`.

## Types

Chromosome/name/strand/gene symbol are strings; coordinates are integers; score is float.

## Shapes

Exactly seven columns; coordinates are BED `[start,end)`.

## Dtypes

Columns are converted to the declared string, integer, and floating-point types.

## Defaults

Sorting is lexicographic by `(chrom,start,end)` unless disabled by the consumer.

## Choices

The type key is `bed6gene`; gene identifier semantics are not enforced.

## Constraints

The schema does not validate an external gene ontology or BED6 score range.

## Outputs

Typed Plus-table rows, serialized headerless and tab-separated.

## Ordering

Source order or configured table sort order.

## Side effects

Read/write operations perform file or standard-stream I/O.

## Failures

Schema mismatch raises `BedTableLoadException`; conversion and I/O failures propagate.

## Related API and CLI

- [`GenomicElements`](../../python/elements/genomic-elements.md)
- [`GenomicElementTools`](../../cli/genomic-element-tools/index.md)
