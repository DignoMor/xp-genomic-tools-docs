# bed6poly output

## Purpose

BED6-plus polymorphism output from `GenomicElementTools export bed6poly`.

## Availability

Supported in the current reference release (`0.3.0a4`).

Available since `0.1.0a2`.

## Inputs

`bed6` regions, a supported `--genome_version`, and RSIDs resolved through
Ensembl. The not-found policy is selected by `--rsid_not_found_handling`.

## Types

Headerless, tab-separated BED6-plus rows. The appended column is named
`polymorphism`; its value is copied from Ensembl's `bases` response field and
is a slash-separated allele string in returned order (for example `A/G` or
`A/G/TT`).

## Shapes

Each output row corresponds to one surviving input region and has BED6 columns
plus exactly one `polymorphism` field. A region may carry multiple slash-separated
alleles in that field.

## Dtypes

Chromosome/name/strand and `polymorphism` are textual; `polymorphism` is a scalar string,
while coordinates and scores use the registered BED6-compatible scalar types.

## Defaults

`--genome_version` defaults to `hg38` and `--rsid_not_found_handling` defaults
to `raise`; `--opath` is required.

## Choices

`--genome_version`: `hg38`, `GRCh38`, `hg19`, or `GRCh37`.
`--rsid_not_found_handling`: `raise` or `drop`.

## Constraints

Input must be `bed6`. Coordinates are BED 0-based, half-open. Ensembl lookup
must resolve each RSID unless `drop` is selected.

## Outputs

Writes the BED6-plus polymorphism table to `--opath`.

## Ordering

Surviving rows retain input order; `drop` removes only unresolved rows.

## Side effects

Performs network requests to Ensembl and creates or replaces `--opath`.

## Failures

Malformed BED6, unsupported genome version, network errors, and unresolved
variants fail under `raise`; unresolved variants are omitted under `drop`.

## Related API and CLI

- [`GenomicElementTools export bed6poly`](../../../cli/genomic-element-tools/export/bed6poly.md)
- [Ensembl SNP simple-info profile](../../snp/ensembl-simple-info.md)
