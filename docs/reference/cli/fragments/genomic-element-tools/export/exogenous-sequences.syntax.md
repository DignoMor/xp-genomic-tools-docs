## Syntax

Parser-derived invocation for `GenomicElementTools export ExogenousSequences`:

```text
GenomicElementTools export ExogenousSequences [-h] --fasta_path FASTA_PATH --region_file_path REGION_FILE_PATH (--region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} | --region_file_schema SCHEMA_PATH) [--output_orientation {genomic,strand}] [--record_id {coordinate,name}] --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--fasta_path` | yes | `str` | inapplicable | `none` | no | Path to the genome file. |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | no | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `none` | no | Named region format (predefined schema). Valid named formats: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph']. |
| `--region_file_schema` | no | `str` | inapplicable | `none` | no | Path to a version-1 region-schema JSON file describing a custom BED3+ or BED6+ table. Relative paths resolve from the current working directory. Mutually exclusive with --region_file_type. |
| `--output_orientation` | no | `inapplicable` | `genomic`, `strand` | `genomic` | no | Orientation of exported FASTA records: 'genomic' (default, genomic-forward) or 'strand' (region-strand orientation from the row-level strand field). |
| `--record_id` | no | `inapplicable` | `coordinate`, `name` | `coordinate` | no | FASTA record ID mode: 'coordinate' (default, chrom:start-end) or 'name' (row-level name field). |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Fasta output file path. |
