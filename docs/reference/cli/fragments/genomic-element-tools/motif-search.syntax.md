## Syntax

Parser-derived invocation for `GenomicElementTools motif_search`:

```text
GenomicElementTools motif_search [-h] --fasta_path FASTA_PATH --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --motif_file MOTIF_FILE [--output_header OUTPUT_HEADER] [--estimate_background_freq ESTIMATE_BACKGROUND_FREQ] [--strand {+,-,both}]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--fasta_path` | yes | `str` | inapplicable | `none` | no | Path to the genome file. |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--motif_file` | yes | `inapplicable` | inapplicable | `none` | no | Motif file in MEME format. |
| `--output_header` | no | `str` | inapplicable | `motif_search` | no | Header for the output file. Output will be saved as <output_header>.<motif_name>.npy |
| `--estimate_background_freq` | no | `str2bool` | inapplicable | `True` | no | Estimate background frequency from the sequence. |
| `--strand` | no | `str` | `+`, `-`, `both` | `+` | no | Strand to search for motif matches. Choices: '+', '-', 'both'. |
