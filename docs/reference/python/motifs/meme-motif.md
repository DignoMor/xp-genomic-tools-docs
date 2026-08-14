# `MemeMotif`

**Purpose/availability:** `from RGTools import MemeMotif` parses and writes the
supported minimal MEME subset and scores motifs. **Constructor** (`__init__`):
`MemeMotif(file_path=None)`; `None` creates an empty collection, otherwise the
file is parsed. No file handle remains open.

## Metadata and collection operations

`get_meme_version`/`set_meme_version`, `get_alphabet`/`set_alphabet`,
`get_strands`/`set_strands`, and `get_bg_freq`/`set_bg_freq` expose and update
version, alphabet string, strand list, and background-frequency list.
`get_motif_list()` preserves file/add order. `get_motif_pwm(name)` returns a
probability NumPy array of shape `(motif_length, alphabet_length)`.
`get_motif_alphabet_length`, `get_motif_length`,
`get_motif_num_source_sites`, and `get_motif_source_eval` return per-motif
metadata. `add_motif(name, motif_info)` requires keys
`alphabet_length`, `motif_length`, `num_source_sites`, `source_eval`, and
`pwm`; rows must sum to approximately 1 (`atol=1e-6`). `clone_empty()` copies
metadata but no motifs. `write_meme_file(path)` writes the supported subset.

Every operation has string names, list metadata, and NumPy PWM shapes above;
there are no implicit defaults beyond constructor `None`. Unknown names raise
`KeyError`; incomplete info, shape mismatch, or unnormalized rows raise
`ValueError`. Full MEME URL/command/alternate-name blocks are unsupported.

## Static scoring operations

`calculate_pwm_score(seq, pwm, alphabet="ACGT", bg_freq=None,
reverse_complement=False)` returns a scalar log-odds score. Sequence length
must equal PWM rows; uniform background is used when omitted; optional reverse
complement uses the library DNA convention. `search_one_motif(seq,
motif_alphabet, motif_pwm, bg_freq=None, strand="+")` returns one score per
sequence position, padding trailing windows with the minimum score. `strand`
choices are `+`, `-`, and `both`; `both` takes the maximum forward/RC score.
Invalid strand and length mismatch raise an error (`ValueError` for score
length; legacy search raises for invalid strand). Scores are ordered by input
sequence position.

## MEME format

Supported text contains `MEME version`, `ALPHABET=`, `strands:`, background
frequencies, and each `MOTIF` plus `letter-probability matrix` rows. It is a
minimal read/write subset, not full MEME.

## Reference fields

**Purpose:** parse, build, serialize, and score motifs. **Availability:**
`0.1.0a2`. **Inputs:** MEME paths, metadata, PWM arrays, and sequences.
**Types:** strings, lists, dictionaries, floats, and NumPy arrays.
**Shapes:** PWM `(motif_length, alphabet_length)`; scores follow positions.
**Dtypes:** floating probability and score arrays. **Defaults:** `file_path=None`,
uniform background, forward strand. **Choices:** `+`, `-`, `both`; minimal MEME
subset. **Constraints:** dimensions, normalization, and sequence length agree.
**Outputs:** metadata, PWM arrays, scores, and MEME text. **Ordering:** motif
and score order is preserved. **Side effects:** writing creates/replaces the
target file; parsing retains no handle. **Failures:** malformed input, invalid
PWM/metadata, unknown names, and invalid strand/length raise documented errors.
