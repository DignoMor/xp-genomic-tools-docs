## Syntax

Parser-derived invocation for `GenomicElementTools get_context_ge windowed_argmax`:

```text
GenomicElementTools get_context_ge windowed_argmax [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --context_file_path CONTEXT_FILE_PATH --context_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --context_stat_path CONTEXT_STAT_PATH --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--context_file_path` | yes | `str` | inapplicable | `none` | no | Path to the context region file. |
| `--context_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `none` | no | Type of the context region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--context_stat_path` | yes | `str` | inapplicable | `none` | no | Path to the context stat .npy file. |
| `--opath` | yes | `str` | inapplicable | `none` | no | Path to the output region file. |
