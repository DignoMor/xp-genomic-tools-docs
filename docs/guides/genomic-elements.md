# Load, inspect, and export genomic elements

This guide walks through the common **element-centric** task of loading a region
collection against a reference genome, inspecting row-aligned sequences, and
exporting exogenous FASTA for downstream tools. For constructor semantics,
annotation rules, and every export variant, use the linked reference pages rather
than treating this page as a contract.

## Prerequisites

- A typed region table ([bed3](../reference/formats/foundation/bed3.md) or another
  supported key) whose `chrom` values match the reference FASTA
- A reference genome [FASTA](../reference/formats/elements/fasta.md)
- An installed `RGTools` release matching this site

The [Python quickstart](../get-started/python-quickstart.md) uses deliberate
synthetic assets you can download from `docs/get-started/assets/`.

## 1. Load a collection

Construct [`GenomicElements`](../reference/python/elements/genomic-elements.md)
with the region path, explicit type key, and genome path:

```python
from RGTools import GenomicElements

ge = GenomicElements(
    "quickstart-synthetic-regions.bed3",
    "bed3",
    "quickstart-synthetic-genome.fa",
)
```

Region row order is preserved at load time (`enable_sort=False`), so annotation
row `i`, extracted sequence `i`, and BED row `i` always refer to the same locus.

## 2. Inspect regions and sequences

```python
try:
    print(ge.get_num_regions())
    table = ge.get_region_bed_table()
    print(table.get_chrom_names().tolist())
    print(ge.get_all_region_seqs())
finally:
    ge.close()
```

For the quickstart synthetic inputs, expect two rows in file order (`chrB` then
`chrA`) and sequences `["GGGC", "ACGT"]`. Sequences follow **region-table
order**, not lexicographic chromosome sorting.

Optional inspection helpers on the same object include
[`get_region_bed_table()`](../reference/python/elements/genomic-elements.md),
[`get_all_region_one_hot()`](../reference/python/elements/genomic-elements.md),
and inherited annotation getters documented on
[`GeneralElements`](../reference/python/general-elements/general-elements.md).

## 3. Export exogenous sequences

Call [`export_exogenous_sequences()`](../reference/python/elements/genomic-elements.md)
to write region sequences as FASTA using the
[`ExogenousSequences`](../reference/python/elements/exogenous-sequences.md)
contract:

```python
ge = GenomicElements(
    "quickstart-synthetic-regions.bed3",
    "bed3",
    "quickstart-synthetic-genome.fa",
)
try:
    ge.export_exogenous_sequences("region-sequences.fasta")
finally:
    ge.close()
```

The CLI equivalent is
[`GenomicElementTools export ExogenousSequences`](../reference/cli/genomic-element-tools/export/exogenous-sequences.md),
shown step-by-step in the [CLI quickstart](../get-started/cli-quickstart.md).

Other [`export`](../reference/cli/genomic-element-tools/export.md) subcommands
produce filtered region tables, annotation sidecars, or specialized formats; link
to each command page instead of duplicating their contracts here.

## Next steps

- [TSS-relative mutagenesis workflow](tss-relative-mutagenesis.md) for TREbed-centric multi-round edits
- [Concepts: genomic elements vs exogenous sequences](../concepts.md#genomic-elements-vs-exogenous-sequences)
- [`GenomicElements` API reference](../reference/python/elements/genomic-elements.md)
