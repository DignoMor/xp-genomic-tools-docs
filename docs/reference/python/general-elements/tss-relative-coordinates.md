# `RGTools.TSSRelativeCoordinates`

**Purpose/availability:** `import RGTools.TSSRelativeCoordinates` exposes
reusable no-zero TSS-relative coordinate arithmetic. Symbols are not re-exported
from the top-level `RGTools` namespace. The current release slice delivers
no-zero offsetting and exact plus-strand point-index conversion
(`track_window_size=1`). Minus-strand conversion, nonzero relaxation windows,
and wider scored windows are not yet delivered and raise `ValueError`.

## Coordinate system

- `+1` is the selected transcription start site base.
- Positive coordinates are downstream; negative coordinates are upstream.
- Coordinate zero does not exist and is invalid input.
- Offsetting across the TSS skips zero so upstream `-1` is adjacent to `+1`.

## `offset_tss_relative_coordinate(coord, delta) -> int`

Offset a no-zero TSS-relative coordinate by an integer delta.

**Failures.** `coord == 0` raises `ValueError`.

## `iter_relaxed_window(target, relaxation) -> Iterator[int]`

Yield ascending TSS-relative coordinates for a symmetric window around
`target`.

**Delivered behavior.** `relaxation == 0` yields exactly `[target]`.

**Failures.** `target == 0` or nonzero `relaxation` raises `ValueError`.

## `tss_relative_to_track_index(*, strand, coord, start, end, tss, track_window_size=1) -> int`

Convert a TSS-relative coordinate to a row-local genomic-forward track index for
interval `[start, end)`.

**Delivered behavior.** Strand `+` with `track_window_size=1`:

1. Genomic position is `tss + coord - 1` when `coord > 0`, else `tss + coord`.
2. Track index is `genomic - start`.
3. The index must satisfy `0 <= index < (end - start)`.

**Failures.** Invalid zero coordinates, invalid intervals, out-of-bounds indices,
strand `-`, and `track_window_size != 1` raise contextual `ValueError`.
