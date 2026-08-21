# MotifTools command reference

Semantic reference for the shipped `MotifTools` CLI. Parser-derived syntax,
defaults, and the complete flag inventory live in the
[generated argparse reference](../generated/motif-tools.md).

## Shared contract

**Purpose.** Motif-centric generation and transformation. Ticket `0.2.0a1`
delivers `anti_motif`, `pwm_seq`, and exclusion-enabled `random_seq`; barcodes
remain planned.

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

## `pwm_seq`

**Purpose.** Sample sequences from one named motif PWM.

**Inputs.**

| Flag | Required | Meaning |
| --- | --- | --- |
| `--motif_file` | yes | Supported-subset MEME input path |
| `--motif_name` | yes | Motif name to sample |
| `--num_sequences` | yes | Positive integer count |
| `--seed` | no | Deterministic seed (`0` is valid) |
| `--output` | yes | Output FASTA path or `-` |
| `--force` | no | Replace an existing destination file |

**Behavior.** Validate the MEME collection and selected motif, then sample each
output position categorically from the corresponding PWM row using the collection
alphabet. Output length equals motif length. Duplicate sequences are allowed.
Sampling uses an isolated random-number generator and never mutates source motif
arrays.

**Outputs.** UTF-8 FASTA with LF line endings, one unwrapped sequence line per
record, identifiers `pwm_<motif_name>_<index>` in generation order, and a final
newline when nonempty.

**Reproducibility.** Identical inputs and a fixed seed reproduce FASTA bytes
within the installed release.

**Failures.** Empty collections, unknown motif names, invalid counts, invalid
PWM rows, alphabet/PWM mismatches, and shared output-contract violations raise
validation errors before output begins.

## `random_seq`

**Purpose.** Generate fixed-length random sequences with optional motif exclusions.

**Inputs.**

| Flag | Required | Meaning |
| --- | --- | --- |
| `--sequence_length` | yes | Positive sequence length |
| `--num_sequences` | yes | Positive output count |
| `--alphabet` | no | Ordered unique-character alphabet (default `ACGT`) |
| `--motif_file` | no | MEME collection required when exclusions are used |
| `--exclude` | no | Repeatable `MOTIF=CUTOFF` |
| `--seed` | no | Deterministic seed (`0` is valid) |
| `--max_attempts` | no | Per-output attempt budget when exclusions are active (default `10000`) |
| `--output` | yes | Output FASTA path or `-` |
| `--force` | no | Replace an existing destination file |

**Behavior.** Validate alphabet, lengths, counts, and exclusion context, then sample
every position uniformly with replacement from the user-ordered alphabet. Without
exclusions, arbitrary literal unique-character alphabets are supported. With
exclusions, reject candidates whose windows on either strand meet selected MEME
score cutoffs using the collection background. Each requested output receives a
fresh attempt budget. Sampling uses an isolated random-number generator.

**Outputs.** UTF-8 FASTA with identifiers `random_seq_<index>` in generation order.

**Exhaustion.** When the attempt budget is exhausted for one output, raise
`SequenceGenerationExhaustedError`, exit `1` at the CLI, emit stderr diagnostics,
and leave no partial final file.

**Failures.** Invalid lengths, counts, alphabets, unused motif files, malformed
exclusions, alphabet/MEME-alphabet violations, and shared output-contract
violations raise validation errors before output begins.

## Planned commands

`barcodes` appears in `--help` but is not yet implemented in this release.
Invoking it exits with a concise validation error.

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
