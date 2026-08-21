# MotifTools

CLI for motif-centric generation and transformation workflows.

```bash
MotifTools --help
MotifTools <subcommand> --help
```

Motif **scoring** against genomic-element or exogeneous-sequence collections remains in
[`GenomicElementTools`](GenomicElementTools.md) and
[`ExogeneousSequenceTools`](ExogeneousSequenceTools.md). MotifTools owns motif
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
| `random_seq` | Planned | Generate random sequences with optional motif exclusions |
| `barcodes` | Planned | Enumerate motif-filtered barcodes |

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

## Python module entrypoint

```bash
python -m MotifTools --help
python -m MotifTools anti_motif --motif_file motifs.meme --output anti.meme
```

## Reference

- [MotifTools command reference](../reference/cli/motif-tools/index.md)
- [Generated parser inventory](../reference/cli/generated/motif-tools.md)
- [MEME motif format](../reference/formats/motifs/meme.md)
