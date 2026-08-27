# `ExogenousSequenceTools onehot`

## Availability

Supported in `ExogenousSequenceTools` for release `0.3.0a4`. Invoke through the installed `ExogenousSequenceTools` console script.

## Purpose

Required flags are `--fasta` and `--opath`. All sequences must have the same
length `L`. The output is an array annotation saved to `--opath` with shape
`(N,4,L)`, channel order `A,C,G,T`, and dtype `numpy.int8`;
ambiguous IUPAC bases encode as zeros. Rows and channels preserve sequence
and alphabet order. Mixed lengths raise `ValueError`; malformed FASTA and
save errors fail non-zero. See [one-hot arrays](../../formats/cli/exogenous-sequence-tools/onehot-outputs.md).

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

Run `ExogenousSequenceTools onehot --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
