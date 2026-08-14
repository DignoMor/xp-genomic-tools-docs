# `RGTools.BedTable.BedRegion`

## Purpose

Represent one BED-like interval with `chrom`, `start`, `end`, and optional fields.

## Availability

Supported in release `0.1.0a2`; canonical import is `RGTools.BedTable.BedRegion`.

## Inputs

`BedRegion(chrom, start, end, **other_fields)`. Mapping access uses `region[field]`; `to_dict()` and `get_fields()` expose fields; `pad_region(upstream_padding, downstream_padding, ignore_strand=False)` creates a padded region.

## Types

Chromosome is a string; coordinates are integer-like; extra fields preserve caller values.

## Shapes

One region has one half-open interval `[start, end)`.

## Dtypes

No coercion contract is promised for extra fields.

## Defaults

`ignore_strand=False`; padding values are required.

## Choices

Strand is `+` or `-`; `ignore_strand=True` treats the region as `+`.

## Constraints

Padding is immutable-style and must leave `start < end` and `start >= 0`.

## Outputs

`to_dict` returns a copy; `get_fields` returns field names; `pad_region` returns a new `BedRegion`. Equality compares only coordinates and chromosome; ordering is chromosome, start, end.

## Ordering

Comparisons sort lexicographically by `(chrom, start, end)`.

## Side effects

No method mutates the source region.

## Failures

Missing/invalid strand raises `InvalidStrandnessException`; invalid padded coordinates raise `InvalidBedRegionException`; unknown mapping keys raise `KeyError`.

## Public members

`BedRegion`, `to_dict`, `get_fields`, `pad_region`, `__getitem__`, `__eq__`, `__lt__`, `__le__`, `__gt__`, and `__ne__`.
