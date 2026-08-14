# CLI overview

Two console scripts ship with **0.1.0a2**:

| Command | Purpose |
| --- | --- |
| [`GenomicElementTools`](GenomicElementTools.md) | Genome-anchored regions: pad, count BigWig, motifs, import/export, masks |
| [`ExogeneousSequenceTools`](ExogeneousSequenceTools.md) | FASTA sequence sets: assemble, mutagenesis, tracks, motifs |

## Invocation

After [install](../install.md):

```bash
GenomicElementTools --help
ExogeneousSequenceTools --help
```

Module form also works:

```bash
python -m GenomicElementTools --help
python -m ExogeneousSequenceTools --help
```

!!! tip "Flags"
    This documentation summarizes commands and nested format names.
    **`--help` on the installed build is authoritative** for flags and defaults.
