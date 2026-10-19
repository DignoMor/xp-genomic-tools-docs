# Adapter, concatenation, barcode, reverse-complement, and collection-stacking outputs

Assembly commands write ordinary FASTA records (no additional metadata).
`add_adapter` emits `left + input + right` and preserves input IDs; each
adapter file must contain exactly one record. `concat` performs paired
sequence joining: positional `seq5 + seq3` pairs and IDs selected by `5`, `3`,
or `5_3`.

`combine` performs collection stacking: records from each `--input_fasta` are
written unchanged, in command-line order and file order within each input.
Each `--input_fasta` requires a paired `--id_suffix` (empty string allowed)
appended to IDs with no extra separator. Output IDs must be unique; a count
mismatch, a duplicate ID, or an existing output path fails with `ValueError`
and does not replace the output file. An empty input contributes no records.

`reverse_complement` rewrites one exogenous FASTA: every record is
reverse-complemented under IUPAC DNA rules with letter case preserved.
Optional `--id_suffix` is appended to each ID with no extra separator.
Output IDs must be unique; a non-IUPAC symbol, a duplicate ID, or an existing
output path fails with `ValueError` and does not replace the output file.
An empty input writes an empty FASTA.

`barcode` consumes barcodes and input records in order. Its output is
`barcode + element`, `element + barcode`, identical barcodes at both ends, or
canonical B + element + reverse-complement(B) for `5_3_rc`. The default stays
`5_3`; `5_3_rc` is opt-in. The new mode and all-mode assigned-barcode
validation are available in reference release `0.5.0a1`. Assigned barcodes in
every mode must contain only A/C/G/T (case-insensitive); original letter case is retained. Invalid assigned
barcodes fail before either output is written. Unused barcodes and element
sequences are not checked by this rule. IDs are original element IDs
(`original`) or barcode sequences (`barcode`). Its metadata CSV has exactly
`barcode`, `class`, `elem_id`, `elem_seq` columns and follows the same order;
`barcode` stores canonical B and `elem_seq` matches FASTA.

For serialized `5_3_rc` constructs, compare the left terminal directly with B
and reverse-complement the right terminal before comparison, including after
whole-construct reversal. This identifies the canonical barcode but cannot
establish element orientation. Normalize only with known physical layout and
read orientation. Historical identical-terminal `5_3` libraries keep their
original interpretation.

## Purpose
Serialized outputs from FASTA assembly operations.
## Availability

Supported in the current reference release (`0.5.0a1`).

Available since `0.1.0a2`.

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
`5`, `3`, `5_3`, `5_3_rc`; `original`, `barcode`.
## Constraints
Adapters contain one record; barcodes cover elements. Assigned barcodes in
every barcode mode may contain only A/C/G/T; unused barcode records and
assembled element sequences are not subject to this validation.
## Outputs
FASTA and four-column metadata CSV.
## Ordering
Input and barcode consumption order.
## Side effects
Creates output files.
## Failures
Invalid choices, cardinality, or I/O fail. An assigned barcode containing a
non-A/C/G/T symbol raises `ValueError` before FASTA or metadata output is
created or changed.

## Related API and CLI

- [`ExogenousSequenceTools assemble`](../../../cli/exogenous-sequence-tools/assemble.md)
