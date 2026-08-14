# Ensembl SNP simple-info profile

## Purpose

Define the in-memory dictionary returned by Ensembl SNP coordinate bridging.

## Availability

Supported in release `0.1.0a2` as an API-derived schema, not a file format.

## Inputs

An Ensembl variation response selected by `EnsemblRestSearch`.

## Types

`chrom` and `bases` are strings; `start` and `end` are integers.

## Shapes

Exactly four fields: `chrom`, `start`, `end`, and `bases`.

## Dtypes

Inapplicable beyond the Python scalar types above.

## Defaults

None.

## Choices

`chrom` uses UCSC `chr` prefixes; `bases` is Ensembl's allele string.

## Constraints

Coordinates are BED 0-based half-open, converted from Ensembl 1-based closed
coordinates. The schema is not serialized to disk.

## Outputs

For example: `{"chrom": "chr1", "start": 100, "end": 101,
"bases": "A/G"}`.

## Ordering

Field ordering is not semantically significant.

## Side effects

None in the dictionary itself; obtaining it requires an Ensembl HTTP request.

## Failures

A variation without a chromosome mapping raises an exception; HTTP failures
propagate from `requests`.
