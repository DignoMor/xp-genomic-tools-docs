# MotifTools

CLI for motif-centric generation and transformation workflows.

```bash
MotifTools --help
MotifTools <subcommand> --help
```

Motif **scoring** against genomic-element or exogenous-sequence collections remains in
[`GenomicElementTools`](GenomicElementTools.md) and
[`ExogenousSequenceTools`](ExogenousSequenceTools.md). MotifTools owns motif
generation and collection transforms such as anti-motifs.

## Shared output flags

Every subcommand accepts:

| Flag | Meaning |
| --- | --- |
| `--output` | Destination path, or `-` for stdout (MEME or FASTA data only) |
| `--force` | Replace an existing destination file (not allowed with `--output -`) |

Path outputs require an existing parent directory, refuse silent overwrite, and
complete with an atomic rename. Successful path commands are silent.

## Commands

| Command | Status | Role |
| --- | --- | --- |
| `anti_motif` | Implemented | Derive an anti-motif MEME collection from an input MEME file |
| `pwm_seq` | Implemented | Sample sequences from one named PWM |
| `random_seq` | Implemented | Generate random sequences with optional motif exclusions |
| `barcodes` | Implemented | Enumerate motif-filtered barcodes exhaustively |

### `anti_motif`

Transform every motif in a supported-subset MEME file into an inverse-enrichment
anti-motif. Output motif names are prefixed with `anti_` and remain in source
order.

Retained `nsites` and E-value fields describe the **source motif** copied as
provenance. They are not newly inferred statistics for the derived anti-motif.

Example:

```bash
MotifTools anti_motif --motif_file motifs.meme --output anti.meme
MotifTools anti_motif --motif_file motifs.meme --output -
```

Reusable Python API: [`RGTools.MotifGeneration.make_anti_motifs`](../reference/python/motifs/motif-generation.md).

### `pwm_seq`

Sample a requested number of sequences from one named motif in a supported-subset
MEME file. Output sequences follow the motif PWM row probabilities using the
collection alphabet. FASTA record identifiers are `pwm_<motif_name>_<index>`
(zero-based).

Example:

```bash
MotifTools pwm_seq --motif_file motifs.meme --motif_name MY_MOTIF --num_sequences 100 --seed 0 --output pwm.fasta
MotifTools pwm_seq --motif_file motifs.meme --motif_name MY_MOTIF --num_sequences 5 --output -
```

Reusable Python API: [`RGTools.MotifGeneration.iter_pwm_sequences`](../reference/python/motifs/motif-generation.md).

### `random_seq`

Generate a requested number of fixed-length random sequences by sampling uniformly
with replacement from an ordered alphabet (default `ACGT`). Optional motif exclusions
reject candidates whose windows on either strand meet selected MEME score cutoffs.
FASTA record identifiers are `random_seq_<index>` (zero-based).

Example:

```bash
MotifTools random_seq --sequence_length 20 --num_sequences 1000 --seed 0 --output controls.fasta
MotifTools random_seq --sequence_length 8 --num_sequences 5 --alphabet XY --output -
MotifTools random_seq --sequence_length 12 --num_sequences 10 --motif_file motifs.meme --exclude MY_MOTIF=8.5 --seed 0 --output filtered.fasta
```

When exclusions cannot be satisfied within the per-output attempt budget (default
10,000), the command exits with code 1 and writes no partial final file.

Reusable Python API: [`RGTools.MotifGeneration.iter_random_sequences`](../reference/python/motifs/motif-generation.md).

### `barcodes`

Enumerate every barcode of a requested length in supplied-alphabet Cartesian order.
Optional motif exclusions retain only candidates that pass the same cutoff rules as
`random_seq`. The pre-exclusion candidate count is checked against
`--max_candidates` (default 1,000,000) before work begins. FASTA identifiers are
`barcode_<index>` in accepted order. When no barcodes survive exclusion, the command
succeeds silently and writes zero-byte FASTA output.

Example:

```bash
MotifTools barcodes --barcode_length 6 --output barcodes.fasta
MotifTools barcodes --barcode_length 4 --alphabet ACGT --motif_file motifs.meme --exclude MY_MOTIF=8.5 --output filtered.fasta
```

Reusable Python API: [`RGTools.MotifGeneration.iter_barcodes`](../reference/python/motifs/motif-generation.md).

## Python module entrypoint

```bash
python -m MotifTools --help
python -m MotifTools anti_motif --motif_file motifs.meme --output anti.meme
```

## Reference

- [MotifTools command reference](../reference/cli/motif-tools/index.md)
- [CLI exact command-path index](../reference/cli/exact-path-index.md)
- [MEME motif format](../reference/formats/motifs/meme.md)
