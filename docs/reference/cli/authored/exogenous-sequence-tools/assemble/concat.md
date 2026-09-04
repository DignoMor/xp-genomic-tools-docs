# `ExogenousSequenceTools assemble concat`

## Availability

Supported in `ExogenousSequenceTools` for release `0.4.0a1`. Invoke through the installed `ExogenousSequenceTools` console script.

## Purpose

Flags `--fasta5`, `--fasta3`, and `--output_fasta` are required.
`--id_method` choices are `5`, `3`, and `5_3` (default `5_3`). Records are
paired by positional `zip` order (extra records are ignored). Output sequence
`i` is `seq5_i + seq3_i`; its ID is respectively `id5_i`, `id3_i`, or
`id5_i_id3_i`. Invalid methods raise `ValueError`. The output is ordered by
the paired inputs.

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

Run `ExogenousSequenceTools assemble concat --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
