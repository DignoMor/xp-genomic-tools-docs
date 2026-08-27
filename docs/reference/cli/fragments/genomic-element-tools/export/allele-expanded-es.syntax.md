## Syntax

Parser-derived invocation for `GenomicElementTools export allele_expanded_ES`:

```text
GenomicElementTools export allele_expanded_ES [-h] --fasta_path FASTA_PATH --region_file_path REGION_FILE_PATH --region_file_type {bed3,bed6,bed6gene,bed3gene,narrowPeak,TREbed,bedGraph} --inpath_polymorphisms INPATH_POLYMORPHISMS [--job_name JOB_NAME] --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--fasta_path` | yes | `str` | inapplicable | `none` | no | Path to the genome file. |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the region file. |
| `--region_file_type` | yes | `str` | `bed3`, `bed6`, `bed6gene`, `bed3gene`, `narrowPeak`, `TREbed`, `bedGraph` | `bed3` | no | Type of the region file. Valid types: ['bed3', 'bed6', 'bed6gene', 'bed3gene', 'narrowPeak', 'TREbed', 'bedGraph'] |
| `--inpath_polymorphisms` | yes | `str` | inapplicable | `none` | no | Input bed6+ polymorphism file with a bases column (e.g., REF/ALT1/ALT2). |
| `--job_name` | no | `str` | inapplicable | `none` | no | Optional job name for record keeping. |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Output path of the allele-expanded fasta file. |
