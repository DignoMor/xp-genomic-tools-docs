# Annotation arrays (`.npy` / `.npz`)

## Purpose

Sidecar NumPy annotations aligned to the current element order.

## Availability

Supported in the current reference release (`0.3.0a4`).

Available since `0.1.0a2`.

## Inputs

`.npy` arrays or `.npz` archives containing exactly one array; the caller
supplies the annotation type because type metadata is not stored.

## Types

Supported annotation kinds are `track`, `stat`, `mask`, and `array`. NPZ has no
embedded type or name metadata.

## Shapes

| Type | Accepted input | Stored/output |
| --- | --- | --- |
| `stat` | `(N,)` or `(N,1)` | `(N,1)` |
| `mask` | `(N,)` or `(N,1)` | `(N,1)` |
| `track` | list of N vectors, or `(N,max_len)` | zero-padded `(N,max_region_len)` |
| `array` | `(N,...)`, at least 2-D | unchanged trailing shape |

## Dtypes

| Type | Dtype rule |
| --- | --- |
| `stat` | any NumPy dtype |
| `mask` | **must be `numpy.bool_`; integer 0/1 is invalid** |
| `track` | numeric or other NumPy dtype |
| `array` | any NumPy dtype |

See the [boolean-mask rule](../boolean-mask.md) for the mask dtype requirement.

## Defaults

`load_region_anno_from_npy` defaults to `anno_type="array"`.

## Choices

Load from `.npy` or single-array `.npz`; caller selects annotation type.

## Constraints

The first dimension must equal `N`, the current region count. Track list entry
`i` must have length equal to region `i`. Multi-array NPZ archives are rejected.

## Outputs

Normalized in-memory arrays and NumPy files on save. Type metadata is not
written to disk.

## Ordering

Row `i` maps to region or sequence row `i` in the current table order.

## Side effects

Load mutates the target collection; save writes or replaces output files.

## Failures

Wrong shape, wrong count, unsupported type, non-boolean masks, and multi-array
NPZ raise `ValueError`.

## Related API and CLI

- [`GeneralElements`](../../python/general-elements/general-elements.md)
- [`GenomicElements`](../../python/elements/genomic-elements.md)
- [`GenomicElementTools track2tss_bed`](../../cli/genomic-element-tools/track2tss-bed.md)
