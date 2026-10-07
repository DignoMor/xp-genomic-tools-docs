## Syntax

Parser-derived invocation for `MotifTools dinucleotide_transversion`:

```text
MotifTools dinucleotide_transversion [-h] --motif_file MOTIF_FILE --motif_name MOTIF_NAME --output OUTPUT [--force] [--warn_score_cutoff WARN_SCORE_CUTOFF]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--motif_file` | yes | `inapplicable` | inapplicable | `none` | no | Input MEME motif collection file. |
| `--motif_name` | yes | `inapplicable` | inapplicable | `none` | no | Name of the motif used to derive the transversion target. |
| `--output` | yes | `inapplicable` | inapplicable | `none` | no | Output FASTA path, or '-' for stdout. |
| `--force` | no | `inapplicable` | inapplicable | `False` | no | Replace an existing output file. |
| `--warn_score_cutoff` | no | `float` | inapplicable | `0` | no | Heuristic source-motif score cutoff (finite real; default 0). Warn on stderr if the full-width target scores at or above this value on either strand. Diagnostics only; does not change FASTA. |
