## Syntax

Parser-derived invocation for `GenomicElementTools select_tss_relative_track`:

```text
GenomicElementTools select_tss_relative_track [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --track_npy TRACK_NPY --strand {+,-} --target_coord TARGET_COORD [--relaxation RELAXATION] --min_score MIN_SCORE [--track_window_size TRACK_WINDOW_SIZE] --coordinate_opath COORDINATE_OPATH --mask_opath MASK_OPATH [--force]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--track_npy` | yes | `str` | inapplicable | `none` | no | Path to aligned numeric track array (.npy or single-array .npz). |
| `--strand` | yes | `str` | `+`, `-` | `none` | no | Selected TSS strand: '+' uses fwdTSS; '-' uses revTSS. |
| `--target_coord` | yes | `int` | inapplicable | `none` | no | Nonzero TSS-relative coordinate to evaluate. |
| `--relaxation` | no | `int` | inapplicable | `0` | no | Nonnegative relaxation radius around target_coord (default 0). |
| `--min_score` | yes | `float` | inapplicable | `none` | no | Inclusive finite minimum score for a match. |
| `--track_window_size` | no | `int` | inapplicable | `1` | no | Scored window width in bases (default 1 for point tracks). |
| `--coordinate_opath` | yes | `str` | inapplicable | `none` | no | Output path for selected TSS-relative coordinates (.npy or .npz). |
| `--mask_opath` | yes | `str` | inapplicable | `none` | no | Output path for match mask (.npy or .npz). |
| `--force` | no | `inapplicable` | inapplicable | `False` | no | Replace existing coordinate/mask destinations after successful computation. |
