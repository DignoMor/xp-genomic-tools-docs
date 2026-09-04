## Syntax

Parser-derived invocation for `GenomicElementTools count_single_bw`:

```text
GenomicElementTools count_single_bw [-h] --region_file_path REGION_FILE_PATH (--region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} | --region_file_schema SCHEMA_PATH) --bw_path BW_PATH [--quantification_type {raw_count,RPK,full_track}] --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | no | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `none` | no | Named region format (predefined schema). Valid named formats: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph']. |
| `--region_file_schema` | no | `str` | inapplicable | `none` | no | Path to a version-1 region-schema JSON file describing a custom BED3+ or BED6+ table. Relative paths resolve from the current working directory. Mutually exclusive with --region_file_type. |
| `--bw_path` | yes | `str` | inapplicable | `none` | no | Bigwig file path. |
| `--quantification_type` | no | `str` | `raw_count`, `RPK`, `full_track` | `raw_count` | no | Type of quantification. |
| `--opath` | yes | `str` | inapplicable | `none` | no | Output path for counting. |
