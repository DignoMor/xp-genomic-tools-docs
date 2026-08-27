# `BedTableIterator`
## Status
Supported for the current reference release.
## Purpose
Iterate BedTable rows as `BedRegion` objects.
## Canonical import
```python
from RGTools.BedTable import BedTableIterator
```
## Signature
::: RGTools.BedTable.BedTableIterator
    options:
      members:
        - __iter__
        - __next__
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_" 
## Parameters
Constructed internally by BedTable `iter_regions`; callers receive the iterator from that method.
## Return or yield behavior
`__next__` yields the next `BedRegion`; `StopIteration` ends iteration.
## Raised exceptions
Propagates errors from the underlying table iteration.
## Constraints
Iteration follows the table's current row order.
## Ordering
Iteration order matches the backing table order.
## Side effects
None beyond reading the backing table.
## Lifecycle behavior
Iterator is exhausted after one pass unless recreated by `iter_regions`.
## Supported protocols and inheritance
Implements the iterator protocol (`__iter__`, `__next__`).
## Example
```python
for region in table.iter_regions():
    print(region["chrom"], region["start"], region["end"])
```
## Related formats or commands
- [BedTable3](bed-table3.md)
