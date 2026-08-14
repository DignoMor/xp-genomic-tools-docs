# `RGTools.logging.Logger`

## Purpose

Provide small indentation-aware logging to stderr, stdout, or an append-only path.

## Availability

Supported in release `0.1.0a2`; canonical import is `RGTools.logging.Logger`.

## Inputs

`Logger(opath="stderr", indent_level=0, indentation="\t")`; `opath` is `stderr`, `stdout`, or a filesystem path. `take_log(message)` accepts a string-like message.

## Types

`indent_level` is an integer and `indentation` is a string.

## Shapes

Not applicable.

## Dtypes

Not applicable.

## Defaults

Output is stderr, level is zero, and one tab is used per level.

## Choices

Output targets are `stderr`, `stdout`, or a path.

## Constraints

`unindent` may not reduce the level below zero.

## Outputs

`take_log` returns `None` and writes one newline-terminated record.

## Ordering

Records are emitted in call order, prefixed with `indentation * indent_level`.

## Side effects

Stream output is written immediately; path output is opened in append mode per call.

## Failures

`unindent` at level zero raises `ValueError`; filesystem failures propagate.
