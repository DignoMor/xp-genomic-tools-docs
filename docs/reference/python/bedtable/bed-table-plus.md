# `BedTable3Plus and BedTable6Plus`
## Status
Supported for the current reference release.
## Purpose
Represent BED3 or BED6 plus caller-declared extra columns.
## Canonical import
```python
from RGTools import BedTable3Plus, BedTable6Plus
```
## Signature
::: RGTools.BedTable.BedTable3Plus
    options:
      members:
        - __init__
        - column_names
        - column_types
        - extra_column_names
        - extra_column_dtype
        - get_region_extra_column
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_"

::: RGTools.BedTable.BedTable6Plus
    options:
      members:
        - __init__
        - column_names
        - column_types
        - extra_column_names
        - extra_column_dtype
        - get_region_extra_column
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_" 
## Parameters
Construct with `extra_column_names`, `extra_column_dtype` (default all `str`), and `enable_sort`. Use inherited BedTable operations and `get_region_extra_column(column_name)`.
## Return or yield behavior
`get_region_extra_column` returns a NumPy array; inherited selection methods return the matching Plus class.
## Raised exceptions
Schema mismatch raises `BedTableLoadException`; unknown extra columns fail through validation.
## Constraints
Extra names and dtypes must be declared together and match the loaded schema.
## Ordering
Inherited lexicographic sorting applies when enabled.
## Side effects
Loads replace contents; reads do not mutate.
## Lifecycle behavior
Same in-memory lifecycle as the parent BedTable class.
## Supported protocols and inheritance
`BedTable6Plus` inherits `BedTable6` and `BedTable3Plus` inherits `BedTable3` supported operations.
## Example
```python
from RGTools import BedTable3Plus

table = BedTable3Plus(extra_column_names=["gene_symbol"], extra_column_dtype=[str])
table.load_from_file("regions.bed3gene")
```
## Related formats or commands
- [bed3gene format](../../formats/foundation/bed3gene.md)
- [bed6gene format](../../formats/foundation/bed6gene.md)
