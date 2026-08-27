# TSS-relative mutagenesis workflow

This guide composes element-centric TREbed selection, mask filtering, and
multi-round [`tss_relative_mutagenesis`](../reference/cli/genomic-element-tools/tss-relative-mutagenesis.md)
into an end-to-end run. Flag-level contracts live on the linked command pages;
this page keeps task order and canonical domain language aligned with
[Concepts](../concepts.md#tss-relative-regulatory-terminology).

## Prerequisites

- Reference genome FASTA whose IDs match [TREbed](../reference/formats/foundation/trebed.md) `chrom` values
- TREbed collection with usable `fwdTSS` / `revTSS` annotations for strands you will mutate
- Per-base score track aligned to regions (for example [`motif_search`](../reference/cli/genomic-element-tools/motif-search.md) output)
- Designed mutation targets as IUPAC DNA FASTAs (one file per **mutation round**)

## Domain terms used below

| Term | Role in this workflow |
| --- | --- |
| **TSS-relative coordinate** | Signed offset from the selected TSS (`+1` is the TSS base; zero is invalid). See [`TSSRelativeCoordinates`](../reference/python/general-elements/tss-relative-coordinates.md). |
| **Mutation round** | One manifest row: one coordinate stat, one target FASTA, one strand applied sequentially to every derived sequence. |
| **Mutation target group** | Cross-round trajectory for one target FASTA record ID; rounds join by ID, not file order. |
| **Replaced window** | Sequence removed immediately before a round inserts its target; optional audit FASTAs capture these windows. |

## 1. Select TSS-relative coordinates

Run [`select_tss_relative_track`](../reference/cli/genomic-element-tools/select-tss-relative-track.md)
for each strand and regulatory position you care about. The command emits a
coordinate stat and a boolean mask using the shared
[TSS-relative coordinate system](../reference/python/general-elements/tss-relative-coordinates.md).

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
tracks). Repeat for other strands or positions as needed.

**Missingness.** Rows with no qualifying score receive coordinate `0` and mask
`false`. Exclude them before mutagenesis —
[`tss_relative_mutagenesis`](../reference/cli/genomic-element-tools/tss-relative-mutagenesis.md)
rejects coordinate zero during preflight.

## 2. Combine masks and subset inputs

Intersect selection masks when a region must pass every criterion using
[`mask_op intersect`](../reference/cli/genomic-element-tools/mask-op/intersect.md):

```bash
GenomicElementTools mask_op intersect \
  --region_file_path regions.trebed \
  --region_file_type TREbed \
  --mask_npy mask_plus.npy \
  --mask_npy mask_minus.npy \
  --opath mask_combined.npy
```

Export surviving TREbed rows and aligned coordinate stats with
[`export MaskedGE`](../reference/cli/genomic-element-tools/export/masked-ge.md):

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

Create a tab-separated round manifest beside the per-round inputs. Paths resolve
relative to the manifest directory.

```text
round_id	coordinate_stat	target_fasta	strand
core_plus	filtered_coords_plus.npy	targets_core.fa	+
distal_minus	filtered_coords_minus.npy	targets_distal.fa	-
```

Each **mutation round** supplies:

- one integer `(N,1)` coordinate stat aligned to the **filtered** TREbed row order
- one target FASTA whose record IDs define **mutation target groups**
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
  sequences.fasta      # N regions × M mutation target groups final sequences
  manifest.tsv         # one row per sequence per mutation round
  replaced/
    core_plus.fasta    # optional audit: replaced window before each round
    distal_minus.fasta
```

Sequence IDs look like `r000001|chr1:1000-2000|target=ref`. Use `--force` to
replace an existing bundle after a successful staging pass.

## 5. Use results downstream

- Import `sequences.fasta` into exogenous-sequence workflows if needed
- Join `manifest.tsv` on `sequence_id` for per-round provenance
- Compare `replaced/<round_id>.fasta` to final records when auditing overlaps

[`ExogeneousSequenceTools mutagenesis`](../reference/cli/exogeneous-sequence-tools/mutagenesis.md)
remains a separate one-round, ordinary-offset tool for FASTA-only inputs; it is
not a substitute for this genomic TSS-relative workflow.

## Related reference

- [`TSSRelativeCoordinates`](../reference/python/general-elements/tss-relative-coordinates.md)
- [`select_tss_relative_track`](../reference/cli/genomic-element-tools/select-tss-relative-track.md)
- [`tss_relative_mutagenesis`](../reference/cli/genomic-element-tools/tss-relative-mutagenesis.md)
- [TREbed format](../reference/formats/foundation/trebed.md)
