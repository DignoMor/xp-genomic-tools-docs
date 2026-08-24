# `MemeMotif`

**Purpose/availability:** `from RGTools import MemeMotif` parses and writes the
supported minimal MEME subset and scores motifs. **Constructor** (`__init__`):
`MemeMotif(file_path=None)`; `None` creates an empty collection, otherwise the
file is parsed under the supported validation envelope. No file handle remains
open.

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
`pwm`; names must be unique; PWM values must be finite and non-negative; rows
must sum to approximately 1 (`atol=1e-6`). `clone_empty()` copies metadata but
no motifs. `write_meme_file(destination)` writes the supported subset to a
filesystem path or a text stream with identical text, including six-decimal
PWM rows, without mutating collection metadata or motif arrays and without
emitting any parsed URL records.

Every operation has string names, list metadata, and NumPy PWM shapes above;
there are no implicit defaults beyond constructor `None`. Unknown names raise
`KeyError`. Incomplete info, shape mismatch, duplicate names, invalid
backgrounds, invalid PWM rows, or malformed/duplicate/misplaced URL records
raise contextual `ValueError`. Parsed URL values are discarded and are not
exposed by getters. Command lines, alternate motif names, and other full-MEME
dialect blocks remain unsupported.

## Static scoring operations

`calculate_pwm_score(seq, pwm, alphabet="ACGT", bg_freq=None,
reverse_complement=False)` returns a scalar log-odds score. Sequence length
must equal PWM rows; uniform background is used when omitted; optional reverse
complement uses the library DNA convention. `search_one_motif(seq,
motif_alphabet, motif_pwm, bg_freq=None, strand="+")` returns one score per
sequence position, padding trailing windows with the minimum score. `strand`
choices are `+`, `-`, and `both`; `both` takes the maximum forward/RC score.
Invalid strand and length mismatch raise an error (`ValueError` for score
length; search raises `ValueError` for invalid strand). Scores are ordered by
input sequence position.

## MEME format

Supported text contains `MEME version`, `ALPHABET=`, `strands:`, background
frequencies, and each `MOTIF` plus `letter-probability matrix` rows. After a
complete matrix, input may include zero or one exact-uppercase `URL <token>`
record; the value is ignored and canonical output omits it. This remains a
minimal read/write subset, not full MEME. See the MEME format reference for the
validation envelope (unique names, finite non-negative normalized PWMs and
backgrounds, truncated-matrix rejection, URL grammar, and path/stream write
equivalence).

## Reference fields

**Purpose:** parse, build, serialize, and score motifs. **Availability:** with
the installed `RGTools` release that documents this page. **Inputs:** MEME
paths, metadata, PWM arrays, sequences, and optional ignored input-only URL
records. **Types:** strings, lists, dictionaries, floats, NumPy arrays, and
text streams for write destinations. **Shapes:** PWM
`(motif_length, alphabet_length)`; scores follow positions. **Dtypes:**
floating probability and score arrays. **Defaults:** `file_path=None`, uniform
background, forward strand. **Choices:** `+`, `-`, `both`; minimal MEME subset
including optional input-only URL. **Constraints:** unique motif names;
dimensions, normalization, and sequence length agree; URL records follow the
strict grammar and are not retained. **Outputs:** metadata, PWM arrays,
scores, and MEME text without URL records. **Ordering:** motif and score order
is preserved. **Side effects:** path writing creates/replaces the target file;
stream writing emits only MEME text; parsing retains no handle and does not
mutate caller arrays after store. **Failures:** contextual `ValueError` for
malformed input, invalid PWM/metadata, or invalid URL records; `KeyError` for
unknown names; invalid strand/length raise documented errors.
