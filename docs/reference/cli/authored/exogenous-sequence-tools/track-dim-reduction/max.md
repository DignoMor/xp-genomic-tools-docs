# `ExogenousSequenceTools track_dim_reduction max`

## Availability

Supported in `ExogenousSequenceTools` for release `0.3.0a4`. Invoke through the installed `ExogenousSequenceTools` console script.

## Purpose

The required nested operation is `max`. Required
flags are `--input_npy` and `--output_npy`; `--search_range` is an optional
`start,end` string, defaulting to the full track. Input must be a 2-D track
`(N, L)`. Columns outside the zero-based half-open range `[start,end)` are
set to negative infinity before reduction. Reduction is axis 1 with
`keepdims=True`, yielding `(N,1)`: max/min values retain the numeric dtype
(subject to NumPy promotion), while argmax/argmin are integer indices. The
row order is unchanged. Note that the same `-inf` masking is used for min and
argmin, so an all-masked or partly masked search can select a masked column;
this is current behavior. Malformed ranges, wrong dimensionality, and NumPy
load/save errors fail non-zero. See [track/stat arrays](../../formats/cli/exogenous-sequence-tools/track-stat-arrays.md).

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
ExogenousSequenceTools track_dim_reduction max \
  --input_npy track.npy \
  --output_npy max_stat.npy \
  --search_range 0,50
```
