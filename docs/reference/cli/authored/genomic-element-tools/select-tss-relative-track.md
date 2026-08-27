# `GenomicElementTools select_tss_relative_track`

## Availability

Supported in `GenomicElementTools` for release `0.3.0a4`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Select a TSS-relative score from required `--track_npy`
relative to a TREbed TSS. Requires `--strand` (`+` or `-`), nonzero
`--target_coord`, finite `--min_score`, `--coordinate_opath`, and
`--mask_opath`. Shared region flags are required and `--region_file_type` must
be `TREbed`. Track and output paths accept `.npy` or single-array `.npz`.

## Defaults

`--relaxation` defaults to `0` (exact coordinate)
and expands to `2r+1` ascending no-zero coordinates for `r > 0`.
`--track_window_size` defaults to `1` for point tracks; set it to the motif
width when consuming motif-search tracks. Strand `+` uses `fwdTSS`; strand `-`
uses `revTSS`. Tracks stay genomic-forward indexed: plus coordinates identify
the genomic-left strand-oriented 5-prime base of the scored window, and minus
coordinates identify the genomic-right 5-prime base (internal trailing padding
is `window_size - 1`). Selection takes the first maximum in ascending
TSS-relative order and matches with an inclusive cutoff
(`max_score >= min_score`). A selected TSS of `-1` is a row-level no-match; the
unselected TSS is ignored. A nonmissing selected TSS must lie inside
`[start,end)`, and every relaxed-window position must map to a complete scored
window inside the row's logical track length (storage padding beyond that
length is never searched). These operation-level indexing rules are stricter
than format-level TREbed readability.

## Outputs

Writes integer coordinates and a boolean mask
as `(N,1)` annotations in input row order only after every row is validated.
Matches emit the selected nonzero coordinate and `true`; no-matches emit `0`
and `false`. Existing destinations are refused unless `--force` is supplied;
either existing path blocks both publications. Forced replacement stages
complete files beside each destination (`.stem.staging.npy` /
`.stem.staging.npz`), backs up existing files (`.basename.bak`), publishes both
with `os.replace`, and rolls back from backups on ordinary commit failure.
Interrupted staging or backup remnants are reported without automatic cleanup.
Boolean/nonnumeric tracks,
unsupported suffixes, multi-array NPZ inputs, invalid window size or
relaxation, zero target, nonfinite cutoffs, searched NaN (with row/track-index
context), out-of-interval selected TSS, unavailable windows, missing parent
directories, and track shape/alignment errors raise before destinations are
created or changed. Score `-inf` is unmatchable; `+inf` is a qualifying
maximum. Compose the mask with `mask_op` and subset regions plus aligned
coordinate stats with `export MaskedGE`.

## Inputs

See Purpose and the parser-derived options table.

## Types

Paths and schema keys are strings unless noted in Purpose.

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

Run `GenomicElementTools select_tss_relative_track --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
