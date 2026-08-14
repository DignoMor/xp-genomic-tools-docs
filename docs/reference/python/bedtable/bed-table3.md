# `RGTools.BedTable.BedTable3`

## Purpose

Manage headerless BED3 tables with `chrom`, `start`, and `end` columns.

## Availability

Supported in release `0.1.0a2`; canonical import is `RGTools.BedTable.BedTable3`.

## Inputs

`BedTable3(enable_sort=True)`; load from TSV, pandas DataFrame, or `BedRegion` list. Public operations include `load_from_file`, `load_from_dataframe`, `load_from_bed_regions`, `apply_logical_filter`, `region_subset`, `to_dataframe`, `write`, coordinate getters, `get_region_by_index`, `iter_regions`, `search_region`, `concat`, `subset_by_index`, and `copy`.

## Types

`chrom` is string, `start` and `end` are integer columns. Coordinate getters return NumPy arrays; filters are one-dimensional boolean arrays.

## Shapes

All operations preserve row alignment. A logical filter has length `N`; subset results have selected row counts.

## Dtypes

Columns are forced to the declared pandas-compatible string/integer types.

## Defaults

Sorting is enabled and uses lexicographic `(chrom, start, end)` order.

## Choices

Files are tab-separated, headerless; `-`/`stdin` reads stdin and `stdout` writes stdout.

## Constraints

`region_subset` returns fully contained regions. `search_region` returns regions overlapping at least `overlapping_base` bases. Missing values write as `.`.

## Outputs

Load/write mutate or serialize the table; selection/copy/concat return new tables. `len(table)` is row count.

## Ordering

Sorting applies when enabled; disabling it preserves loaded order and annotation alignment.

## Side effects

Load replaces contents; write performs file/stream I/O; no file handles remain open after operations.

## Failures

Column/schema mismatch raises `BedTableLoadException`; non-boolean or wrong-length filters raise `ValueError`; I/O errors propagate.

## Public members

`BedTable3`, `column_names`, `column_types`, `extra_column_names`, `extra_column_dtype`, `load_from_file`, `load_from_dataframe`, `load_from_bed_regions`, `apply_logical_filter`, `region_subset`, `to_dataframe`, `write`, `get_chrom_names`, `get_start_locs`, `get_end_locs`, `get_region_by_index`, `iter_regions`, `search_region`, `concat`, `subset_by_index`, `copy`, and `__len__`.
