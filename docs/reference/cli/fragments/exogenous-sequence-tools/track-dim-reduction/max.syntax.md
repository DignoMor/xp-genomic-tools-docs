## Syntax

Parser-derived invocation for `ExogenousSequenceTools track_dim_reduction max`:

```text
ExogenousSequenceTools track_dim_reduction max [-h] --input_npy INPUT_NPY --output_npy OUTPUT_NPY [--search_range SEARCH_RANGE]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--input_npy` | yes | `inapplicable` | inapplicable | `none` | no | Path to the signal track npy file. |
| `--output_npy` | yes | `inapplicable` | inapplicable | `none` | no | Path to the output stat npy file. |
| `--search_range` | no | `str` | inapplicable | `none` | no | Search range for the signal track. Format: 'start,end'. If not provided, the whole signal track will be used. Range follows half-open and 0-index convention. |
