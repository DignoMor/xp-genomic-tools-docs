## Syntax

Parser-derived invocation for `GenomicElementTools import stat_list`:

```text
GenomicElementTools import stat_list [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --inpath INPATH --opath OPATH [--dtype {str,np.int32,np.int64,np.float32,np.float64}]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--inpath, -I` | yes | `inapplicable` | inapplicable | `none` | no | Input path of the list file containing one stat value per region. |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Output path of the region file. |
| `--dtype` | no | `str` | `str`, `np.int32`, `np.int64`, `np.float32`, `np.float64` | `str` | no | Dtype of the outputted array. |
