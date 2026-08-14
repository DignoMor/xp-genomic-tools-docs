# Motif-search track outputs

For each motif in a supported MEME file, `motif_search` writes one `.npy`
track named `<output_header>.<motif_name>.npy`. The track is row-aligned to
FASTA order and has one score per sequence position (`(N,L)` for homogeneous
sequences). Scores use MEME alphabet/background rules, pseudocount smoothing,
and `+` or `both` strand search according to `--reverse_complement`.

## Purpose
Reusable motif score tracks.
## Availability
Release `0.1.0a2`.
## Inputs
FASTA and supported MEME subset.
## Types
Floating score arrays.
## Shapes
`(N,L)` for homogeneous sequence lengths.
## Dtypes
Native motif-search numeric dtype.
## Defaults
Estimate background true; reverse complement false.
## Choices
`+` or `both` strand mode.
## Constraints
Rows align to FASTA records.
## Outputs
One `.npy` per motif.
## Ordering
Motif and sequence input order.
## Side effects
Creates one output file per motif.
## Failures
Invalid MEME/FASTA or incompatible lengths fail.
