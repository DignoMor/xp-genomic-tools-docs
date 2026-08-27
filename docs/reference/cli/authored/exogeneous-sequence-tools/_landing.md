# ExogeneousSequenceTools reference

This is the semantic reference for the `ExogeneousSequenceTools` console
script in release `0.3.0a4`. It covers all seven top-level commands and every
nested path. Exact parser spelling, required status, choices, defaults, and
help text are generated from the installed argparse tree:
[generated syntax](../generated/exogeneous-sequence-tools.md). The inventory
used for completeness checks is [`inventory.json`](inventory.json).

## Shared model and process behavior

An exogenous FASTA is read in record order. Each record is a synthetic BED3
row `(id, 0, len(sequence))`; there is no genome BED input. Annotation row
`i` belongs to FASTA record `i`. Paths are filesystem paths and outputs are
created by the command; commands do not mutate the input FASTA. Missing flags
are rejected by argparse (process exit 2); unreadable files, malformed FASTA,
NumPy errors, and library validation errors terminate with a non-zero process
exit and their underlying exception when invoked through the console script.

## Format references

- [Exogenous FASTA](../../formats/cli/exogeneous-sequence-tools/exogenous-fasta.md)
- [Assembly outputs](../../formats/cli/exogeneous-sequence-tools/assembly-outputs.md)
- [Mutagenesis](../../formats/cli/exogeneous-sequence-tools/mutagenesis.md)
- [Track and stat arrays](../../formats/cli/exogeneous-sequence-tools/track-stat-arrays.md)
- [Motif outputs](../../formats/cli/exogeneous-sequence-tools/motif-outputs.md)
- [One-hot outputs](../../formats/cli/exogeneous-sequence-tools/onehot-outputs.md)
