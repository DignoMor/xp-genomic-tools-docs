# `GenomicElementTools export ExogenousSequences`

## Availability

Supported in `GenomicElementTools` for release `0.3.0a4`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Requires genome FASTA plus GE regions and `--opath`; writes region sequences as
FASTA using the [FASTA profile](../../formats/elements/fasta.md). Optional
`--output_orientation {genomic,strand}` (default `genomic`) controls sequence
orientation: genomic-forward, or region-strand orientation that reverse-complements
complete `-` records once. Optional `--record_id {coordinate,name}` (default
`coordinate`) selects FASTA IDs as `chrom:start-end` or the row-level name.
Strand and name modes require those fields on the selected region schema; IDs
must be unique under the chosen identity mode. Input row order is preserved.
Every interval must be fully contained in its chromosome
(`0 <= start < end <= chromosome_length`); missing chromosomes, invalid
intervals, unsupported modes, or invalid strand/name values fail before any
destination FASTA is created or replaced.

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

Argparse exits for missing required flags or invalid choices. Missing chromosomes,
intervals that violate BED containment, unsupported orientation/identity modes,
invalid strand or name values, and duplicate record IDs raise `ValueError`
without creating or replacing `--opath`.

## Example

Run `GenomicElementTools export ExogenousSequences --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
