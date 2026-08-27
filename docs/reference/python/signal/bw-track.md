# BigWig signal tracks

## Status

Supported for the current reference release.

## Purpose

Read BigWig signal tracks and quantify BED-coordinate intervals. `BaseBwTrack`
defines the abstract quantification contract; `SingleBwTrack` and
`PairedBwTrack` implement concrete read-only track queries.

## Canonical import

```python
from RGTools.BwTrack import BaseBwTrack, SingleBwTrack, PairedBwTrack
```

`SingleBwTrack` and `PairedBwTrack` are also re-exported from `RGTools`.

## Signature

Abstract base and concrete track members rendered from the aligned release
source:

::: RGTools.BwTrack.BaseBwTrack
    options:
      members:
        - quantify_signal
        - get_supported_quantification_type
        - count_single_region
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_"

::: RGTools.BwTrack.SingleBwTrack
    options:
      members:
        - __init__
        - count_single_region
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_"

::: RGTools.BwTrack.PairedBwTrack
    options:
      members:
        - __init__
        - count_single_region
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_"

## Parameters

`SingleBwTrack(bw_path)` opens one read-only BigWig. `PairedBwTrack(bw_pl_path,
bw_mn_path)` opens plus and minus BigWigs. `count_single_region` receives
`chrom`, integer `start` and `end`, quantification options, padding controls,
and (for paired tracks) `strand`.

## Return or yield behavior

`quantify_signal` and `count_single_region` return a NumPy scalar or
scalar-compatible value for `raw_count` or `RPK`, the signal array for
`full_track`, or `numpy.nan` for a dropped interval.

## Raised exceptions

Unsupported quantification type, invalid padding policy, and invalid paired
strand raise an exception. BigWig open and read errors propagate from
`pyBigWig`.

## Constraints

Coordinates are zero-based, half-open BED intervals. Padding adds `l_pad` to
the left and `r_pad` to the right. Missing chromosomes produce a zero vector.
Paired minus values are made absolute, then optionally negated (`negative_mn`)
and reversed (`flip_mn`); `.` adds the plus and minus quantifications.

## Ordering

Vector positions retain BigWig genomic order. `flip_mn=True` reverses only the
minus vector before quantification.

## Side effects

Construction opens read-only BigWig resources; object destruction closes them.
Queries do not write files.

## Lifecycle behavior

Tracks should be allowed to go out of scope or be deleted so underlying
`pyBigWig` handles close. No explicit `close()` is required beyond normal
object lifetime.

## Supported protocols and inheritance

`BaseBwTrack` is abstract and cannot be instantiated for queries.
`SingleBwTrack` and `PairedBwTrack` inherit `quantify_signal` and
`get_supported_quantification_type`.

## Example

```python
from RGTools import SingleBwTrack

track = SingleBwTrack("signal.bw")
value = track.count_single_region("chr1", 1000, 2000)
```

## Related formats or commands

- [BigWig signal format](../../formats/signal/bigwig.md)
