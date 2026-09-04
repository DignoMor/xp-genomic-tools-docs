## Syntax

Parser-derived invocation for `GenomicElementTools export TREbed`:

```text
GenomicElementTools export TREbed [-h] --region_file_path REGION_FILE_PATH (--region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} | --region_file_schema SCHEMA_PATH) --pl_sig_track PL_SIG_TRACK --mn_sig_track MN_SIG_TRACK --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | no | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `none` | no | Named region format (predefined schema). Valid named formats: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph']. |
| `--region_file_schema` | no | `str` | inapplicable | `none` | no | Path to a version-1 region-schema JSON file describing a custom BED3+ or BED6+ table. Relative paths resolve from the current working directory. Mutually exclusive with --region_file_type. |
| `--pl_sig_track` | yes | `inapplicable` | inapplicable | `none` | no | Path to plus strand GROcap/PROcap signal track npy/npz file. |
| `--mn_sig_track` | yes | `inapplicable` | inapplicable | `none` | no | Path to minus strand GROcap/PROcap signal track npy/npz file. |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Output path for the TREbed file. |
