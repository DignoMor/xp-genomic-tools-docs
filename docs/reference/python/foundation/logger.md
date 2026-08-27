# `Logger`
## Status
Supported for the current reference release.
## Purpose
Provide small indentation-aware logging to stderr, stdout, or an append-only path.
## Canonical import
```python
from RGTools.logging import Logger
```
## Signature
::: RGTools.logging.Logger
    options:
      members:
        - __init__
        - indent
        - unindent
        - take_log
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_" 
## Parameters
`Logger(opath="stderr", indent_level=0, indentation="\t")`; `take_log(message)` accepts a string-like message.
## Return or yield behavior
`indent` and `unindent` return `None`. `take_log` returns `None` after writing one newline-terminated record.
## Raised exceptions
`unindent` at level zero raises `ValueError`. Filesystem failures propagate.
## Constraints
`opath` must be `stderr`, `stdout`, or a filesystem path. `unindent` may not reduce the level below zero.
## Ordering
Records are emitted in call order, prefixed with `indentation * indent_level`.
## Side effects
Stream output is written immediately; path output opens in append mode per `take_log` call.
## Lifecycle behavior
No explicit close; path mode opens and closes the file on each write.
## Supported protocols and inheritance
Standard Python object; not iterable or context-managed by the library.
## Example
```python
from RGTools.logging import Logger

log = Logger(opath="stderr")
log.indent()
log.take_log("loading regions")
log.unindent()
```
## Related formats or commands
N/A.
