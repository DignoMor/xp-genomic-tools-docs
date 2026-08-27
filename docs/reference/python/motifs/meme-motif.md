# `MemeMotif`

## Status

Supported for the current reference release.

## Purpose

Parse, build, serialize, and score motifs in the supported minimal MEME subset.
`from RGTools import MemeMotif` is the canonical import for the collection
class.

## Canonical import

```python
from RGTools import MemeMotif
```

## Signature

Curated constructor, metadata, collection, and scoring members rendered from
the aligned release source:

::: RGTools.MemeMotif.MemeMotif
    options:
      members:
        - __init__
        - write_meme_file
        - clone_empty
        - get_meme_version
        - set_meme_version
        - get_alphabet
        - set_alphabet
        - get_strands
        - set_strands
        - get_bg_freq
        - set_bg_freq
        - get_motif_list
        - get_motif_pwm
        - get_motif_alphabet_length
        - get_motif_length
        - get_motif_num_source_sites
        - get_motif_source_eval
        - add_motif
        - calculate_pwm_score
        - search_one_motif
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_"

## Parameters

`MemeMotif(file_path=None)` accepts an optional MEME path; `None` creates an
empty collection. `add_motif` requires motif metadata keys and a PWM array.
Scoring methods accept sequence strings, PWM arrays, alphabet, background, and
optional strand or reverse-complement flags.

## Return or yield behavior

Metadata getters return strings, lists, or floats. PWM getters return NumPy
arrays with shape `(motif_length, alphabet_length)`. Scoring methods return
scalar log-odds values or per-position score arrays padded to sequence length.
`write_meme_file` returns `None`.

## Raised exceptions

Malformed input, invalid PWM or background rows, duplicate names, truncated
matrices, and malformed optional URL records raise contextual `ValueError`.
Unknown motif names raise `KeyError`. Invalid strand or sequence length
mismatch raise `ValueError`.

## Constraints

PWM rows must be finite, non-negative, and sum to approximately 1
(`atol=1e-6`). Motif names must be unique. Parsed URL values are discarded and
never emitted by `write_meme_file`. This remains a minimal MEME subset, not
full MEME dialect support.

## Ordering

Motif list order follows file or `add_motif` order. `search_one_motif` scores
are ordered by input sequence position.

## Side effects

Path writing creates or replaces the destination file or stream. Parsing retains
no file handle after construction and does not mutate caller arrays after
store.

## Lifecycle behavior

No long-lived file handle after parse or write. Collections live in memory until
released by the caller.

## Supported protocols and inheritance

Standard Python object. Static scoring helpers are declared on the class.

## Example

```python
from RGTools import MemeMotif

meme = MemeMotif("motifs.meme")
score = MemeMotif.calculate_pwm_score("ACGT", meme.get_motif_pwm("M1"))
```

## Related formats or commands

- [MEME motif format](../../formats/motifs/meme.md)
- [`MotifGeneration`](motif-generation.md)
- [`MotifTools` CLI](../../cli/motif-tools/index.md)
