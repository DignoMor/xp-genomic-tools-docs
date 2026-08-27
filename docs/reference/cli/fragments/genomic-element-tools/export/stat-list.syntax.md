## Syntax

Parser-derived invocation for `GenomicElementTools export stat_list`:

```text
GenomicElementTools export stat_list [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --stat_npy STAT_NPY --opath OPATH [--dtype {str,np.int32,np.int64,np.float32,np.float64}]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--stat_npy` | yes | `inapplicable` | inapplicable | `none` | no | Path to the stat npy/npz file. |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Output path of the list file. Use "-" or "stdout" to write to stdout. |
| `--dtype` | no | `str` | `str`, `np.int32`, `np.int64`, `np.float32`, `np.float64` | `str` | no | Dtype used to cast values before writing. |
