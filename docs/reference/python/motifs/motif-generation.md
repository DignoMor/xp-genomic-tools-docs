# `RGTools.MotifGeneration`

## Status

Supported for the current reference release. Symbols are not re-exported from
the top-level `RGTools` namespace.

## Purpose

Expose reusable motif generation, exclusion evaluation, and anti-motif
transformation algorithms used by `MotifTools` and library callers.

## Canonical import

```python
from RGTools.MotifGeneration import (
    MotifExclusion,
    SequenceGenerationExhaustedError,
    make_anti_motifs,
    iter_pwm_sequences,
    iter_random_sequences,
    iter_barcodes,
    parse_motif_exclusion,
    parse_motif_exclusions,
    validate_motif_exclusions,
    candidate_violates_exclusions,
)
```

## Signature

Curated module members rendered from the aligned release source:

::: RGTools.MotifGeneration
    options:
      members:
        - MotifExclusion
        - SequenceGenerationExhaustedError
        - parse_motif_exclusion
        - parse_motif_exclusions
        - validate_motif_exclusions
        - candidate_violates_exclusions
        - make_anti_motifs
        - iter_pwm_sequences
        - iter_random_sequences
        - iter_barcodes
      show_root_heading: true
      show_source: false
      heading_level: 4
      filters:
        - "!^_"

## Parameters

- `MotifExclusion(motif_name, cutoff)` — immutable exclusion value.
- `parse_motif_exclusion(value)` / `parse_motif_exclusions(values)` — CLI-style
  `MOTIF=CUTOFF` strings.
- `validate_motif_exclusions(meme, exclusions, *, alphabet, target_length,
  max_attempts=None)` — preflight for constrained generation.
- `candidate_violates_exclusions(sequence, meme, exclusions)` — shared
  evaluator for one candidate sequence.
- Generators accept `MemeMotif` collections, counts, optional seeds, alphabets,
  exclusions, and attempt budgets as documented on each function.

## Return or yield behavior

`make_anti_motifs` returns a new `MemeMotif`. Iterator functions yield
sequence strings in generation or enumeration order. Parsers return
`MotifExclusion` values or tuples thereof. `candidate_violates_exclusions`
returns a boolean.

## Raised exceptions

Invalid collection state, dimensions, alphabets, exclusion context, or attempt
budgets raise contextual `ValueError` before yielding. Constrained random
generation raises `SequenceGenerationExhaustedError` when a per-output attempt
budget is exhausted.

## Constraints

Anti-motif transformation preserves source motif order and metadata provenance.
With exclusions active, MEME alphabet must be exactly `ACGT` and generated
alphabets must be uppercase subsets of `ACGT`. Scores equal to the cutoff count
as matches. Identical inputs and a fixed seed reproduce order and sequences
within the installed release.

## Ordering

Output motif order follows source order. Accepted random sequences and barcodes
preserve generation or Cartesian enumeration order after exclusion filtering.

## Side effects

Never mutates the input `MemeMotif` collection or its PWM arrays. Sampling uses
private `random.Random` instances and does not mutate process-global random
state.

## Lifecycle behavior

Iterators are exhausted after yielding the requested logical outputs. No
persistent handles remain open.

## Supported protocols and inheritance

`MotifExclusion` is an immutable dataclass. `SequenceGenerationExhaustedError`
is a typed exception with diagnostic fields.

## Example

```python
from RGTools import MemeMotif
from RGTools.MotifGeneration import make_anti_motifs, iter_pwm_sequences

meme = MemeMotif("motifs.meme")
anti = make_anti_motifs(meme)
first = next(iter_pwm_sequences(meme, meme.get_motif_list()[0], 1, seed=0))
```

## Related formats or commands

- [`MemeMotif`](meme-motif.md)
- [MEME motif format](../../formats/motifs/meme.md)
- [`MotifTools` CLI](../../cli/motif-tools/index.md)
