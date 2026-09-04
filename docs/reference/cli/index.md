# CLI command grouped index

Supported release `0.4.0a1`. Three installed console scripts own distinct genomic workflows. Browse by ownership, then open a tool landing for task-oriented groupings and per-command semantics.

## Genomic-element-centric: `GenomicElementTools`

Genome-anchored BED-like regions with aligned annotation arrays: quantify BigWig signal, pad regions, import and export element collections, boolean mask algebra, TSS-relative selection and mutagenesis, and motif scoring on extracted windows.

- Canonical landing: [`GenomicElementTools`](genomic-element-tools/index.md)
- Search terms: `GenomicElementTools`, `genomic-element-tools`
- Browse by task on the tool landing:
  - Region and signal
  - Sequence and motif
  - import
  - export
  - mask_op
  - get_context_ge

## Exogenous-sequence-centric: `ExogenousSequenceTools`

Ordered exogenous FASTA libraries with synthetic BED3 coordinates: assemble adapters and barcodes, generate tracks and stats, run indexed mutagenesis, search motifs across sequences, and reduce track dimensionality without a genome reference BED.

- Canonical landing: [`ExogenousSequenceTools`](exogenous-sequence-tools/index.md)
- Search terms: `ExogenousSequenceTools`, `exogenous-sequence-tools`
- Top-level command groups: `assemble`, `gen_track`, `motif_search`, `mutagenesis`, `onehot`, `print_stat`, `track_dim_reduction`

## Motif-centric: `MotifTools`

MEME motif generation and transformation: sample PWM or uniform sequences, enumerate barcode spaces, and derive inverse-weight motif collections. Motif scoring whose primary subject is a genomic-element or exogenous-sequence collection remains in the other console scripts.

- Canonical landing: [`MotifTools`](motif-tools/index.md)
- Search terms: `MotifTools`, `motif-tools`
- Top-level command groups: `anti_motif`, `barcodes`, `pwm_seq`, `random_seq`
