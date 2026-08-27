## Syntax

Parser-derived invocation for `GenomicElementTools export CountTable`:

```text
GenomicElementTools export CountTable [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --opath OPATH --sample_name SAMPLE_NAME --stat_npy STAT_NPY [--region_id_type {default,gene_symbol}]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Output path of the count table. |
| `--sample_name` | yes | `inapplicable` | inapplicable | `none` | yes | Sample name. |
| `--stat_npy` | yes | `inapplicable` | inapplicable | `none` | yes | Path to the stat npy file. |
| `--region_id_type` | no | `str` | `default`, `gene_symbol` | `default` | no | Type of the region id (default, gene_symbol). |
