# BigWig signal profile

## Purpose

Define the supported read-only BigWig input used by `RGTools.BwTrack`.

## Availability

Supported in release `0.1.0a2` through `pyBigWig`; this is a binary input
profile, not a writer or a general BigWig validator.

## Inputs

A BigWig path with chromosome names matching query `chrom` strings. Queries use
BED zero-based half-open `[start, end)` coordinates.

## Types

Signal values are numeric; missing chromosomes and missing values become zero.

## Shapes

An interval query yields one value per base in the requested interval.

## Dtypes

Numeric BigWig values are exposed as NumPy vectors; NaNs are coerced to zero.

## Defaults

Track-level defaults are defined by `SingleBwTrack` and `PairedBwTrack`; see
the [BigWig Python reference](../../python/signal/bw-track.md).

## Choices

No file-level choices. Quantification choices are `raw_count`, `RPK`, and
`full_track`.

## Constraints

The profile is read/query only. Paired tracks use separate plus/minus files;
minus values are treated as absolute signal before optional orientation/sign
transformations.

## Outputs

The profile supplies a numeric vector to track quantification; it does not
write a derived BigWig.

## Ordering

Values follow genomic base order from `start` through `end - 1`.

## Side effects

Reading opens a pyBigWig resource and performs no file writes.

## Failures

Invalid paths, malformed files, or read failures propagate from `pyBigWig`.
