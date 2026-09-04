# `MotifTools barcodes`

## Availability

Supported in `MotifTools` for release `0.4.0a1`. Invoke through the installed `MotifTools` console script.

## Purpose

**Purpose.** Exhaustively enumerate motif-filtered barcodes in supplied-alphabet order.

## Inputs

| Flag | Required | Meaning |
| --- | --- | --- |
| `--barcode_length` | yes | Positive barcode length |
| `--alphabet` | no | Ordered unique-character alphabet (default `ACGT`) |
| `--motif_file` | no | MEME collection required when exclusions are used |
| `--exclude` | no | Repeatable `MOTIF=CUTOFF` |
| `--max_candidates` | no | Pre-exclusion candidate limit (default `1000000`) |
| `--output` | yes | Output FASTA path or `-` |
| `--force` | no | Replace an existing destination file |

## Constraints

Preflight the candidate count `len(alphabet) ** barcode_length` against
`--max_candidates`, then stream the Cartesian product in supplied-alphabet order.
Shared motif exclusions retain only surviving candidates. Identifiers are
`barcode_<index>` in accepted order.

## Outputs

UTF-8 FASTA with accepted barcode order, or zero bytes when no barcode
survives.

## Failures

Invalid lengths, alphabets, oversized candidate spaces, exclusion
validation failures, and shared output-contract violations raise validation errors
before output begins.

## Reference fields

**Purpose:** motif generation and transformation CLI. **Availability:** with the
installed release that documents this page. **Inputs:** MEME paths and shared
output flags. **Types:** paths and text streams. **Defaults:** none beyond
parser defaults in the generated reference. **Choices:** subcommand names listed
above. **Constraints:** shared output contract and anti-motif provenance rules.
**Outputs:** MEME subset files or stdout MEME text. **Ordering:** anti-motifs
preserve source motif order. **Side effects:** atomic path writes only.
**Failures:** exit codes `2` (usage/validation) and `1` (I/O) without
tracebacks for expected failures.

## Types

Paths and schema keys are strings unless noted in Purpose.

## Shapes

Annotation arrays align by first dimension with region or sequence order.

## Dtypes

See linked format references and Purpose.

## Defaults

Parser defaults appear in the generated options table.

## Choices

Parser choices appear in the generated options table.

## Ordering

Output rows retain input order unless stated otherwise in Purpose.

## Side effects

Reads declared inputs and writes declared outputs; inputs are not mutated.

## Example

With `MotifTools` installed:

```bash
MotifTools barcodes \
  --barcode_length 2 \
  --alphabet AC \
  --output /tmp/barcodes-spec.fasta
```

Identical inputs reproduce these FASTA bytes in release `0.4.0a1`:

```text
>barcode_0
AA
>barcode_1
AC
>barcode_2
CA
>barcode_3
CC
```
