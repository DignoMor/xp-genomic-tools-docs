# `GenomicElementTools count_paired_bw`

## Availability

Supported in `GenomicElementTools` for release `0.4.0a1`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Count paired plus/minus [BigWigs](../../../formats/signal/bigwig.md)
`--bw_pl` and `--bw_mn`. Regions use the shared flags against a [BED-like region
table](../../../formats/foundation/bed-like.md); `--override_strand` optionally
supplies strand. `--negative_mn` and `--flip_mn` are required booleans.

## Types

`raw_count`, `RPK`, and `full_track` have the same
stat-versus-track shapes as `count_single_bw`; output annotation is `count`.

## Defaults

Quantification defaults to `raw_count`; strand is
resolved from override, then from BED6 strand capability on the loaded table
(named or custom), with missing strand capability or falsy strand becoming
`.`. `.npz` alone selects NPZ; other suffixes select NPY. Both tracks must be
readable. Provide exactly one of `--region_file_type` or `--region_file_schema`.

## Outputs

One value/track per input row, in order.
Track, region, boolean, or quantification errors are library errors; argparse
validation exits 2.

## Inputs

See Purpose and the parser-derived options table.

## Shapes

Annotation arrays align by first dimension with region or sequence order.

## Dtypes

See linked format references and Purpose.

## Choices

Parser choices appear in the generated options table.

## Constraints

See Purpose and linked format references.

## Ordering

Output rows retain input order unless stated otherwise in Purpose.

## Side effects

Reads declared inputs and writes declared outputs; inputs are not mutated.

## Failures

Argparse exits for missing required flags or invalid choices; runtime validation errors propagate from the implementation.

## Example

Run `GenomicElementTools count_paired_bw --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
