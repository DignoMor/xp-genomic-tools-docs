# GenomicElementTools command reference

This is the semantic reference for release `0.3.0a1`. It covers every shipped
top-level command and nested path. Exact usage, aliases, parser-required flags,
choices, defaults, and parser help are maintained in the [generated argparse
reference](../generated/genomic-element-tools.md); the sections below add the
constraints that argparse cannot express.

## Shared contract

**Purpose.** Operate on an ordered Genomic Elements (GE) region table, with
optional annotations and a genome FASTA. Region coordinates are BED 0-based,
half-open (`start` inclusive, `end` exclusive). Region tables are headerless,
tab-separated, and selected annotations align by first dimension with the
current region order.

**Availability.** `GenomicElementTools` is the shipped console entry point in
`0.3.0a1`; no separate count-table console entry point is shipped. Missing required flags or invalid
argparse choices exit with standard argparse status 2. Runtime data and
contract violations generally raise `ValueError` or the underlying library
exception; exact exception messages are not part of the interface.

**Types.** Paths and schema keys are strings. Region tables contain typed
BED-like rows.

**Shapes.** Annotation arrays have first dimension `N`, the number of regions:
stat is scalar per row (normally `(N,)` or `(N, 1)`), track is per-base/
per-position (`(N, L)`), mask is boolean (`(N,)` or `(N, 1)`), and array is a
general per-row array.

**Dtypes.** Masks must be NumPy `bool` dtype; integer 0/1 arrays are rejected.
NPZ inputs must contain exactly one array unless the operation explicitly says
otherwise.

**Defaults.** Defaults are operation-specific and are stated in each path.

**Choices.** Parser-derived choices are listed in the generated reference;
semantic choices are repeated in the relevant path below.

**Constraints.** First-dimension alignment, coordinate conventions, and
operation-specific restrictions are stated per path.

**Outputs.** Each path identifies its serialized or visual output.

**Ordering.** Unless stated otherwise, output rows and annotation values retain
input order; annotation row `i` belongs to region row `i`. Outputs overwrite
the requested path (or create the suffix selected by the operation).

**Side effects.** Commands read the declared region, genome, annotation, track,
motif, or remote-service inputs and write the declared output files; they do
not mutate input files.

**Failures.** Missing required flags and invalid choices exit through argparse;
invalid files, mismatched lengths/shapes, unsupported dtypes, unavailable
records, and operation-specific violations raise the documented `ValueError`,
library, or I/O failure.

## Command paths

Each subsection supplies the applicable semantic fields. The parser table in
the generated reference is authoritative for every flag spelling, alias,
required status, choice, and default.

### `count_single_bw`

**Purpose / Inputs.** Count `--bw_path` BigWig signal for the regions supplied by
`--region_file_path` and `--region_file_type`.

**Types / shapes / dtypes.** BigWig is a signal track. `--quantification_type`
choices are `raw_count`, `RPK`, and `full_track`; scalar modes produce stat
values `(N,)`, while `full_track` produces a track `(N, L_i)` (variable lengths
are represented by the library's track convention).

**Defaults / constraints.** `--opath` is required. The default quantification
is `raw_count`; `.npz` selects NPZ output and every other suffix selects NPY.
The BigWig must be readable and cover queried regions.

**Outputs / side effects / failures.** Writes annotation named `count`, in
input order. Missing/corrupt BigWig, unsupported quantification, region
loading, or incompatible lengths raise library errors; parser errors exit 2.

### `count_paired_bw`

**Purpose / Inputs.** Count paired plus/minus BigWigs `--bw_pl` and `--bw_mn`.
Regions use the shared flags; `--override_strand` optionally supplies strand.
`--negative_mn` and `--flip_mn` are required booleans.

**Types / shapes / dtypes.** `raw_count`, `RPK`, and `full_track` have the same
stat-versus-track shapes as `count_single_bw`; output annotation is `count`.

**Defaults / constraints.** Quantification defaults to `raw_count`; strand is
resolved from override, then region strand, with bed3/falsy strand becoming
`.`. `.npz` alone selects NPZ; other suffixes select NPY. Both tracks must be
readable.

**Outputs / ordering / failures.** One value/track per input row, in order.
Track, region, boolean, or quantification errors are library errors; argparse
validation exits 2.

### `pad_region`

**Purpose / Inputs.** Pad or shrink each region by `--upstream_pad` and
`--downstream_pad`; `--ignore_strand` controls strand-aware interpretation.

**Defaults / choices / constraints.** Invalid intervals use
`--method_resolving_invalid_region`: `raise`, `fallback` (default), or `drop`.
`--opath` is required. No FASTA is required.

**Outputs / ordering / failures.** Writes the same region schema. Kept rows
retain input order; `drop` reduces row count, while `fallback` retains the
original row. Invalid padding with `raise` raises
`InvalidBedRegionException`; malformed regions and parser errors fail.

### `bed2tssbed`

**Purpose / Inputs.** Convert each region to a one-base BED interval. `--output_site`
is `TSS` (default) or `center`; `--opath` is required.

**Constraints / outputs.** TSS is `start` on `+` and `end - 1` on `-`; center is
`(start + end) // 2`. Non-coordinate columns are preserved and rows remain in
order. Output has `[site, site+1)` coordinates and the input schema.

**Failures.** Missing/invalid strand for TSS and unknown output site follow the
legacy library failure (`UnboundLocalError` for those unresolved cases); parser
choice failures exit 2.

### `onehot`

**Purpose / Inputs.** Extract `--fasta_path` sequences for the GE regions and
write the one-hot encoding to required `--opath`.

**Types / shapes / dtypes.** Output is an `int8` NumPy one-hot array transposed
to `(N, 4, L)`; regions must be equal length (`L`) and FASTA IDs must exactly
match region chromosomes. Channel order is explicitly `A, C, G, T`.

**Outputs / side effects / failures.** Writes NPY via `np.save`, preserving
region order. Missing FASTA records, unequal lengths, invalid coordinates, and
unreadable input raise library errors.

### `motif_search`

**Purpose / Inputs.** Score each FASTA-backed region against motifs in required
`--motif_file` (MEME profile). `--output_header` names outputs.

**Defaults / choices / constraints.** `--estimate_background_freq` defaults
true; `--strand` choices are `+`, `-`, `both` (default `+`). Motif files must
be valid supported MEME and sequences must be readable.

**Outputs / shapes / ordering.** For each motif, writes
`<output_header>.<motif_name>.npy`, a track annotation aligned to regions in
input order. Motif name sanitization follows the implementation's filename
rules. Missing chromosomes, invalid MEME, or incompatible motif lengths fail.

### `track2tss_bed`

**Purpose / Inputs.** Use required `--track` annotation to locate a point per
region; `--output_site` currently supports `MaxAbsSig` (default).

**Types / shapes / outputs.** Track has first dimension `N`; for row `i`, site
is `region.start + argmax(abs(track[i]))`. Writes one-base intervals to required
`--opath`, preserving order and non-coordinate columns.

**Failures.** Track/region alignment, indexing, or unknown output site raises
`ValueError` or a library error; parser failures exit 2.

### `filter_motif_score`

**Purpose / Inputs.** Filter motif tracks from required `--motif_search_npy`
using required integer `--filter_base`, with `--min_score` and `--max_score`.

**Defaults / constraints.** Defaults are `-inf` and `+inf`; retention is strict:
`min_score < track[filter_base] < max_score`. Track first dimension aligns to
regions.

**Outputs / ordering / failures.** Writes `<output_header>.bed` and
`<output_header>.motif.npy`, preserving surviving row order. Out-of-range base,
alignment errors, or empty-result library limitations can raise indexing or
library errors.

### `select_tss_relative_track`

**Purpose / Inputs.** Select a TSS-relative score from required `--track_npy`
relative to a TREbed TSS. Requires `--strand` (`+` or `-`), nonzero
`--target_coord`, finite `--min_score`, `--coordinate_opath`, and
`--mask_opath`. Shared region flags are required and `--region_file_type` must
be `TREbed`. Track and output paths accept `.npy` or single-array `.npz`.

**Defaults / constraints.** `--relaxation` defaults to `0` (exact coordinate)
and expands to `2r+1` ascending no-zero coordinates for `r > 0`.
`--track_window_size` defaults to `1` for point tracks; set it to the motif
width when consuming motif-search tracks. Strand `+` uses `fwdTSS`; strand `-`
uses `revTSS`. Tracks stay genomic-forward indexed: plus coordinates identify
the genomic-left strand-oriented 5-prime base of the scored window, and minus
coordinates identify the genomic-right 5-prime base (internal trailing padding
is `window_size - 1`). Selection takes the first maximum in ascending
TSS-relative order and matches with an inclusive cutoff
(`max_score >= min_score`). A selected TSS of `-1` is a row-level no-match; the
unselected TSS is ignored. A nonmissing selected TSS must lie inside
`[start,end)`, and every relaxed-window position must map to a complete scored
window inside the row's logical track length (storage padding beyond that
length is never searched). These operation-level indexing rules are stricter
than format-level TREbed readability.

**Outputs / ordering / failures.** Writes integer coordinates and a boolean mask
as `(N,1)` annotations in input row order only after every row is validated.
Matches emit the selected nonzero coordinate and `true`; no-matches emit `0`
and `false`. Existing destinations are refused unless `--force` is supplied;
either existing path blocks both publications. Forced replacement stages
complete files beside each destination (`.stem.staging.npy` /
`.stem.staging.npz`), backs up existing files (`.basename.bak`), publishes both
with `os.replace`, and rolls back from backups on ordinary commit failure.
Interrupted staging or backup remnants are reported without automatic cleanup.
Boolean/nonnumeric tracks,
unsupported suffixes, multi-array NPZ inputs, invalid window size or
relaxation, zero target, nonfinite cutoffs, searched NaN (with row/track-index
context), out-of-interval selected TSS, unavailable windows, missing parent
directories, and track shape/alignment errors raise before destinations are
created or changed. Score `-inf` is unmatchable; `+inf` is a qualifying
maximum. Compose the mask with `mask_op` and subset regions plus aligned
coordinate stats with `export MaskedGE`.

### `tss_relative_mutagenesis`

**Purpose / Inputs.** Apply one or more sequential TSS-relative replacement
rounds to sequences extracted from a TREbed collection. Requires shared region
flags with `--region_file_type TREbed`, `--fasta_path`, required
`--round_manifest`, and required `--output_dir`. Optional
`--write_replaced_windows` emits per-round audit FASTAs; optional `--force`
authorizes replacing an existing output directory after successful staging.

**Round manifest.** Tab-separated manifest with an exact header:
`round_id`, `coordinate_stat`, `target_fasta`, `strand`. One data row defines
one mutation round; row order is execution order. The manifest must contain at
least one round. Round IDs are nonempty, unique, and safe as filename
components (letters, digits, `.`, `_`, `-` only). Paths in `coordinate_stat`
and `target_fasta` resolve relative to the manifest's parent directory when not
absolute.

**Coordinate stats.** Each round's `coordinate_stat` is an integer `(N,1)`
annotation aligned to the original TREbed row order, where `N` is the region
count. Float-valued integral coordinates are not coerced. Coordinate zero is
invalid and rejected during preflight.

**Target FASTAs.** Each round's `target_fasta` supplies one or more mutation
targets as FASTA records. Record IDs must be nonempty, unique, free of ASCII
whitespace, and must not contain the reserved output delimiter `|`. Every target
sequence must be nonempty IUPAC DNA (case is preserved). All targets within one
round must have equal positive length; different rounds may use different
lengths. The first round defines the target-ID set and output order; every later
round must contain exactly the same ID set (later file order is ignored when
joining by ID).

**Mutation target groups.** A target group is the cross-round trajectory sharing
one target ID. Before round one, each original region expands across every target
group. With `N` regions and `M` target IDs per round, exactly `N × M` derived
sequences exist throughout all rounds. Derived-sequence order is region-major,
then first-round target-ID order.

**Strand / TSS semantics.** Each round's `strand` is exactly `+` or `-` and
applies to every row and target group in that round. Plus rounds use `fwdTSS`;
minus rounds use `revTSS`. A selected TSS of `-1` or a nonmissing selected TSS
outside `[start,end)` fails preflight. Placement uses the shared
`RGTools.TSSRelativeCoordinates` rules with the round's target length as the
replacement-window width. On minus rounds, target sequences are
reverse-complemented with IUPAC rules before insertion.

**Sequential rounds.** Rounds execute in manifest order. Each round replaces a
window equal to its target length inside the current derived sequence, so every
output sequence preserves the original region length after every round.
Overlapping rounds are allowed; later rounds overwrite earlier bases in
overlapping windows. Every replacement window must fit completely inside the
extracted region sequence before any round mutates sequences.

**Outputs / ordering.** Publishes an output-directory bundle (no stdout data
mode). Required artifacts:

- `sequences.fasta` — exactly `N × M` final records
- `manifest.tsv` — long-form mutation-event table with exactly `N × M × R` rows
  for `R` rounds

With `--write_replaced_windows`, the bundle also contains
`replaced/<round_id>.fasta` for every round. Each replaced-window record holds
the exact sequence removed immediately before that round inserts its target
(same IDs and record order as `sequences.fasta`; sequence length equals that
round's target length). For overlapping rounds, a later replaced window
includes changes from earlier rounds.

**Sequence IDs.** Stable FASTA IDs have the form
`rNNNNNN|chrom:start-end|target=TARGET_ID`, where the row number is one-based
and expands beyond six digits when needed. The row ordinal distinguishes
duplicate genomic intervals. `chrom` and target IDs must not contain `|`.

**Output manifest.** Tab-separated with exact columns, in order:
`sequence_id`, `region_row`, `chrom`, `start`, `end`, `region_name`,
`target_id`, `round_index`, `round_id`, `strand`, `tss_relative_coordinate`,
`target_length`. One row per derived sequence per round. `region_row` and
`round_index` are one-based; genomic interval fields remain BED zero-based
half-open. Rows are ordered by derived-sequence order, then round order within
each sequence.

**Publication / `--force`.** The output parent directory must already exist and
be writable; the command does not create missing parents. Without `--force`, an
existing output directory is rejected. The complete bundle is written to a
unique sibling staging directory, then published with rename-based replacement.
An ordinary publication failure restores the prior bundle. Interrupted staging
or backup siblings beside the output directory are detected and reported for
manual recovery rather than automatic cleanup. `--force` authorizes replacement
only of the exact resolved output directory.

**Preflight failures.** Validation runs before staging final artifacts:
TREbed-only region type; genome coverage; reserved `|` in chromosome names;
manifest header and round IDs; coordinate shape, dtype, and alignment; target
files, alphabets, lengths, and cross-round ID sets; selected TSS availability
and interval membership; coordinate zero; replacement-window bounds for every
derived sequence and round. Errors identify the round, region row, target
group, and coordinate where possible.

**Composition.** Typical upstream steps are
[`select_tss_relative_track`](#select_tss_relative_track) (coordinate stat and
mask), [`mask_op`](#mask_op-intersect) (combine masks), and
[`export MaskedGE`](#export-maskedge) (subset regions and aligned coordinate
stats). See the [TSS-relative mutagenesis workflow](../../../guides/tss-relative-mutagenesis.md).

### `get_context_ge nearest`

**Purpose / Inputs.** For each query region, select the closest same-chromosome
context from required `--context_file_path` / `--context_file_type`.

**Outputs / ordering / constraints.** Output uses the context schema and one
selected context per query, in query order; distance is the minimum absolute
distance among endpoint pairs. `--opath` is required and no FASTA is needed.

**Failures.** No context on a query chromosome raises `ValueError`; malformed
files and parser failures fail normally.

### `get_context_ge windowed_argmax`

**Purpose / Inputs.** Select the maximum-stat context inside each query window,
using required `--context_stat_path` aligned to context rows.

**Outputs / ordering / constraints.** A context is eligible only when fully
contained (`start >= window.start`, `end <= window.end`). Ties choose earliest
context index; one context is written per query in query order.

**Failures.** Empty eligible windows, stat/context mismatch, and malformed data
raise `ValueError` or a library error.

### `mask_op intersect`

**Purpose / Inputs.** Element-wise AND of at least two repeated `--mask_npy`
arrays aligned to shared region flags.

**Shapes / dtypes / outputs.** Inputs are boolean `(N,)` or `(N,1)`; output is
boolean `(N,1)` saved as NPY to required `--opath`. This is not interval
intersection. See the [mask format](../../formats/boolean-mask.md).

**Failures.** Fewer than two masks, non-boolean dtype, NPZ ambiguity, or length
mismatch raises `ValueError`/library error.

### `mask_op union`

Same inputs and shapes as `intersect`, but computes element-wise OR. Output is
boolean `(N,1)` NPY in region order. Fewer than two masks, non-boolean input,
ambiguous NPZ, and alignment failures raise `ValueError`/library errors.

### `mask_op opposite`

Takes one required boolean `--mask_npy`, computes element-wise NOT, and writes
boolean `(N,1)` NPY to `--opath`. Region alignment and non-boolean rejection are
the same as the other mask operations.

### `import stat_list`

**Purpose / Inputs.** Read one value per region from required `--inpath` ListFile
and save required `--opath` (`.npy` or `.npz`) as stat `region_list`.

**Defaults / types / constraints.** `--dtype` defaults to `str`; choices are
`str`, `np.int32`, `np.int64`, `np.float32`, `np.float64`. List length must equal
`N`; suffix other than `.npy`/`.npz` raises `ValueError`.

**Outputs / ordering / failures.** One stat per input region, in order. Bad
length, conversion, list file, or suffix raises `ValueError`/I/O errors.

### `import allele_expanded_ES`

**Purpose / Inputs.** Parse allele-expanded FASTA `--inpath` and emit regions
under `--anno_oheader`; optional parallel `--stat_name`, `--stat_npy`, and
`--stat_selection_method` lists must have equal lengths.

**Outputs / constraints.** Writes sorted `.bed3` groups and optional `.ref.npy`
and `.alt.npy` stats. IDs encode `chrom_start_end_ref` or
`chrom_start_end_<pos>:<ref>2<alt>`; each group has exactly one reference.

**Failures.** Bad headers, missing reference, unequal parallel lists, or invalid
selection methods raise `ValueError`.

### `export stat_list`

Exports required `--stat_npy` as one value per region to required `--opath`
(`-`/`stdout` allowed), with optional `--dtype`. Values retain region order;
length mismatch and conversion errors fail.

### `export ExogeneousSequences`

Requires genome FASTA plus GE regions and `--opath`; writes region sequences as
FASTA using the [FASTA profile](../../formats/elements/fasta.md). IDs and order
follow the ExogeneousSequences contract; missing records or invalid intervals
fail.

### `export WTES`

Same FASTA inputs as `ExogeneousSequences`, plus required integer
`--num_replicates`. Writes replicate copies in library-defined WTES ID/order;
invalid replicate counts and FASTA/region errors fail.

### `export allele_expanded_ES`

Requires genome, GE regions, polymorphism `--inpath_polymorphisms` (bed6+ bases
column), and `--opath`; optional `--job_name`. Writes TRE-centered reference/
alternate FASTA using the allele-expanded ID scheme above. Invalid bases,
coordinates, or unresolved variants fail.

### `export CountTable`

Takes repeated parallel `--sample_name`/`--stat_npy` pairs, GE regions, and CSV
`--opath`; `--region_id_type` is `default` or `gene_symbol`. Writes a reusable
[CountTable](../../formats/cli/genomic-element-tools/counttable.md): header
contains samples, rows are regions, and values remain in region order. Pair
lengths, stat alignment, and CSV output errors fail.

### `export Heatmap`

Takes parallel `--track_npy`/`--title`/`--negative` lists, percentile controls
(`--per_track_max_percentile` default 99; `--vmax_percentile` default 50), and
`--opath`. Writes a visual image only (no reusable format page); tracks align
to regions. Parallel-list, percentile, rendering, and I/O failures fail.

### `export ChromFilteredGE`

Reads `--chrom_size` and writes to `--opath` only rows whose chromosome occurs
in the size file. Output schema and surviving row order are preserved; malformed
size files and region I/O fail.

### `export MaskedGE`

Applies required boolean `--mask_npy` to GE regions and writes filtered regions;
optional parallel `--anno_name`/`--anno_npy`/`--anno_type` and `--anno_oheader`
filter annotations of type `track`, `stat`, `mask`, or `array`. Mask dtype and
first-dimension alignment are enforced. Output retains surviving order; mismatch
or non-boolean masks fail.

### `export TREbed`

Takes plus/minus signal tracks `--pl_sig_track` and `--mn_sig_track` and writes
TSS-regulatory-element rows to `--opath` using the reusable
[TREbed format](../../formats/cli/genomic-element-tools/trebed.md). Tracks
align to regions; coordinates are BED half-open and output order follows input.
Missing tracks, invalid shapes, and I/O errors fail.

### `export MergedGE`

Merges left/right region files with required region paths/type, parallel
annotation names/paths/types, and `--oheader`. Annotation types are only
`track`, `stat`, `mask`, or `array`; first dimensions align within each input.
Merged output follows library merge ordering and writes under the output header.
Mismatched parallel arguments, incompatible regions, or annotation errors fail.

### `export bed6poly`

Reads only `bed6` regions and writes a bed6+ polymorphism table to required
`--opath`. Optional `--genome_version` accepts `hg38`, `GRCh38`, `hg19`, or
`GRCh37` and defaults to `hg38`; optional `--rsid_not_found_handling` accepts
`raise` or `drop` and defaults to `raise`. See the [bed6poly format](../../formats/cli/genomic-element-tools/bed6poly.md).
RSIDs are resolved through Ensembl; `raise` propagates not-found/network errors,
while `drop` omits unresolved rows. Surviving rows retain input order.
