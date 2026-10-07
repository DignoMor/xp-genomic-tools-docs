## Syntax

Parser-derived invocation for `MotifTools dinucleotide_transversion`:

```text
MotifTools dinucleotide_transversion [-h] --motif_file MOTIF_FILE --motif_name MOTIF_NAME --output OUTPUT [--force]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--motif_file` | yes | `inapplicable` | inapplicable | `none` | no | Input MEME motif collection file. |
| `--motif_name` | yes | `inapplicable` | inapplicable | `none` | no | Name of the motif used to derive the transversion target. |
| `--output` | yes | `inapplicable` | inapplicable | `none` | no | Output FASTA path, or '-' for stdout. |
| `--force` | no | `inapplicable` | inapplicable | `False` | no | Replace an existing output file. |
