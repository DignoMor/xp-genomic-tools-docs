# Motif generation and search

This guide connects **motif-centric** generation with **element-centric** and
**exogenous-sequence-centric** motif search while keeping each operation on its
own CLI surface. Detailed contracts live on the linked API, command, and
[MEME format](../reference/formats/motifs/meme.md) pages — this page stays
task-oriented.

## Choose the right tool

| Task | Owner | Typical entrypoint |
| --- | --- | --- |
| Generate or transform motifs and synthetic sequences | **MotifTools** (motif-centric) | [`pwm_seq`](../reference/cli/motif-tools/pwm-seq.md), [`random_seq`](../reference/cli/motif-tools/random-seq.md) |
| Score genomic regions with motifs | **GenomicElementTools** (element-centric) | [`motif_search`](../reference/cli/genomic-element-tools/motif-search.md) |
| Score exogenous FASTA collections with motifs | **ExogenousSequenceTools** (exogenous-sequence-centric) | [`motif_search`](../reference/cli/exogenous-sequence-tools/motif-search.md) |

Python equivalents for motif objects and generation live under
[`MemeMotif`](../reference/python/motifs/meme-motif.md) and
[`MotifGeneration`](../reference/python/motifs/motif-generation.md).

## Synthetic teaching assets

These deliberate **synthetic** files are published with the site (not private
test fixtures):

| Asset | Role |
| --- | --- |
| [quickstart-synthetic-motif.meme](../get-started/assets/quickstart-synthetic-motif.meme) | Tiny [MEME](../reference/formats/motifs/meme.md) collection (`QUICKSTART_MOTIF`, width 3) |
| [quickstart-synthetic-regions.bed3](../get-started/assets/quickstart-synthetic-regions.bed3) | Two-region [bed3](../reference/formats/foundation/bed3.md) table for element-centric search |
| [quickstart-synthetic-genome.fa](../get-started/assets/quickstart-synthetic-genome.fa) | Matching reference [FASTA](../reference/formats/elements/fasta.md) |

## 1. Generate sequences from a motif (MotifTools)

Sample PWM draws with a fixed seed so outputs are reproducible:

```bash
MotifTools pwm_seq \
  --motif_file assets/quickstart-synthetic-motif.meme \
  --motif_name QUICKSTART_MOTIF \
  --num_sequences 2 \
  --seed 0 \
  --output pwm-sequences.fasta
```

Release **0.4.0a1** reproduces:

```text
>pwm_QUICKSTART_MOTIF_0
GCG
>pwm_QUICKSTART_MOTIF_1
ACG
```

For uniform random sequences (optionally with motif exclusions), use
[`MotifTools random_seq`](../reference/cli/motif-tools/random-seq.md) as shown in
the [CLI quickstart](../get-started/cli-quickstart.md).

**Determinism.** `--seed` controls an isolated generator; `0` is valid. Identical
inputs and seed reproduce FASTA bytes for a given release.

**Failures.** Invalid MEME input, unknown motif names, nonpositive counts, and
output-path conflicts fail before partial files are written. Random generation
with active motif exclusions can exhaust its attempt budget and raise
`SequenceGenerationExhaustedError` (see the command reference).

## 2. Search an exogenous FASTA collection

After generation, score the collection with the exogenous-sequence tool:

```bash
ExogenousSequenceTools motif_search \
  --fasta pwm-sequences.fasta \
  --motif_file assets/quickstart-synthetic-motif.meme \
  --output_header es_scores
```

This writes `es_scores.QUICKSTART_MOTIF.npy`, a `(N, L)` track aligned to input
sequence order (`N=2`, `L=3` for the example above). Interpretation details and
dtype rules are on the
[motif track output format](../reference/formats/cli/exogenous-sequence-tools/motif-outputs.md).

## 3. Search genomic regions instead

When sequences come from the reference genome, use the element-centric command on
the same synthetic inputs as the [Python quickstart](../get-started/python-quickstart.md):

```bash
GenomicElementTools motif_search \
  --fasta_path assets/quickstart-synthetic-genome.fa \
  --region_file_path assets/quickstart-synthetic-regions.bed3 \
  --region_file_type bed3 \
  --motif_file assets/quickstart-synthetic-motif.meme \
  --output_header ge_scores
```

Output tracks follow region row order with shape `(num_regions, region_length)`
for homogeneous regions (`(2, 4)` here). Use these tracks directly or feed them
into downstream element-centric steps such as
[`select_tss_relative_track`](../reference/cli/genomic-element-tools/select-tss-relative-track.md)
(see the [TSS-relative mutagenesis guide](tss-relative-mutagenesis.md)).

**Do not cross wires.** MotifTools generates sequences; it does not score region
or exogenous collections. Each `motif_search` command validates MEME input,
sequence readability, and compatible track lengths before writing `.npy` outputs.

## Next steps

- [Genomic elements workflow](genomic-elements.md) for load/inspect/export before motif scoring
- [MotifTools CLI reference](../reference/cli/motif-tools/index.md)
- [MEME format contract](../reference/formats/motifs/meme.md)
