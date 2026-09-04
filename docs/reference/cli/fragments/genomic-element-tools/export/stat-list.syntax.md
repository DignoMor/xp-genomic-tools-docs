## Syntax

Parser-derived invocation for `GenomicElementTools export stat_list`:

```text
GenomicElementTools export stat_list [-h] --region_file_path REGION_FILE_PATH (--region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} | --region_file_schema SCHEMA_PATH) --stat_npy STAT_NPY --opath OPATH [--dtype {str,np.int32,np.int64,np.float32,np.float64}]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | no | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `none` | no | Named region format (predefined schema). Valid named formats: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph']. |
| `--region_file_schema` | no | `str` | inapplicable | `none` | no | Path to a version-1 region-schema JSON file describing a custom BED3+ or BED6+ table. Relative paths resolve from the current working directory. Mutually exclusive with --region_file_type. |
| `--stat_npy` | yes | `inapplicable` | inapplicable | `none` | no | Path to the stat npy/npz file. |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Output path of the list file. Use "-" or "stdout" to write to stdout. |
| `--dtype` | no | `str` | `str`, `np.int32`, `np.int64`, `np.float32`, `np.float64` | `str` | no | Dtype used to cast values before writing. |
