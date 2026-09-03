# `GenomicElements`

## Status

Supported for the current reference release. See the site home page for the
bound release identity.

## Purpose

Combine a headerless typed region table with a genome FASTA and expose
region-aligned sequence extraction, annotation filtering, merge, and export
operations shared with `GeneralElements`.

## Canonical import

```python
from RGTools import GenomicElements
```

## Signature

Curated constructor and member signatures rendered from the aligned release
source:

::: RGTools.GenomicElements.GenomicElements
    options:
      members:
        - __init__
        - fasta_path
        - region_file_type
        - region_file_path
        - get_num_regions
        - get_region_file_suffix2class_dict
        - BedTable6Gene
        - BedTable3Gene
        - BedTableNarrowPeak
        - BedTableBedGraph
        - BedTableTREBed
        - merge_genomic_elements
        - export_exogenous_sequences
        - get_all_region_seqs
        - get_region_bed_table
        - apply_logical_filter
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_"

## Parameters

Constructor arguments are `region_file_path`, `region_file_type`, and
`fasta_path`. Paths are strings or path-like values. `region_file_type` must
be one of the keys returned by `get_region_file_suffix2class_dict()`. Region
order from the file is preserved because sorting is disabled at load time.

## Return or yield behavior

The constructor returns a live collection object. Methods return region tables,
sequence lists, filtered collections, exported files, or inherited annotation
views as documented on each member below and on
[GeneralElements operations](../general-elements/load-mask-from-arr.md).

## Raised exceptions

Invalid `region_file_type` raises `ValueError` during construction. Missing
chromosomes, intervals that are not fully contained in their chromosome
(`start < 0`, `start >= end`, or `end` beyond chromosome length), incompatible
merge inputs, and annotation alignment failures raise `ValueError`. Index errors
propagate from underlying tables.

## Constraints

Region rows and every loaded annotation share first-dimension alignment. Merge
requires matching region type and FASTA path. `export_exogenous_sequences`
accepts optional `output_orientation` (`genomic`/`strand`) and `record_id`
(`coordinate`/`name`), refuses an existing output path, and validates the
complete region collection against the genome before publishing any FASTA.

## Ordering

Region row `i`, extracted sequence `i`, and annotation row `i` refer to the
same locus. Merge optionally sorts the combined table; otherwise loaded order
is preserved.

## Side effects

Construction reads the region table and caches the FASTA path. Methods may read
or write files (`apply_logical_filter`, `export_exogenous_sequences`, merge
output). Inherited annotation loaders mutate in-memory arrays only until an
explicit save.

## Lifecycle behavior

Call `close()` (inherited) to release the cached FASTA index. The destructor
attempts best-effort cleanup. Prefer explicit `close()` in long-running scripts.

## Supported protocols and inheritance

`GenomicElements` subclasses `GeneralElements`. Supported inherited operations
include `get_region_seq`, `get_region_lens`, `get_all_region_one_hot`,
annotation load/save/getters, `apply_logical_filter`, `close`, and
`one_hot_encoding`. Parser assembly helpers and underscore-prefixed internals
are not part of the supported public surface.

## Example

```python
from RGTools import GenomicElements

ge = GenomicElements("regions.bed3", "bed3", "genome.fa")
print(ge.get_num_regions())
sequences = ge.get_all_region_seqs()
table = ge.get_region_bed_table()
ge.close()
```

## Related formats or commands

- [FASTA region sequences](../../formats/elements/fasta.md)
- [BED-like region tables](../../formats/foundation/bed-like.md)
- [Annotation arrays](../../formats/elements/annotation-arrays.md)
- [`GenomicElementTools mask_op intersect`](../../cli/genomic-element-tools/mask-op/intersect.md)
