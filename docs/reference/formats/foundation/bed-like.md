# BED-like region tables

## Purpose

Define the supported tab-separated, headerless region representations used by BedTable and GenomicElements.

## Availability

Supported in release `0.1.0a2`; coordinates are BED 0-based, half-open `[start,end)`.

## Inputs

Each row is tab-delimited and must match its declared schema. See the independent references for [bed3](bed3.md), [bed6](bed6.md), [bed3gene](bed3gene.md), [bed6gene](bed6gene.md), [narrowPeak](narrowpeak.md), [TREbed](trebed.md), and [bedGraph](bedgraph.md). The custom paired layout is documented as [BedTablePairEnd](pair-end.md).

## Types

`bed3`: `chrom` str, `start` int, `end` int. `bed6` adds `name` str, `score` float, `strand` str. `bed3gene`/`bed6gene` add `gene_symbol` str. `narrowPeak` adds `signalValue`, `pValue`, `qValue` float and `peak` int. `TREbed` adds `name` str, `fwdTSS` int, `revTSS` int. `bedGraph` adds `dataValue` float.

## Shapes

Rows have exactly the schema's column count; annotation row `i` aligns with region row `i`.

## Dtypes

Types are forced to the schema types. Missing disk values are `.` and load as missing values.

## Defaults

Optional sorting is lexicographic by `(chrom,start,end)`; GenomicElements preserves input order by disabling sorting.

## Choices

Region type keys are names, not filename extensions. Standard BEDPE, BED12, and track-header variants are not supported by this contract.

## Constraints

The contracts define columns only for `narrowPeak`, `TREbed`, and `bedGraph`; ENCODE peak semantics, TSS base/ordering, and track headers are not validated.

## Outputs

Tables serialize as tab-separated rows without a header; missing values write as `.`.

## Ordering

Input order is retained when sorting is disabled; otherwise lexicographic chromosome order applies.

## Side effects

Read/write operations perform file or standard-stream I/O.

## Failures

Wrong column count or unsupported type key raises `BedTableLoadException` or the caller's unsupported-type error. I/O failures propagate.
