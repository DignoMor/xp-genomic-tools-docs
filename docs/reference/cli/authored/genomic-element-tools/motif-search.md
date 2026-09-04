# `GenomicElementTools motif_search`

## Availability

Supported in `GenomicElementTools` for release `0.4.0a1`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Score each FASTA-backed region against motifs in required
`--motif_file` (MEME profile). `--output_header` names outputs.

## Defaults

`--estimate_background_freq` defaults
true; `--strand` choices are `+`, `-`, `both` (default `+`). Motif files must
be valid supported MEME and sequences must be readable.

**Outputs / shapes / ordering.** For each motif, writes
`<output_header>.<motif_name>.npy`, a track annotation aligned to regions in
input order. Motif name sanitization follows the implementation's filename
rules. Missing chromosomes, invalid MEME, or incompatible motif lengths fail.

## Inputs

See Purpose and the parser-derived options table.

## Types

Paths and schema keys are strings unless noted in Purpose.

## Shapes

Annotation arrays align by first dimension with region or sequence order.

## Dtypes

See linked format references and Purpose.

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

Run `GenomicElementTools motif_search --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
