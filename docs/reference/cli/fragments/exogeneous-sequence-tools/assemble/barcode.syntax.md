## Syntax

Parser-derived invocation for `ExogeneousSequenceTools assemble barcode`:

```text
ExogeneousSequenceTools assemble barcode [-h] --barcode_fasta BARCODE_FASTA --input_fasta INPUT_FASTA --input_class INPUT_CLASS --output_fasta OUTPUT_FASTA [--fasta_id_type {original,barcode}] --metadata_path METADATA_PATH [--barcode_method {5,3,5_3}]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--barcode_fasta` | yes | `inapplicable` | inapplicable | `none` | no | Path to the barcode fasta file. |
| `--input_fasta` | yes | `inapplicable` | inapplicable | `none` | yes | Path to the input fasta file.  |
| `--input_class` | yes | `inapplicable` | inapplicable | `none` | yes | Class of the input fasta file. |
| `--output_fasta` | yes | `inapplicable` | inapplicable | `none` | no | Path to the output fasta file. |
| `--fasta_id_type` | no | `inapplicable` | `original`, `barcode` | `original` | no | Type of the fasta id. |
| `--metadata_path` | yes | `inapplicable` | inapplicable | `none` | no | Path to the output metadata file. |
| `--barcode_method` | no | `inapplicable` | `5`, `3`, `5_3` | `5_3` | no | Method to use to add barcode to the exogeneous sequences. |
