# BLASTn target-screen RPM matrix

This is the active raw-RPM table for Supplementary Figure S2. It contains the 20 reference targets in the selected-reference BLASTn database and 23 sampling dates. Each cell is the mean BLASTn-derived RPM across the three 315,147-read equal-depth subsamples for that date. The upstream hit aggregator omits target/date rows with no hits; these are explicitly represented here as `0` RPM, as in the figure-generation script.

The source is `02_BLAST_VALIDATION/blast_sample_mean.tsv`. The export script
checks that the matrix is complete (20 targets × 23 dates) before writing this
result table. `blastn_target_reference_mapping_20_targets.tsv` is the
companion list of the exact 20 included references and their accessions.
