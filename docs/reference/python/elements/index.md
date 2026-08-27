# Element collections

Supported `RGTools` element collection interfaces for the current reference
release. Import concrete classes from `RGTools`; `GeneralElements` is the
abstract shared base.

## `GeneralElements`

See the dedicated [`GeneralElements`](../general-elements/general-elements.md)
reference page for the abstract contract, curated inherited operations,
mkdocstrings-rendered signatures, and lifecycle requirements.

## `GenomicElements`

See the dedicated [`GenomicElements`](genomic-elements.md) reference page for
the supported constructor, curated members, mkdocstrings-rendered signatures,
and complete semantic contract.

## `ExogenousSequences`

See the dedicated [`ExogenousSequences`](exogenous-sequences.md) reference
page for exogenous FASTA loading, synthetic BED3 regions, filtering, and
supported inherited operations. Narrative prose uses “exogenous”; the public
class identifier remains `ExogenousSequences` for this release.

## Related operations

- [`GeneralElements.load_mask_from_arr()`](../general-elements/load-mask-from-arr.md)
- [`TSSRelativeCoordinates`](../general-elements/tss-relative-coordinates.md)

## Related formats

- [FASTA region sequences](../../formats/elements/fasta.md)
- [Annotation arrays](../../formats/elements/annotation-arrays.md)
- [BED-like region tables](../../formats/foundation/bed-like.md)
