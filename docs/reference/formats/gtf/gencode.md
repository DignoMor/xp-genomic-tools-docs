# GENCODE-oriented GTF profile

## Purpose

Describe the supported annotation input consumed by `RGTools.GTF_utils`.

## Availability

Supported in release `0.1.0a2` as a read-only, GENCODE-oriented nine-column
GTF profile.

## Inputs

Tab-separated records with the nine standard GTF columns and an attributes
column. Leading `#` comments and blank lines are accepted.

## Types

The `start` and `end` columns are integers; other fixed columns and parsed
attribute values are strings. Attributes use `key "value";` pairs.

## Shapes

Exactly nine tab-separated fields per record.

## Dtypes

Inapplicable beyond integer coordinates.

## Defaults

No writer or coordinate-conversion default exists; records retain source
coordinates.

## Choices

The strand field must be `+` or `-`.

## Constraints

Coordinates remain 1-based closed GTF integers. GFF3, arbitrary attribute
dialects, and automatic BED conversion are outside this supported profile.

## Outputs

Parsed `GTFRecord` values and collected comments.

## Ordering

Source record order is preserved.

## Side effects

Read-only file access.

## Failures

Invalid strand raises `RGToolsInternalException`; malformed records or
unsupported attribute syntax may raise parsing errors.
