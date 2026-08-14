# `EnsemblRestSearch`

## Purpose

Query Ensembl variation records and choose SNP-like variants at genomic
locations.

The returned dictionary follows the [Ensembl SNP simple-info profile](../../formats/snp/ensembl-simple-info.md).

## Availability

Supported in release `0.1.0a2` as `RGTools.SNP_utils.EnsemblRestSearch`; it is
also available from the `RGTools.SNP_utils` module. This API depends on the
Ensembl REST service.

## Inputs

`EnsemblRestSearch(genome_version="hg38", species="human")` configures the
service. `get_rsid_from_location(chrom, pos)` takes a chromosome and a
zero-based position. `get_rsid_snp_simple_info(rsid)` and
`prioritize_rsids(rsids)` take rsID strings or an iterable of them.

## Types

Genome version, species, chromosome, and rsID are strings; `pos` is an int.
Simple-info results are dictionaries with string `chrom`/`bases` and integer
`start`/`end`. `prioritize_rsids` returns `(rsid, info)` or `(None, None)`.

## Shapes

Location lookup returns a list of rsID strings. A simple-info dictionary has
exactly the fields `chrom`, `start`, `end`, and `bases`.

## Dtypes

Inapplicable: values are Python strings, integers, lists, and dictionaries.

## Defaults

`genome_version="hg38"` and `species="human"`. `hg38`/`GRCh38` use
`https://rest.ensembl.org`; `hg19`/`GRCh37` use
`https://grch37.rest.ensembl.org`.

## Choices

Supported genome aliases are `hg38`, `GRCh38`, `hg19`, and `GRCh37`.

## Constraints

Ensembl coordinates on the wire are 1-based closed. `pos` is converted from
zero-based to one-based and `chr` is stripped from location queries. Returned
simple info converts to UCSC `chr` plus BED 0-based half-open coordinates.
`prioritize_rsids` considers only length-one variants with at least two
single-base alleles and selects the greatest allele count (ties retain input
order).

## Outputs

`get_rsid_from_location` returns only variants whose Ensembl `start` and `end`
equal the queried one-based position. `get_rsid_snp_simple_info` returns
`{"chrom": "chr...", "start": int, "end": int, "bases": "A/G"}`.
`prioritize_rsids` returns the selected rsID and its simple-info dictionary.

## Ordering

Location results retain Ensembl response order. Prioritization retains input
order for equal allele counts.

## Side effects

Each operation issues an HTTP GET with an `application/json` content header;
there is no cache or offline database. `EnsemblRestSearch.genome_version2url_dict`
is a read-only property returning the supported alias-to-base-URL mapping.

## Failures

Unsupported genome versions and missing chromosome mappings raise an exception.
HTTP failures propagate through `requests` `raise_for_status`. Network access
is therefore required; documentation and deterministic tests do not make live
requests.

## EnsemblRestSearch constructor

`EnsemblRestSearch(genome_version="hg38", species="human")` stores the
selected REST server and species.

## `EnsemblRestSearch.genome_version2url_dict`

Property returning the four supported genome-version aliases and their REST
base URLs.

## `EnsemblRestSearch.get_rsid_from_location`

Queries `/overlap/region/{species}/{chrom}:{pos+1}-{pos+1}?feature=variation`
and filters the response to exact single-base spans.

## `EnsemblRestSearch.get_rsid_snp_simple_info`

Fetches a variation record, selects its chromosome mapping, and converts its
coordinates into the library's simple-info BED schema.

## `EnsemblRestSearch.prioritize_rsids`

Fetches each candidate, excludes non-SNP-like variants, and returns the
remaining candidate with the most alternate alleles.
