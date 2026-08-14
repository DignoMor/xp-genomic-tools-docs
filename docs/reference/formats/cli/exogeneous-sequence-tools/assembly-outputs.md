# Adapter, concatenation, and barcode outputs

Assembly commands write ordinary FASTA records (no additional metadata).
`add_adapter` emits `left + input + right` and preserves input IDs; each
adapter file must contain exactly one record. `concat` emits positional
`seq5 + seq3` pairs and IDs selected by `5`, `3`, or `5_3`.

`barcode` consumes barcodes and input records in order. Its output is
`barcode + element`, `element + barcode`, or both sides. IDs are original
element IDs (`original`) or barcode sequences (`barcode`). Its metadata CSV
has exactly `barcode`, `class`, `elem_id`, `elem_seq` columns and follows the
same order. Too few barcodes or invalid choices fail with `ValueError`.

## Purpose
Serialized outputs from FASTA assembly operations.
## Availability
Release `0.1.0a2`.
## Inputs
FASTA records, adapters, barcodes, and classes.
## Types
Sequence strings, IDs, and metadata CSV fields.
## Shapes
One output record per paired or consumed input.
## Dtypes
Text FASTA and CSV.
## Defaults
`5_3`; original IDs.
## Choices
`5`, `3`, `5_3`; `original`, `barcode`.
## Constraints
Adapters contain one record; barcodes cover elements.
## Outputs
FASTA and four-column metadata CSV.
## Ordering
Input and barcode consumption order.
## Side effects
Creates output files.
## Failures
Invalid choices, cardinality, or I/O fail.
