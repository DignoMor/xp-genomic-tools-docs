# `ExogenousSequenceTools assemble combine`

## Availability

Supported in `ExogenousSequenceTools` for release `0.4.0a1`. Invoke through the installed `ExogenousSequenceTools` console script.

## Purpose

Flags `--input_fasta`, `--id_suffix`, and `--output_fasta` are required.
`--input_fasta` and `--id_suffix` are repeatable and pair one-to-one by
position. Omitting `--id_suffix` entirely is an argparse error; an unequal
count raises `ValueError`. An empty suffix is valid.

This command performs **collection stacking**: it writes the records of each
input FASTA, in command-line order and in file order within each input, into
one FASTA. Sequences are unchanged. Each output ID is the input ID followed
by that input's suffix concatenated literally (no extra separator). A single
input with its suffix succeeds. Empty inputs contribute no records; stacking
only empty inputs writes an empty FASTA. Output IDs must be unique after
suffixing (`ValueError` names the duplicated ID and the contributing source
FASTA files). Distinct suffixes can disambiguate shared input IDs. An
existing `--output_fasta` is refused and left unchanged. Failed runs leave
no output FASTA.

This is not paired sequence joining. Use
[`assemble concat`](concat.md) when corresponding records of two FASTAs
should be concatenated so each sequence grows. See the
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

Inputs appear in command-line order; records within each input keep file order.

## Side effects

Reads declared inputs and writes declared outputs; inputs are not mutated.

## Failures

Argparse exits for missing required flags or invalid choices; runtime validation errors propagate from the implementation.

## Example

```bash
ExogenousSequenceTools assemble combine \
  --input_fasta sublib_a.fa \
  --id_suffix "" \
  --input_fasta sublib_b.fa \
  --id_suffix _b \
  --output_fasta pooled.fa
```

With `sublib_a.fa` containing `>x` / `AAA` then `>y` / `CCC`, and
`sublib_b.fa` containing `>x` / `GGG` then `>z` / `TTT`, the output is
`>x` / `AAA`, `>y` / `CCC`, `>x_b` / `GGG`, `>z_b` / `TTT`.
