# One-hot output arrays

`onehot` writes a NumPy array annotation with shape `(N,4,L)` (channel-first),
where channels are ordered `A,C,G,T`. Sequences must all have length `L`;
ambiguous bases encode as zero channels. The saved numeric dtype is
`numpy.int8`. FASTA and output row order is preserved. Mixed lengths
raise `ValueError`.

## Purpose
Channel-first one-hot sequence arrays.
## Availability

Supported in the current reference release (`0.4.0a1`).

Available since `0.1.0a2`.

## Inputs
Equal-length exogenous FASTA.
## Types
Numeric array with sequence channels.
## Shapes
`(N,4,L)`.
## Dtypes
`numpy.int8`.
## Defaults
Alphabet order `A,C,G,T`.
## Choices
Four canonical base channels.
## Constraints
All sequences have identical length; ambiguous bases are zero.
## Outputs
One `.npy` array.
## Ordering
FASTA row and channel order.
## Side effects
Creates requested output path.
## Failures
Mixed lengths or invalid input fail.

## Related API and CLI

- [`ExogenousSequenceTools onehot`](../../../cli/exogenous-sequence-tools/onehot.md)
