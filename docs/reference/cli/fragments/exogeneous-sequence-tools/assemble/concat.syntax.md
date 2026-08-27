## Syntax

Parser-derived invocation for `ExogeneousSequenceTools assemble concat`:

```text
ExogeneousSequenceTools assemble concat [-h] --fasta5 FASTA5 --fasta3 FASTA3 --output_fasta OUTPUT_FASTA [--id_method {5,3,5_3}]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--fasta5` | yes | `inapplicable` | inapplicable | `none` | no | Path to the 5' fasta file. |
| `--fasta3` | yes | `inapplicable` | inapplicable | `none` | no | Path to the 3' fasta file. |
| `--output_fasta` | yes | `inapplicable` | inapplicable | `none` | no | Path to the output fasta file. |
| `--id_method` | no | `inapplicable` | `5`, `3`, `5_3` | `5_3` | no | Method to use to generate the id of the output fasta file. |
