# Mutagenesis locations and outputs

`--loc_npy` is a NumPy stat annotation, normally integer `int64`, shape
`(N,1)`, with row `i` the zero-based replacement offset for input sequence
`i`. A target FASTA supplies replacement sequences. Equal input/target counts
pair element-wise; unequal counts broadcast each target across all inputs.
Output IDs are `<input_id>_mut_<target_id>` and output order is element-wise
input order or broadcast target-major/input-minor order. The replacement may
change sequence length if target length differs.

## Purpose
Location-driven sequence replacement.
## Availability

Supported in the current reference release (`0.3.0a4`).

Available since `0.1.0a2`.

## Inputs
FASTA targets and `(N,1)` location NPY.
## Types
Strings and integer offsets.
## Shapes
Locations `(N,1)`; output count `N` or `N*M`.
## Dtypes
Location values are integer-compatible.
## Defaults
Equal counts pair element-wise.
## Choices
Element-wise or broadcast mode is count-dependent.
## Constraints
Rows align to input records.
## Outputs
Mutated FASTA records.
## Ordering
Input order or target-major/input-minor.
## Side effects
Creates output FASTA.
## Failures
Invalid files, arrays, or offsets fail.

## Related API and CLI

- [`ExogenousSequenceTools mutagenesis`](../../../cli/exogenous-sequence-tools/mutagenesis.md)
