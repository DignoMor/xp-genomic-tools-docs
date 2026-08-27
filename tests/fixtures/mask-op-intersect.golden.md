# `GenomicElementTools mask_op intersect`

## Purpose

Compute the element-wise logical AND across aligned boolean mask annotations.
This is boolean array algebra, not genomic interval intersection.

## Availability

Supported in `GenomicElementTools` for release `0.3.0a4`. Invoke it through the
installed `GenomicElementTools` console script.

## Inputs

- `--region_file_path`: a headerless supported BED-like region table. Its row
  count establishes mask length and alignment.
- `--region_file_type`: the region schema key shown in the generated choices.
- `--mask_npy`: a `.npy` array or `.npz` containing exactly one array. Supply
  the flag at least twice.

## Types

Paths and the region type key are strings. Each loaded mask is a NumPy array.

## Shapes

Each mask must have shape `(N,)` or `(N, 1)`, where `N` is the number of region
rows. The saved result has shape `(N, 1)`.

## Dtypes

Every input mask and the output use NumPy boolean dtype. See the
[boolean-mask format](../formats/boolean-mask.md#dtype).

## Defaults

No semantic input or output default applies: all four non-help flags are
required. The parser metadata default for `--region_file_type` is described
under Syntax because the required flag prevents that default from taking effect.

## Choices

`--region_file_type` accepts exactly the parser-derived choices in the table.
The remaining flags have no enumerated choices.

## Constraints

Provide at least two masks. All masks must have boolean dtype, an accepted
shape, and first-dimension alignment with the region table. A single-array NPZ
is accepted; a multi-array NPZ is rejected.

## Outputs

`--opath` receives a NumPy `.npy` boolean mask containing the logical AND of all
inputs. Use a `.npy` suffix; if the supplied path has no suffix, NumPy appends
`.npy`. The filename is not used to select another output format.

## Ordering

Output row `i` corresponds to region row `i`. Input mask order does not change
the result because logical AND is commutative.

## Side effects

Reads the region and mask files and writes or replaces the file at `--opath`
(or `--opath.npy` when NumPy appends the missing suffix). No region table is
modified.

## Failures

Argparse exits for missing required flags or invalid region-type choices. The
command raises `ValueError` for fewer than two masks, non-boolean masks, shape
or region-count mismatches, multi-array NPZ input, or an unsupported region
schema encountered while loading.

## Example

Intersect two boolean masks aligned to the same three-region BED3 table:

```bash
GenomicElementTools mask_op intersect \
  --region_file_path regions.bed3 \
  --region_file_type bed3 \
  --mask_npy mask_a.npy \
  --mask_npy mask_b.npy \
  --opath intersect.npy
```

Each input mask has shape `(3,)` or `(3, 1)` with boolean dtype. The saved
`intersect.npy` contains the element-wise logical AND with shape `(3, 1)`.
