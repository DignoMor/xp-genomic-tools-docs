## Syntax

Parser-derived invocation for `GenomicElementTools pad_region`:

```text
GenomicElementTools pad_region [-h] --region_file_path REGION_FILE_PATH (--region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} | --region_file_schema SCHEMA_PATH) --upstream_pad UPSTREAM_PAD --downstream_pad DOWNSTREAM_PAD --opath OPATH [--ignore_strand IGNORE_STRAND] [--method_resolving_invalid_region {raise,fallback,drop}]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | no | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `none` | no | Named region format (predefined schema). Valid named formats: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph']. |
| `--region_file_schema` | no | `str` | inapplicable | `none` | no | Path to a version-1 region-schema JSON file describing a custom BED3+ or BED6+ table. Relative paths resolve from the current working directory. Mutually exclusive with --region_file_type. |
| `--upstream_pad` | yes | `int` | inapplicable | `none` | no | Amount to extend to the upstream of the region. Positive value will expand the region and negative value will shrink the region. |
| `--downstream_pad` | yes | `int` | inapplicable | `none` | no | Amount to extend to the downstream of the region. Positive value will expand the region and negative value will shrink the region. |
| `--opath` | yes | `str` | inapplicable | `none` | no | Output path for the padded BED file |
| `--ignore_strand` | no | `str2bool` | inapplicable | `False` | no | Ignore the strand information in the input file.  |
| `--method_resolving_invalid_region` | no | `str` | `raise`, `fallback`, `drop` | `fallback` | no | Method to resolve invalid region after padding. |
