# GenomicElementTools command reference

This is the semantic reference for release `0.3.0a4`. It covers every shipped
top-level command and nested path. Exact usage, aliases, parser-required flags,
choices, defaults, and parser help are maintained in the [generated argparse
reference](../generated/genomic-element-tools.md); the sections below add the
constraints that argparse cannot express.

## Availability

Supported in `GenomicElementTools` for release `0.3.0a4`.

## Purpose

`GenomicElementTools` operates on genomic-element collections: [BED-like region
tables](../../../formats/foundation/bed-like.md) with aligned
[annotation arrays](../../../formats/elements/annotation-arrays.md). Commands
group into region and signal work (BigWig quantification, padding, TSS point
BED, context lookup, [TSS-relative](../../python/general-elements/tss-relative-coordinates.md)
selection and mutagenesis), sequence and motif scoring on extracted windows,
boolean mask algebra, and nested import/export of regions plus attached
annotations. Parser-derived syntax for every path appears in the generated
reference linked above; the pages below document semantics argparse cannot
express.

## Example

Count per-region signal from one [BigWig](../../../formats/signal/bigwig.md)
over a BED6 table — see [`count_single_bw`](count-single-bw.md) for a minimal
worked invocation.
