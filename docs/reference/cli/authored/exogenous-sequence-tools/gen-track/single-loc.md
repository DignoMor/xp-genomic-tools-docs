# `ExogenousSequenceTools gen_track single_loc`

## Availability

Supported in `ExogenousSequenceTools` for release `0.3.0a4`. Invoke through the installed `ExogenousSequenceTools` console script.

## Purpose

`operation=single_loc` is required. Flags `--fasta`, `--loc` (required
integer), and `--output_npy` (required) produce an integer `int64` stat array
of shape `(N, 1)`, every row equal to `loc`, aligned to FASTA order. The
output is written as `.npy`; input and output filesystem errors fail
non-zero. See [track/stat arrays](../../formats/cli/exogenous-sequence-tools/track-stat-arrays.md).

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

Run `ExogenousSequenceTools gen_track single_loc --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
