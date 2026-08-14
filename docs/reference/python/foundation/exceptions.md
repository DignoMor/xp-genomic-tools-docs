# RGTools exceptions

## Purpose

Stable exception classes for foundation, GTF, and BedTable failures.

## Availability

Supported in release `0.1.0a2`; import from `RGTools.exceptions`.

## Inputs

Exception constructors accept optional message arguments, following Python's standard `Exception` convention.

## Types

`RGToolsInternalException` is the base. `GTFHandleFilterException`, `GTFRecordNoFeatureException`, and `BedTableException` derive from it. `BedTableLoadException`, `InvalidBedRegionException`, and `InvalidStrandnessException` derive from `BedTableException`.

## Shapes

Not applicable.

## Dtypes

Not applicable.

## Defaults

No message is required.

## Choices

Use the most specific class exposed by the operation.

## Constraints

These classes describe failure categories; exact human-readable messages are not compatibility guarantees.

## Outputs

An exception object carrying the supplied arguments.

## Ordering

Not applicable.

## Side effects

None.

## Failures

`BedTableLoadException` indicates schema or load-shape failure; `InvalidBedRegionException` indicates invalid padded coordinates; `InvalidStrandnessException` indicates missing or invalid strandness.

## Public members

`RGToolsInternalException`, `GTFHandleFilterException`, `GTFRecordNoFeatureException`, `BedTableException`, `BedTableLoadException`, `InvalidBedRegionException`, and `InvalidStrandnessException`.
