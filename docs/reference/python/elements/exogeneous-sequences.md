# `ExogeneousSequences`

## Status

Supported for the current reference release.

## Purpose

Load exogenous FASTA records into memory and expose the shared
`GeneralElements` annotation, filtering, and sequence operations against
synthetic BED3 regions. Narrative prose uses “exogenous”; the public class
identifier remains `ExogeneousSequences` for this release.

## Canonical import

```python
from RGTools import ExogeneousSequences
```

## Signature

Curated constructor and member signatures rendered from the aligned release
source:

::: RGTools.ExogeneousSequences.ExogeneousSequences
    options:
      members:
        - __init__
        - fasta_path
        - region_file_type
        - region_file_path
        - get_sequence_ids
        - get_region_bed_table
        - get_all_region_seqs
        - get_all_region_lens
        - apply_logical_filter
        - write_sequences_to_fasta
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_"

## Parameters

Constructor argument is `fasta_path`, a path to a multi-record FASTA file.
`apply_logical_filter` accepts a boolean mask and output FASTA path.
`write_sequences_to_fasta` accepts parallel `seq_ids`, `sequences`, and
`fasta_path`.

## Return or yield behavior

The constructor returns a live collection. Methods return sequence lists,
synthetic region tables, filtered collections, or `None` for static writers.
Inherited annotation and sequence helpers behave as on
[`GeneralElements`](../general-elements/general-elements.md).

## Raised exceptions

`region_file_path` raises `NotImplementedError`. Existing output paths for
filter or static write raise `ValueError`. Annotation alignment and dtype
failures raise `ValueError` as on `GeneralElements`.

## Constraints

Synthetic regions use `chrom=seq_id`, `start=0`, `end=len(sequence)`.
`region_file_type` is fixed to `"bed3"`. IDs and sequence counts must pair when
writing FASTA output.

## Ordering

FASTA record order is preserved for IDs, sequences, and synthetic regions.
Filtered collections retain mask-selected order.

## Side effects

Construction reads the entire FASTA into memory. `apply_logical_filter` and
`write_sequences_to_fasta` create new files and refuse existing destinations.
Inherited annotation loaders mutate in-memory arrays only until an explicit
save.

## Lifecycle behavior

Call `close()` (inherited) to release any cached FASTA index used by inherited
sequence helpers. Prefer explicit cleanup in long-running scripts.

## Supported protocols and inheritance

`ExogeneousSequences` subclasses `GeneralElements`. Supported inherited
operations include `get_region_seq`, annotation load/save/getters,
`get_all_region_one_hot`, `close`, and `one_hot_encoding`. Parser assembly
helpers are internal and excluded from this page.

## Example

```python
from RGTools import ExogeneousSequences

es = ExogeneousSequences("synthetic.fa")
print(es.get_sequence_ids())
sequences = es.get_all_region_seqs()
es.close()
```

## Related formats or commands

- [FASTA region sequences](../../formats/elements/fasta.md)
- [`ExogeneousSequenceTools` CLI](../../cli/exogeneous-sequence-tools/index.md)
