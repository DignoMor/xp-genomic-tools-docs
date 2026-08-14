# BigWig signal tracks

## Purpose

Read a BigWig signal track and quantify a BED-coordinate interval.

The file profile is described in the [BigWig signal format reference](../../formats/signal/bigwig.md).

## Availability

Supported in release `0.1.0a2` from `RGTools.BwTrack`. Import
`BaseBwTrack`, `SingleBwTrack`, and `PairedBwTrack` from that module; the two
concrete classes are also re-exported by `RGTools`.

## Inputs

`SingleBwTrack(bw_path)` opens one BigWig. `PairedBwTrack(bw_pl_path,
bw_mn_path)` opens plus and minus BigWigs. `count_single_region` receives
`chrom`, integer `start` and `end`, and (for paired tracks) `strand`.

## Types

Paths are strings or path-like values accepted by `pyBigWig.open`. Coordinates
are integers. `strand` is `+`, `-`, or `.` for paired tracks. Signal is a
NumPy numeric vector; `quantify_signal` returns a scalar or vector.

## Shapes

An interval uses BED `[start, end)` and produces a vector of length `end -
start` after padding. `raw_count` and `RPK` are scalars; `full_track` is that
one-dimensional vector.

## Dtypes

Signal values are numeric and NaNs are converted to zero before quantification.

## Defaults

`output_type="raw_count"`, `l_pad=0`, `r_pad=0`,
`min_len_after_padding=50`, and `method_resolving_invalid_padding="raise"`.
Paired tracks additionally default to `flip_mn=False` and `negative_mn=True`.

## Choices

Quantification types are `raw_count` (sum), `RPK` (sum divided by vector
length times `1e3`), and `full_track` (the vector). Paired strand choices are
`+`, `-`, and `.`. Invalid padding methods are `fallback`, `raise`, and
`drop`.

## Constraints

Coordinates are zero-based, half-open. Padding adds `l_pad` to the left and
`r_pad` to the right. If the requested minimum cannot be met, `fallback`
queries the original interval, `raise` raises, and `drop` logs to stderr and
returns `numpy.nan`. Missing chromosomes produce a zero vector. Paired minus
values are made absolute, then optionally negated (`negative_mn`) and reversed
(`flip_mn`); `.` adds the plus and minus quantifications.

## Outputs

`BaseBwTrack.quantify_signal(signal, output_type)` and
`count_single_region(...)` return a NumPy scalar/scalar-compatible value for
`raw_count` or `RPK`, the signal array for `full_track`, or `numpy.nan` for a
dropped interval.

## Ordering

Vector positions retain BigWig genomic order. `flip_mn=True` reverses only the
minus vector before quantification.

## Side effects

Construction opens read-only BigWig resources; object destruction closes them.
Queries do not write files. Paired `.` combines strand results after each has
been quantified.

## Failures

Unsupported quantification type, invalid padding policy, and invalid paired
strand raise an exception. BigWig open/read errors propagate from
`pyBigWig`.

## `BaseBwTrack`

### BaseBwTrack constructor

`BaseBwTrack()` is abstract and cannot be used directly for track queries.

### `BaseBwTrack.quantify_signal`

Static operation implementing the three quantification choices above. The
base class is abstract and is not instantiated for querying.

### `BaseBwTrack.get_supported_quantification_type`

Static operation returning the list `['raw_count', 'RPK', 'full_track']` in
that order.

### `BaseBwTrack.count_single_region`

Abstract operation with `chrom`, `start`, `end`, and subclass-specific
options. Concrete classes implement it as described below.

## `SingleBwTrack`

### SingleBwTrack constructor

`SingleBwTrack(bw_path)` opens one read-only BigWig.

### `SingleBwTrack.count_single_region`

Queries the padded interval from the single track, replaces missing chromosome
values/NaNs with zero, and applies the selected quantification.

## `PairedBwTrack`

### PairedBwTrack constructor

`PairedBwTrack(bw_pl_path, bw_mn_path)` opens plus and minus read-only BigWigs.

### `PairedBwTrack.count_single_region`

Queries both tracks using the same padded interval. `+` returns plus, `-`
returns transformed minus, and `.` returns the sum of both quantifications.
