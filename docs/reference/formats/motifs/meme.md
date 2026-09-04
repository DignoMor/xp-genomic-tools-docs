# MEME motif format

## Purpose

Minimal MEME text interchange supported by `RGTools.MemeMotif` and motif-search
commands on the genomic-element and exogenous-sequence CLIs.

## Availability

Supported in the current reference release (`0.4.0a1`).

Available since `0.1.0a2`.

## Inputs

Supported files include:

- `MEME version …`
- `ALPHABET=…` declaring the motif alphabet in file order
- `strands: …` declaring searchable strands
- `Background letter frequencies` header and one frequency line aligned to the alphabet
- Per motif: `MOTIF <name>`, `letter-probability matrix:` header (`alength`, `w`,
  `nsites`, `E`), then exactly `w` probability rows of `alength` values
- After a complete PWM, zero or one optional input-only `URL` record (`URL` plus
  one opaque token; value is ignored and never re-emitted)

## Types

Headers and motif names are strings. Background frequencies and PWM values are
floating probabilities. Metadata lists retain file order.

## Shapes

Each motif PWM has shape `(w, alphabet_length)` where `w` is motif width and
`alphabet_length` matches `ALPHABET`.

## Dtypes

PWM and background values are floating point. Parsed URL tokens are not retained.

## Defaults

Construction has no semantic defaults beyond values read from the file.

## Choices

This is a minimal MEME subset. Full MEME dialect blocks (command lines,
alternate names, lowercase `url`, multiple URLs, and other extensions) are out
of scope.

## Constraints

- Motif names must be unique.
- Background frequencies must align with the alphabet, be finite, nonnegative,
  and sum to 1 within `atol=1e-3`.
- PWM rows must be finite, nonnegative, and sum to 1 within `atol=1e-6`.
- Optional `URL` grammar is singular per motif and must not appear before any
  motif or inside an incomplete matrix.
- `search_one_motif` and CLI motif search interpret strand from the MEME `strands`
  field and optional reverse-complement flags; `+`, `-`, and `both` modes apply
  at operation level.

## Outputs

Parsed in-memory motifs or compatible MEME text via `write_meme_file` to a path
or text stream. Canonical writers omit parsed URL records and use six-decimal
PWM rows.

## Ordering

Motif list order follows file or `add_motif` order. PWM rows follow file order.
`calculate_pwm_score` and search helpers return per-position **log-odds** scores
ordered by sequence position.

## Side effects

Parsing reads the source and constructs in-memory motif data. Path writing
creates or replaces the destination file. Neither operation mutates caller PWM
arrays after store.

## Failures

Malformed headers, truncated matrices, duplicate names, invalid numerical
metadata, malformed URL records, and PWM/background envelope violations raise
contextual `ValueError`. Unknown motif names raise `KeyError`.

## Related API and CLI

- [`MemeMotif`](../../python/motifs/meme-motif.md)
- [`MotifGeneration`](../../python/motifs/motif-generation.md)
- [`MotifTools`](../../cli/motif-tools/index.md)
- [`GenomicElementTools motif_search`](../../cli/genomic-element-tools/motif-search.md)
- [`ExogenousSequenceTools motif_search`](../../cli/exogenous-sequence-tools/motif-search.md)
- [Motif-search track outputs (CLI)](../cli/exogenous-sequence-tools/motif-outputs.md)
