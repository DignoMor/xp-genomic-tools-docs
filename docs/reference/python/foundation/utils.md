# `RGTools.utils`
## Status
Supported for the current reference release.
## Purpose
Expose string conversion, reverse-complement, and JSON encoding helpers.
## Canonical import
```python
from RGTools.utils import str2bool, str2none, reverse_complement, NumpyEncoder
```
## Signature
::: RGTools.utils
    options:
      members:
        - str2bool
        - str2none
        - reverse_complement
        - NumpyEncoder
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_" 
## Parameters
`str2bool(value)`, `str2none(value)`, `reverse_complement(seq, mapping=...)`, and `NumpyEncoder` for `json.dumps(..., cls=NumpyEncoder)`.
## Return or yield behavior
`str2bool` returns bool; `str2none` returns `None` or the original string. Reverse complement returns a sequence of the same length. `NumpyEncoder` encodes arrays and NumPy scalars for JSON.
## Raised exceptions
Unknown reverse-complement symbols raise `KeyError`. JSON unsupported values retain standard encoder failures.
## Constraints
`str2bool` treats empty, `FALSE`, and `None` tokens case-insensitively as false. `str2none` maps `NONE` case-insensitively to `None`. Every reverse-complement symbol must occur in the supplied or default map.
## Ordering
Reverse complement reverses sequence order before mapping.
## Side effects
None.
## Lifecycle behavior
N/A.
## Supported protocols and inheritance
`NumpyEncoder` subclasses `json.JSONEncoder`.
## Example
```python
from RGTools.utils import reverse_complement

rc = reverse_complement("ACGT")
```
## Related formats or commands
N/A.
