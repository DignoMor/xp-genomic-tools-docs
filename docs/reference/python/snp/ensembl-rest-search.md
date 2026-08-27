# `EnsemblRestSearch`

## Status

Supported for the current reference release. This client depends on the Ensembl
REST service; documentation builds do not perform live network requests.

## Purpose

Query Ensembl variation records and choose SNP-like variants at genomic
locations. Returned dictionaries follow the
[Ensembl SNP simple-info profile](../../formats/snp/ensembl-simple-info.md).

## Canonical import

```python
from RGTools.SNP_utils import EnsemblRestSearch
```

## Signature

Supported public members rendered from the aligned release source. Internal
underscore-prefixed helpers are excluded from this page:

::: RGTools.SNP_utils.EnsemblRestSearch
    options:
      members:
        - __init__
        - genome_version2url_dict
        - get_rsid_from_location
        - get_rsid_snp_simple_info
        - prioritize_rsids
      show_root_heading: true
      show_source: false
      heading_level: 4
      inherited_members: false
      filters:
        - "!^_"

## Parameters

`EnsemblRestSearch(genome_version="hg38", species="human")` configures the
service. `get_rsid_from_location(chrom, pos)` takes a chromosome and a
zero-based position. `get_rsid_snp_simple_info(rsid)` and `prioritize_rsids(rsids)`
take rsID strings or an iterable of them.

## Return or yield behavior

`get_rsid_from_location` returns a list of rsID strings.
`get_rsid_snp_simple_info` returns a dictionary with `chrom`, `start`, `end`,
and `bases`. `prioritize_rsids` returns `(rsid, info)` or `(None, None)`.
`genome_version2url_dict` returns the supported alias-to-base-URL mapping.

## Raised exceptions

Unsupported genome versions and missing chromosome mappings raise an exception.
HTTP failures propagate through `requests` `raise_for_status`.

## Constraints

Ensembl coordinates on the wire are 1-based closed. `pos` is converted from
zero-based to one-based and `chr` is stripped from location queries. Returned
simple info converts to UCSC `chr` plus BED 0-based half-open coordinates.
`prioritize_rsids` considers only length-one variants with at least two
single-base alleles and selects the greatest allele count (ties retain input
order).

## Ordering

Location results retain Ensembl response order. Prioritization retains input
order for equal allele counts.

## Side effects

Each operation issues an HTTP GET with an `application/json` content header.
There is no cache or offline database.

## Lifecycle behavior

Stateless beyond stored server URL and species string. Each call performs its
own HTTP request.

## Supported protocols and inheritance

Standard Python object. No supported inheritance hierarchy.

## Example

```python
from RGTools.SNP_utils import EnsemblRestSearch

client = EnsemblRestSearch(genome_version="hg38")
# Live network required at runtime:
# rsids = client.get_rsid_from_location("chr1", 100000)
```

## Related formats or commands

- [Ensembl SNP simple-info format](../../formats/snp/ensembl-simple-info.md)
