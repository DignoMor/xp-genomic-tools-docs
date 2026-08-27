## Syntax

Parser-derived invocation for `GenomicElementTools count_paired_bw`:

```text
GenomicElementTools count_paired_bw [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --bw_pl BW_PL --bw_mn BW_MN [--override_strand OVERRIDE_STRAND] [--quantification_type {raw_count,RPK,full_track}] --negative_mn NEGATIVE_MN --flip_mn FLIP_MN --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--bw_pl` | yes | `str` | inapplicable | `none` | no | Plus strand bigwig file. |
| `--bw_mn` | yes | `str` | inapplicable | `none` | no | Minus strand bigwig file. |
| `--override_strand` | no | `str` | inapplicable | `none` | no | Override the strand information in the input file (None if use the input strand info). |
| `--quantification_type` | no | `str` | `raw_count`, `RPK`, `full_track` | `raw_count` | no | Type of quantification. |
| `--negative_mn` | yes | `str2bool` | inapplicable | `none` | no | Whether to output the minus strand signal as negative. |
| `--flip_mn` | yes | `str2bool` | inapplicable | `none` | no | If to flip the minus strand signal. |
| `--opath` | yes | `str` | inapplicable | `none` | no | Output path for counting. |
