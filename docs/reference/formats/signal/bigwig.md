# BigWig signal profile

## Purpose

Define the read-only BigWig input consumed by `RGTools.BwTrack` and genomic
signal-counting CLIs.

## Availability

Supported in the current reference release (`0.3.0a4`).

Available since `0.1.0a2`.

## Inputs

Binary BigWig files opened through `pyBigWig`. Chromosome names in queries must
match BigWig chromosome keys. Interval queries use BED zero-based, half-open
`[start, end)` coordinates.

## Types

Signal values are numeric. Missing chromosomes and missing interval values are
represented as zero in query results.

## Shapes

An interval query yields one value per base from `start` through `end - 1`.

## Dtypes

Numeric BigWig values are exposed as NumPy vectors. NaNs are coerced to zero.

## Defaults

`SingleBwTrack` and `PairedBwTrack` define track-level quantification defaults;
see the [BigWig Python reference](../../python/signal/bw-track.md).

## Choices

Quantification modes are `raw_count`, `RPK`, and `full_track`. `PairedBwTrack`
accepts strand `.`, `+`, or `-` and optional minus-track `negative_mn` and
`flip_mn` transforms before quantification.

## Constraints

This profile is read/query only; no BigWig writer contract exists. Paired tracks
use separate plus and minus files. Minus values are made absolute, then
optionally negated or reversed. Unstranded (`.`) paired quantification combines
strands according to the selected mode.

## Outputs

Numeric vectors or scalar quantifications passed to callers. No derived BigWig
file is written.

## Ordering

Values follow genomic base order within the queried interval. `flip_mn=True`
reverses only the minus vector before quantification.

## Side effects

Construction opens read-only `pyBigWig` resources; object destruction closes
them. Queries perform no file writes.

## Failures

Invalid paths, malformed BigWig files, unsupported quantification type, invalid
padding policy, and invalid paired strand raise library exceptions. Open and
read errors propagate from `pyBigWig`.

## Related API and CLI

- [`BaseBwTrack`, `SingleBwTrack`, `PairedBwTrack`](../../python/signal/bw-track.md)
- [`GenomicElementTools count_single_bw`](../../cli/genomic-element-tools/count-single-bw.md)
- [`GenomicElementTools count_paired_bw`](../../cli/genomic-element-tools/count-paired-bw.md)
