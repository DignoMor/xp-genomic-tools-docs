# `GenomicElementTools export MergedGE`

## Availability

Supported in `GenomicElementTools` for release `0.4.0a1`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Merges left/right region files that share one schema selector — exactly one of
`--region_file_type` or `--region_file_schema` — with parallel annotation
names/paths/types and `--oheader`. Annotation types are only `track`, `stat`,
`mask`, or `array`; first dimensions align within each input. Merge requires
the same named format or the same canonical custom schema file with
structurally compatible snapshots (relative, absolute, and symlink spellings
of one file are accepted when snapshots match; distinct files are rejected
even when structurally identical). Named outputs keep `.<named-format>`
suffixes; custom merges write `.bed3plus` or `.bed6plus` by base type and do
not publish schema sidecars. Mismatched parallel arguments, incompatible
schemas, or annotation errors fail before outputs are replaced.

## Inputs

See Purpose and the parser-derived options table.

## Types

Paths and schema keys are strings unless noted in Purpose.

## Shapes

Annotation arrays align by first dimension with region or sequence order.

## Dtypes

See linked format references and Purpose.

## Defaults

Parser defaults appear in the generated options table.

## Choices

Parser choices appear in the generated options table.

## Constraints

See Purpose and linked format references.

## Outputs

See Purpose for the serialized output contract.

## Ordering

Output rows retain input order unless stated otherwise in Purpose.

## Side effects

Reads declared inputs and writes declared outputs; inputs are not mutated.

## Failures

Argparse exits for missing required flags or invalid choices; runtime validation errors propagate from the implementation.

## Example

Run `GenomicElementTools export MergedGE --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
