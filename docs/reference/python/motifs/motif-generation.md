# `RGTools.MotifGeneration`

**Purpose/availability:** `import RGTools.MotifGeneration` exposes reusable motif
generation and transformation algorithms behind `MotifTools`. Symbols are not
re-exported from the top-level `RGTools` namespace. Ticket `0.2.0a1` ships
`make_anti_motifs`, `iter_pwm_sequences`, and unconstrained
`iter_random_sequences`; motif exclusion and barcode iterators remain planned.

## `make_anti_motifs(meme) -> MemeMotif`

Transform every motif in a supported-subset `MemeMotif` collection into an
anti-motif collection.

**Inputs.** A parsed `MemeMotif` with at least one motif; finite non-negative
normalized PWM rows; non-negative finite `nsites` and E-value metadata; finite
strictly positive normalized background frequencies aligned with the alphabet.

**Behavior.** For each source motif:

1. Copy the PWM.
2. Compute `smoothed = normalize(PWM * nsites + 1)` per row.
3. Compute `inverse = normalize(background**2 / smoothed)` per row.
4. Add motif `anti_<source_name>` with the inverse PWM.
5. Copy source `nsites` and E-value as **provenance** (they describe the source
   motif, not newly inferred anti-motif statistics).

Collection headers (MEME version, alphabet, strands, backgrounds) and motif order
are preserved. The source collection and its PWM arrays are never mutated.

**Outputs.** A new `MemeMotif` suitable for `write_meme_file` to a path or text
stream.

**Ordering.** Output motifs follow source order.

**Failures.** Empty collections, invalid PWM rows, invalid metadata, and
non-positive backgrounds raise contextual `ValueError` before any output motif is
constructed.

## `iter_pwm_sequences(meme, motif_name, num_sequences, *, seed=None) -> Iterator[str]`

Sample a requested number of sequences from one named motif PWM.

**Inputs.** A parsed `MemeMotif` with at least one motif; a motif name present in
the collection; a positive integer count; optional integer seed (`0` is valid).

**Behavior.** Validate collection state, motif dimensions, and normalized PWM
rows before yielding. For each output sequence, sample every position
categorically from the corresponding PWM row using the collection alphabet.
Output length equals motif length. Duplicate sequences are allowed. Sampling uses
a private `random.Random` instance and never mutates process-global random state
or source motif arrays.

**Outputs.** An iterator of sequence strings in generation order.

**Reproducibility.** Identical inputs and a fixed seed reproduce order and
sequences within the installed release.

**Failures.** Empty collections, unknown motif names, non-positive counts,
alphabet/PWM mismatches, and invalid PWM rows raise contextual `ValueError`
before yielding.

## `iter_random_sequences(sequence_length, num_sequences, *, alphabet="ACGT", seed=None) -> Iterator[str]`

Sample fixed-length sequences uniformly from a user-ordered alphabet with
replacement.

**Inputs.** Positive integer sequence length and count; optional alphabet string
(default `ACGT`) whose characters must be unique; optional integer seed (`0` is
valid).

**Behavior.** Validate lengths, counts, and alphabet before yielding. Sample every
position uniformly with replacement from the supplied alphabet order. Duplicate
output sequences are allowed. Motif exclusion is **not yet delivered**.

**Outputs.** An iterator of sequence strings in RNG draw order.

**Reproducibility.** Identical inputs and a fixed seed reproduce order and
sequences within the installed release.

**Failures.** Non-positive lengths or counts, empty alphabets, duplicate alphabet
characters, and unsupported exclusion inputs raise contextual `ValueError` before
yielding.

## Planned API (not yet shipped)

| Symbol | Role |
| --- | --- |
| `MotifExclusion` | Immutable motif name + score cutoff for exclusions |
| `SequenceGenerationExhaustedError` | Typed exhaustion for constrained generators |
| `iter_barcodes` | Deterministic barcode enumeration |

## Reference fields

**Purpose:** reusable motif generation/transform helpers. **Availability:** with
the installed `RGTools` release documenting this page. **Inputs:** `MemeMotif`
collections. **Types:** `MemeMotif`, NumPy PWM arrays. **Shapes:** PWM
`(motif_length, alphabet_length)`. **Dtypes:** floating probabilities.
**Defaults:** none. **Choices:** none beyond valid collection state.
**Constraints:** anti-motif formula and provenance rules above. **Outputs:** new
`MemeMotif` collections. **Ordering:** preserves source motif order.
**Side effects:** none on the input collection. **Failures:** contextual
`ValueError` for invalid input state.

## Related pages

- [`MemeMotif`](meme-motif.md)
- [MEME motif format](../../formats/motifs/meme.md)
- [`MotifTools` CLI](../../cli/motif-tools/index.md)
