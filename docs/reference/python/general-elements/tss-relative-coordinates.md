# `RGTools.TSSRelativeCoordinates`

## Status

Supported for the current reference release. Symbols are not re-exported from
the top-level `RGTools` namespace.

## Purpose

Expose reusable no-zero TSS-relative coordinate arithmetic. The module
converts between strand-oriented TSS-relative coordinates and genomic-forward
track indices for point tracks and wider scored windows.

## Canonical import

```python
import RGTools.TSSRelativeCoordinates as tss
```

## Signature

Module functions rendered from the aligned release source:

::: RGTools.TSSRelativeCoordinates
    options:
      members:
        - offset_tss_relative_coordinate
        - iter_relaxed_window
        - tss_relative_to_track_index
      show_root_heading: true
      show_source: false
      heading_level: 4
      filters:
        - "!^_"

## Parameters

- `offset_tss_relative_coordinate(coord, delta)` — integer coordinate and offset.
- `iter_relaxed_window(target, relaxation)` — center coordinate and nonnegative
  radius.
- `tss_relative_to_track_index(*, strand, coord, start, end, tss,
  track_window_size=1)` — strand, no-zero coordinate, BED interval, selected
  TSS, and optional window width.

## Return or yield behavior

`offset_tss_relative_coordinate` returns an integer. `iter_relaxed_window`
yields ascending coordinates, skipping zero. `tss_relative_to_track_index`
returns a zero-based row-local track index.

## Raised exceptions

Zero coordinates, negative relaxation, invalid strand, nonpositive
`track_window_size`, invalid intervals, and out-of-bounds windows raise
contextual `ValueError`.

## Constraints

`+1` is the selected transcription start site base. Positive coordinates are
downstream; negative coordinates are upstream. Coordinate zero does not exist.
Track arrays remain genomic-forward for both strands. The scored window must
fit inside the interval without clipping.

## Ordering

`iter_relaxed_window` yields ascending coordinates. Through `0.3.0a2`,
minus-strand conversion incorrectly used `tss + linear(coord)` for both
strands; `0.3.0a3` corrects direction so minus-strand negative coordinates
map toward larger genomic positions.

## Side effects

None.

## Lifecycle behavior

Not applicable: module functions are stateless.

## Supported protocols and inheritance

Not applicable: standalone module functions.

## Example

```python
import RGTools.TSSRelativeCoordinates as tss

index = tss.tss_relative_to_track_index(
    strand="-",
    coord=-2,
    start=100,
    end=200,
    tss=150,
)
```

## Related formats or commands

- [`GenomicElementTools select_tss_relative_track`](../../cli/genomic-element-tools/index.md)
- [TSS-relative mutagenesis guide](../../../guides/tss-relative-mutagenesis.md)
