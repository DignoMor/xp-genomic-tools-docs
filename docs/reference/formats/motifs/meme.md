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

## Types, shapes, defaults, ordering, outputs

Names and headers are strings; metadata lists are ordered; each PWM has shape
`(w, alphabet_length)` with floating probabilities. Motifs retain file/add
order. `write_meme_file` writes the same supported-subset text to a filesystem
path or a text stream, using six-decimal PWM rows. Construction has no extra
semantic defaults beyond the file values.

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

Full MEME URL, command, alternate-name, and other dialect blocks are outside
this subset. Validation failures raise contextual `ValueError`; unknown
in-memory motif names raise `KeyError`. Parsing and writing do not mutate
stored motif arrays or collection metadata.

## Reference fields

**Purpose:** minimal MEME text interchange. **Availability:** documented with
the installed `MemeMotif` release. **Inputs:** headers, metadata, and PWM rows.
**Types:** text, names, lists, and floating probabilities. **Shapes:** motif
matrix `(w, alphabet_length)`. **Dtypes:** floating matrix values. **Defaults:**
values come from the file. **Choices:** documented minimal headers and blocks.
**Constraints:** unique names; background and PWM numerical envelope above;
full dialects are out of scope. **Outputs:** parsed motifs or compatible text to a
path or text stream. **Ordering:** motif and row order retained. **Side effects:** path writing creates/replaces the target file; stream writing only writes text; no mutation of source arrays. **Failures:** contextual `ValueError` for validation; `KeyError` for unknown names.
