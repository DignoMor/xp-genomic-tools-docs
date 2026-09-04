# `GenomicElementTools export bed6poly`

## Availability

Supported in `GenomicElementTools` for release `0.4.0a1`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Reads only `bed6` regions and writes a bed6+ polymorphism table to required
`--opath`. Optional `--genome_version` accepts `hg38`, `GRCh38`, `hg19`, or
`GRCh37` and defaults to `hg38`; optional `--rsid_not_found_handling` accepts
`raise` or `drop` and defaults to `raise`. See the [bed6poly format](../../formats/cli/genomic-element-tools/bed6poly.md).
RSIDs are resolved through Ensembl; `raise` propagates not-found/network errors,
while `drop` omits unresolved rows. Surviving rows retain input order.

## Inputs

See Purpose and the parser-derived options table.

## Types

Paths and schema keys are strings unless noted in Purpose.

## Shapes

Annotation arrays align by first dimension with region or sequence order.

## Dtypes

See linked format references and Purpose.

## Defaults

Parser defaults appear in the generated options table.

## Choices

Parser choices appear in the generated options table.

## Constraints

See Purpose and linked format references.

## Outputs

See Purpose for the serialized output contract.

## Ordering

Output rows retain input order unless stated otherwise in Purpose.

## Side effects

Reads declared inputs and writes declared outputs; inputs are not mutated.

## Failures

Argparse exits for missing required flags or invalid choices; runtime validation errors propagate from the implementation.

## Example

Run `GenomicElementTools export bed6poly --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
