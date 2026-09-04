# `GenomicElementTools import stat_list`

## Availability

Supported in `GenomicElementTools` for release `0.4.0a1`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Read one value per region from required `--inpath` ListFile
and save required `--opath` (`.npy` or `.npz`) as stat `region_list`.

**Defaults / types / constraints.** `--dtype` defaults to `str`; choices are
`str`, `np.int32`, `np.int64`, `np.float32`, `np.float64`. List length must equal
`N`; suffix other than `.npy`/`.npz` raises `ValueError`.

## Outputs

One stat per input region, in order. Bad
length, conversion, list file, or suffix raises `ValueError`/I/O errors.

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

## Failures

Argparse exits for missing required flags or invalid choices; runtime validation errors propagate from the implementation.

## Example

Run `GenomicElementTools import stat_list --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
