# `RGTools.BedTable.BedTablePairEnd`

!!! warning "Experimental"
    This is the only API in this reference slice labeled experimental. A later release may change or remove it without a deprecation period when disclosed in release notes.

## Purpose

Represent paired intervals in the custom ten-column-plus layout; this is distinct from standard BEDPE.

## Availability

Experimental in release `0.1.0a2`; canonical import is `RGTools.BedTable.BedTablePairEnd`.

## Inputs

Construct with optional extra columns. The fixed columns are `chrom,start,end,chrom2,start2,end2,name,score,strand,strand2`; use inherited loading/I/O plus pair getters and `search_second_region`/pair-aware search.

## Types

Chromosomes/strands/names are strings, coordinates integers, score float, extras caller-declared.

## Shapes

Each row contains two intervals and optional extra values.

## Dtypes

Columns are forced to their declared schema types.

## Defaults

Sorting is always enabled; there is no disable-sort hook.

## Choices

This layout is custom and is not standard BEDPE.

## Constraints

Sorting is by the first mate. The second-mate inverse index is rebuilt on load.

## Outputs

Pair coordinate/name/score/strand getters (`get_other_region_chroms`, `get_other_region_starts`, `get_other_region_ends`, `get_pair_names`, `get_pair_scores`, `get_region_strands`, `get_other_region_strands`) return one array value per row; `get_region_extra_column` returns an extra-column array; searches return matching indices.

## Ordering

First-mate lexicographic `(chrom,start,end)` ordering applies.

## Side effects

Loading replaces table contents and rebuilds the second-mate index; writing performs TSV I/O.

## Failures

Schema/column mismatch raises `BedTableLoadException`; inherited filter and I/O failures apply.

## Public members

`BedTablePairEnd`, `column_names`, `column_types`, `extra_column_names`, `extra_column_dtype`, `get_other_region_chroms`, `get_other_region_starts`, `get_other_region_ends`, `get_pair_names`, `get_pair_scores`, `get_region_strands`, `get_other_region_strands`, `get_region_extra_column`, `search_pair_extra_column`, and `search_second_region`.
