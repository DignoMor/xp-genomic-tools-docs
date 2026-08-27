## Syntax

Parser-derived invocation for `MotifTools pwm_seq`:

```text
MotifTools pwm_seq [-h] --motif_file MOTIF_FILE --motif_name MOTIF_NAME --num_sequences NUM_SEQUENCES [--seed SEED] --output OUTPUT [--force]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--motif_file` | yes | `inapplicable` | inapplicable | `none` | no | Input MEME motif collection file. |
| `--motif_name` | yes | `inapplicable` | inapplicable | `none` | no | Name of the motif to sample. |
| `--num_sequences` | yes | `int` | inapplicable | `none` | no | Number of sequences to generate. |
| `--seed` | no | `int` | inapplicable | `none` | no | Deterministic random seed (0 is valid). |
| `--output` | yes | `inapplicable` | inapplicable | `none` | no | Output FASTA path, or '-' for stdout. |
| `--force` | no | `inapplicable` | inapplicable | `False` | no | Replace an existing output file. |
