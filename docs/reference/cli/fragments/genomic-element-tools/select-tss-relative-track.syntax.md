## Syntax

Parser-derived invocation for `GenomicElementTools select_tss_relative_track`:

```text
GenomicElementTools select_tss_relative_track [-h] --region_file_path REGION_FILE_PATH (--region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} | --region_file_schema SCHEMA_PATH) --track_npy TRACK_NPY --strand {+,-} --target_coord TARGET_COORD [--relaxation RELAXATION] --min_score MIN_SCORE [--track_window_size TRACK_WINDOW_SIZE] --coordinate_opath COORDINATE_OPATH --mask_opath MASK_OPATH [--force]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | no | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `none` | no | Named region format (predefined schema). Valid named formats: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph']. |
| `--region_file_schema` | no | `str` | inapplicable | `none` | no | Path to a version-1 region-schema JSON file describing a custom BED3+ or BED6+ table. Relative paths resolve from the current working directory. Mutually exclusive with --region_file_type. |
| `--track_npy` | yes | `str` | inapplicable | `none` | no | Path to aligned numeric track array (.npy or single-array .npz). |
| `--strand` | yes | `str` | `+`, `-` | `none` | no | Selected TSS strand: '+' uses fwdTSS; '-' uses revTSS. |
| `--target_coord` | yes | `int` | inapplicable | `none` | no | Nonzero TSS-relative coordinate to evaluate. |
| `--relaxation` | no | `int` | inapplicable | `0` | no | Nonnegative relaxation radius around target_coord (default 0). |
| `--min_score` | yes | `float` | inapplicable | `none` | no | Inclusive finite minimum score for a match. |
| `--track_window_size` | no | `int` | inapplicable | `1` | no | Scored window width in bases (default 1 for point tracks). |
| `--coordinate_opath` | yes | `str` | inapplicable | `none` | no | Output path for selected TSS-relative coordinates (.npy or .npz). |
| `--mask_opath` | yes | `str` | inapplicable | `none` | no | Output path for match mask (.npy or .npz). |
| `--force` | no | `inapplicable` | inapplicable | `False` | no | Replace existing coordinate/mask destinations after successful computation. |
