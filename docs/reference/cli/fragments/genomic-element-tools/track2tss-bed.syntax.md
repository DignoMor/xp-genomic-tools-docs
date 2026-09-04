## Syntax

Parser-derived invocation for `GenomicElementTools track2tss_bed`:

```text
GenomicElementTools track2tss_bed [-h] --region_file_path REGION_FILE_PATH (--region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} | --region_file_schema SCHEMA_PATH) --track TRACK --opath OPATH [--output_site OUTPUT_SITE]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | no | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `none` | no | Named region format (predefined schema). Valid named formats: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph']. |
| `--region_file_schema` | no | `str` | inapplicable | `none` | no | Path to a version-1 region-schema JSON file describing a custom BED3+ or BED6+ table. Relative paths resolve from the current working directory. Mutually exclusive with --region_file_type. |
| `--track` | yes | `str` | inapplicable | `none` | no | The track npy file path. |
| `--opath` | yes | `str` | inapplicable | `none` | no | Output path for the TSS BED file |
| `--output_site` | no | `str` | inapplicable | `MaxAbsSig` | no | The site for output. [TSS] (MaxAbsSig) |
