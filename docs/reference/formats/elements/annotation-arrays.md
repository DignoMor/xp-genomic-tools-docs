# Annotation arrays (`.npy` / `.npz`)

## Purpose

Sidecar NumPy annotations aligned to the current element order.

## Availability

Supported by `GeneralElements` and both concrete collections in `0.1.0a2`.

## Inputs

`.npy` arrays or `.npz` archives containing exactly one array; the caller
supplies the annotation type because type metadata is not stored.

## Types, shapes, and dtypes

| Type | Accepted input | Stored/output | Dtype rule |
| --- | --- | --- | --- |
| `stat` | `(N,)` or `(N,1)` | `(N,1)` | any NumPy dtype |
| `mask` | `(N,)` or `(N,1)` | `(N,1)` | **must be `numpy.bool_`; integer 0/1 is invalid** |
| `track` | list of N vectors, or `(N,max_len)` | zero-padded `(N,max_region_len)`; getters slice each row | numeric or other NumPy dtype |
| `array` | `(N,...)`, at least 2-D | unchanged | any NumPy dtype |

## Defaults and choices

`load_region_anno_from_npy` defaults to `anno_type="array"`; supported types
are `track`, `stat`, `mask`, and `array`. NPZ has no type or name metadata.

## Constraints, ordering, and failures

The first dimension must equal `N`, the current region count. Track list entry
`i` must have length equal to region `i`; output row `i` always belongs to
region `i`. Multi-array NPZ, wrong shape, wrong count, unsupported type, and
non-boolean masks raise `ValueError`. Save methods write the in-memory array;
they do not write type metadata. `get_track_list` slices padded tracks back to
per-region lengths; scalar/index getters return one value or one trailing-shape
array.

See the [boolean-mask rule](../boolean-mask.md) for the same dtype requirement.

## Reference fields

**Purpose:** persist region-aligned NumPy annotations. **Availability:**
`0.1.0a2`. **Inputs:** `.npy`, single-array `.npz`, or array-like values.
**Types:** NumPy arrays and vector lists. **Shapes:** `(N,)`, `(N,1)`,
`(N,max_region_len)`, or `(N,...)`. **Dtypes:** masks must be `numpy.bool_`;
others are retained. **Defaults:** annotation type `array`. **Choices:**
`track`, `stat`, `mask`, `array`; NPY or one-array NPZ. **Constraints:** first
dimension and track lengths align. **Outputs:** normalized arrays and files.
**Ordering:** row `i` maps to region `i`. **Side effects:** load mutates;
save writes. **Failures:** invalid dtype/shape/count/type or multi-array NPZ
raises `ValueError`.
