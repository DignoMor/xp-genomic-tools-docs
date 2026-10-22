# `ExogenousSequenceTools assemble barcode`

## Availability

The barcode command is available through the installed `ExogenousSequenceTools`
console script. The `5_3_rc` mode and assigned-barcode alphabet restriction are
available in release `0.5.0a2`.

## Purpose

Required repeatable flags: `--barcode_fasta`, `--input_fasta`, and
`--input_class`; required outputs: `--output_fasta` and `--metadata_path`.
`--barcode_method` choices `5`, `3`, `5_3`, and `5_3_rc` (default `5_3`)
place the barcode before, after, identically on both sides, or as canonical B
at the left and its reverse complement at the right. The `5_3_rc` mode is
opt-in; existing modes keep their historical sequences. Assigned barcodes in
every mode must contain only A/C/G/T, in either case; input case is preserved.
Unused barcode records are ignored by this validation, and element sequences
keep their existing alphabet handling. Invalid assigned barcodes raise
`ValueError` before either output is created or changed. `--fasta_id_type` choices `original` and
`barcode` (default `original`) select element IDs or the full barcode list as
FASTA IDs. Barcodes are consumed in order across input FASTAs; input classes
are applied in corresponding input-file order. The total element count must
not exceed barcode count (`ValueError`). Metadata CSV columns are
`barcode,class,elem_id,elem_seq`, in consumption order; `barcode` remains the
canonical input B and `elem_seq` matches the FASTA sequence. See the
[assembly output format](../../formats/cli/exogenous-sequence-tools/assembly-outputs.md).

For a `5_3_rc` construct in its serialized orientation, compare the left
terminal directly with canonical B and reverse-complement the right terminal
before comparison. Apply the same terminal rule after reversing the whole
construct. This preserves barcode identity but does not reveal the element's
orientation. Normalize observations only when the physical library layout and
read orientation are known. Historical `5_3` libraries have identical terminal
barcodes and retain their historical interpretation; do not apply the new
layout rule to them.

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

Example: for B=`AAGC` and element=`CCAA`, `--barcode_method 5_3_rc` emits
`AAGCCCAAGCTT`; its whole-construct reverse complement is
`AAGCTTGGGCTT`. The canonical left terminal remains `AAGC` in either
orientation after layout-aware normalization.

**Compatibility.** The new construction is opt-in and the default remains
`5_3`. The A/C/G/T restriction applies to assigned barcodes in existing modes
too; ambiguous or unsupported assigned barcode symbols previously accepted
are now rejected. Unused pool records are unaffected.
