# `GeneralElements`

## Status

Supported for the current reference release. Abstract base class; do not
instantiate directly.

## Purpose

Define the shared element-collection contract for sequence access, annotation
load/save/getters, filtering, one-hot encoding, and FASTA-backed resource
lifecycle. Concrete collections implement the abstract hooks documented below.

## Canonical import

```python
from RGTools import GeneralElements
```

Concrete callers normally use `GenomicElements` or `ExogenousSequences`.

## Signature

Abstract contract and supported inherited operations rendered from the aligned
release source. Abstract hooks are marked in the generated output:

::: RGTools.GeneralElements.GeneralElements
    options:
      members:
        - __init__
        - fasta_path
        - region_file_type
        - region_file_path
        - get_region_bed_table
        - get_all_region_seqs
        - close
        - get_region_seq
        - get_region_lens
        - get_all_region_one_hot
        - apply_logical_filter
        - get_num_regions
        - load_region_anno_from_npy
        - load_region_track_from_list
        - load_region_stat_from_arr
        - load_mask_from_arr
        - load_region_array_from_arr
        - get_anno_dim
        - get_anno_type
        - get_track_list
        - get_stat_arr
        - get_mask_arr
        - get_arr_anno
        - get_region_track_by_index
        - get_region_stat_by_index
        - get_region_mask_by_index
        - get_region_array_by_index
        - save_anno_npy
        - save_anno_npz
        - one_hot_encoding
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_"

## Parameters

Subclasses supply `fasta_path`, `region_file_type`, `region_file_path`,
`get_region_bed_table`, `get_all_region_seqs`, and `apply_logical_filter`.
Annotation loaders accept names, paths or arrays, and optional type metadata as
documented on each member.

## Return or yield behavior

Methods return region tables, sequences, arrays, filtered collections, or
`None` for in-place annotation attachment. `get_region_seq` returns a string or
`None` for a missing chromosome.

## Raised exceptions

Invalid annotation types, dimensions, alignment, track lengths, non-boolean
masks, and multi-array NPZ raise `ValueError`. Unknown annotation names or
wrong getter kinds raise `ValueError`. Illegal non-IUPAC characters in
`one_hot_encoding` raise `AssertionError`.

## Constraints

Annotation row `i` must align with region row `i`. NPZ inputs must contain
exactly one array. Masks require boolean dtype.

## Ordering

Region order from the backing table or FASTA record order is preserved unless a
subclass operation explicitly sorts or filters.

## Side effects

Loaders mutate in-memory annotation dictionaries. `close` releases a cached
FASTA index. File writes occur only through explicit save or subclass filter
operations.

## Lifecycle behavior

Call `close()` to release the cached FASTA index. The destructor attempts
best-effort cleanup. Prefer explicit `close()` in long-running scripts.

## Supported protocols and inheritance

`GeneralElements` is abstract. Subclasses must implement the abstract
properties and methods above. Parser assembly helpers and underscore-prefixed
internals are not part of the supported public surface.

## Example

```python
from RGTools import GenomicElements

ge = GenomicElements("regions.bed3", "bed3", "genome.fa")
ge.load_mask_from_arr("passing", mask_arr)
ge.close()
```

## Related formats or commands

- [FASTA region sequences](../../formats/elements/fasta.md)
- [Annotation arrays](../../formats/elements/annotation-arrays.md)
- [`GeneralElements.load_mask_from_arr()`](load-mask-from-arr.md)
