## Syntax

Parser-derived invocation for `GenomicElementTools export ChromFilteredGE`:

```text
GenomicElementTools export ChromFilteredGE [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --chrom_size CHROM_SIZE --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--chrom_size` | yes | `inapplicable` | inapplicable | `none` | no | Chromosome size file. |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Output path of the filtered GenomicElements. |
