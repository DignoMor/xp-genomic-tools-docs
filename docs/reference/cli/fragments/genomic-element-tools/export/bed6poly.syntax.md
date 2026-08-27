## Syntax

Parser-derived invocation for `GenomicElementTools export bed6poly`:

```text
GenomicElementTools export bed6poly [-h] --region_file_path REGION_FILE_PATH --region_file_type {bed6} [--genome_version {hg38,GRCh38,hg19,GRCh37}] [--rsid_not_found_handling {raise,drop}] --opath OPATH
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--region_file_path` | yes | `str` | inapplicable | `none` | no | Path to the input region file. |
| `--region_file_type` | yes | `str` | `bed6` | `bed6` | no | Type of the region file. |
| `--genome_version` | no | `str` | `hg38`, `GRCh38`, `hg19`, `GRCh37` | `hg38` | no | Genome version for Ensembl REST API lookup. |
| `--rsid_not_found_handling` | no | `str` | `raise`, `drop` | `raise` | no | Handling strategy when an rsid is not found in Ensembl REST API. |
| `--opath` | yes | `inapplicable` | inapplicable | `none` | no | Output path for the bed6poly file. |
