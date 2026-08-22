# xp-genomic-tools

Regulatory genomic utilities for BED-like regions, sequences, motifs, and BigWig
tracks.

This site documents release **0.3.0a1**.

## What ships in 0.3.0a1

| Component | Kind | Role |
| --- | --- | --- |
| `RGTools` | Python library | Regions, FASTA, motifs, BigWig tracks, annotations |
| `GenomicElementTools` | CLI | Region transforms, signal counting, motifs, import/export, masks, TSS-relative selection and mutagenesis |
| `ExogeneousSequenceTools` | CLI | Assemble, mutate, and analyze exogenous (non-genome-anchored) sequences |
| `MotifTools` | CLI | Generate random/PWM sequences, enumerate barcodes, and transform motifs |

!!! warning "Alpha release"
    **0.3.0a1** is a pre-release. APIs and CLI flags may change. Pin the tag if
    you need a fixed cut.

`CountTableTools` is **not** included in this release.

## Where to start

1. [Install](install.md) from the `0.3.0a1` code tag
2. Skim [Concepts](concepts.md) and [Formats](formats.md)
3. Use the [CLI overview](cli/index.md), then the tool pages
4. For Python imports, see [Library (RGTools)](library.md)

Code repository: [DignoMor/xp-genomic-tools](https://github.com/DignoMor/xp-genomic-tools) (tag `0.3.0a1`).
