# `GenomicElementTools get_context_ge windowed_argmax`

## Availability

Supported in `GenomicElementTools` for release `0.3.0a4`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Select the maximum-stat context inside each query window on [BED-like region
rows](../../../formats/foundation/bed-like.md), using required
`--context_stat_path` aligned to context rows.

## Outputs

A context is eligible only when fully
contained (`start >= window.start`, `end <= window.end`). Ties choose earliest
context index; one context is written per query in query order.

## Failures

Empty eligible windows, stat/context mismatch, and malformed data
raise `ValueError` or a library error.

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

Run `GenomicElementTools get_context_ge windowed_argmax --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
