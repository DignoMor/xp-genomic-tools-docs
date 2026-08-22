# GenomicElementTools

CLI for genome-anchored region workflows.

```bash
GenomicElementTools --help
GenomicElementTools <subcommand> --help
```

## Shared inputs

Most subcommands that load regions take:

| Flag | Meaning |
| --- | --- |
| `--region_file_path` | Path to the region TSV |
| `--region_file_type` | Type key (`bed3`, `bed6`, `narrowPeak`, …) |

Commands that need sequence also take:

| Flag | Meaning |
| --- | --- |
| `--fasta_path` | Genome FASTA (IDs must match `chrom`) |

See [Concepts](../concepts.md) and [Formats](../formats.md).

## Command groups

### Region transforms

| Command | Nested | Role |
| --- | --- | --- |
| `pad_region` | — | Pad regions while preserving GenomicElements order |
| `bed2tssbed` | — | Convert BED to TSS BED |
| `track2tss_bed` | — | Derive TSS BED from a signal track |
| `get_context_ge` | `nearest`, `windowed_argmax` | Context windows around regions |

### BigWig counting

| Command | Role |
| --- | --- |
| `count_single_bw` | Quantify one BigWig over regions → `.npy` / `.npz` |
| `count_paired_bw` | Same for plus/minus paired BigWigs |

### Sequence and motif

| Command | Role |
| --- | --- |
| `onehot` | One-hot encode equal-length region sequences |
| `motif_search` | Search MEME motifs in region sequences |
| `filter_motif_score` | Filter motif search scores |

!!! warning
    Empty results from `filter_motif_score` can hit a known alpha edge case.
    See the [FAQ](../faq.md).

### Import / export

Nested under `import` / `export`:

**`import` formats (`informat`)**

- `stat_list`
- `allele_expanded_ES`

**`export` formats (`oformat`)**

- `stat_list`
- `ExogeneousSequences`
- `WTES`
- `allele_expanded_ES`
- `CountTable`
- `Heatmap`
- `ChromFilteredGE`
- `MaskedGE`
- `TREbed`
- `MergedGE`
- `bed6poly`

### Mask operations

| Command | Nested | Role |
| --- | --- | --- |
| `mask_op` | [`intersect`](../reference/cli/mask-op-intersect.md), `union`, `opposite` | Logical ops on mask arrays |

### TSS-relative selection

| Command | Role |
| --- | --- |
| `select_tss_relative_track` | Select a TSS-relative track score; emit coordinate + mask annotations |

## Examples

Pad regions (flags abbreviated; check `--help` for the full set):

```bash
GenomicElementTools pad_region \
  --region_file_path regions.bed \
  --region_file_type bed3 \
  --upstream_pad 100 \
  --downstream_pad 100 \
  --opath padded.bed
```

Count a single BigWig:

```bash
GenomicElementTools count_single_bw --help
```

Export region sequences to FASTA:

```bash
GenomicElementTools export ExogeneousSequences --help
```
