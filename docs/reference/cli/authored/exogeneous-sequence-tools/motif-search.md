# `ExogeneousSequenceTools motif_search`

## Availability

Supported in `ExogeneousSequenceTools` for release `0.3.0a4`. Invoke through the installed `ExogeneousSequenceTools` console script.

## Purpose

Required flags are `--fasta`, `--motif_file`, and `--output_header`.
`--estimate_background_freq` is parsed as a boolean (`str2bool`), default
`true`; `--reverse_complement` is the same type, default `false`. MEME motifs
are read in file order. One track `.npy` is written per motif at
`<output_header>.<motif_name>.npy`, with shape `(N,L)` for homogeneous input
sequences and each row aligned to its sequence. Tracks are named by motif;
the score search uses strand `+` unless reverse-complement mode selects
`both`. Background estimation, `N` handling, pseudocount `(counts+1)/(sites+
alphabet_size)`, and reverse-complement estimation follow the implementation.
Invalid MEME/FASTA, incompatible track lengths, and filesystem errors fail
non-zero. See [motif track outputs](../../formats/cli/exogeneous-sequence-tools/motif-outputs.md).

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

Run `ExogeneousSequenceTools motif_search --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
