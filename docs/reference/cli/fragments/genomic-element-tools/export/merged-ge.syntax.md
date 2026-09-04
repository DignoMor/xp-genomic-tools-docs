## Syntax

Parser-derived invocation for `GenomicElementTools export MergedGE`:

```text
GenomicElementTools export MergedGE [-h] --left_region_file_path LEFT_REGION_FILE_PATH --right_region_file_path RIGHT_REGION_FILE_PATH (--region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} | --region_file_schema SCHEMA_PATH) --anno_name ANNO_NAME --left_anno_path LEFT_ANNO_PATH --right_anno_path RIGHT_ANNO_PATH --anno_type {track,stat,mask,array} --oheader OHEADER
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--left_region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the left region file. |
| `--right_region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the right region file. |
| `--region_file_type` | no | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `none` | no | Named region format (predefined schema). Valid named formats: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph']. |
| `--region_file_schema` | no | `str` | inapplicable | `none` | no | Path to a version-1 region-schema JSON file describing a custom BED3+ or BED6+ table. Relative paths resolve from the current working directory. Mutually exclusive with --region_file_type. |
| `--anno_name` | yes | `inapplicable` | inapplicable | `none` | yes | Annotation name to merge. Can be specified multiple times. |
| `--left_anno_path` | yes | `inapplicable` | inapplicable | `none` | yes | Path to left annotation npy/npz file. Can be specified multiple times. |
| `--right_anno_path` | yes | `inapplicable` | inapplicable | `none` | yes | Path to right annotation npy/npz file. Can be specified multiple times. |
| `--anno_type` | yes | `inapplicable` | `track`, `stat`, `mask`, `array` | `none` | yes | Annotation type for each annotation. Can be specified multiple times. |
| `--oheader` | yes | `str` | inapplicable | `none` | no | Output header for merged files. |
