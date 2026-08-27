## Syntax

Parser-derived invocation for `ExogeneousSequenceTools motif_search`:

```text
ExogeneousSequenceTools motif_search [-h] --fasta FASTA --motif_file MOTIF_FILE --output_header OUTPUT_HEADER [--estimate_background_freq ESTIMATE_BACKGROUND_FREQ] [--reverse_complement REVERSE_COMPLEMENT]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--fasta` | yes | `inapplicable` | inapplicable | `none` | no | Path to the sequence fasta file. |
| `--motif_file` | yes | `str` | inapplicable | `none` | no | The file containing the motifs to search for. |
| `--output_header` | yes | `str` | inapplicable | `none` | no | The header of the output file. |
| `--estimate_background_freq` | no | `str2bool` | inapplicable | `True` | no | Estimate background frequency from the sequence. |
| `--reverse_complement` | no | `str2bool` | inapplicable | `False` | no | Reverse complement the sequence while matching for motifs. |
