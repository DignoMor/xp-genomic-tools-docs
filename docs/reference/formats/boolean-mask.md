# Boolean mask annotation

## Purpose

Represent one boolean selection value per element or genomic region.

## Availability

Supported in the current reference release (`0.3.0a4`).

Available since `0.1.0a2`.

## Inputs

Load from a NumPy `.npy` file or an `.npz` file containing exactly one array,
or pass an array-like value to a public mask loader.

## Types

An in-memory NumPy array; file paths are strings or path-like values where the
calling API accepts them.

## Shapes

Accepted load shapes are `(N,)` and `(N, 1)`. In memory, masks are normalized
to `(N, 1)`, with row `i` corresponding to element row `i`.

## Dtype

The dtype must be NumPy boolean (`numpy.bool_`, displayed as `bool`). Integer
masks containing `0` and `1` are invalid and are not coerced; convert them
explicitly before loading if boolean interpretation is intended.

## Dtypes

Only NumPy boolean dtype is supported.

## Defaults

No dtype or shape default applies. Annotation type metadata is not stored in
`.npy` or `.npz`; the caller identifies the array as a mask.

## Choices

The supported serialized containers are `.npy` and single-array `.npz`.

## Constraints

`N` must equal the region count. A `.npz` archive must contain exactly one
array. A two-dimensional mask must have exactly one column.

## Outputs

Saved masks are NumPy arrays suitable for reloading as mask annotations. APIs
that normalize before saving write shape `(N, 1)`.

## Ordering

Array order is significant: mask row `i` applies to region row `i` in the
current region-table order.

## Side effects

Loading mutates the target collection's in-memory annotations. Save operations
write or replace their requested output file.

## Failures

Mask loading raises `ValueError` for non-boolean dtype, invalid shape,
region-count mismatch, or a multi-array NPZ archive. File-system and NumPy load
errors propagate from the underlying reader.

## Related API and CLI

- [`load_mask_from_arr`](../python/general-elements/load-mask-from-arr.md)
- [`GenomicElementTools mask_op intersect`](../cli/genomic-element-tools/mask-op/intersect.md)
