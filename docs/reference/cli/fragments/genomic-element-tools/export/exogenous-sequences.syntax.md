## Syntax

Parser-derived invocation for `GenomicElementTools export ExogenousSequences`:

```text
GenomicElementTools export ExogenousSequences [-h] --fasta_path FASTA_PATH --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} [--output_orientation {genomic,strand}] [--record_id {coordinate,name}] --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--fasta_path` | yes | `str` | inapplicable | `none` | no | Path to the genome file. |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--output_orientation` | no | `inapplicable` | `genomic`, `strand` | `genomic` | no | Orientation of exported FASTA records: 'genomic' (default, genomic-forward) or 'strand' (region-strand orientation from the row-level strand field). |
| `--record_id` | no | `inapplicable` | `coordinate`, `name` | `coordinate` | no | FASTA record ID mode: 'coordinate' (default, chrom:start-end) or 'name' (row-level name field). |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Fasta output file path. |
