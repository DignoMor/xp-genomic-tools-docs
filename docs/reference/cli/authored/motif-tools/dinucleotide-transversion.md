# `MotifTools dinucleotide_transversion`

## Availability

Supported on the MotifTools console script. This command is unscheduled and is
not bound to a completed release tag.

## Purpose

**Purpose.** Generate one deterministic full-width PWM-derived transversion
target from a named motif. Every position transverts relative to the
source-PWM consensus. The command does not prove motif knockout.

## Inputs

| Flag | Required | Meaning |
| --- | --- | --- |
| `--motif_file` | yes | Supported-subset MEME input path |
| `--motif_name` | yes | Exact motif name in the collection |
| `--output` | yes | Output FASTA path or `-` |
| `--force` | no | Replace an existing destination file |

## Constraints

The collection is loaded through the existing `MemeMotif` parser. Required
`nsites` and `E`, matrix dimensions, and current validation remain in force.
The selected alphabet must contain exactly A, C, G, and T. PWM columns follow
declared alphabet order; ties use letter order A, C, G, T.

Consensus is the maximum-probability base in each column. Pairs are taken from
position zero in original PWM orientation. For consensus A or G the allowed
replacements are C and T; for consensus C or T they are A and G. Each pair
selects the allowed dinucleotide with the minimum product of the two
source-PWM probabilities. Equal products, including zeros, resolve
lexicographically A, C, G, T. An unmatched terminal chooses its
minimum-probability allowed transversion with the same letter order. Width one
and uninformative columns are retained. There is no seed, method selector,
sampling, or genomic-allele input.

Identical inputs reproduce FASTA bytes within a given MotifTools install.

## Outputs

UTF-8 FASTA with LF line endings, exactly one unwrapped uppercase A/C/G/T
sequence of full PWM width, identifier
`dinucleotide_transversion_<motif_name>`, and a final newline. Path and stdout
bytes are identical.

## Failures

Empty collections, unknown motif names, unsupported alphabets, invalid PWM
rows or dimensions, missing required source statistics, and shared
output-contract violations fail before any target is published.

## Types

Paths and schema keys are strings unless noted in Purpose.

## Shapes

The output sequence length equals the selected motif width.

## Dtypes

See linked format references and Purpose.

## Defaults

Parser defaults appear in the generated options table.

## Choices

Parser choices appear in the generated options table.

## Ordering

The target retains original PWM orientation. Pairing starts at the left edge.

## Side effects

Reads declared inputs and writes declared outputs; source motif arrays are not
mutated.

## Example

Even width, odd width, and tied consensus columns from inline MEME files:

```bash
cat > /tmp/dtv-even.meme <<'EOF'
MEME version 4

ALPHABET=ACGT

strands: + -

Background letter frequencies
A 0.25 C 0.25 G 0.25 T 0.25

MOTIF EVEN2
letter-probability matrix: alength= 4 w= 2 nsites= 8 E= 1e-4
0.700000  0.100000  0.100000  0.100000
0.100000  0.700000  0.100000  0.100000
EOF

MotifTools dinucleotide_transversion \
  --motif_file /tmp/dtv-even.meme \
  --motif_name EVEN2 \
  --output /tmp/dtv-even.fasta
```

That even-width example writes:

```text
>dinucleotide_transversion_EVEN2
CA
```

```bash
cat > /tmp/dtv-odd.meme <<'EOF'
MEME version 4

ALPHABET=ACGT

strands: + -

Background letter frequencies
A 0.25 C 0.25 G 0.25 T 0.25

MOTIF ODD3
letter-probability matrix: alength= 4 w= 3 nsites= 8 E= 1e-4
0.700000  0.100000  0.100000  0.100000
0.100000  0.700000  0.100000  0.100000
0.100000  0.100000  0.700000  0.100000
EOF

MotifTools dinucleotide_transversion \
  --motif_file /tmp/dtv-odd.meme \
  --motif_name ODD3 \
  --output /tmp/dtv-odd.fasta
```

That odd-width example writes:

```text
>dinucleotide_transversion_ODD3
CAC
```

```bash
cat > /tmp/dtv-tied.meme <<'EOF'
MEME version 4

ALPHABET=ACGT

strands: + -

Background letter frequencies
A 0.25 C 0.25 G 0.25 T 0.25

MOTIF TIED
letter-probability matrix: alength= 4 w= 2 nsites= 8 E= 1e-4
0.400000  0.400000  0.100000  0.100000
0.400000  0.400000  0.100000  0.100000
EOF

MotifTools dinucleotide_transversion \
  --motif_file /tmp/dtv-tied.meme \
  --motif_name TIED \
  --output /tmp/dtv-tied.fasta
```

That tied-column example writes:

```text
>dinucleotide_transversion_TIED
TT
```
