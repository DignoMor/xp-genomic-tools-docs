# MEME motif format

## Purpose and availability

Minimal MEME text read/write supported by `RGTools.MemeMotif` (from the
aligned release that documents this page).

## Inputs and schema

Supported files include `MEME version`, `ALPHABET=...`, `strands: ...`, a
`Background letter frequencies` header and one frequency line, then zero or
more `MOTIF <name>` blocks. Each motif has a `letter-probability matrix:`
header with `alength`, `w`, `nsites`, and `E`, followed by exactly `w` rows of
`alength` probabilities.

After a complete probability matrix, the supported **input** profile also
accepts zero or one optional per-motif `URL` record: the exact uppercase
keyword `URL`, whitespace, and exactly one opaque non-whitespace token. The
value is ignored in memory. Canonical writers never emit a `URL` record. This
is the standard optional MEME per-motif URL field (verified against JASPAR
matrix `MA0139.2` as a motivating producer), not a blanket JASPAR-compatibility
promise.

## Types, shapes, defaults, ordering, outputs

Names and headers are strings; metadata lists are ordered; each PWM has shape
`(w, alphabet_length)` with floating probabilities. Motifs retain file/add
order. `write_meme_file` writes the same supported-subset text to a filesystem
path or a text stream, using six-decimal PWM rows and omitting any parsed URL
records. Construction has no extra semantic defaults beyond the file values.

## Constraints and failures

The supported envelope rejects:

- missing or malformed required headers or matrix headers
- truncated matrices or rows with the wrong width
- duplicate motif names
- invalid numerical metadata (`alength`, `w`, `nsites`, `E`)
- background frequencies that are missing letters, misaligned with the
  alphabet, non-finite, negative, or not summing to 1 within `atol=1e-3`
- PWM values that are non-finite, negative, or whose rows do not sum to 1
  within `atol=1e-6`
- bare `URL`, `URL` with extra tokens, a second `URL` for the same motif, or a
  `URL` before any motif
- a URL-like line where a PWM row is still required (matrix failure)

Lowercase `url`, prefix-like `URLfoo`, command lines, alternate motif names,
and other full-MEME dialect blocks remain outside this subset. Validation
failures raise contextual `ValueError`; unknown in-memory motif names raise
`KeyError`. Parsing and writing do not mutate stored motif arrays or
collection metadata.

## Reference fields

**Purpose:** minimal MEME text interchange. **Availability:** documented with
the installed `MemeMotif` release. **Inputs:** headers, metadata, PWM rows, and
optional ignored input-only `URL` records. **Types:** text, names, lists, and
floating probabilities. **Shapes:** motif matrix `(w, alphabet_length)`.
**Dtypes:** floating matrix values. **Defaults:** values come from the file.
**Choices:** documented minimal headers and blocks. **Constraints:** unique
names; background and PWM numerical envelope above; URL grammar and singular
cardinality above; full dialects beyond optional input-only URL are out of
scope. **Outputs:** parsed motifs or compatible text to a path or text stream
without URL records. **Ordering:** motif and row order retained. **Side
effects:** path writing creates/replaces the target file; stream writing only
writes text; no mutation of source arrays. **Failures:** contextual
`ValueError` for validation; `KeyError` for unknown names.
