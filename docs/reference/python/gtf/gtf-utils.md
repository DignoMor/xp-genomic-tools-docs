# GENCODE-oriented GTF streaming

## Purpose

Read, iterate, inspect, and filter supported GENCODE-like GTF annotation.

See the [GENCODE GTF format profile](../../formats/gtf/gencode.md) for the
accepted file dialect.

## Availability

Supported in release `0.1.0a2` from `RGTools.GTF_utils`; import `GTFRecord` and
`GTFHandle` from that module. The profile is read-only and streaming.

## Inputs

`GTFRecord` accepts the nine parsed fields (`chr_name`, `record_source`,
`feature_type`, `start_loc`, `end_loc`, `score`, `strand`, `phase`) plus an
attribute dictionary `add_info`. `GTFHandle(gtf_path, filter=...)` accepts a
path and a record predicate.

## Types

Coordinates are integers. Fixed fields and attributes are strings except
coordinates; `add_info` is a string-to-string dictionary. A filter is a
callable receiving one `GTFRecord` and returning a truth value.

## Shapes

Inapplicable: records are scalar objects and iteration yields one record at a
time.

## Dtypes

Inapplicable.

## Defaults

`filter` defaults to a predicate accepting every record. Empty lines are
skipped. Leading `#` lines are collected as comments.

## Choices

`strand` must be `+` or `-`; `.` is rejected. GTF attributes use the
GENCODE-like `key "value";` convention.

## Constraints

Coordinates remain GTF 1-based closed integers as read; no BED conversion is
performed. The parser is intentionally GENCODE-oriented and does not promise
general GFF3 or other attribute dialects. Iteration preserves file order.

## Outputs

`GTFHandle` yields `GTFRecord` objects. `get_comments` returns comment text,
`count_total` returns an integer, and `filter_check` validates the active
filter and returns `None`.

## Ordering

Records and comments retain source-file order. Re-iteration starts at the
beginning of the file.

## Side effects

Opening/iteration reads the file; iteration reopens it when needed. No GTF
write API exists. `filter_by_*` creates a new handle and leaves the source
handle's predicate unchanged.

## Failures

Invalid strand raises `RGToolsInternalException`. Missing fixed or attribute
fields raise `GTFRecordNoFeatureException`; when encountered by a handle
filter they are wrapped as `GTFHandleFilterException`. File and malformed-line
errors propagate from the reader.

## `GTFRecord`

### Constructor

`GTFRecord(chr_name, record_source, feature_type, start_loc, end_loc, score,
strand, phase, add_info)` stores parsed fixed fields and attributes.

### `GTFRecord.search_general_info`

`search_general_info(key)` returns one fixed-column value. Valid keys are
`chr_name`, `record_source`, `feature_type`, `start_loc`, `end_loc`, `score`,
`strand`, and `phase`.

### `GTFRecord.search_add_info`

`search_add_info(key)` returns the requested parsed attribute.

## `GTFHandle`

### GTFHandle constructor

`GTFHandle(gtf_path, filter=...)` opens the file and `iter(handle)` returns a
reusable iterator over records passing the active filter. `next(handle)` yields
the next record; blank lines are ignored.

### `GTFHandle.__iter__`

`iter(handle)` reopens the file from the beginning and returns the reusable
handle iterator.

### `GTFHandle.__next__`

`next(handle)` yields the next passing record or raises `StopIteration` at EOF.

### `GTFHandle.filter_by_general_record`

Returns a new handle applying the existing predicate AND equality on a fixed
field.

### `GTFHandle.filter_by_add_record`

Returns a new handle applying the existing predicate AND equality on an
attribute.

### `GTFHandle.get_comments`

Returns collected leading comments with the leading `#` removed, following
whitespace left-trimmed, and each line newline removed; comments are joined by
`\n`.

### `GTFHandle.count_total`

Counts records passing the active filter, consuming and reopening iteration.

### `GTFHandle.filter_check`

Walks the active filter to validate it; `n_lines` optionally limits the walk.
