## Syntax

Parser-derived invocation for `GenomicElementTools export MaskedGE`:

```text
GenomicElementTools export MaskedGE [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --mask_npy MASK_NPY --opath OPATH [--anno_name ANNO_NAME] [--anno_npy ANNO_NPY] [--anno_type {track,stat,mask,array}] [--anno_oheader ANNO_OHEADER]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--mask_npy` | yes | `inapplicable` | inapplicable | `none` | no | Path to boolean mask annotation npy/npz file. |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Output path of the filtered GenomicElements. |
| `--anno_name` | no | `inapplicable` | inapplicable | `[]` | yes | Annotation name to export after masking. Can be specified multiple times. |
| `--anno_npy` | no | `inapplicable` | inapplicable | `[]` | yes | Path to annotation npy/npz file. Can be specified multiple times. |
| `--anno_type` | no | `inapplicable` | `track`, `stat`, `mask`, `array` | `[]` | yes | Annotation type for each annotation. Can be specified multiple times. |
| `--anno_oheader` | no | `str` | inapplicable | `none` | no | Output header for masked annotation files. |
