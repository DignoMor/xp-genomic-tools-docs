# TSS-relative mutagenesis workflow

This guide composes `select_tss_relative_track`, mask filtering, and
`tss_relative_mutagenesis` into an end-to-end element-centric mutagenesis run.
For flag-level detail, see
[`tss_relative_mutagenesis`](../reference/cli/genomic-element-tools/index.md#tss_relative_mutagenesis)
and [`select_tss_relative_track`](../reference/cli/genomic-element-tools/index.md#select_tss_relative_track).

## Prerequisites

- Reference genome FASTA whose IDs match TREbed `chrom` values
- [TREbed](../reference/formats/foundation/trebed.md) region collection with
  usable `fwdTSS` / `revTSS` annotations for the strands you will mutate
- Per-base score track aligned to regions (for example motif-search output)
- Designed mutation targets as IUPAC DNA FASTAs (one file per round)

## 1. Select TSS-relative coordinates

For each strand and regulatory position you care about, run track selection to
emit a coordinate stat and a boolean mask. Coordinates use the shared
[TSS-relative coordinate system](../reference/python/general-elements/tss-relative-coordinates.md)
(no zero; `+1` is the selected TSS base).

```bash
GenomicElementTools select_tss_relative_track \
  --region_file_path regions.trebed \
  --region_file_type TREbed \
  --track_npy motif_scores.npy \
  --strand + \
  --target_coord -10 \
  --min_score 5.0 \
  --track_window_size 8 \
  --coordinate_opath coords_plus.npy \
  --mask_opath mask_plus.npy
```

Set `--track_window_size` to the scored window width (motif width for motif
tracks). Repeat for other strands or positions as needed. Rows with no
qualifying score receive coordinate `0` and mask `false`; exclude them before
mutagenesis (the mutagenesis command rejects coordinate zero).

## 2. Combine masks and subset inputs

Intersect selection masks when a region must pass every criterion:

```bash
GenomicElementTools mask_op intersect \
  --region_file_path regions.trebed \
  --region_file_type TREbed \
  --mask_npy mask_plus.npy \
  --mask_npy mask_minus.npy \
  --opath mask_combined.npy
```

Export the surviving TREbed rows and aligned coordinate stats together:

```bash
GenomicElementTools export MaskedGE \
  --region_file_path regions.trebed \
  --region_file_type TREbed \
  --fasta_path genome.fa \
  --mask_npy mask_combined.npy \
  --opath filtered.trebed \
  --anno_name coord_plus \
  --anno_npy coords_plus.npy \
  --anno_type stat \
  --anno_oheader filtered_coords_plus
```

Repeat `MaskedGE` exports or parallel annotation lists if multiple coordinate
stats must stay aligned with the filtered region set.

## 3. Declare mutation rounds

Create a tab-separated round manifest beside the per-round inputs. Paths are
resolved relative to the manifest directory.

```text
round_id	coordinate_stat	target_fasta	strand
core_plus	filtered_coords_plus.npy	targets_core.fa	+
distal_minus	filtered_coords_minus.npy	targets_distal.fa	-
```

Each round supplies:

- one integer `(N,1)` coordinate stat aligned to the **filtered** TREbed row order
- one target FASTA whose record IDs define [mutation target groups](../concepts.md#tss-relative-regulatory-terminology)
- one strand (`+` uses `fwdTSS`; `-` uses `revTSS`)

Every round must contain the same target-ID set. The first round's ID order
defines output sequence order.

Example `targets_core.fa`:

```text
>ref
ACGTACGT
>alt
TTTTTTTT
```

All targets in a round must share one length. Supply minus-strand targets in
strand-oriented form; the command reverse-complements them on `-` rounds.

## 4. Run mutagenesis

```bash
GenomicElementTools tss_relative_mutagenesis \
  --fasta_path genome.fa \
  --region_file_path filtered.trebed \
  --region_file_type TREbed \
  --round_manifest rounds.tsv \
  --output_dir mutagenesis_bundle \
  --write_replaced_windows
```

The command publishes a complete bundle under `mutagenesis_bundle/`:

```text
mutagenesis_bundle/
  sequences.fasta      # N regions × M target groups final sequences
  manifest.tsv         # one row per sequence per round
  replaced/
    core_plus.fasta    # optional audit: sequence removed before each round
    distal_minus.fasta
```

Sequence IDs look like `r000001|chr1:1000-2000|target=ref`. Use `--force` to
replace an existing bundle after a successful staging pass.

## 5. Use results downstream

- Import `sequences.fasta` into exogenous-sequence workflows if needed
- Join `manifest.tsv` on `sequence_id` for per-round provenance
- Compare `replaced/<round_id>.fasta` to final records when auditing overlaps

`ExogeneousSequenceTools mutagenesis` remains a separate one-round,
ordinary-offset tool for FASTA-only inputs; it is not a substitute for this
genomic TSS-relative workflow.
