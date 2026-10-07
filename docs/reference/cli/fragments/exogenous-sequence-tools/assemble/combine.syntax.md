## Syntax

Parser-derived invocation for `ExogenousSequenceTools assemble combine`:

```text
ExogenousSequenceTools assemble combine [-h] --input_fasta INPUT_FASTA --id_suffix ID_SUFFIX --output_fasta OUTPUT_FASTA
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--input_fasta` | yes | `inapplicable` | inapplicable | `none` | yes | Path to an input FASTA. Repeat once per collection, in output order. |
| `--id_suffix` | yes | `inapplicable` | inapplicable | `none` | yes | Literal suffix for IDs from the corresponding --input_fasta (same count). |
| `--output_fasta` | yes | `inapplicable` | inapplicable | `none` | no | Path to the output fasta file. |
