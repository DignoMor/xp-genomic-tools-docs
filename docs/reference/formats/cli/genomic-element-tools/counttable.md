# CountTable output

## Purpose

Reusable CSV output from `GenomicElementTools export CountTable`.

## Availability

Supported in release `0.1.0a2`. A separate count-table CLI is not shipped.

## Inputs

An ordered GE region table and parallel sample names and stat-array paths.

## Types

CSV text; region identifiers and sample names are strings; sample values are
numeric statistics.

## Shapes

There are `N` data rows, one per region, and one statistic column per sample,
plus the selected region identifier column.

## Dtypes

Input statistics must be numeric and have one value per region. Serialized
values are parsed as numeric CSV fields.

## Defaults

No output delimiter or float-format default is a compatibility guarantee;
`--opath` is the required output path.

## Choices

`--region_id_type` is `default` or `gene_symbol`.

## Constraints

All sample/stat parallel lists must have equal length, and every stat array
must align to the same `N` regions.

## Outputs

A header row identifying samples and `N` data rows are written to `--opath`.

## Ordering

Rows retain GE region order; columns follow supplied sample order.

## Side effects

Reads region/stat files and creates or replaces the CSV at `--opath`.

## Failures

Parallel-list, identifier, alignment, numeric conversion, and file errors fail
with parser, `ValueError`, or I/O errors as applicable.
