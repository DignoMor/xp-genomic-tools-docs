# `BedTablePairEnd` format

!!! warning "Experimental"
    This custom paired-interval layout is experimental and distinct from standard BEDPE. It may change or be removed without a deprecation period when disclosed in release notes.

## Purpose

Represent two linked intervals and pair metadata in one headerless TSV row.

## Availability

Experimental.
Supported in the current reference release (`0.3.0a4`).

Available since `0.1.0a2`.

## Inputs

Rows contain `chrom,start,end,chrom2,start2,end2,name,score,strand,strand2`, followed by optional extras.

## Types

Chromosomes, name, and strands are strings; coordinates are integers; score is float; extras use caller-declared types.

## Shapes

At least ten columns per row; both intervals use BED `[start,end)` coordinates.

## Dtypes

Columns are forced to the declared schema and extras to their configured dtypes.

## Defaults

Sorting is always enabled by first-mate `(chrom,start,end)`.

## Choices

This is a custom layout, explicitly **not BEDPE**.

## Constraints

The second-mate inverse index is rebuilt after loads; no standard BEDPE interoperability is promised.

## Outputs

Paired table rows serialize as headerless tab-separated text; missing values write as `.`.

## Ordering

Rows are sorted by the first mate.

## Side effects

Loads replace rows and rebuild the inverse index; writes perform file or standard-stream I/O.

## Failures

Schema mismatch raises `BedTableLoadException`; conversion and I/O failures propagate.

## Related API and CLI

- [`BedTablePairEnd`](../../python/bedtable/bed-table-pair-end.md) (experimental)
