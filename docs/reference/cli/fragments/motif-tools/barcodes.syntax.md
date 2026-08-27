## Syntax

Parser-derived invocation for `MotifTools barcodes`:

```text
MotifTools barcodes [-h] --barcode_length BARCODE_LENGTH [--alphabet ALPHABET] [--motif_file MOTIF_FILE] [--exclude EXCLUDE] [--max_candidates MAX_CANDIDATES] --output OUTPUT [--force]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--barcode_length` | yes | `int` | inapplicable | `none` | no | Length of each enumerated barcode. |
| `--alphabet` | no | `inapplicable` | inapplicable | `ACGT` | no | Ordered alphabet for Cartesian enumeration (default ACGT). |
| `--motif_file` | no | `inapplicable` | inapplicable | `none` | no | MEME motif collection for exclusions. |
| `--exclude` | no | `inapplicable` | inapplicable | `none` | yes | Motif exclusion MOTIF=CUTOFF (repeatable). |
| `--max_candidates` | no | `int` | inapplicable | `1000000` | no | Maximum pre-exclusion candidate count before enumeration. |
| `--output` | yes | `inapplicable` | inapplicable | `none` | no | Output FASTA path, or '-' for stdout. |
| `--force` | no | `inapplicable` | inapplicable | `False` | no | Replace an existing output file. |
