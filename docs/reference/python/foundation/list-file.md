# `ListFile`
## Status
Supported for the current reference release.
## Purpose
Read and write plain text lists with one item per line.
## Canonical import
```python
from RGTools import ListFile
```
## Signature
::: RGTools.ListFile.ListFile
    options:
      members:
        - __init__
        - read_file
        - write_list_to_file
        - get_contents
        - get_num_lines
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_" 
## Parameters
`ListFile(filter_empty_lines=True)`; `read_file(path)`; static `write_list_to_file(contents, path)`; `get_contents(dtype="str")`; `get_num_lines()`.
## Return or yield behavior
`read_file` and `write_list_to_file` return `None`. `get_contents` returns a one-dimensional NumPy array. `get_num_lines` returns an integer.
## Raised exceptions
Filesystem and invalid dtype errors propagate from underlying Python/NumPy operations.
## Constraints
`-`/`stdin` read standard input; `-`/`stdout` write standard output. No uniqueness or sorting is applied.
## Ordering
Input order is preserved for retained lines.
## Side effects
Reading replaces in-memory contents. Writing creates or replaces the target or writes stdout.
## Lifecycle behavior
Hold one loaded list per instance until replaced by `read_file`.
## Supported protocols and inheritance
N/A.
## Example
```python
from RGTools import ListFile

lf = ListFile()
lf.read_file("samples.txt")
print(lf.get_num_lines())
```
## Related formats or commands
- [ListFile format](../../formats/foundation/list-file.md)
