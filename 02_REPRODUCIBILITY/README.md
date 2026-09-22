# Reproducibility scripts and source data

This directory contains portable figure-generation scripts, shared plotting
style, source matrices, plotted-value tables, software/database versions and
recorded method commands. Scripts resolve inputs from the bundle and write
regenerated files to `regenerated_output/` by default, or to the directory set
through `RIA_FIGURE_OUTPUT`.

Each retained figure lists its source data and generation script in
`../ASSET_MANIFEST.tsv`.

The original full-depth TaxProfiler QC provenance is retained under
`../03_CORE_ANALYSIS_DATA/02_READS_AND_QC/taxprofiler_20260430/`. Raw FASTQ
data are intentionally external to the repository and are described by a
portable filename manifest.
