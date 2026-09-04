# `GenomicElementTools track2tss_bed`

## Availability

Supported in `GenomicElementTools` for release `0.4.0a1`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Use required `--track` [annotation array](../../../formats/elements/annotation-arrays.md)
to locate a point per region; `--output_site` currently supports `MaxAbsSig`
(default).

**Types / shapes / outputs.** Track has first dimension `N`; for row `i`, site
is `region.start + argmax(abs(track[i]))`. Writes one-base intervals to required
`--opath`, preserving order and non-coordinate columns.

## Failures

Track/region alignment, indexing, or unknown output site raises
`ValueError` or a library error; parser failures exit 2.

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

## Example

Run `GenomicElementTools track2tss_bed --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
