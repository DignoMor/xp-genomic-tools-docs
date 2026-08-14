# `GeneralElements.load_mask_from_arr`

## Purpose

Attach a named boolean selection mask to an element collection.

## Availability

Supported in release `0.1.0a2`. The method is declared by
`RGTools.GeneralElements.GeneralElements` and inherited by `GenomicElements`
and `ExogeneousSequences`. The module is available as
`from RGTools import GeneralElements`; concrete collections are the normal
public callers because `GeneralElements` is abstract.

## Inputs

- `anno_name`: name used to retrieve or save the annotation.
- `anno_arr`: array-like boolean values aligned to the collection's regions.

## Types

`anno_name` is a string. `anno_arr` is accepted by `numpy.asarray` and must
produce a NumPy array.

## Shapes

Accepted shapes are `(N,)` and `(N, 1)`, where `N` is the number of regions.
A one-dimensional input is normalized and stored as `(N, 1)`.

## Dtypes

The converted array must have NumPy boolean dtype (`numpy.bool_`). See the
[boolean-mask format](../../formats/boolean-mask.md#dtype).

## Defaults

No argument has a default.

## Choices

`anno_name` has no enumerated choices. The annotation kind is fixed to `mask`.

## Constraints

The first dimension must equal the current region count. Two-dimensional input
must have exactly one column. Integer `0`/`1` values are not coerced to boolean.

## Outputs

Returns `None`. The collection stores the normalized `(N, 1)` array, annotation
length `1`, and annotation type `mask` under `anno_name`.

## Ordering

Stored row `i` remains aligned to region row `i`; the method does not reorder
either regions or mask values.

## Side effects

Mutates the in-memory annotation dictionaries of the collection. It performs no
file I/O.

## Failures

Raises `ValueError` when dtype is not boolean, the first dimension differs from
the region count, or the shape is neither `(N,)` nor `(N, 1)`.
