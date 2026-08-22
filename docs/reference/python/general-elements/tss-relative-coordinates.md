# `RGTools.TSSRelativeCoordinates`

**Purpose/availability:** `import RGTools.TSSRelativeCoordinates` exposes
reusable no-zero TSS-relative coordinate arithmetic. Symbols are not re-exported
from the top-level `RGTools` namespace. The module converts between strand-oriented
TSS-relative coordinates and genomic-forward track indices for point tracks and
wider scored windows.

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
`target`. A nonnegative relaxation radius `r` yields exactly `2r+1`
coordinates and skips zero (for example `target=-1`, `r=1` → `[-2, -1, 1]`).

**Failures.** `target == 0` or negative `relaxation` raises `ValueError`.

## `tss_relative_to_track_index(*, strand, coord, start, end, tss, track_window_size=1) -> int`

Convert a TSS-relative coordinate to a row-local genomic-forward track index for
interval `[start, end)`.

Track arrays remain genomic-forward for both strands. A value at index `i`
describes a genomic-forward window of width `track_window_size` beginning at
`start + i`.

1. Genomic position of the reported strand-oriented 5-prime base is
   `tss + coord - 1` when `coord > 0`, else `tss + coord`.
2. Strand `+`: reported coordinate is the genomic-left 5-prime base; index is
   `genomic - start`.
3. Strand `-`: reported coordinate is the genomic-right 5-prime base; index is
   `genomic - start - (track_window_size - 1)`.
4. The scored window must fit inside the interval; otherwise conversion raises
   contextual `ValueError` (no clipping, wrapping, or shrinking).

**Failures.** Invalid strand, zero coordinates, nonpositive
`track_window_size`, invalid intervals, and out-of-bounds windows raise
contextual `ValueError`. Callers that need TREbed row identity (such as
`select_tss_relative_track`) add that context when re-raising.
