## Syntax

Parser-derived invocation for `GenomicElementTools import allele_expanded_ES`:

```text
GenomicElementTools import allele_expanded_ES [-h] --inpath INPATH --anno_oheader ANNO_OHEADER [--stat_name STAT_NAME] [--stat_npy STAT_NPY] [--stat_selection_method {max_abs_fc}]
```

### Options

| Flags | Required | Type | Choices | Default | Repeatable | Parser help |
| --- | --- | --- | --- | --- | --- | --- |
| `--inpath, -I` | yes | `inapplicable` | inapplicable | `none` | no | Input path of the allele-expanded FASTA file. |
| `--anno_oheader` | yes | `inapplicable` | inapplicable | `none` | no | Output header for generated files. |
| `--stat_name` | no | `inapplicable` | inapplicable | `[]` | yes | Name of stat annotation to import (append once per stat file). |
| `--stat_npy` | no | `inapplicable` | inapplicable | `[]` | yes | Path to stat npy/npz file aligned to FASTA entries (append once per stat_name). |
| `--stat_selection_method` | no | `inapplicable` | `max_abs_fc` | `[]` | yes | Method to pick a representative alternate stat per region. |
