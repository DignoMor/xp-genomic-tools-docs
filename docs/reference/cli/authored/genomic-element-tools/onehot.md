# `GenomicElementTools onehot`

## Availability

Supported in `GenomicElementTools` for release `0.4.0a1`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Extract `--fasta_path` sequences for the GE regions and
write the one-hot encoding to required `--opath`.

## Types

Output is an `int8` NumPy one-hot array transposed
to `(N, 4, L)`; regions must be equal length (`L`) and FASTA IDs must exactly
match region chromosomes. Channel order is explicitly `A, C, G, T`.

## Outputs

Writes NPY via `np.save`, preserving
region order. Missing FASTA records, unequal lengths, invalid coordinates, and
unreadable input raise library errors.

## Inputs

See Purpose and the parser-derived options table.

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

## Ordering

Output rows retain input order unless stated otherwise in Purpose.

## Side effects

Reads declared inputs and writes declared outputs; inputs are not mutated.

## Failures

Argparse exits for missing required flags or invalid choices; runtime validation errors propagate from the implementation.

## Example

Run `GenomicElementTools onehot --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
