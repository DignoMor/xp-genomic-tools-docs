# GENCODE-oriented GTF profile

## Purpose

Describe the supported annotation input consumed by `RGTools.GTF_utils`.

## Availability

Supported in the current reference release (`0.3.0a4`).

Available since `0.1.0a2`.

## Inputs

Tab-separated GTF records with nine standard columns plus an attributes field.
Leading `#` comment lines and blank lines are accepted. This profile is oriented
to GENCODE-style nine-column GTF; GFF3 and arbitrary dialects are out of scope.

## Types

`start` and `end` columns are integers stored as GTF 1-based closed coordinates.
Other fixed columns and parsed attribute values are strings. Attributes use
`key "value";` pairs.

## Shapes

Exactly nine tab-separated fields per record.

## Dtypes

Beyond integer coordinates, values remain Python scalar strings or integers in
parsed records.

## Defaults

No writer or automatic coordinate-conversion default exists. Records retain
source GTF integers.

## Choices

The strand field must be `+` or `-`; `.` is rejected. `filter_by_*` helpers
select subsets such as `feature_type` without rewriting source coordinates.

## Constraints

Coordinates remain 1-based closed GTF integers in parsed `GTFRecord` values; no
automatic BED conversion is performed by this profile. Attribute dialect must
match supported `key "value";` parsing.

## Outputs

Parsed `GTFRecord` objects and collected comment lines. No GTF write API exists.

## Ordering

Source record order is preserved across iteration. Re-iteration reopens the file
from the beginning.

## Side effects

Read-only file access. `filter_by_*` creates a new filtered handle without
mutating the source handle predicates.

## Failures

Invalid strand raises `RGToolsInternalException`. Malformed records or
unsupported attribute syntax may raise parsing errors. Filter predicates that
match no records raise filter-specific exceptions at operation level.

## Related API and CLI

- [`GTFHandle` and `GTFRecord`](../../python/gtf/gtf-utils.md)
