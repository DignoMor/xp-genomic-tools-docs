## Syntax

Parser-derived invocation for `GenomicElementTools export ExogeneousSequences`:

```text
GenomicElementTools export ExogeneousSequences [-h] --fasta_path FASTA_PATH --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--fasta_path` | yes | `str` | inapplicable | `none` | no | Path to the genome file. |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Fasta output file path. |
