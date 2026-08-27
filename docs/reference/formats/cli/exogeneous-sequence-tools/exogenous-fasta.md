# Exogenous FASTA profile

**Purpose:** input and output sequence records for `ExogeneousSequenceTools`.
Records are standard FASTA `>id` plus sequence text, read in file order;
IDs are strings and sequences are strings of bases. Each record is represented
internally as BED3 `(id,0,len)`, using zero-based, half-open coordinates.
There is no required alphabet normalization or line-wrapping promise.

**Alignment:** row `i` and every annotation row `i` refer to FASTA record `i`.
Writers preserve supplied ID and sequence order. Missing/unreadable files and
malformed FASTA fail with a library/file error and a non-zero CLI exit.

## Purpose
Exogenous sequence interchange.
## Availability

Supported in the current reference release (`0.3.0a4`).

Available since `0.1.0a2`.

## Inputs
Multi-record FASTA.
## Types
String IDs and sequence text.
## Shapes
One variable-length sequence per record.
## Dtypes
Text; no NumPy dtype.
## Defaults
BED view starts at zero.
## Choices
FASTA record IDs and sequences.
## Constraints
Annotation rows align with record order.
## Outputs
FASTA records and synthetic BED3 rows.
## Ordering
Source record order.
## Side effects
Output files are created by writers.
## Failures
Malformed or unreadable files fail.

## Related API and CLI

- [`ExogeneousSequences`](../../../python/elements/exogeneous-sequences.md)
- [`ExogeneousSequenceTools`](../../../cli/exogeneous-sequence-tools/index.md)
