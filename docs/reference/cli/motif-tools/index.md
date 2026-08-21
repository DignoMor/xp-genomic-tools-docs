# MotifTools command reference

Semantic reference for the shipped `MotifTools` CLI. Parser-derived syntax,
defaults, and the complete flag inventory live in the
[generated argparse reference](../generated/motif-tools.md).

## Shared contract

**Purpose.** Motif-centric generation and transformation. Ticket `0.2.0a1`
delivers `anti_motif`; sequence generators remain planned.

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

## `anti_motif`

**Purpose.** Derive an anti-motif collection from every motif in an input MEME
file.

**Inputs.**

| Flag | Required | Meaning |
| --- | --- | --- |
| `--motif_file` | yes | Supported-subset MEME input path |
| `--output` | yes | Output MEME path or `-` |
| `--force` | no | Replace an existing destination file |

**Behavior.** For each source motif, compute row-wise smoothed probabilities
`normalize(PWM * nsites + 1)`, then inverse weights
`normalize(background**2 / smoothed)`, prefix the name with `anti_`, and copy
source `nsites` and E-value as provenance metadata (not recomputed
anti-motif statistics). Collection headers (version, alphabet, strands,
backgrounds) and motif order are preserved. The source collection is never mutated.

**Outputs.** MEME subset compatible with `MemeMotif` (see
[MemeMotif](../../python/motifs/meme-motif.md)).

**Ordering.** Output motifs follow source file order.

**Side effects.** Writes the destination MEME file or stdout only.

**Failures.** Empty collections, invalid PWM rows, non-positive backgrounds, and
malformed MEME input raise validation errors before output begins.

## Planned commands

`random_seq`, `pwm_seq`, and `barcodes` appear in `--help` but are not yet
implemented in this release. Invoking them exits with a concise validation error.

## Reference fields

**Purpose:** motif generation and transformation CLI. **Availability:** with the
installed release that documents this page. **Inputs:** MEME paths and shared
output flags. **Types:** paths and text streams. **Defaults:** none beyond
parser defaults in the generated reference. **Choices:** subcommand names listed
above. **Constraints:** shared output contract and anti-motif provenance rules.
**Outputs:** MEME subset files or stdout MEME text. **Ordering:** anti-motifs
preserve source motif order. **Side effects:** atomic path writes only.
**Failures:** exit codes `2` (usage/validation) and `1` (I/O) without
tracebacks for expected failures.
