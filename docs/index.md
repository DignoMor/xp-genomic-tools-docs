# xp-genomic-tools

Regulatory genomic utilities for BED-like regions, sequences, motifs, and BigWig
tracks.

This site documents release **0.5.0a2**.

## Changes in 0.5.0a2

`MotifTools barcodes --exclude_rc_collisions` keeps the first accepted barcode
from each distinct reverse-complement pair in supplied-alphabet order. The
option retains palindromes and works with or without motif exclusions. When
enabled, it requires a nonempty unique uppercase A/C/G/T alphabet; subsets and
custom order are supported. Default enumeration stays the same.

The Python iterator exposes the matching keyword-only
`exclude_rc_collisions=False` option. See the
[barcode command](reference/cli/motif-tools/barcodes.md) and
[Python API](reference/python/motifs/motif-generation.md) for details.

## What ships in 0.5.0a2

| Component | Kind | Role |
| --- | --- | --- |
| `RGTools` | Python library | Regions, FASTA, motifs, BigWig tracks, annotations |
| `GenomicElementTools` | CLI | Region transforms, signal counting, motifs, import/export, masks, TSS-relative selection and mutagenesis |
| `ExogenousSequenceTools` | CLI | Assemble, mutate, and analyze exogenous (non-genome-anchored) sequences |
| `MotifTools` | CLI | Generate random/PWM sequences, enumerate barcodes, and transform motifs |

!!! warning "Alpha release"
    **0.5.0a2** is a pre-release. APIs and CLI flags may change. Pin the tag if
    you need a fixed cut.

`CountTableTools` is **not** included in this release.

## Where to start

1. Open [Get started](get-started/index.md) and pick the [Python](get-started/python-quickstart.md) or [CLI](get-started/cli-quickstart.md) quickstart
2. [Install](install.md) from the `0.5.0a2` code tag when you need setup detail
3. Skim [Concepts](concepts.md) and [Data formats](formats.md)
4. Use [Python API](library.md) or [CLI commands](reference/cli/index.md) for exact lookup; browse [How-to guides](guides/index.md) for workflows
5. Agents: start from the [Agent reference](agent-reference.md) HTML index or the compact [`llms.txt`](llms.txt) peer

Code repository: [DignoMor/xp-genomic-tools](https://github.com/DignoMor/xp-genomic-tools) (tag `0.5.0a2`).
