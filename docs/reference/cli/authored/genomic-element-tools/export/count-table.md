# `GenomicElementTools export CountTable`

## Availability

Supported in `GenomicElementTools` for release `0.3.0a4`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Takes repeated parallel `--sample_name`/`--stat_npy` pairs, GE regions, and CSV
`--opath`; `--region_id_type` is `default` or `gene_symbol`. Writes a reusable
[CountTable](../../formats/cli/genomic-element-tools/counttable.md): header
contains samples, rows are regions, and values remain in region order. Pair
lengths, stat alignment, and CSV output errors fail.

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

Run `GenomicElementTools export CountTable --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
