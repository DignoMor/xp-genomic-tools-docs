# `ExogenousSequenceTools assemble reverse_complement`

## Availability

Supported in `ExogenousSequenceTools` for release `0.4.0a2`. Invoke through the installed `ExogenousSequenceTools` console script.

## Purpose

Flags `--fasta` and `--output_fasta` are required. Optional `--id_suffix`
defaults to the empty string. Every input record is reverse-complemented with
the same IUPAC, case-preserving DNA rule used by
`GenomicElementTools export ExogenousSequences --output_orientation strand`.
Record order is preserved. Each output ID is the input ID followed by the
suffix concatenated literally (no extra separator). Output IDs must be unique
after suffixing (`ValueError` names the duplicated ID and the source FASTA).
A non-IUPAC symbol raises `ValueError`. An empty input FASTA writes an empty
output FASTA. An existing `--output_fasta` is refused and left unchanged.
Failed runs leave no output FASTA. See the
[assembly output format](../../formats/cli/exogenous-sequence-tools/assembly-outputs.md).

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

```bash
ExogenousSequenceTools assemble reverse_complement \
  --fasta library.fa \
  --output_fasta library_rc.fa \
  --id_suffix _rc
```

With `library.fa` containing `>a` / `ACGTn` then `>b` / `RYk`, the output is
`>a_rc` / `nACGT` then `>b_rc` / `mRY`.
