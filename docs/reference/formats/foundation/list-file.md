# ListFile format

## Purpose

Represent a plain text list with one item per line.

## Availability

Supported in release `0.1.0a2`; no filename extension is required.

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
