# CLI quickstart: smoke test then genomic export

This path separates installation checks from data problems: first run a
deterministic MotifTools command with **no input files**, then export exogenous
sequences from the same synthetic genomic inputs used in the
[Python quickstart](python-quickstart.md).

## Step 0 — synthetic genomic inputs

Download or copy these deliberate **synthetic** assets (not private test
fixtures):

| Asset | Role |
| --- | --- |
| [quickstart-synthetic-regions.bed3](assets/quickstart-synthetic-regions.bed3) | Two-region [bed3](../reference/formats/foundation/bed3.md) table |
| [quickstart-synthetic-genome.fa](assets/quickstart-synthetic-genome.fa) | Matching reference [FASTA](../reference/formats/elements/fasta.md) |

Place them in a working directory (for example `./assets/`).

## Step 1 — zero-input MotifTools smoke test

[`MotifTools random_seq`](../reference/cli/motif-tools/random-seq.md) needs only
length, count, seed, and an output path:

```bash
MotifTools random_seq \
  --sequence_length 8 \
  --num_sequences 2 \
  --seed 0 \
  --output random-smoke.fasta
```

Release **0.3.0a4** reproduces these bytes exactly:

```text
>random_seq_0
TTAGTTGT
>random_seq_1
GCCGCAGC
```

If this command fails, fix installation before debugging genomic inputs.

## Step 2 — export exogenous sequences from genomic regions

[`GenomicElementTools export ExogenousSequences`](../reference/cli/genomic-element-tools/export/exogenous-sequences.md)
extracts each region's sequence as FASTA using the
[`ExogenousSequences`](../reference/python/elements/exogenous-sequences.md)
contract:

```bash
GenomicElementTools export ExogenousSequences \
  --fasta_path assets/quickstart-synthetic-genome.fa \
  --region_file_path assets/quickstart-synthetic-regions.bed3 \
  --region_file_type bed3 \
  --opath region-sequences.fasta
```

Expected output for the synthetic inputs:

```text
>chrB:1-5
GGGC
>chrA:0-4
ACGT
```

IDs and row order follow the BED table, not chromosome sorting.

## Next steps

- [Python quickstart](python-quickstart.md) for the same inputs in `RGTools`
- [GenomicElementTools CLI reference](../reference/cli/genomic-element-tools/index.md)
- [Motif generation and search guide](../guides/motif-generation-and-search.md)
