# ExogeneousSequenceTools reference

This is the semantic reference for the `ExogeneousSequenceTools` console
script in release `0.1.0a2`. It covers all seven top-level commands and every
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

## `assemble`

The nested `operation` is required and is one of `add_adapter`, `concat`, or
`barcode`. All operations write a new FASTA and preserve produced sequence
order.

### `assemble add_adapter`

Flags: `--fasta` (required), `--left_adapter_fasta` (required),
`--right_adapter_fasta` (optional, default `None`), and `--output_fasta`
(required). Each adapter FASTA must contain exactly one record. The output for
input record `i` is `left + input_i + right`, with the input ID unchanged;
omitting the optional right adapter means an empty string. A multi-record
adapter raises `ValueError`; file/FASTA errors are non-zero failures. See the
[adapter and assembly output format](../../formats/cli/exogeneous-sequence-tools/assembly-outputs.md).

### `assemble concat`

Flags `--fasta5`, `--fasta3`, and `--output_fasta` are required.
`--id_method` choices are `5`, `3`, and `5_3` (default `5_3`). Records are
paired by positional `zip` order (extra records are ignored). Output sequence
`i` is `seq5_i + seq3_i`; its ID is respectively `id5_i`, `id3_i`, or
`id5_i_id3_i`. Invalid methods raise `ValueError`. The output is ordered by
the paired inputs.

### `assemble barcode`

Required repeatable flags: `--barcode_fasta`, `--input_fasta`, and
`--input_class`; required outputs: `--output_fasta` and `--metadata_path`.
`--barcode_method` choices `5`, `3`, `5_3` (default `5_3`) place the barcode
before, after, or on both sides. `--fasta_id_type` choices `original` and
`barcode` (default `original`) select element IDs or the full barcode list as
FASTA IDs. Barcodes are consumed in order across input FASTAs; input classes
are applied in corresponding input-file order. The total element count must
not exceed barcode count (`ValueError`). Metadata CSV columns are
`barcode,class,elem_id,elem_seq`, in consumption order. See the
[assembly output format](../../formats/cli/exogeneous-sequence-tools/assembly-outputs.md).

## `mutagenesis`

Required flags are `--fasta`, `--loc_npy`, `--mut_fasta`, and `--output_fasta`.
`loc_npy` is a stat array of shape `(N, 1)` (integer offsets, zero-based) and
is aligned to the input records. If input and mutation FASTAs have equal
record counts, entries pair element-wise. Otherwise each target is applied to
every input, with targets as the outer loop and inputs as the inner loop.
Replacement at `loc` is `seq[:loc] + target + seq[loc+len(target):]`.
Output IDs are `<input_id>_mut_<target_id>`, and output ordering follows the
pairing mode above. Sequence length is preserved when replacement spans the
same length; the implementation otherwise permits length changes. Invalid
FASTA/NPY or shape/alignment errors are non-zero failures. See the
[mutagenesis input/output format](../../formats/cli/exogeneous-sequence-tools/mutagenesis.md).

## `gen_track single_loc`

`operation=single_loc` is required. Flags `--fasta`, `--loc` (required
integer), and `--output_npy` (required) produce an integer `int64` stat array
of shape `(N, 1)`, every row equal to `loc`, aligned to FASTA order. The
output is written as `.npy`; input and output filesystem errors fail
non-zero. See [track/stat arrays](../../formats/cli/exogeneous-sequence-tools/track-stat-arrays.md).

## `track_dim_reduction`

The required nested operation is `max`, `argmax`, `min`, or `argmin`. Required
flags are `--input_npy` and `--output_npy`; `--search_range` is an optional
`start,end` string, defaulting to the full track. Input must be a 2-D track
`(N, L)`. Columns outside the zero-based half-open range `[start,end)` are
set to negative infinity before reduction. Reduction is axis 1 with
`keepdims=True`, yielding `(N,1)`: max/min values retain the numeric dtype
(subject to NumPy promotion), while argmax/argmin are integer indices. The
row order is unchanged. Note that the same `-inf` masking is used for min and
argmin, so an all-masked or partly masked search can select a masked column;
this is current behavior. Malformed ranges, wrong dimensionality, and NumPy
load/save errors fail non-zero. See [track/stat arrays](../../formats/cli/exogeneous-sequence-tools/track-stat-arrays.md).

## `print_stat`

`--input_npy` is required. The input must have a second dimension of exactly
1 (normally `(N,1)`); otherwise `ValueError` is raised. Values in column 0
are printed one per line, in row order, using NumPy's normal string
conversion. There is no output file and no mutation of the input.

## `motif_search`

Required flags are `--fasta`, `--motif_file`, and `--output_header`.
`--estimate_background_freq` is parsed as a boolean (`str2bool`), default
`true`; `--reverse_complement` is the same type, default `false`. MEME motifs
are read in file order. One track `.npy` is written per motif at
`<output_header>.<motif_name>.npy`, with shape `(N,L)` for homogeneous input
sequences and each row aligned to its sequence. Tracks are named by motif;
the score search uses strand `+` unless reverse-complement mode selects
`both`. Background estimation, `N` handling, pseudocount `(counts+1)/(sites+
alphabet_size)`, and reverse-complement estimation follow the implementation.
Invalid MEME/FASTA, incompatible track lengths, and filesystem errors fail
non-zero. See [motif track outputs](../../formats/cli/exogeneous-sequence-tools/motif-outputs.md).

## `onehot`

Required flags are `--fasta` and `--opath`. All sequences must have the same
length `L`. The output is an array annotation saved to `--opath` with shape
`(N,4,L)`, channel order `A,C,G,T`, and dtype `numpy.int8`;
ambiguous IUPAC bases encode as zeros. Rows and channels preserve sequence
and alphabet order. Mixed lengths raise `ValueError`; malformed FASTA and
save errors fail non-zero. See [one-hot arrays](../../formats/cli/exogeneous-sequence-tools/onehot-outputs.md).

## Purpose
Complete semantic reference for all ExogeneousSequenceTools paths.
## Availability
Release `0.1.0a2`.
## Inputs
FASTA, NumPy, MEME, and scalar parser inputs.
## Types
Strings, paths, booleans, integers, records, and NumPy arrays.
## Shapes
Tracks `(N,L)`, stats `(N,1)`, one-hot `(N,4,L)`.
## Dtypes
Generated locations are `int64`; other rules are path-specific.
## Defaults
Parser-derived defaults are linked above.
## Choices
Nested operations and method choices are listed per path.
## Constraints
Alignment, homogeneity, adapter, and barcode constraints apply.
## Outputs
FASTA, CSV, `.npy`, or stdout.
## Ordering
Input order except explicit broadcast target-major ordering.
## Side effects
Creates requested outputs; inputs are not modified.
## Failures
Missing flags exit 2; validation and I/O failures exit non-zero.
