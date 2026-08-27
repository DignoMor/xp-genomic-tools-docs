# `GenomicElementTools bed2tssbed`

## Availability

Supported in `GenomicElementTools` for release `0.3.0a4`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Convert each [BED-like region row](../../../formats/foundation/bed-like.md) to
a one-base BED interval. `--output_site` is `TSS` (default) or `center`;
`--opath` is required.

## Constraints

TSS is `start` on `+` and `end - 1` on `-`; center is
`(start + end) // 2`. Non-coordinate columns are preserved and rows remain in
order. Output has `[site, site+1)` coordinates and the input schema.

## Failures

Missing/invalid strand for TSS and unknown output site follow the
legacy library failure (`UnboundLocalError` for those unresolved cases); parser
choice failures exit 2.

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

## Outputs

See Purpose for the serialized output contract.

## Ordering

Output rows retain input order unless stated otherwise in Purpose.

## Side effects

Reads declared inputs and writes declared outputs; inputs are not mutated.

## Example

Collapse stranded promoters to one-base TSS intervals:

```bash
GenomicElementTools bed2tssbed \
  --region_file_path promoters.bed6 \
  --region_file_type bed6 \
  --opath promoters.tss.bed3 \
  --output_site TSS
```

Each output row keeps non-coordinate columns from the input schema and uses
`[site, site+1)` coordinates at the transcription start site.
