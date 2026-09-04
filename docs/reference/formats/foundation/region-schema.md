# Region schema (version 1)

## Purpose

Declare a BED3 or BED6 base plus ordered extra columns so
`GenomicElements` can load headerless metadata-bearing region tables through
the existing three-argument constructor.

## Availability

Supported in the current reference release (`0.4.0a1`).

## Inputs

A UTF-8 JSON object with exactly three root fields:

```json
{
  "schema_version": 1,
  "base_type": "bed6",
  "extra_columns": [
    {"name": "gene symbol (ref)", "dtype": "str"},
    {"name": "count", "dtype": "int"},
    {"name": "score_extra", "dtype": "float"}
  ]
}
```

`extra_columns` may be empty for plain BED3 or BED6 tables.

## Types

`schema_version` must be the integer `1`. `base_type` is exactly `bed3` or
`bed6`. Each extra column declares a `name` and a `dtype` of exactly `str`,
`int`, or `float`.

## Shapes

Region rows remain headerless and tab-delimited. Every row must have exactly
the base column count plus the declared extras. Annotation row `i` stays
aligned with region row `i`.

## Dtypes

Safe dtype names map to Python `str`, `int`, and `float`. The disk missing-value
marker remains `.` for all three dtypes and round-trips through table write.

## Defaults

`GenomicElements` disables BedTable sorting so input row order is preserved.

## Choices

Pass a predefined named format (`bed3`, `bed6`, `bed3gene`, `bed6gene`,
`narrowPeak`, `TREbed`, `bedGraph`) or a schema-file path as the Python
`region_file_type` constructor argument. Predefined names win over same-named
files; select a shadowed file with an explicit relative path such as `./bed3`
or an absolute path. Relative schema paths resolve from the current working
directory.

On generic `GenomicElementTools` primary region inputs, choose exactly one of:

- `--region_file_type` with a named format choice, or
- `--region_file_schema` with a path to this JSON file.

The flags are mutually exclusive. Named choices remain the argparse choice
list; schema paths are ordinary filesystem paths and are not listed as named
choices. Both selectors feed the same `GenomicElements` constructor boundary.

## Constraints

Extra names must be nonempty and unique, must not collide with the selected
base columns, and must not contain tab, newline, carriage-return, or NUL.
Spaces and ordinary punctuation are allowed. Unknown root or extra-column
fields, unsupported versions, and unsupported bases are rejected. Matching
column names alone do not confer named-format semantics such as TREbed.
TREbed-only commands therefore continue to require `--region_file_type TREbed`
and reject `--region_file_schema` even when the JSON declares the same fields.

Generic commands use schema capabilities (BED3 geometry; BED6 name, score, and
strand when present). Region-preserving operations keep ordered extras,
dtypes, values, and row-order guarantees. Fixed-schema exporters such as
FASTA, TREbed, polymorphism BED6+, and NumPy annotation outputs emit only the
fields their own contracts declare and do not acquire arbitrary custom extras.
Region-preserving outputs do not automatically publish a schema sidecar; reuse
the original schema file. Schema and region validation complete before command
outputs are created or replaced.

Context selection (`get_context_ge`) gives the query and context collections
independent mutually exclusive selectors. Selected context rows keep the
context schema. Collection and CLI merges accept the same named format or the
same canonical custom schema file when snapshotted schemas are structurally
compatible; distinct schema files are not merge-compatible even when they
declare the same columns. Custom merge outputs use `.bed3plus` or `.bed6plus`
according to the resolved base.

## Outputs

Named and custom selectors construct `BedTable3Plus` or `BedTable6Plus`
tables, including schemas with no extras. Direct `BedTable3` / `BedTable6` /
Plus construction APIs remain available independently.

## Ordering

Extra columns follow declaration order. Filtering and other derived collection
construction preserve extra names, dtypes, values, row order, and annotation
alignment.

## Side effects

Construction reads the schema file once and snapshots the resolved table
constructor. Later changes or deletion of that schema file do not alter
operations on the live collection.

## Failures

Malformed JSON, unreadable selectors, contract violations, wrong column
counts, and unparseable values fail before a usable collection is returned.
Exception text includes a contextual fragment naming the failing field or
selector.

## Related API and CLI

- [`GenomicElements`](../../python/elements/genomic-elements.md)
- [BED-like region tables](bed-like.md)
- [`BedTable Plus`](../../python/bedtable/bed-table-plus.md)
- [`GenomicElementTools`](../../cli/genomic-element-tools/index.md)
