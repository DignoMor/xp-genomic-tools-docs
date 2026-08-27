## Syntax

Parser-derived invocation for `GenomicElementTools export WTES`:

```text
GenomicElementTools export WTES [-h] --fasta_path FASTA_PATH --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --num_replicates NUM_REPLICATES --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--fasta_path` | yes | `str` | inapplicable | `none` | no | Path to the genome file. |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--num_replicates` | yes | `int` | inapplicable | `none` | no | Number of replicates for each region sequence. |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Output path of the WTES fasta file. |
