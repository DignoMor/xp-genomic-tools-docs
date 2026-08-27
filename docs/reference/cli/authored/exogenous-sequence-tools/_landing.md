# ExogenousSequenceTools reference

This is the semantic reference for the `ExogenousSequenceTools` console
script in release `0.3.0a4`. It covers all seven top-level commands and every
nested path. Parser-derived spelling, required status, choices, defaults, and
help appear on each canonical command page and in the
[site-wide exact-path index](../exact-path-index.md). The inventory used
for completeness checks is [`inventory.json`](inventory.json).

## Shared model and process behavior

An exogenous FASTA is read in record order. Each record is a synthetic BED3
row `(id, 0, len(sequence))`; there is no genome BED input. Annotation row
`i` belongs to FASTA record `i`. Paths are filesystem paths and outputs are
created by the command; commands do not mutate the input FASTA. Missing flags
are rejected by argparse (process exit 2); unreadable files, malformed FASTA,
NumPy errors, and library validation errors terminate with a non-zero process
exit and their underlying exception when invoked through the console script.

## Format references

- [Exogenous FASTA](../../formats/cli/exogenous-sequence-tools/exogenous-fasta.md)
- [Assembly outputs](../../formats/cli/exogenous-sequence-tools/assembly-outputs.md)
- [Mutagenesis](../../formats/cli/exogenous-sequence-tools/mutagenesis.md)
- [Track and stat arrays](../../formats/cli/exogenous-sequence-tools/track-stat-arrays.md)
- [Motif outputs](../../formats/cli/exogenous-sequence-tools/motif-outputs.md)
- [One-hot outputs](../../formats/cli/exogenous-sequence-tools/onehot-outputs.md)

## Purpose

`ExogenousSequenceTools` transforms exogenous sequence libraries represented as
ordered FASTA records with synthetic BED3 coordinates (see [Exogenous
FASTA](../../formats/cli/exogenous-sequence-tools/exogenous-fasta.md)). Commands
assemble barcoded or adapter-flanked constructs, generate per-base tracks and
stats, run mutagenesis at indexed positions, search motifs across each sequence,
and reduce track dimensionality — without requiring a genome reference BED.

## Example

Attach 5′ and 3′ adapters to an exogenous library — see
[`assemble add_adapter`](assemble/add-adapter.md) for required FASTA inputs and
the [assembly output contract](../../formats/cli/exogenous-sequence-tools/assembly-outputs.md).
