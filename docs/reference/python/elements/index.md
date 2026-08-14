# Element collections

These are the supported `RGTools` element collection interfaces for release
`0.1.0a2`. Import concrete classes from `RGTools`; `GeneralElements` is the
abstract shared base.

Every entry below states the acceptance fields: **Purpose**, **Availability**,
**Inputs**, **Types**, **Shapes**, **Dtypes**, **Defaults**, **Choices**,
**Constraints**, **Outputs**, **Ordering**, **Side effects**, and **Failures**.

## `GeneralElements`

**Purpose**  Shared sequence, annotation, filtering, and lifecycle operations.

**Availability**  `from RGTools import GeneralElements`; abstract and not
instantiable directly. `GenomicElements` and `ExogeneousSequences` inherit the
operations below.

**Constructor**  `GeneralElements()` (`__init__`) is called by subclasses. **Inputs:** no
user arguments. **Types/shapes/dtypes:** annotations start empty. **Defaults:**
no cached FASTA index. **Constraints:** subclasses implement the abstract
properties `fasta_path`, `region_file_type`, `region_file_path` and methods
`get_region_bed_table`, `get_all_region_seqs`, and `apply_logical_filter`.

**Properties and inherited operations:** `fasta_path` (FASTA path),
`region_file_type` (schema key), `region_file_path` (region path), `close()`
(releases the cached index), `get_region_seq(chrom, start, end,
index_genome=True)` (BED 0-based half-open string, or `None` for a missing
chromosome), `get_region_lens()` (one length per region),
`get_num_regions()` (integer), `get_all_region_one_hot()` (int8 shape
`(N,L,4)`; requires homogeneous lengths), and `one_hot_encoding(seq)` (static,
int8 shape `(L,4)`, alphabet A,C,G,T; IUPAC ambiguity is zero; an illegal
non-IUPAC character raises `AssertionError`). `__del__` is best-effort cleanup.

**Annotations:** `load_region_anno_from_npy(anno_name, npy_path,
anno_type="array")`, `load_region_track_from_list`, `load_region_stat_from_arr`,
`load_mask_from_arr`, `load_region_array_from_arr`, `get_anno_dim`,
`get_anno_type`, `get_track_list`, `get_stat_arr`, `get_mask_arr`,
`get_arr_anno`, `get_region_track_by_index`, `get_region_stat_by_index`,
`get_region_mask_by_index`, `get_region_array_by_index`, `save_anno_npy`, and
`save_anno_npz` are public. Annotation row `i` remains aligned to region row
`i`; see [annotation arrays](../../formats/elements/annotation-arrays.md).

**Failures:** invalid types, dimensions, first-dimension alignment, track
lengths, non-boolean masks, and multi-array NPZ raise `ValueError`; unknown
annotation names or wrong getter kinds raise `ValueError` (index errors
propagate). Type metadata is in memory only, never serialized.

## `GenomicElements`

**Purpose/availability:** `from RGTools import GenomicElements` combines a
headerless typed region table with a genome FASTA. **Constructor** (`__init__`):
`GenomicElements(region_file_path, region_file_type, fasta_path)`; paths are
strings/path-like values, type is one of `bed3`, `bed6`, `bed3gene`, `bed6gene`,
`narrowPeak`, `TREbed`, `bedGraph`. Region order is preserved (sorting is
disabled) for annotation alignment. Invalid type raises `ValueError`.

**Properties/methods:** `get_region_bed_table()` returns a copy;
`get_all_region_seqs()` returns one sequence per row and fails if a chromosome
is absent; `apply_logical_filter(logical, new_region_file_path)` writes a new
region table, carries every annotation through the same boolean selection, and
returns a new collection; `export_exogeneous_sequences(fasta_path)` writes
`chrom:start-end` FASTA headers, refuses an existing path, and raises
`ValueError` for missing chromosomes; `get_num_regions` and every
`GeneralElements` operation are inherited. Static public factories are
`get_region_file_suffix2class_dict`, `BedTable6Gene`, `BedTable3Gene`,
`BedTableNarrowPeak`, `BedTableBedGraph`, `BedTableTREBed`, plus the supported
CLI-adjacent helpers `set_parser_genome` and
`set_parser_genomic_element_region`, and
`merge_genomic_elements(left_ge, right_ge, output_region_path, anno2merge,
sort_new_ge=True)`. Merge requires matching region type and FASTA path and
raises `ValueError` on incompatible annotations.

Unrelated parser-construction internals remain excluded from this reference.

**Inputs/types/shapes/dtypes/defaults/choices/outputs/order/failures:** see
the constructor, annotation rules above, and the [region and FASTA formats](../../formats/elements/fasta.md).

## `ExogeneousSequences`

**Purpose/availability:** `from RGTools import ExogeneousSequences` loads all
records from an exogenous FASTA into memory. **Constructor** (`__init__`):
`ExogeneousSequences(fasta_path)`; IDs are strings and sequences are strings.

**Properties/methods:** `fasta_path` is the source path, `region_file_type` is
fixed to `"bed3"`, and `region_file_path` raises `NotImplementedError`.
`get_sequence_ids()` preserves FASTA record order; `get_region_bed_table()`
returns synthetic BED3 rows `(id, 0, len(sequence))`;
`get_all_region_seqs()`, `get_all_region_lens()`, and all inherited sequence
and annotation operations apply in that order. `apply_logical_filter(logical,
new_fasta_path)` writes selected records, carries annotations, and returns a
new collection. Static `write_sequences_to_fasta(seq_ids, sequences,
fasta_path)` writes paired records. The supported CLI-adjacent helpers
`set_parser_genome` and `set_parser_exogeneous_sequences` register supported
arguments on a supplied argparse parser and return `None`; other parser
construction internals remain excluded.

**Constraints/failures:** IDs and sequence counts must pair; annotations must
align to the synthetic rows. File and FASTA parser errors propagate.

## Reference fields

**Purpose:** element collections. **Availability:** `0.1.0a2`. **Inputs:**
paths, region keys, sequences, and annotations. **Types:** strings, paths,
lists, and NumPy arrays. **Shapes:** aligned arrays start with `N`;
per-region tracks follow region lengths. **Dtypes:** masks are `numpy.bool_`,
one-hot output is `int8`. **Defaults:** annotations empty; indexed FASTA
access. **Choices:** documented region keys and annotation kinds.
**Constraints:** row alignment and valid BED coordinates. **Outputs:** tables,
sequences, arrays, and files. **Ordering:** current region/FASTA order.
**Side effects:** loaders mutate annotations; writers create files; `close`
releases resources. **Failures:** invalid paths, keys, shapes, dtypes, missing
chromosomes, and incompatible merges raise documented errors.
