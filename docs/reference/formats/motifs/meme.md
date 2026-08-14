# MEME motif format

## Purpose and availability

Minimal MEME text read/write supported by `RGTools.MemeMotif` in `0.1.0a2`.

## Inputs and schema

The file includes `MEME version`, `ALPHABET=...`, `strands: ...`, a background
letter-frequency header and line, then repeated `MOTIF <name>` and
`letter-probability matrix:` blocks. Each PWM row has one probability per
alphabet letter; rows must sum to 1 within `atol=1e-6` when added.

## Types, shapes, defaults, ordering, outputs

Names and headers are strings; metadata lists are ordered; each PWM has shape
`(w, alphabet_length)` and floating probabilities. Motifs retain file/add
order. `write_meme_file` emits this subset; parser construction has no extra
semantic defaults beyond the file values.

## Constraints and failures

Full MEME URL, command, alternate-name, and other dialect blocks are outside
the supported subset. Parse errors propagate from the subset parser; malformed
motif metadata or PWM validation raises `ValueError`, and unknown in-memory
motifs raise `KeyError`.

## Reference fields

**Purpose:** minimal MEME text interchange. **Availability:** `0.1.0a2` via
`MemeMotif`. **Inputs:** headers, metadata, and PWM rows. **Types:** text,
names, lists, and floating probabilities. **Shapes:** motif matrix `(w,
alphabet_length)`. **Dtypes:** floating matrix values. **Defaults:** values
come from the file. **Choices:** documented minimal headers and blocks.
**Constraints:** rows sum within `atol=1e-6`; full dialects are out of scope.
**Outputs:** parsed motifs or compatible text. **Ordering:** motif and row
order retained. **Side effects:** writing creates/replaces the target file.
**Failures:** parse/validation/unsupported-dialect errors propagate; unknown
names raise `KeyError`.
