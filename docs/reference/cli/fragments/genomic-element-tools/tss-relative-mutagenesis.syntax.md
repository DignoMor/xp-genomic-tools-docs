## Syntax

Parser-derived invocation for `GenomicElementTools tss_relative_mutagenesis`:

```text
GenomicElementTools tss_relative_mutagenesis [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --fasta_path FASTA_PATH --round_manifest ROUND_MANIFEST --output_dir OUTPUT_DIR [--write_replaced_windows] [--force]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--fasta_path` | yes | `str` | inapplicable | `none` | no | Path to the genome file. |
| `--round_manifest` | yes | `str` | inapplicable | `none` | no | TSV round manifest with header round_id, coordinate_stat, target_fasta, strand. |
| `--output_dir` | yes | `str` | inapplicable | `none` | no | Output directory bundle for sequences.fasta and manifest.tsv. |
| `--write_replaced_windows` | no | `inapplicable` | inapplicable | `False` | no | Also write replaced/<round_id>.fasta audit FASTAs. |
| `--force` | no | `inapplicable` | inapplicable | `False` | no | Replace an existing output directory after successful staging. |
