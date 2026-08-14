# `RGTools.BedTable.BedTableIterator`

## Purpose

Iterate over a BedTable as `BedRegion` values.

## Availability

Supported in release `0.1.0a2`; canonical import is `RGTools.BedTable.BedTableIterator`.

## Inputs

Construct with a BedTable instance.

## Types

The iterator yields `BedRegion` objects.

## Shapes

Yields one value per table row.

## Dtypes

Yielded field types follow the table schema.

## Defaults

Starts at row zero.

## Choices

None.

## Constraints

Iteration follows the table's current row order.

## Outputs

`__iter__` returns the iterator; `__next__` returns the next region.

## Ordering

Stable current table order.

## Side effects

Advances iterator state.

## Failures

`StopIteration` signals exhaustion.
