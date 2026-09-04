# `GenomicElementTools import allele_expanded_ES`

## Availability

Supported in `GenomicElementTools` for release `0.4.0a1`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Parse allele-expanded FASTA `--inpath` and emit regions
under `--anno_oheader`; optional parallel `--stat_name`, `--stat_npy`, and
`--stat_selection_method` lists must have equal lengths.

## Outputs

Writes sorted `.bed3` groups and optional `.ref.npy`
and `.alt.npy` stats. IDs encode `chrom_start_end_ref` or
`chrom_start_end_<pos>:<ref>2<alt>`; each group has exactly one reference.

## Failures

Bad headers, missing reference, unequal parallel lists, or invalid
selection methods raise `ValueError`.

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

Run `GenomicElementTools import allele_expanded_ES --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
