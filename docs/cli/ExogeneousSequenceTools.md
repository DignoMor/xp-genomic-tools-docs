# ExogeneousSequenceTools

CLI for exogenous (non-genome-anchored) FASTA sequence workflows.

```bash
ExogeneousSequenceTools --help
ExogeneousSequenceTools <subcommand> --help
```

!!! note "Spelling"
    The command name is **ExogeneousSequenceTools** (with that spelling).

## Shared inputs

Most subcommands take:

| Flag | Meaning |
| --- | --- |
| `--fasta` | Input sequence FASTA |

Some assemble / track commands take additional FASTA or `.npy` paths instead of
(or in addition to) `--fasta`. Use `--help` on the nested command.

## Command groups

### Assemble

| Command | Nested | Role |
| --- | --- | --- |
| `assemble` | `add_adapter` | Prepend/append adapter FASTAs |
| `assemble` | `concat` | Concatenate two FASTAs (`--fasta5` / `--fasta3`) |
| `assemble` | `barcode` | Attach barcodes and write metadata |

### Mutagenesis

| Command | Role |
| --- | --- |
| `mutagenesis` | Mutate bases at locations from a `.npy` using a target FASTA |

### Tracks and stats

| Command | Nested | Role |
| --- | --- | --- |
| `gen_track` | `single_loc` | Generate a signal track from locations |
| `track_dim_reduction` | `max`, `argmax`, `min`, `argmin` | Reduce track `.npy` along a search range |
| `print_stat` | — | Print region/stat summaries from an input `.npy` |

### Sequence and motif

| Command | Role |
| --- | --- |
| `onehot` | One-hot encode exogenous sequences |
| `motif_search` | Search MEME motifs in exogenous FASTA |

## Examples

Add adapters:

```bash
ExogeneousSequenceTools assemble add_adapter \
  --fasta inserts.fa \
  --left_adapter_fasta left.fa \
  --right_adapter_fasta right.fa \
  --output_fasta assembled.fa
```

Motif search:

```bash
ExogeneousSequenceTools motif_search --help
```

Track reduction:

```bash
ExogeneousSequenceTools track_dim_reduction max --help
```
