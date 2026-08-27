# `ExogenousSequenceTools print_stat`

## Availability

Supported in `ExogenousSequenceTools` for release `0.3.0a4`. Invoke through the installed `ExogenousSequenceTools` console script.

## Purpose

`--input_npy` is required. The input must have a second dimension of exactly
1 (normally `(N,1)`); otherwise `ValueError` is raised. Values in column 0
are printed one per line, in row order, using NumPy's normal string
conversion. There is no output file and no mutation of the input.

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

Run `ExogenousSequenceTools print_stat --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
