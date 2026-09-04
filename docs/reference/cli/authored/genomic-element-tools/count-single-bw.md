# `GenomicElementTools count_single_bw`

## Availability

Supported in `GenomicElementTools` for release `0.4.0a1`. Invoke through the installed `GenomicElementTools` console script.

## Purpose

Count [`--bw_path` BigWig](../../../formats/signal/bigwig.md) signal for the
regions supplied by `--region_file_path` and `--region_file_type` ([BED-like
region table](../../../formats/foundation/bed-like.md)).

## Types

BigWig is a signal track. `--quantification_type`
choices are `raw_count`, `RPK`, and `full_track`; scalar modes produce stat
values `(N,)`, while `full_track` produces a track `(N, L_i)` (variable lengths
are represented by the library's track convention).

## Defaults

`--opath` is required. The default quantification
is `raw_count`; `.npz` selects NPZ output and every other suffix selects NPY.
The BigWig must be readable and cover queried regions.

## Outputs

Writes [annotation](../../../formats/elements/annotation-arrays.md) named
`count`, in input order. Missing/corrupt BigWig, unsupported quantification,
region loading, or incompatible lengths raise library errors; parser errors
exit 2.

## Inputs

See Purpose and the parser-derived options table.

## Shapes

Annotation arrays align by first dimension with region or sequence order.

## Dtypes

See linked format references and Purpose.

## Choices

Parser choices appear in the generated options table.

## Constraints

See Purpose and linked format references.

## Ordering

Output rows retain input order unless stated otherwise in Purpose.

## Side effects

Reads declared inputs and writes declared outputs; inputs are not mutated.

## Failures

Argparse exits for missing required flags or invalid choices; runtime validation errors propagate from the implementation.

## Example

Count raw signal over three gene bodies from one BigWig:

```bash
GenomicElementTools count_single_bw \
  --region_file_path genes.bed6 \
  --region_file_type bed6 \
  --bw_path signal.bw \
  --quantification_type raw_count \
  --opath counts.npz
```

The output is a `count` stat annotation with shape `(N,)` aligned to the input
region order; `.npz` selects NPZ serialization and other suffixes select NPY.
