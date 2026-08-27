# `MotifTools random_seq`

## Availability

Supported in `MotifTools` for release `0.3.0a4`. Invoke through the installed `MotifTools` console script.

## Purpose

**Purpose.** Generate fixed-length random sequences with optional motif exclusions.

## Inputs

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

## Constraints

Validate alphabet, lengths, counts, and exclusion context, then sample
every position uniformly with replacement from the user-ordered alphabet. Without
exclusions, arbitrary literal unique-character alphabets are supported. With
exclusions, reject candidates whose windows on either strand meet selected MEME
score cutoffs using the collection background. Each requested output receives a
fresh attempt budget. Sampling uses an isolated random-number generator.

## Outputs

UTF-8 FASTA with identifiers `random_seq_<index>` in generation order.

## Failures

When the attempt budget is exhausted for one output, raise
`SequenceGenerationExhaustedError`, exit `1` at the CLI, emit stderr diagnostics,
and leave no partial final file.

Invalid lengths, counts, alphabets, unused motif files, malformed
exclusions, alphabet/MEME-alphabet violations, and shared output-contract
violations raise validation errors before output begins.

## Types

Paths and schema keys are strings unless noted in Purpose.

## Shapes

Annotation arrays align by first dimension with region or sequence order.

## Dtypes

See linked format references and Purpose.

## Defaults

Parser defaults appear in the generated options table.

## Choices

Parser choices appear in the generated options table.

## Ordering

Output rows retain input order unless stated otherwise in Purpose.

## Side effects

Reads declared inputs and writes declared outputs; inputs are not mutated.

## Example

From the `code/` checkout with `code/.venv` activated:

```bash
MotifTools random_seq \
  --sequence_length 8 \
  --num_sequences 2 \
  --seed 0 \
  --output /tmp/random-spec.fasta
```

Identical inputs reproduce these FASTA bytes in release `0.3.0a4`:

```text
>random_seq_0
TTAGTTGT
>random_seq_1
GCCGGCCG
```
