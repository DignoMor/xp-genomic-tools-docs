# `MotifTools anti_motif`

## Availability

Supported in `MotifTools` for release `0.3.0a4`. Invoke through the installed `MotifTools` console script.

## Purpose

**Purpose.** Derive an anti-motif collection from every motif in an input MEME
file.

## Inputs

| Flag | Required | Meaning |
| --- | --- | --- |
| `--motif_file` | yes | Supported-subset MEME input path |
| `--output` | yes | Output MEME path or `-` |
| `--force` | no | Replace an existing destination file |

## Constraints

For each source motif, compute row-wise smoothed probabilities
`normalize(PWM * nsites + 1)`, then inverse weights
`normalize(background**2 / smoothed)`, prefix the name with `anti_`, and copy
source `nsites` and E-value as provenance metadata (not recomputed
anti-motif statistics). Collection headers (version, alphabet, strands,
backgrounds) and motif order are preserved. The source collection is never mutated.

## Outputs

MEME subset compatible with `MemeMotif` (see
[MemeMotif](../../python/motifs/meme-motif.md)).

**Ordering.** Output motifs follow source file order.

**Side effects.** Writes the destination MEME file or stdout only.

## Failures

Empty collections, invalid PWM rows, non-positive backgrounds, and
malformed MEME input raise validation errors before output begins.

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

Create a tiny MEME collection inline, then derive its anti-motif:

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

MotifTools anti_motif \
  --motif_file /tmp/doc-example.meme \
  --output /tmp/anti-doc-example.meme
```

The output MEME collection contains one motif named `anti_DOC_EXAMPLE` derived
from the `DOC_EXAMPLE` PWM above.
