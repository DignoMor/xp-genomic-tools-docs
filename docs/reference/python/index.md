# Python API grouped index

Supported `RGTools` release `0.3.0a4`. Browse by API area; each entry shows the exact qualified name and links to the canonical page.

## Foundation

Shared exceptions, logging, utilities, and list-file helpers.

### `RGTools.exceptions`

- Canonical page: [`RGTools exceptions`](foundation/exceptions/)
- Status: Supported
- Members: `RGToolsInternalException`, `GTFHandleFilterException`, `GTFRecordNoFeatureException`, `BedTableException`, `BedTableLoadException`, `InvalidBedRegionException`, `InvalidStrandnessException`
- Search terms: `RGTools.exceptions`

### `RGTools.ListFile.ListFile`

- Canonical page: [`ListFile`](foundation/list-file/)
- Aliases: `ListFile`
- Status: Supported
- Members: `ListFile`, `read_file`, `write_list_to_file`, `get_contents`, `get_num_lines`
- Search terms: `RGTools.ListFile.ListFile`, `ListFile`

### `RGTools.logging.Logger`

- Canonical page: [`Logger`](foundation/logger/)
- Aliases: `Logger`
- Status: Supported
- Members: `Logger`, `indent`, `unindent`, `take_log`
- Search terms: `RGTools.logging.Logger`, `Logger`

### `RGTools.utils`

- Canonical page: [`Foundation utilities`](foundation/utils/)
- Aliases: `str2bool`, `str2none`, `reverse_complement`, `NumpyEncoder`
- Status: Supported
- Members: `str2bool`, `str2none`, `reverse_complement`, `NumpyEncoder`
- Search terms: `RGTools.utils`, `str2bool`, `str2none`, `reverse_complement`, `NumpyEncoder`

## BedTable

Region records, iterators, and BED3/BED6 table implementations.

### `RGTools.BedTable.BedRegion`

- Canonical page: [`BedRegion`](bedtable/bed-region/)
- Aliases: `BedRegion`
- Status: Supported
- Members: `BedRegion`, `to_dict`, `get_fields`, `pad_region`, `__getitem__`, `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ne__`
- Search terms: `RGTools.BedTable.BedRegion`, `BedRegion`

### `RGTools.BedTable.BedTable3`

- Canonical page: [`BedTable3`](bedtable/bed-table3/)
- Aliases: `BedTable3`
- Status: Supported
- Members: `BedTable3`, `column_names`, `column_types`, `extra_column_names`, `extra_column_dtype`, `load_from_file`, `load_from_dataframe`, `load_from_bed_regions`, `apply_logical_filter`, `region_subset`, `to_dataframe`, `write`, `get_chrom_names`, `get_start_locs`, `get_end_locs`, `get_region_by_index`, `iter_regions`, `search_region`, `concat`, `subset_by_index`, `copy`, `__len__`
- Search terms: `RGTools.BedTable.BedTable3`, `BedTable3`

### `RGTools.BedTable.BedTable3Plus`

- Canonical page: [`BedTable Plus`](bedtable/bed-table-plus/)
- Aliases: `BedTable3Plus`, `BedTable6Plus`
- Status: Supported
- Members: `BedTable3Plus`, `BedTable6Plus`, `column_names`, `column_types`, `extra_column_names`, `extra_column_dtype`, `get_region_extra_column`
- Search terms: `RGTools.BedTable.BedTable3Plus`, `BedTable3Plus`, `BedTable6Plus`

### `RGTools.BedTable.BedTable6`

- Canonical page: [`BedTable6`](bedtable/bed-table6/)
- Aliases: `BedTable6`
- Status: Supported
- Members: `BedTable6`, `column_names`, `column_types`, `get_region_names`, `get_region_scores`, `get_region_strands`, `region_subset`, `load_from_BedTable3`
- Search terms: `RGTools.BedTable.BedTable6`, `BedTable6`

### `RGTools.BedTable.BedTableIterator`

- Canonical page: [`BedTableIterator`](bedtable/iterator/)
- Aliases: `BedTableIterator`
- Status: Supported
- Members: `BedTableIterator`, `__iter__`, `__next__`
- Search terms: `RGTools.BedTable.BedTableIterator`, `BedTableIterator`

### `RGTools.BedTable.BedTablePairEnd` (experimental)

- Canonical page: [`BedTablePairEnd`](bedtable/bed-table-pair-end/)
- Aliases: `BedTablePairEnd`
- Status: Experimental
- Members: `BedTablePairEnd`, `column_names`, `column_types`, `extra_column_names`, `extra_column_dtype`, `get_other_region_chroms`, `get_other_region_starts`, `get_other_region_ends`, `get_pair_names`, `get_pair_scores`, `get_region_strands`, `get_other_region_strands`, `get_region_extra_column`, `search_pair_extra_column`, `search_second_region`
- Search terms: `RGTools.BedTable.BedTablePairEnd`, `BedTablePairEnd`

## Element collections

Abstract and concrete genomic and exogenous sequence collections.

### `RGTools.ExogenousSequences.ExogenousSequences`

- Canonical page: [`ExogenousSequences`](elements/exogenous-sequences/)
- Aliases: `ExogenousSequences`
- Status: Supported
- Members: `ExogenousSequences`, `__init__`, `fasta_path`, `region_file_type`, `region_file_path`, `get_sequence_ids`, `get_region_bed_table`, `get_all_region_seqs`, `get_all_region_lens`, `apply_logical_filter`, `write_sequences_to_fasta`
- Search terms: `RGTools.ExogenousSequences.ExogenousSequences`, `ExogenousSequences`

### `RGTools.GeneralElements.GeneralElements`

- Canonical page: [`GeneralElements`](general-elements/general-elements/)
- Aliases: `GeneralElements`
- Status: Supported
- Members: `GeneralElements`, `__init__`, `fasta_path`, `region_file_type`, `region_file_path`, `get_region_bed_table`, `get_all_region_seqs`, `close`, `get_region_seq`, `get_region_lens`, `get_all_region_one_hot`, `apply_logical_filter`, `get_num_regions`, `load_region_anno_from_npy`, `load_region_track_from_list`, `load_region_stat_from_arr`, `load_mask_from_arr`, `load_region_array_from_arr`, `get_anno_dim`, `get_anno_type`, `get_track_list`, `get_stat_arr`, `get_mask_arr`, `get_arr_anno`, `get_region_track_by_index`, `get_region_stat_by_index`, `get_region_mask_by_index`, `get_region_array_by_index`, `save_anno_npy`, `save_anno_npz`, `one_hot_encoding`
- Search terms: `RGTools.GeneralElements.GeneralElements`, `GeneralElements`

### `RGTools.GenomicElements.GenomicElements`

- Canonical page: [`GenomicElements`](elements/genomic-elements/)
- Aliases: `GenomicElements`
- Status: Supported
- Members: `GenomicElements`, `__init__`, `fasta_path`, `region_file_type`, `region_file_path`, `get_num_regions`, `get_region_file_suffix2class_dict`, `BedTable6Gene`, `BedTable3Gene`, `BedTableNarrowPeak`, `BedTableTREBed`, `BedTableBedGraph`, `merge_genomic_elements`, `export_exogenous_sequences`, `get_all_region_seqs`, `get_region_bed_table`, `apply_logical_filter`
- Search terms: `RGTools.GenomicElements.GenomicElements`, `GenomicElements`

## Operations

Standalone supported operations with dedicated reference pages.

### `GeneralElements.load_mask_from_arr`

- Canonical page: [`GeneralElements.load_mask_from_arr`](general-elements/load-mask-from-arr/)
- Aliases: `load_mask_from_arr`
- Status: Supported
- Members: `load_mask_from_arr`
- Search terms: `GeneralElements.load_mask_from_arr`, `load_mask_from_arr`

### `RGTools.TSSRelativeCoordinates`

- Canonical page: [`TSS-relative coordinates`](general-elements/tss-relative-coordinates/)
- Aliases: `offset_tss_relative_coordinate`, `iter_relaxed_window`, `tss_relative_to_track_index`
- Status: Supported
- Members: `offset_tss_relative_coordinate`, `iter_relaxed_window`, `tss_relative_to_track_index`
- Search terms: `RGTools.TSSRelativeCoordinates`, `offset_tss_relative_coordinate`, `iter_relaxed_window`, `tss_relative_to_track_index`

## Motifs

MEME motif collections and synthetic sequence generation.

### `RGTools.MemeMotif.MemeMotif`

- Canonical page: [`MemeMotif`](motifs/meme-motif/)
- Aliases: `MemeMotif`
- Status: Supported
- Members: `MemeMotif`, `__init__`, `write_meme_file`, `clone_empty`, `get_meme_version`, `set_meme_version`, `get_alphabet`, `set_alphabet`, `get_strands`, `set_strands`, `get_bg_freq`, `set_bg_freq`, `get_motif_list`, `get_motif_pwm`, `get_motif_alphabet_length`, `get_motif_length`, `get_motif_num_source_sites`, `get_motif_source_eval`, `add_motif`, `calculate_pwm_score`, `search_one_motif`
- Search terms: `RGTools.MemeMotif.MemeMotif`, `MemeMotif`

### `RGTools.MotifGeneration`

- Canonical page: [`Motif generation`](motifs/motif-generation/)
- Aliases: `MotifGeneration`
- Status: Supported
- Members: `MotifExclusion`, `SequenceGenerationExhaustedError`, `parse_motif_exclusion`, `parse_motif_exclusions`, `validate_motif_exclusions`, `candidate_violates_exclusions`, `make_anti_motifs`, `iter_pwm_sequences`, `iter_random_sequences`, `iter_barcodes`
- Search terms: `RGTools.MotifGeneration`, `MotifGeneration`

## BigWig signal

BigWig signal quantification helpers.

### `RGTools.BwTrack.BaseBwTrack`

- Canonical page: [`BigWig signal tracks`](signal/bw-track/)
- Aliases: `BaseBwTrack`, `SingleBwTrack`, `PairedBwTrack`
- Status: Supported
- Members: `BaseBwTrack`, `quantify_signal`, `get_supported_quantification_type`, `count_single_region`, `SingleBwTrack`, `PairedBwTrack`
- Search terms: `RGTools.BwTrack.BaseBwTrack`, `BaseBwTrack`, `SingleBwTrack`, `PairedBwTrack`

## GENCODE GTF

Streaming GTF record and handle utilities.

### `RGTools.GTF_utils`

- Canonical page: [`GENCODE GTF streaming`](gtf/gtf-utils/)
- Aliases: `GTFRecord`, `GTFHandle`
- Status: Supported
- Members: `GTFRecord`, `search_general_info`, `search_add_info`, `GTFHandle`, `__init__`, `__iter__`, `__next__`, `filter_by_general_record`, `filter_by_add_record`, `get_comments`, `count_total`, `filter_check`
- Search terms: `RGTools.GTF_utils`, `GTFRecord`, `GTFHandle`

## Ensembl SNP

Ensembl REST rsID lookup helpers.

### `RGTools.SNP_utils.EnsemblRestSearch`

- Canonical page: [`EnsemblRestSearch`](snp/ensembl-rest-search/)
- Aliases: `EnsemblRestSearch`
- Status: Supported
- Members: `EnsemblRestSearch`, `__init__`, `genome_version2url_dict`, `get_rsid_from_location`, `get_rsid_snp_simple_info`, `prioritize_rsids`
- Search terms: `RGTools.SNP_utils.EnsemblRestSearch`, `EnsemblRestSearch`
