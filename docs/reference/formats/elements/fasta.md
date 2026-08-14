# FASTA profiles

## Genome FASTA

**Purpose:** sequence source for `GenomicElements`. **Inputs/types:** standard
multi-FASTA records, with string record IDs exactly matching region `chrom`.
BED coordinates are 0-based, half-open; extraction returns the string slice
`[start:end]`. **Ordering:** output follows region-table order. **Failures:**
missing chromosome returns `None` for `get_region_seq` and raises during bulk
extraction/export. Genome FASTA is read/indexed, not written by this API.

## Exogenous and exported FASTA

`ExogeneousSequences` reads all records in file order and exposes synthetic
BED3 `(id,0,len)` regions. `write_sequences_to_fasta` and genomic export write
standard `>id` records; genomic export uses `chrom:start-end`, refuses an
existing destination, and preserves region order. Sequence collections and
annotation first dimensions must remain aligned.

**Defaults/choices/shapes/dtypes:** no line-wrapping, alphabet, or dtype
conversion is promised; sequences are strings and lengths are integer bases.

## Reference fields

**Purpose:** genome and exogenous sequence records. **Availability:** `0.1.0a2`.
**Inputs:** multi-FASTA and BED half-open coordinates. **Types:** IDs/sequences
are strings; coordinates are integers. **Shapes:** sequence length is
`end-start`; synthetic rows are BED3. **Dtypes:** sequence text has no NumPy
dtype; coordinates are integer. **Defaults:** start inclusive, end exclusive.
**Choices:** genome, exogenous, or exported-region profiles. **Constraints:**
IDs match `chrom`; order remains aligned. **Outputs:** strings, synthetic
regions, or FASTA files. **Ordering:** source/region order. **Side effects:**
indexing reads; writers create files and export refuses overwrite. **Failures:**
missing chromosomes, malformed FASTA, and existing paths fail as stated.
