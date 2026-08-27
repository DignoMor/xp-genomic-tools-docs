## Syntax

Parser-derived invocation for `MotifTools random_seq`:

```text
MotifTools random_seq [-h] --sequence_length SEQUENCE_LENGTH --num_sequences NUM_SEQUENCES [--alphabet ALPHABET] [--motif_file MOTIF_FILE] [--exclude EXCLUDE] [--seed SEED] [--max_attempts MAX_ATTEMPTS] --output OUTPUT [--force]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--sequence_length` | yes | `int` | inapplicable | `none` | no | Length of each generated sequence. |
| `--num_sequences` | yes | `int` | inapplicable | `none` | no | Number of sequences to generate. |
| `--alphabet` | no | `inapplicable` | inapplicable | `ACGT` | no | Ordered alphabet for uniform sampling (default ACGT). |
| `--motif_file` | no | `inapplicable` | inapplicable | `none` | no | MEME motif collection for exclusions. |
| `--exclude` | no | `inapplicable` | inapplicable | `none` | yes | Motif exclusion MOTIF=CUTOFF (repeatable). |
| `--seed` | no | `int` | inapplicable | `none` | no | Deterministic random seed (0 is valid). |
| `--max_attempts` | no | `int` | inapplicable | `10000` | no | Maximum candidate attempts per output when exclusions are used. |
| `--output` | yes | `inapplicable` | inapplicable | `none` | no | Output FASTA path, or '-' for stdout. |
| `--force` | no | `inapplicable` | inapplicable | `False` | no | Replace an existing output file. |
