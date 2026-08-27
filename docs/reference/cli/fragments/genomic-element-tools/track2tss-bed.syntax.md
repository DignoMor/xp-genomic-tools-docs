## Syntax

Parser-derived invocation for `GenomicElementTools track2tss_bed`:

```text
GenomicElementTools track2tss_bed [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --track TRACK --opath OPATH [--output_site OUTPUT_SITE]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--track` | yes | `str` | inapplicable | `none` | no | The track npy file path. |
| `--opath` | yes | `str` | inapplicable | `none` | no | Output path for the TSS BED file |
| `--output_site` | no | `str` | inapplicable | `MaxAbsSig` | no | The site for output. [TSS] (MaxAbsSig) |
