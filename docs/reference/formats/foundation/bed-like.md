# BED-like region tables

## Purpose

Define the supported tab-separated, headerless region representations used by BedTable and GenomicElements.

## Availability

Supported in the current reference release (`0.3.0a4`).

Available since `0.1.0a2`.

## Inputs

Each row is tab-delimited and must match its declared schema. See the
independent references for [bed3](bed3.md), [bed6](bed6.md),
[bed3gene](bed3gene.md), [bed6gene](bed6gene.md), [narrowPeak](narrowpeak.md),
[TREbed](trebed.md), and [bedGraph](bedgraph.md). Custom ordered extras use a
[version-1 region schema](region-schema.md). The custom paired layout is
documented as [BedTablePairEnd](pair-end.md).

## Types

`bed3`: `chrom` str, `start` int, `end` int. `bed6` adds `name` str, `score`
float, `strand` str. `bed3gene`/`bed6gene` add `gene_symbol` str. `narrowPeak`
adds `signalValue`, `pValue`, `qValue` float and `peak` int. `TREbed` adds
`name` str, `fwdTSS` int, `revTSS` int. `bedGraph` adds `dataValue` float.
Custom schemas declare the same BED3 or BED6 base plus ordered `str` / `int` /
`float` extras.

## Shapes

Rows have exactly the schema's column count; annotation row `i` aligns with
region row `i`.

## Dtypes

Types are forced to the schema types. Missing disk values are `.` and load as
missing values.

## Defaults

Optional sorting is lexicographic by `(chrom,start,end)`; GenomicElements
preserves input order by disabling sorting.

## Choices

Region type keys are names, not filename extensions. `GenomicElements` also
accepts a path to a version-1 region-schema JSON file; predefined names take
precedence over same-named files. On generic `GenomicElementTools` primary
inputs, use mutually exclusive `--region_file_type` (named) or
`--region_file_schema` (JSON path). Standard BEDPE, BED12, and track-header
variants are not supported by this contract.

## Constraints

The contracts define columns only for `narrowPeak`, `TREbed`, and `bedGraph`;
ENCODE peak semantics, TSS base/ordering, and track headers are not validated.
Custom schemas do not acquire named-format semantics merely by reproducing
columns.

## Outputs

Tables serialize as tab-separated rows without a header; missing values write
as `.`. Named and custom `GenomicElements` selectors construct Plus tables.

## Ordering

Input order is retained when sorting is disabled; otherwise lexicographic
chromosome order applies. Derived collections retain declared extras in
declaration order.

## Side effects

Read/write operations perform file or standard-stream I/O. Resolved custom
schemas are snapshotted at collection construction.

## Failures

Wrong column count raises `BedTableLoadException`. Unsupported selectors and
invalid schema JSON raise the caller's unsupported-type or schema error. I/O
failures propagate.

## Related API and CLI

- [Region schema (version 1)](region-schema.md)
- [`BedTable3`](../../python/bedtable/bed-table3.md)
- [`GenomicElements`](../../python/elements/genomic-elements.md)
- [`GenomicElementTools`](../../cli/genomic-element-tools/index.md)
