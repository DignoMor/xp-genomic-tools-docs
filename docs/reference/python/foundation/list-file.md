# `RGTools.ListFile.ListFile`

## Purpose

Read and write plain text lists with one item per line.

## Availability

Supported in release `0.1.0a2`; canonical import is `from RGTools import ListFile`.

## Inputs

Construct with `ListFile(filter_empty_lines=True)`. Call `read_file(path)`, `get_contents(dtype="str")`, `get_num_lines()`, or static `write_list_to_file(contents, path)`.

## Types

Paths are strings; contents are line-like values; `get_contents` returns a NumPy array whose dtype is selected by the supplied dtype expression.

## Shapes

The result is one-dimensional with one item per retained line.

## Dtypes

Default output dtype is string; callers may request another NumPy-compatible dtype.

## Defaults

Empty lines are filtered by default.

## Choices

`-`/`stdin` read standard input; `-`/`stdout` write standard output.

## Constraints

No uniqueness or sorting is applied. A filtered line is stripped; with filtering disabled only line endings are removed.

## Outputs

`read_file` and writing return `None`; `get_contents` returns the array; `get_num_lines` returns an integer.

## Ordering

Input order is preserved exactly for retained lines.

## Side effects

Reading replaces in-memory contents. Writing creates/replaces the target or writes stdout.

## Failures

Filesystem and invalid dtype errors propagate from the underlying Python/NumPy operations.
