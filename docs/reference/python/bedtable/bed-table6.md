# `BedTable6`
## Status
Supported for the current reference release.
## Purpose
Extend BED3 with `name`, `score`, and `strand`.
## Canonical import
```python
from RGTools import BedTable6
```
## Signature
::: RGTools.BedTable.BedTable6
    options:
      members:
        - __init__
        - column_names
        - column_types
        - get_region_names
        - get_region_scores
        - get_region_strands
        - region_subset
        - load_from_BedTable3
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_" 
## Parameters
Construct with the same keyword options as `BedTable3`. Use `get_region_names`, `get_region_scores`, `get_region_strands`, and `load_from_BedTable3`.
## Return or yield behavior
Getter arrays and `BedTable6` instances; inherited methods return the concrete class.
## Raised exceptions
Inherited `BedTableLoadException`, `ValueError`, and I/O failures apply.
## Constraints
`load_from_BedTable3` fills added columns with `.`. All inherited BedTable3 schema and overlap constraints apply.
## Ordering
Inherited sorting and row alignment apply.
## Side effects
Load methods replace table contents.
## Lifecycle behavior
Same in-memory lifecycle as `BedTable3`.
## Supported protocols and inheritance
Inherits supported `BedTable3` protocols and table operations not re-listed here.
## Example
```python
from RGTools import BedTable6

table = BedTable6()
table.load_from_file("regions.bed6")
names = table.get_region_names()
```
## Related formats or commands
- [bed6 format](../../formats/foundation/bed6.md)
