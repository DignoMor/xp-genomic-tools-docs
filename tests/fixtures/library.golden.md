# Library (RGTools)

`RGTools` is the importable Python library behind the CLIs. For end-to-end
workflows, prefer the [CLI pages](cli/index.md). This page is a light import
overview for **0.3.0a4**.

## Common imports

```python
from RGTools import (
    BedTable3,
    GenomicElements,
    ExogeneousSequences,
    MemeMotif,
    ListFile,
    SingleBwTrack,
)
```

Useful modules if you need them explicitly:

```python
import RGTools.BedTable
import RGTools.BwTrack
import RGTools.GTF_utils
import RGTools.SNP_utils
```

## What to use for what

| Need | Start with |
| --- | --- |
| Load / write BED-like regions | `BedTable3` / `BedTable6` / related classes |
| Regions + genome FASTA + annotations | `GenomicElements` |
| FASTA-only sequence sets | `ExogeneousSequences` |
| MEME motif files | `MemeMotif` |
| Anti-motif transforms | `RGTools.MotifGeneration.make_anti_motifs` |
| TSS-relative coordinates | `RGTools.TSSRelativeCoordinates` |
| BigWig signal | `SingleBwTrack` / paired track helpers |
| One-item-per-line lists | `ListFile` |

## CLI from Python

The CLI classes are importable if you need programmatic entry:

```python
from GenomicElementTools.cli import GenomicElementTools
from ExogeneousSequenceTools.cli import ExogeneousSequenceTools
from MotifTools.cli import MotifTools
```

For most users, the console scripts are enough.

## Detailed reference

### Element collections

- [Element collections overview](reference/python/elements/index.md)
- [`GeneralElements`](reference/python/general-elements/general-elements.md)
- [`GenomicElements`](reference/python/elements/genomic-elements.md)
- [`ExogeneousSequences`](reference/python/elements/exogeneous-sequences.md)

### Foundation

- [Exceptions](reference/python/foundation/exceptions.md)
- [Logger](reference/python/foundation/logger.md)
- [Utilities](reference/python/foundation/utils.md)
- [ListFile](reference/python/foundation/list-file.md)

### BedTable

- [BedRegion](reference/python/bedtable/bed-region.md)
- [BedTableIterator](reference/python/bedtable/iterator.md)
- [BedTable3](reference/python/bedtable/bed-table3.md)
- [BedTable6](reference/python/bedtable/bed-table6.md)
- [BedTable3Plus and BedTable6Plus](reference/python/bedtable/bed-table-plus.md)
- [BedTablePairEnd (experimental)](reference/python/bedtable/bed-table-pair-end.md)

### Motifs, signal, GTF, and SNP

- [MemeMotif](reference/python/motifs/meme-motif.md)
- [MotifGeneration](reference/python/motifs/motif-generation.md)
- [TSSRelativeCoordinates](reference/python/general-elements/tss-relative-coordinates.md)
- [BigWig signal tracks](reference/python/signal/bw-track.md)
- [GENCODE GTF streaming](reference/python/gtf/gtf-utils.md)
- [EnsemblRestSearch](reference/python/snp/ensembl-rest-search.md)
