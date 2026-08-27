# Python quickstart: genomic elements

This walkthrough loads two synthetic genomic regions, explains how sequence order
follows the region table, and verifies one-hot array shape. It uses the
[`GenomicElements`](../reference/python/elements/genomic-elements.md) collection
against a tiny reference genome.

## Synthetic inputs

These files are **deliberate synthetic teaching assets**, not private test
fixtures. Download them from the built site or copy them from this repository:

| Asset | Role |
| --- | --- |
| [quickstart-synthetic-regions.bed3](assets/quickstart-synthetic-regions.bed3) | Two-region [bed3](../reference/formats/foundation/bed3.md) table (`chrB` then `chrA`) |
| [quickstart-synthetic-genome.fa](assets/quickstart-synthetic-genome.fa) | Matching [FASTA](../reference/formats/elements/fasta.md) reference (`chrA`, `chrB`) |

The BED table is intentionally **not** chromosome-sorted so you can see that
row order—not lexicographic `chrom` order—defines sequence and annotation
alignment.

## Load regions and inspect order

```python
from pathlib import Path

from RGTools import GenomicElements

assets = Path("assets")  # directory containing the downloaded synthetic files
regions = assets / "quickstart-synthetic-regions.bed3"
genome = assets / "quickstart-synthetic-genome.fa"

ge = GenomicElements(str(regions), "bed3", str(genome))
try:
    bed_table = ge.get_region_bed_table()
    print(bed_table.get_chrom_names().tolist())  # ['chrB', 'chrA']
    print(ge.get_all_region_seqs())              # ['GGGC', 'ACGT']
finally:
    ge.close()
```

Expected behavior for release **0.3.0a4**:

- Region row `0` is `chrB:1-5` → sequence `GGGC` (four bases from the `chrB` FASTA record)
- Region row `1` is `chrA:0-4` → sequence `ACGT`
- Sequences follow **BED row order**, not sorted chromosome names

## One-hot encoding shape

Homogeneous region lengths yield a bulk one-hot tensor with shape
`(num_regions, region_length, 4)`:

```python
ge = GenomicElements(str(regions), "bed3", str(genome))
try:
    one_hot = ge.get_all_region_one_hot()
    print(one_hot.shape)  # (2, 4, 4)
finally:
    ge.close()
```

Each `(region_length, 4)` slice is the per-base one-hot row for that region.
See [`GenomicElements.get_all_region_one_hot()`](../reference/python/elements/genomic-elements.md)
for ordering and ambiguity rules.

## Export exogenous sequences (optional)

To produce a FASTA file of region sequences for exogenous-sequence workflows,
call [`export_exogenous_sequences()`](../reference/python/elements/genomic-elements.md)
or use the CLI [`export ExogenousSequences`](../reference/cli/genomic-element-tools/export/exogenous-sequences.md)
described in the [CLI quickstart](cli-quickstart.md).

## Next steps

- [CLI quickstart](cli-quickstart.md) for the companion command-line path
- [Concepts: genomic elements vs exogenous sequences](../concepts.md#genomic-elements-vs-exogenous-sequences)
- [`GenomicElements` reference](../reference/python/elements/genomic-elements.md)
- [Genomic elements how-to guide](../guides/genomic-elements.md)
