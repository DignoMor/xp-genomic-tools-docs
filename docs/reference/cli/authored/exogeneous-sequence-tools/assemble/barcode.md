# `ExogeneousSequenceTools assemble barcode`

## Availability

Supported in `ExogeneousSequenceTools` for release `0.3.0a4`. Invoke through the installed `ExogeneousSequenceTools` console script.

## Purpose

Required repeatable flags: `--barcode_fasta`, `--input_fasta`, and
`--input_class`; required outputs: `--output_fasta` and `--metadata_path`.
`--barcode_method` choices `5`, `3`, `5_3` (default `5_3`) place the barcode
before, after, or on both sides. `--fasta_id_type` choices `original` and
`barcode` (default `original`) select element IDs or the full barcode list as
FASTA IDs. Barcodes are consumed in order across input FASTAs; input classes
are applied in corresponding input-file order. The total element count must
not exceed barcode count (`ValueError`). Metadata CSV columns are
`barcode,class,elem_id,elem_seq`, in consumption order. See the
[assembly output format](../../formats/cli/exogeneous-sequence-tools/assembly-outputs.md).

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

Run `ExogeneousSequenceTools assemble barcode --help` after installation to inspect required flags, then supply tiny synthetic inputs aligned with the linked format pages.
