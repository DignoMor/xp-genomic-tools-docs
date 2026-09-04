## Syntax

Parser-derived invocation for `GenomicElementTools mask_op union`:

```text
GenomicElementTools mask_op union [-h] --region_file_path REGION_FILE_PATH (--region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} | --region_file_schema SCHEMA_PATH) --mask_npy MASK_NPY --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | no | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `none` | no | Named region format (predefined schema). Valid named formats: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph']. |
| `--region_file_schema` | no | `str` | inapplicable | `none` | no | Path to a version-1 region-schema JSON file describing a custom BED3+ or BED6+ table. Relative paths resolve from the current working directory. Mutually exclusive with --region_file_type. |
| `--mask_npy` | yes | `str` | inapplicable | `none` | yes | Path to input mask array (.npy or single-array .npz). Use multiple times. |
| `--opath` | yes | `str` | inapplicable | `none` | no | Output path for the resulting mask array (.npy). |
