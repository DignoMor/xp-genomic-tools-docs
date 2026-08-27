# `BedRegion`
## Status
Supported for the current reference release.
## Purpose
Represent one BED-like interval with `chrom`, `start`, `end`, and optional fields.
## Canonical import
```python
from RGTools.BedTable import BedRegion
```
## Signature
::: RGTools.BedTable.BedRegion
    options:
      members:
        - __init__
        - to_dict
        - get_fields
        - pad_region
        - __getitem__
        - __eq__
        - __lt__
        - __le__
        - __gt__
        - __ne__
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_" 
## Parameters
`BedRegion(chrom, start, end, **other_fields)`. Mapping access uses `region[field]`. `pad_region(upstream_padding, downstream_padding, ignore_strand=False)` creates a padded region.
## Return or yield behavior
`to_dict` returns a copy; `get_fields` returns field names; `pad_region` returns a new `BedRegion`. Comparison operators return booleans.
## Raised exceptions
Missing or invalid strand raises `InvalidStrandnessException`; invalid padded coordinates raise `InvalidBedRegionException`; unknown mapping keys raise `KeyError`.
## Constraints
Padding must leave `start < end` and `start >= 0`. Strand is `+` or `-`; `ignore_strand=True` treats the region as `+`.
## Ordering
Comparisons sort lexicographically by `(chrom, start, end)`.
## Side effects
No method mutates the source region.
## Lifecycle behavior
N/A.
## Supported protocols and inheritance
Supports mapping access via `__getitem__` and rich comparison operators.
## Example
```python
from RGTools.BedTable import BedRegion

region = BedRegion("chr1", 100, 200)
padded = region.pad_region(50, 50)
```
## Related formats or commands
- [bed3 format](../../formats/foundation/bed3.md)
