# `GenomicElementTools mask_op union`

## Availability

Supported in `GenomicElementTools` for release `0.3.0a4`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Same inputs and shapes as `intersect`, but computes element-wise OR. Output is
boolean `(N,1)` NPY in region order. Fewer than two masks, non-boolean input,
ambiguous NPZ, and alignment failures raise `ValueError`/library errors.

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

Run `GenomicElementTools mask_op union --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
