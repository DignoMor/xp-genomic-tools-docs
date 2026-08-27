# GENCODE-oriented GTF streaming

## Status

Supported for the current reference release.

## Purpose

Read, iterate, inspect, and filter supported GENCODE-like GTF annotation in a
streaming, read-only profile.

## Canonical import

```python
from RGTools.GTF_utils import GTFRecord, GTFHandle
```

## Signature

Record and handle members rendered from the aligned release source:

::: RGTools.GTF_utils.GTFRecord
    options:
      members:
        - __init__
        - search_general_info
        - search_add_info
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_"

::: RGTools.GTF_utils.GTFHandle
    options:
      members:
        - __init__
        - __iter__
        - __next__
        - filter_by_general_record
        - filter_by_add_record
        - get_comments
        - count_total
        - filter_check
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_"

## Parameters

`GTFRecord` accepts the nine parsed fixed fields plus an attribute dictionary
`add_info`. `GTFHandle(gtf_path, filter=...)` accepts a path and a record
predicate. Filter helpers take field or attribute keys and expected values.

## Return or yield behavior

`GTFHandle` yields `GTFRecord` objects. `get_comments` returns comment text;
`count_total` returns an integer; `filter_check` returns `None` after
validation.

## Raised exceptions

Invalid strand raises `RGToolsInternalException`. Missing fixed or attribute
fields raise `GTFRecordNoFeatureException`; when encountered by a handle filter
they are wrapped as `GTFHandleFilterException`. File and malformed-line errors
propagate from the reader.

## Constraints

Coordinates remain GTF 1-based closed integers as read; no BED conversion is
performed. `strand` must be `+` or `-`. The parser is GENCODE-oriented and does
not promise general GFF3 dialect support.

## Ordering

Records and comments retain source-file order. Re-iteration starts at the
beginning of the file.

## Side effects

Opening and iteration read the file; iteration reopens it when needed. No GTF
write API exists. `filter_by_*` creates a new handle and leaves the source
handle predicate unchanged.

## Lifecycle behavior

Handles may be reused for multiple passes; each full iteration reopens the
underlying file from the beginning.

## Supported protocols and inheritance

`GTFHandle` implements the iterator protocol via `__iter__` and `__next__`.

## Example

```python
from RGTools.GTF_utils import GTFHandle

with open("genes.gtf") as _:
    pass
handle = GTFHandle("genes.gtf")
for record in handle:
    if record.search_general_info("feature_type") == "gene":
        print(record.search_add_info("gene_name"))
```

## Related formats or commands

- [GENCODE GTF format](../../formats/gtf/gencode.md)
