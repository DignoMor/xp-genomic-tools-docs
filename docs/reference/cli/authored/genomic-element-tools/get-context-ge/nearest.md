# `GenomicElementTools get_context_ge nearest`

## Availability

Supported in `GenomicElementTools` for release `0.3.0a4`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

For each query region, select the closest same-chromosome
context from required `--context_file_path` / `--context_file_type`.

## Outputs

Output uses the context schema and one
selected context per query, in query order; distance is the minimum absolute
distance among endpoint pairs. `--opath` is required and no FASTA is needed.

## Failures

No context on a query chromosome raises `ValueError`; malformed
files and parser failures fail normally.

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

## Ordering

Output rows retain input order unless stated otherwise in Purpose.

## Side effects

Reads declared inputs and writes declared outputs; inputs are not mutated.

## Example

Run `GenomicElementTools get_context_ge nearest --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
