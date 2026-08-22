# Install

## Requirements

- Python **≥ 3.9**
- Runtime dependencies install with the package (`numpy`, `pandas`, `biopython`,
  `pyBigWig`, `requests`, `matplotlib`)

Notes:

- NumPy is constrained to **`>=1.24,<2`**
- `matplotlib` is required for `GenomicElementTools export Heatmap`

## Install from the 0.2.0a2 tag

There is no PyPI publish for this alpha. Install from the tagged code repository:

```bash
pip install "git+https://github.com/DignoMor/xp-genomic-tools.git@0.2.0a2"
```

Editable install from a local clone of the code repo:

```bash
git clone https://github.com/DignoMor/xp-genomic-tools.git
cd xp-genomic-tools
git checkout 0.2.0a2
pip install -e ".[dev]"
```

## Verify

```bash
GenomicElementTools --help
ExogeneousSequenceTools --help
MotifTools --help
```

You can also run:

```bash
python -m GenomicElementTools --help
python -m ExogeneousSequenceTools --help
python -m MotifTools --help
```

Console scripts are the primary entrypoints; module invocation is supported as
well.

## Quick Python check

```python
from RGTools import BedTable3, GenomicElements, MemeMotif, ListFile, SingleBwTrack
```
