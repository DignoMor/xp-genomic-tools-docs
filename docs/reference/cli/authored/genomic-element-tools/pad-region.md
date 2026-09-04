# `GenomicElementTools pad_region`

## Availability

Supported in `GenomicElementTools` for release `0.4.0a1`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Pad or shrink each [BED-like region row](../../../formats/foundation/bed-like.md)
by `--upstream_pad` and `--downstream_pad`; `--ignore_strand` controls
strand-aware interpretation. Select the region schema with exactly one of
`--region_file_type` (named format) or `--region_file_schema` (version-1
[region schema](../../../formats/foundation/region-schema.md) JSON path).

## Defaults

Invalid intervals use
`--method_resolving_invalid_region`: `raise`, `fallback` (default), or `drop`.
`--opath` is required. No FASTA is required.

## Outputs

Writes the same region schema, including ordered custom extras when a custom
schema was selected. Kept rows retain input order; `drop` reduces row count,
while `fallback` retains the original row. Invalid padding with `raise` raises
`InvalidBedRegionException`; malformed regions, invalid schemas, and parser
errors fail before `--opath` is created or replaced.

## Inputs

See Purpose and the parser-derived options table. Provide exactly one of
`--region_file_type` or `--region_file_schema`.

## Types

Paths and schema keys are strings unless noted in Purpose.

## Shapes

Annotation arrays align by first dimension with region or sequence order.

## Dtypes

See linked format references and Purpose.

## Choices

Parser choices appear in the generated options table. Named formats are listed
under `--region_file_type`; `--region_file_schema` accepts a filesystem path.

## Constraints

See Purpose and linked format references. Custom schemas do not acquire named
format semantics merely by reproducing columns.

## Ordering

Output rows retain input order unless stated otherwise in Purpose.

## Side effects

Reads declared inputs and writes declared outputs; inputs are not mutated.
Custom outputs do not publish a schema sidecar; reuse the original schema file.

## Failures

Argparse exits for missing required flags, invalid choices, or providing both
selectors; runtime validation errors propagate from the implementation before
output publication.

## Example

```bash
GenomicElementTools pad_region \
  --region_file_path regions.bed \
  --region_file_schema schema.json \
  --upstream_pad 2 \
  --downstream_pad 2 \
  --ignore_strand true \
  --opath padded.bed
```

`schema.json` may declare a BED6+ table, for example:

```json
{
  "schema_version": 1,
  "base_type": "bed6",
  "extra_columns": [
    {"name": "gene symbol (ref)", "dtype": "str"},
    {"name": "count", "dtype": "int"},
    {"name": "score_extra", "dtype": "float"}
  ]
}
```
