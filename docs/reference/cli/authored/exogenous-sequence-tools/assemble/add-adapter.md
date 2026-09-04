# `ExogenousSequenceTools assemble add_adapter`

## Availability

Supported in `ExogenousSequenceTools` for release `0.4.0a1`. Invoke through the installed `ExogenousSequenceTools` console script.

## Purpose

Flags: `--fasta` (required), `--left_adapter_fasta` (required),
`--right_adapter_fasta` (optional, default `None`), and `--output_fasta`
(required). Each adapter FASTA must contain exactly one record. The output for
input record `i` is `left + input_i + right`, with the input ID unchanged;
omitting the optional right adapter means an empty string. A multi-record
adapter raises `ValueError`; file/FASTA errors are non-zero failures. See the
[adapter and assembly output format](../../formats/cli/exogenous-sequence-tools/assembly-outputs.md).

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

Run `ExogenousSequenceTools assemble add_adapter --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
