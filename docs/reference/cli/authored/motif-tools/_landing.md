# MotifTools command reference

Semantic reference for the shipped `MotifTools` CLI. Parser-derived syntax,
defaults, and the complete flag inventory live in the
[generated argparse reference](../generated/motif-tools.md).

## Shared contract

**Purpose.** Motif-centric generation and transformation. Release `0.3.0a4`
includes `anti_motif`, `pwm_seq`, exclusion-enabled `random_seq`, and `barcodes`
delivered in `0.2.0a1`.

**Availability.** `MotifTools` is the motif-generation console entry point.
Motif scoring whose primary subject is a genomic-element or exogeneous-sequence
collection remains in `GenomicElementTools` and `ExogeneousSequenceTools`.

**Inputs.** Supported-subset MEME files for `anti_motif` (see
[MEME format](../../formats/motifs/meme.md)).

**Types.** Paths and text streams.

**Shapes.** MEME collections with PWM arrays shaped
`(motif_length, alphabet_length)`.

**Dtypes.** Floating-point PWM probabilities in the supported MEME subset.

**Outputs.** Supported-subset MEME files with six-decimal PWM rows, or MEME text
on stdout when `--output -`.

**Defaults.** Parser defaults appear in the generated reference; `anti_motif`
has no command-specific defaults beyond optional `--force`.

**Choices.** Top-level subcommands: `anti_motif`, `random_seq`, `pwm_seq`,
`barcodes`.

**Constraints.**

- `--output -` writes data only to stdout; diagnostics use stderr.
- `--output -` cannot be combined with `--force`.
- Path outputs require an existing parent directory and refuse overwrite unless
  `--force` is supplied.
- Completed path outputs are written atomically via temporary file + rename.
- Successful path commands produce no stdout or stderr.

**Failures.**

- Missing subcommand, argparse usage errors, and preflight validation failures
  exit `2` without traceback.
- I/O failures exit `1` without traceback.
