# `RGTools.BedTable.BedTable6`

## Purpose

Extend BED3 with `name`, `score`, and `strand`.

## Availability

Supported in release `0.1.0a2`; canonical import is `RGTools.BedTable.BedTable6`.

## Inputs

Construct with the same keyword options as BedTable3. In addition to inherited operations, use `get_region_names`, `get_region_scores`, `get_region_strands`, and `load_from_BedTable3`.

## Types

Columns are `chrom` string, `start`/`end` integer, `name` string, `score` float, `strand` string.

## Shapes

Each getter returns one value per row; conversion from BedTable3 preserves row count.

## Dtypes

Scores are floating-point; other types follow BED6 schema.

## Defaults

Sorting defaults to enabled through BedTable3.

## Choices

`load_from_BedTable3` fills added columns with `.`.

## Constraints

All inherited BedTable3 schema, selection, overlap, and I/O constraints apply.

## Outputs

Getter arrays and BedTable6 instances; inherited methods return the concrete class.

## Ordering

Inherited sorting and row alignment apply.

## Side effects

Load methods replace table contents.

## Failures

Inherited `BedTableLoadException`, `ValueError`, and I/O failures apply.

## Public members

`BedTable6`, `column_names`, `column_types`, `get_region_names`, `get_region_scores`, `get_region_strands`, `region_subset`, and `load_from_BedTable3`.
