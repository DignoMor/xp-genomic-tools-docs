# `GenomicElementTools export allele_expanded_ES`

## Availability

Supported in `GenomicElementTools` for release `0.4.0a1`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Requires genome, GE regions, polymorphism `--inpath_polymorphisms` (bed6+ bases
column), and `--opath`; optional `--job_name`. Writes TRE-centered reference/
alternate FASTA using the allele-expanded ID scheme above. Invalid bases,
coordinates, or unresolved variants fail.

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

Run `GenomicElementTools export allele_expanded_ES --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
