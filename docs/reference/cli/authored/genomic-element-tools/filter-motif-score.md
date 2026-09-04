# `GenomicElementTools filter_motif_score`

## Availability

Supported in `GenomicElementTools` for release `0.4.0a1`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Filter motif tracks from required `--motif_search_npy`
using required integer `--filter_base`, with `--min_score` and `--max_score`.

## Defaults

Defaults are `-inf` and `+inf`; retention is strict:
`min_score < track[filter_base] < max_score`. Track first dimension aligns to
regions.

## Outputs

Writes `<output_header>.bed` and
`<output_header>.motif.npy`, preserving surviving row order. Out-of-range base,
alignment errors, or empty-result library limitations can raise indexing or
library errors.

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

Run `GenomicElementTools filter_motif_score --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
