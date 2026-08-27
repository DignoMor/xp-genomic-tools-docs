# `GenomicElementTools export Heatmap`

## Availability

Supported in `GenomicElementTools` for release `0.3.0a4`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Takes parallel `--track_npy`/`--title`/`--negative` lists, optional repeated
`--absolute` values, percentile controls (`--per_track_max_percentile` default
99; `--vmax_percentile` default 50), and `--opath`. Writes a visual image only
(no reusable format page); tracks align to regions.

`--absolute` chooses per-track rendering. Omit it to keep every track in
magnitude mode (same as `--absolute True` for each track). If you pass any
`--absolute` values, provide exactly one per track: `True` keeps magnitude
mode, and `False` selects signed mode. Parallel-list length mismatches fail.

Magnitude mode converts values to absolute magnitudes, uses sequential red or
blue coloring from `--negative`, may negate the mean profile when `--negative`
is true, and zero-pads shorter rows. Signed mode keeps raw negative and
positive values in the heatmap and mean, ignores `--negative` for polarity and
palette, uses the fixed `RdBu_r` diverging colormap with a panel color bar,
pads shorter rows as missing rather than zero, and centers the scale exactly at
zero with symmetric limits. Explicit non-finite cells are masked in both modes
and excluded from scale estimation, shared row-order keys, and position-wise
means. Mixed panels share one ascending row order based on each region's
maximum finite absolute magnitude across tracks, with original order retained
for ties. A track-row or entire track with no finite value fails with the track
title and region-row context. Parallel-list, percentile, rendering, and I/O
failures fail.

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

Run `GenomicElementTools export Heatmap --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
