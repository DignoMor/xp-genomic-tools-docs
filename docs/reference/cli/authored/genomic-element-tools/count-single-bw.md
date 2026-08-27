# `GenomicElementTools count_single_bw`

## Availability

Supported in `GenomicElementTools` for release `0.3.0a4`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Count `--bw_path` BigWig signal for the regions supplied by
`--region_file_path` and `--region_file_type`.

## Types

BigWig is a signal track. `--quantification_type`
choices are `raw_count`, `RPK`, and `full_track`; scalar modes produce stat
values `(N,)`, while `full_track` produces a track `(N, L_i)` (variable lengths
are represented by the library's track convention).

## Defaults

`--opath` is required. The default quantification
is `raw_count`; `.npz` selects NPZ output and every other suffix selects NPY.
The BigWig must be readable and cover queried regions.

## Outputs

Writes annotation named `count`, in
input order. Missing/corrupt BigWig, unsupported quantification, region
loading, or incompatible lengths raise library errors; parser errors exit 2.

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

Run `GenomicElementTools count_single_bw --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
