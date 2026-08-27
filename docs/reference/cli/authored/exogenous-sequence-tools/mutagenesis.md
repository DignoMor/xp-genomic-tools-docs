# `ExogenousSequenceTools mutagenesis`

## Availability

Supported in `ExogenousSequenceTools` for release `0.3.0a4`. Invoke through the installed `ExogenousSequenceTools` console script.

## Purpose

Required flags are `--fasta`, `--loc_npy`, `--mut_fasta`, and `--output_fasta`.
`loc_npy` is a stat array of shape `(N, 1)` (integer offsets, zero-based) and
is aligned to the input records. If input and mutation FASTAs have equal
record counts, entries pair element-wise. Otherwise each target is applied to
every input, with targets as the outer loop and inputs as the inner loop.
Replacement at `loc` is `seq[:loc] + target + seq[loc+len(target):]`.
Output IDs are `<input_id>_mut_<target_id>`, and output ordering follows the
pairing mode above. Sequence length is preserved when replacement spans the
same length; the implementation otherwise permits length changes. Invalid
FASTA/NPY or shape/alignment errors are non-zero failures. See the
[mutagenesis input/output format](../../formats/cli/exogenous-sequence-tools/mutagenesis.md).

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

Run `ExogenousSequenceTools mutagenesis --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
