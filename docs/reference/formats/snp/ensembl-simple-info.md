# Ensembl SNP simple-info profile

## Purpose

Define the in-memory dictionary returned by Ensembl SNP coordinate bridging in
`RGTools.SNP_utils`.

## Availability

Supported in the current reference release (`0.4.0a1`).

Available since `0.1.0a2`.

## Inputs

An Ensembl variation response selected by `EnsemblRestSearch` from a supported
genome build (`hg38`, `GRCh38`, `hg19`, or `GRCh37`). This is an API-derived
schema, not an on-disk file format.

## Types

`chrom` and `bases` are strings; `start` and `end` are integers.

## Shapes

Exactly four fields: `chrom`, `start`, `end`, and `bases`.

## Dtypes

Python scalar types only; no NumPy dtype applies to the dictionary itself.

## Defaults

No default allele ordering beyond Ensembl's returned `bases` string.

## Choices

`chrom` uses UCSC `chr` prefixes. `bases` is Ensembl's slash-separated allele
string (for example `A/G`).

## Constraints

Stored coordinates are BED 0-based half-open, converted from Ensembl 1-based
closed wire coordinates. Location queries pass 0-based `pos` to helpers, which
add one before the Ensembl request. The schema is not serialized to disk.

## Outputs

Example: `{"chrom": "chr1", "start": 100, "end": 101, "bases": "A/G"}`.

## Ordering

Field ordering in the dictionary is not semantically significant.

## Side effects

The dictionary itself has no side effects. Obtaining it requires an Ensembl HTTP
request at runtime. Documentation tests validate structure only and do not call
live Ensembl services.

## Failures

A variation without a chromosome mapping raises an exception. HTTP failures,
unsupported genome versions, and unresolved RSIDs propagate from the client or
from callers such as `GenomicElementTools export bed6poly` when
`--rsid_not_found_handling` is `raise`.

## Related API and CLI

- [`EnsemblRestSearch`](../../python/snp/ensembl-rest-search.md)
- [`GenomicElementTools export bed6poly`](../../cli/genomic-element-tools/export/bed6poly.md)
