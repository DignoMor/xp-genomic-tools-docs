# Track and stat arrays

CLI `.npy` arrays use NumPy's native serialization. A track consumed by
`track_dim_reduction` has shape `(N,L)`; its output and `gen_track`/`print_stat`
stat arrays have shape `(N,1)`. `single_loc` writes `int64`; extrema retain
NumPy's value dtype and arg-extrema write integer indices. Row `i` remains
aligned to input element `i`. `search_range=start,end` is zero-based,
half-open; out-of-range columns are set to `-inf` before reduction.

## Purpose
NumPy track and stat interchange.
## Availability

Supported in the current reference release (`0.4.0a1`).

Available since `0.1.0a2`.

## Inputs
`.npy` arrays.
## Types
Track and stat arrays.
## Shapes
Tracks `(N,L)`; stats `(N,1)`.
## Dtypes
Generated locations `int64`; extrema follow NumPy.
## Defaults
Full track when search range is omitted.
## Choices
`max`, `argmax`, `min`, `argmin`, `single_loc`.
## Constraints
First dimension remains aligned.
## Outputs
`.npy` stat arrays or stdout.
## Ordering
Row order is preserved.
## Side effects
Creates output NPY files.
## Failures
Wrong dimensions and malformed ranges fail.

## Related API and CLI

- [`ExogenousSequenceTools track_dim_reduction`](../../../cli/exogenous-sequence-tools/track-dim-reduction.md)
- [`ExogenousSequenceTools gen_track`](../../../cli/exogenous-sequence-tools/gen-track.md)
- [Annotation arrays](../../elements/annotation-arrays.md)
