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
`fasta_path`. Paths are strings or path-like values. `region_file_type` is a
schema selector: a predefined named format from
`get_region_file_suffix2class_dict()`, or a path to a version-1 region-schema
JSON file. Predefined names take precedence over same-named files; use an
explicit relative or absolute path to select a shadowed schema file. Relative
schema paths resolve from the current working directory. Region order from the
file is preserved because sorting is disabled at load time.

## Return or yield behavior

The constructor returns a live collection object. Methods return region tables,
sequence lists, filtered collections, exported files, or inherited annotation
views as documented on each member below and on
[GeneralElements operations](../general-elements/load-mask-from-arr.md). Named
and custom selectors construct `BedTable3Plus` or `BedTable6Plus` tables,
including schemas with no extras.

## Raised exceptions

Unknown selectors raise `ValueError` stating that the value is neither a
supported named format nor a readable schema file. Malformed schema JSON and
schema contract violations raise contextual `ValueError` before rows load.
Wrong column counts raise `BedTableLoadException`. Missing chromosomes,
intervals that are not fully contained in their chromosome (`start < 0`,
`start >= end`, or `end` beyond chromosome length), incompatible merge inputs,
and annotation alignment failures raise `ValueError`. Index errors propagate
from underlying tables.

## Constraints

Region rows and every loaded annotation share first-dimension alignment. Merge
requires matching region type and FASTA path. `export_exogenous_sequences`
accepts optional `output_orientation` (`genomic`/`strand`) and `record_id`
(`coordinate`/`name`), refuses an existing output path, and validates the
complete region collection against the genome before publishing any FASTA.
Resolved schemas are snapshotted for the collection lifetime so filtering and
derived construction reuse extras without rereading the schema file.

## Ordering

Region row `i`, extracted sequence `i`, and annotation row `i` refer to the
same locus. Merge optionally sorts the combined table; otherwise loaded order
is preserved. Region-preserving filters keep declared extra columns, dtypes,
values, and annotation alignment.

## Side effects

Construction reads the region table and caches the FASTA path. Custom schema
files are read once at construction. Methods may read or write files
(`apply_logical_filter`, `export_exogenous_sequences`, merge output). Inherited
annotation loaders mutate in-memory arrays only until an explicit save.

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

Custom schema example:

```python
from RGTools import GenomicElements

# schema.json declares base_type bed6 and ordered str/int/float extras.
ge = GenomicElements("regions.bed", "schema.json", "genome.fa")
table = ge.get_region_bed_table()
print(table.extra_column_names)
ge.close()
```

## Related formats or commands

- [Region schema (version 1)](../../formats/foundation/region-schema.md)
- [FASTA region sequences](../../formats/elements/fasta.md)
- [BED-like region tables](../../formats/foundation/bed-like.md)
- [Annotation arrays](../../formats/elements/annotation-arrays.md)
- [`GenomicElementTools mask_op intersect`](../../cli/genomic-element-tools/mask-op/intersect.md)
