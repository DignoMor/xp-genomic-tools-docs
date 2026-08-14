# `BedTable3Plus` and `BedTable6Plus`

## Purpose

Represent BED3 or BED6 plus caller-declared columns.

## Availability

Supported in release `0.1.0a2`; canonical imports are `RGTools.BedTable.BedTable3Plus` and `RGTools.BedTable.BedTable6Plus`.

## Inputs

Construct with `extra_column_names`, `extra_column_dtype` (default all `str`), and `enable_sort`. Use inherited BedTable operations and `get_region_extra_column(column_name)`.

## Types

Extra dtypes are Python `int`, `float`, or `str` declarations; names and values are column-aligned.

## Shapes

Each extra column has one value per row.

## Dtypes

Values are forced to the declared extra dtype.

## Defaults

Extra dtype defaults to string; sorting defaults to enabled.

## Choices

BedTable3Plus starts from BED3; BedTable6Plus starts from BED6.

## Constraints

Extra names and dtypes must be declared together and match the loaded schema. Inherited headerless TSV and alignment rules apply.

## Outputs

`get_region_extra_column` returns a NumPy array; inherited selection methods return the matching Plus class.

## Ordering

Inherited lexicographic sorting applies when enabled.

## Side effects

Loads replace contents; reads do not mutate.

## Failures

Schema mismatch raises `BedTableLoadException`; unknown extra columns and invalid dtype declarations fail through the table's validation/conversion path.

## Public members

`BedTable3Plus` and `BedTable6Plus` each expose `column_names`, `column_types`, `extra_column_names`, `extra_column_dtype`, and `get_region_extra_column`, in addition to inherited BedTable operations.
