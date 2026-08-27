# xp-genomic-tools

Regulatory genomic utilities for BED-like regions, sequences, motifs, and BigWig
tracks.

This site documents release **0.3.0a4**.

## What ships in 0.3.0a4

| Component | Kind | Role |
| --- | --- | --- |
| `RGTools` | Python library | Regions, FASTA, motifs, BigWig tracks, annotations |
| `GenomicElementTools` | CLI | Region transforms, signal counting, motifs, import/export, masks, TSS-relative selection and mutagenesis |
| `ExogeneousSequenceTools` | CLI | Assemble, mutate, and analyze exogenous (non-genome-anchored) sequences |
| `MotifTools` | CLI | Generate random/PWM sequences, enumerate barcodes, and transform motifs |

!!! warning "Alpha release"
    **0.3.0a4** is a pre-release. APIs and CLI flags may change. Pin the tag if
    you need a fixed cut.

`CountTableTools` is **not** included in this release.

## Where to start

1. Open [Get started](get-started/index.md) and pick the [Python](get-started/python-quickstart.md) or [CLI](get-started/cli-quickstart.md) quickstart
2. [Install](install.md) from the `0.3.0a4` code tag when you need setup detail
3. Skim [Concepts](concepts.md) and [Formats](formats.md)
4. Use the [CLI overview](cli/index.md) or [Library (RGTools)](library.md) for deeper lookup

Code repository: [DignoMor/xp-genomic-tools](https://github.com/DignoMor/xp-genomic-tools) (tag `0.3.0a4`).
