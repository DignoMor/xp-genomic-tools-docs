# `BedTable3`
## Status
Supported for the current reference release.
## Purpose
Manage headerless BED3 tables with `chrom`, `start`, and `end` columns.
## Canonical import
```python
from RGTools import BedTable3
```
## Signature
::: RGTools.BedTable.BedTable3
    options:
      members:
        - __init__
        - column_names
        - column_types
        - extra_column_names
        - extra_column_dtype
        - load_from_file
        - load_from_dataframe
        - load_from_bed_regions
        - apply_logical_filter
        - region_subset
        - to_dataframe
        - write
        - get_chrom_names
        - get_start_locs
        - get_end_locs
        - get_region_by_index
        - iter_regions
        - search_region
        - concat
        - subset_by_index
        - copy
        - __len__
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_" 
## Parameters
`BedTable3(enable_sort=True)`; load from TSV, pandas DataFrame, or `BedRegion` list.
## Return or yield behavior
Load and write mutate or serialize the table; selection, copy, and concat return new tables. `len(table)` is row count. Coordinate getters return NumPy arrays.
## Raised exceptions
Column or schema mismatch raises `BedTableLoadException`; non-boolean or wrong-length filters raise `ValueError`; I/O errors propagate.
## Constraints
Files are tab-separated and headerless. `region_subset` returns fully contained regions. `search_region` requires at least `overlapping_base` overlapping bases.
## Ordering
Sorting uses lexicographic `(chrom, start, end)` when enabled; disabling preserves loaded order.
## Side effects
Load replaces contents; write performs file or stream I/O; no handles remain open after operations.
## Lifecycle behavior
Hold table state in memory until replaced by a load or reassigned.
## Supported protocols and inheritance
Supports `len()` and returns `BedTable3` instances from copy-like operations.
## Example
```python
from RGTools import BedTable3

table = BedTable3(enable_sort=False)
table.load_from_file("regions.bed3")
print(len(table))
```
## Related formats or commands
- [bed3 format](../../formats/foundation/bed3.md)
- [BED-like region tables](../../formats/foundation/bed-like.md)
