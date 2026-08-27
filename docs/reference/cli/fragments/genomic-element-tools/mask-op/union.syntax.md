## Syntax

Parser-derived invocation for `GenomicElementTools mask_op union`:

```text
GenomicElementTools mask_op union [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --mask_npy MASK_NPY --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--mask_npy` | yes | `str` | inapplicable | `none` | yes | Path to input mask array (.npy or single-array .npz). Use multiple times. |
| `--opath` | yes | `str` | inapplicable | `none` | no | Output path for the resulting mask array (.npy). |
