## Syntax

Parser-derived invocation for `GenomicElementTools filter_motif_score`:

```text
GenomicElementTools filter_motif_score [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --motif_search_npy MOTIF_SEARCH_NPY --output_header OUTPUT_HEADER --filter_base FILTER_BASE [--min_score MIN_SCORE] [--max_score MAX_SCORE]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--motif_search_npy` | yes | `inapplicable` | inapplicable | `none` | no | Numpy file containing motif search scores. |
| `--output_header` | yes | `inapplicable` | inapplicable | `none` | no | Output header for filtered GenomicElements bed file. |
| `--filter_base` | yes | `int` | inapplicable | `none` | no | Base index for filtering motif search scores. |
| `--min_score` | no | `float` | inapplicable | `-inf` | no | Minimum score for filtering motif search scores. |
| `--max_score` | no | `float` | inapplicable | `inf` | no | Maximum score for filtering motif search scores. |
