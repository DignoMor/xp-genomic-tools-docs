# `RGTools exceptions`
## Status
Supported for the current reference release.
## Purpose
Stable exception classes for foundation, GTF, and BedTable failures.
## Canonical import
```python
from RGTools.exceptions import (
    BedTableException,
    BedTableLoadException,
    InvalidBedRegionException,
    InvalidStrandnessException,
)
```
## Signature
Curated exception types rendered from the aligned release source:

::: RGTools.exceptions
    options:
      members:
        - RGToolsInternalException
        - GTFHandleFilterException
        - GTFRecordNoFeatureException
        - BedTableException
        - BedTableLoadException
        - InvalidBedRegionException
        - InvalidStrandnessException
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_" 
## Parameters
Constructors accept optional message arguments following Python's standard `Exception` convention.
## Return or yield behavior
Each constructor returns an exception instance carrying the supplied arguments.
## Raised exceptions
`BedTableLoadException` indicates schema or load-shape failure; `InvalidBedRegionException` indicates invalid padded coordinates; `InvalidStrandnessException` indicates missing or invalid strandness. GTF filter and record failures use the GTF-specific types.
## Constraints
Use the most specific class exposed by the failing operation. Human-readable messages are not compatibility guarantees.
## Ordering
Not applicable for this entry.
## Side effects
None.
## Lifecycle behavior
No explicit close or release contract; exceptions are raised and discarded by callers.
## Supported protocols and inheritance
`BedTableLoadException`, `InvalidBedRegionException`, and `InvalidStrandnessException` subclass `BedTableException`, which subclasses `RGToolsInternalException`.
## Example
```python
from RGTools.exceptions import BedTableLoadException

try:
    ...
except BedTableLoadException as exc:
    raise RuntimeError("region table failed to load") from exc
```
## Related formats or commands
- [GENCODE GTF streaming](../gtf/gtf-utils.md)
- [BedTable3](../bedtable/bed-table3.md)
