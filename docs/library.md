# Library (RGTools)

`RGTools` is the importable Python library behind the CLIs. For end-to-end
workflows, prefer the [CLI pages](cli/index.md). This page is a light import
overview for **0.1.0a1**.

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
| BigWig signal | `SingleBwTrack` / paired track helpers |
| One-item-per-line lists | `ListFile` |

## CLI from Python

The CLI classes are importable if you need programmatic entry:

```python
from GenomicElementTools.cli import GenomicElementTools
from ExogeneousSequenceTools.cli import ExogeneousSequenceTools
```

For most users, the console scripts are enough.

## Detailed reference

- [`GeneralElements.load_mask_from_arr`](reference/python/general-elements/load-mask-from-arr.md)
