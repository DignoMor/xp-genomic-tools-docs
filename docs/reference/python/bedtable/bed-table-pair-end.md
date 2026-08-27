# `BedTablePairEnd`
!!! warning "Experimental"
    This paired-end surface may change without a deprecation period when disclosed in release notes.

## Status
Experimental for the current reference release.
## Purpose
Represent paired intervals in the custom ten-column-plus layout; this is distinct from standard BEDPE.
## Canonical import
```python
from RGTools import BedTablePairEnd
```
## Signature
::: RGTools.BedTable.BedTablePairEnd
    options:
      members:
        - __init__
        - column_names
        - column_types
        - extra_column_names
        - extra_column_dtype
        - get_other_region_chroms
        - get_other_region_starts
        - get_other_region_ends
        - get_pair_names
        - get_pair_scores
        - get_region_strands
        - get_other_region_strands
        - get_region_extra_column
        - search_pair_extra_column
        - search_second_region
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_" 
## Parameters
Construct with optional extra columns. Fixed columns are `chrom,start,end,chrom2,start2,end2,name,score,strand,strand2`.
## Return or yield behavior
Pair coordinate, name, score, and strand getters return one array value per row; searches return matching indices.
## Raised exceptions
Schema or column mismatch raises `BedTableLoadException`; inherited filter and I/O failures apply.
## Constraints
Sorting is always enabled by first mate. The second-mate inverse index is rebuilt on load. This layout is custom and is not standard BEDPE.
## Ordering
First-mate lexicographic `(chrom,start,end)` ordering applies.
## Side effects
Loading replaces table contents and rebuilds the second-mate index; writing performs TSV I/O.
## Lifecycle behavior
Hold table state in memory until replaced by a load.
## Supported protocols and inheritance
Inherits supported `BedTable3` loading, filtering, and I/O operations not re-listed here.
## Example
```python
from RGTools import BedTablePairEnd

pairs = BedTablePairEnd()
pairs.load_from_file("pairs.tsv")
```
## Related formats or commands
- [BedTablePairEnd format](../../formats/foundation/pair-end.md)
