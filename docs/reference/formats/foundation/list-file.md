# ListFile format

## Purpose

Represent a plain text list with one item per line.

## Availability

Supported in the current reference release (`0.3.0a4`).

Available since `0.1.0a2`.

## Inputs

Text files or stdin; each line is one item.

## Types

Items are text on disk and can be converted to a requested NumPy dtype in memory.

## Shapes

One-dimensional sequence with one entry per retained line.

## Dtypes

The default in-memory dtype is string; conversion is caller-selected.

## Defaults

Empty/whitespace-only lines are filtered by default.

## Choices

`-` or `stdin` means standard input; `-` or `stdout` means standard output.

## Constraints

No uniqueness or ordering guarantee beyond source order; with filtering disabled, blank lines are retained after line-ending removal.

## Outputs

Writing emits one item and newline per line.

## Ordering

Source order is preserved.

## Side effects

File or stream I/O.

## Failures

Standard OS/IO and conversion errors propagate.

## Related API and CLI

- [`ListFile`](../../python/foundation/list-file.md)
- [`GenomicElementTools import stat_list`](../../cli/genomic-element-tools/import/stat-list.md)
