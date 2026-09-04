# `MotifTools pwm_seq`

## Availability

Supported in `MotifTools` for release `0.4.0a1`. Invoke through the installed `MotifTools` console script.

## Purpose

**Purpose.** Sample sequences from one named motif PWM.

## Inputs

| Flag | Required | Meaning |
| --- | --- | --- |
| `--motif_file` | yes | Supported-subset MEME input path |
| `--motif_name` | yes | Motif name to sample |
| `--num_sequences` | yes | Positive integer count |
| `--seed` | no | Deterministic seed (`0` is valid) |
| `--output` | yes | Output FASTA path or `-` |
| `--force` | no | Replace an existing destination file |

## Constraints

Validate the MEME collection and selected motif, then sample each
output position categorically from the corresponding PWM row using the collection
alphabet. Output length equals motif length. Duplicate sequences are allowed.
Sampling uses an isolated random-number generator and never mutates source motif
arrays.

Identical inputs and a fixed seed reproduce FASTA bytes
within the installed release.

## Outputs

UTF-8 FASTA with LF line endings, one unwrapped sequence line per
record, identifiers `pwm_<motif_name>_<index>` in generation order, and a final
newline when nonempty.

## Failures

Empty collections, unknown motif names, invalid counts, invalid
PWM rows, alphabet/PWM mismatches, and shared output-contract violations raise
validation errors before output begins.

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

Create a tiny MEME collection inline, then sample two sequences with a fixed
seed:

```bash
cat > /tmp/doc-example.meme <<'EOF'
MEME version 4

ALPHABET=ACGT

strands: + -

Background letter frequencies
A 0.25 C 0.25 G 0.25 T 0.25

MOTIF DOC_EXAMPLE
letter-probability matrix: alength= 4 w= 3 nsites= 8 E= 1e-4
0.700000  0.100000  0.100000  0.100000
0.100000  0.700000  0.100000  0.100000
0.100000  0.100000  0.700000  0.100000
EOF

MotifTools pwm_seq \
  --motif_file /tmp/doc-example.meme \
  --motif_name DOC_EXAMPLE \
  --num_sequences 2 \
  --seed 0 \
  --output /tmp/pwm-doc-example.fasta
```

Identical inputs reproduce these FASTA bytes in release `0.4.0a1`:

```text
>pwm_DOC_EXAMPLE_0
GCG
>pwm_DOC_EXAMPLE_1
ACG
```
