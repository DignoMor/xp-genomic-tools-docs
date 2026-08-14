# TREbed output

## Purpose

Region-table output from `GenomicElementTools export TREbed`, representing
transcription-regulatory-element/TSS annotations from plus/minus signal.

## Availability

Supported in release `0.1.0a2`.

## Inputs

BED-like GE regions and aligned plus (`--pl_sig_track`) and minus
(`--mn_sig_track`) signal tracks. For each region, the exporter takes
`argmax(abs(plus_track[i]))` and `argmax(abs(minus_track[i]))` (first maximum
wins), then adds each relative index to the region's BED `start`.

## Types

Headerless, tab-separated TREbed region table with registered BED-like schema.

## Shapes

Each signal track has first dimension `N`, the number of input regions; each
row is a numeric per-position vector. Empty vectors use relative position zero.

## Dtypes

Signal arrays are numeric. The output is BED3 plus `name` (string), `fwdTSS`
(integer), and `revTSS` (integer).

## Defaults

No FASTA or alternate output-format default applies; `--opath` is required.

## Choices

The region type and signal-track choices are those exposed by the parser;
TREbed is the fixed output format and has no alternate choice.

## Constraints

Coordinates are 0-based, half-open. `fwdTSS = start + argmax(abs(plus))` and
`revTSS = start + argmax(abs(minus))`; track first dimensions must align to the
region count. The generated `name` is exactly `chrom:start-end`.

## Outputs

The exporter writes a TREbed table to `--opath`.

## Ordering

Rows follow input region order; the exporter emits one row per input region.

## Side effects

Reads the regions and signal tracks and creates or replaces `--opath`.

## Failures

Missing files, invalid coordinates, shape mismatch, schema errors, and output
I/O failures raise the applicable library or I/O exception.
