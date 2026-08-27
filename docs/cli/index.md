# CLI overview

Three console scripts ship with **0.3.0a4**. Browse by ownership in the
[grouped CLI index](../reference/cli/index.md) or look up a known invocation in
the [exact command-path index](../reference/cli/exact-path-index.md).

| Command | Purpose |
| --- | --- |
| [`GenomicElementTools`](GenomicElementTools.md) | Genome-anchored regions: pad, count BigWig, motifs, import/export, masks |
| [`ExogeneousSequenceTools`](ExogeneousSequenceTools.md) | FASTA sequence sets: assemble, mutagenesis, tracks, motifs |
| [`MotifTools`](MotifTools.md) | Motif generation: `random_seq`, `pwm_seq`, `barcodes`, `anti_motif` |

## Invocation

After [install](../install.md):

```bash
GenomicElementTools --help
ExogeneousSequenceTools --help
MotifTools --help
```

Module form also works:

```bash
python -m GenomicElementTools --help
python -m ExogeneousSequenceTools --help
python -m MotifTools --help
```

!!! tip "Flags"
    This documentation summarizes commands and nested format names.
    **`--help` on the installed build is authoritative** for flags and defaults.
