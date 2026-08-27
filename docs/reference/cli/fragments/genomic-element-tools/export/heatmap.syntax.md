## Syntax

Parser-derived invocation for `GenomicElementTools export Heatmap`:

```text
GenomicElementTools export Heatmap [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --track_npy TRACK_NPY --title TITLE --negative NEGATIVE [--absolute ABSOLUTE] [--per_track_max_percentile PER_TRACK_MAX_PERCENTILE] [--vmax_percentile VMAX_PERCENTILE] --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--track_npy` | yes | `inapplicable` | inapplicable | `none` | yes | Path to the track npy file. |
| `--title` | yes | `str` | inapplicable | `none` | yes | Title of the heatmap. |
| `--negative` | yes | `str2bool` | inapplicable | `none` | yes | Legacy magnitude-mode control: select the Blues palette and negate the mean profile when True, or Reds when False. Required for every track; ignored for signed (--absolute False) rendering. |
| `--absolute` | no | `str2bool` | inapplicable | `none` | yes | Whether to render the track by absolute magnitude (True) or as signed values (False). Omit to use magnitude mode for every track; when supplied, provide one value per track. Non-finite cells are masked in both modes; signed mode also treats shorter-row padding as missing. |
| `--per_track_max_percentile` | no | `int` | inapplicable | `99` | no | Percentile used to determine the maximum value per track. |
| `--vmax_percentile` | no | `int` | inapplicable | `50` | no | Percentile used to determine the vmax. |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Output path of the heatmap. |
