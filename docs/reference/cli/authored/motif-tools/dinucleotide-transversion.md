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
| `--warn_score_cutoff` | no | Finite real diagnostic cutoff (default `0`). Inclusive comparison on either strand; stderr only |

## Constraints

The collection is loaded through the existing `MemeMotif` parser. Required
`nsites` and `E` remain in force; collections that omit those matrix-header
statistics stay rejected. Deferred statistics-free MEME compatibility is not
provided. Matrix dimensions and current validation remain in force.
The selected alphabet must contain exactly A, C, G, and T. PWM columns follow
declared alphabet order; ties use letter order A, C, G, T.

Consensus is the maximum-probability base in each column. Pairs are taken from
position zero in original PWM orientation. For consensus A or G the allowed
replacements are C and T; for consensus C or T they are A and G. Each pair
selects the allowed dinucleotide with the minimum product of the two
source-PWM probabilities. Equal products, including zeros, resolve
lexicographically A, C, G, T. An unmatched terminal chooses its
minimum-probability allowed transversion with the same letter order. Width one
and uninformative columns are retained. Every position transverts relative to
the derived consensus, not necessarily relative to an observed genomic allele.
There is no seed, method selector, sampling, or genomic-allele input.

Identical inputs reproduce FASTA bytes within a given MotifTools install.

## Outputs

UTF-8 FASTA with LF line endings, exactly one unwrapped uppercase A/C/G/T
sequence of full PWM width, identifier
`dinucleotide_transversion_<motif_name>`, and a final newline. Path and stdout
bytes are identical. Stdout is FASTA-only; source-motif warnings use stderr.

## Failures

Empty collections, unknown motif names, unsupported alphabets, invalid PWM
rows or dimensions, missing required source statistics, non-finite
`--warn_score_cutoff` values, and shared output-contract violations fail
before any target is published.

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
Callers reverse-complement the FASTA when inserting at minus-strand hits in
genomic-forward parents; this command does not orient by genomic strand.

## Side effects

Reads declared inputs and writes declared outputs; source motif arrays are not
mutated. After generation, the CLI scores the isolated full-width target
against the selected source motif on both strands with
`MemeMotif.calculate_pwm_score` (declared alphabet, MEME background
frequencies, log10 scoring, existing numerical epsilon). If either score is
at or above `--warn_score_cutoff`, it prints a warning on stderr naming the
motif, both strand scores, and the cutoff, then still publishes the same
FASTA with exit status 0. Changing the cutoff or MEME background changes
diagnostics only.

Default cutoff `0` is a heuristic score threshold, not a p-value. Reduced
motif score and motif knockout are not guaranteed. The check covers only the
source motif inside the isolated target; evaluate other motifs or insertion
boundaries separately if required.

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

and this warning on stderr, because the reverse-complement score is above the
default heuristic cutoff `0`. That warning is not a p-value and does not prove
or disprove motif knockout:

```text
Warning: motif TIED scores -0.7958800168 (forward) and 0.4082399652 (reverse complement) against the source PWM; cutoff 0.
```

The even-width and odd-width examples above emit no source-motif warning at
default cutoff `0`. A width-one fixture whose forward score equals the cutoff
warns on stderr and still writes FASTA:

```bash
cat > /tmp/dtv-warn.meme <<'EOF'
MEME version 4

ALPHABET=ACGT

strands: + -

Background letter frequencies
A 0.25 C 0.25 G 0.25 T 0.25

MOTIF FWD0
letter-probability matrix: alength= 4 w= 1 nsites= 8 E= 1e-4
0.400000  0.250000  0.100000  0.250000
EOF

MotifTools dinucleotide_transversion \
  --motif_file /tmp/dtv-warn.meme \
  --motif_name FWD0 \
  --output -
```

That command writes the following FASTA on stdout:

```text
>dinucleotide_transversion_FWD0
C
```

and this warning on stderr:

```text
Warning: motif FWD0 scores 0 (forward) and -0.3979400084 (reverse complement) against the source PWM; cutoff 0.
```

Compose the generated FASTA with ordinary-offset mutagenesis. The mutagenesis
command is unchanged: aligned integer offsets have shape `(N, 1)`, and
callers reverse-complement the target for minus-strand hits.

```bash
python - <<'PY'
from pathlib import Path
import numpy as np
Path("/tmp/parent302.fa").write_text(">parent302\n" + "A" * 302 + "\n")
np.save("/tmp/parent302.loc.npy", np.array([[10]], dtype=np.int64))
PY

MotifTools dinucleotide_transversion \
  --motif_file /tmp/dtv-odd.meme \
  --motif_name ODD3 \
  --output /tmp/dtv-odd.fasta

ExogenousSequenceTools mutagenesis \
  --fasta /tmp/parent302.fa \
  --loc_npy /tmp/parent302.loc.npy \
  --mut_fasta /tmp/dtv-odd.fasta \
  --output_fasta /tmp/parent302.mut.fa
```

That plus-strand replacement keeps parent length 302, inserts `CAC` at offset
10, and names the record `parent302_mut_dinucleotide_transversion_ODD3`. For a
minus-strand hit, reverse-complement the generated sequence (`GTG` for this
odd-width example) before passing `--mut_fasta`; neither command orients
automatically.
