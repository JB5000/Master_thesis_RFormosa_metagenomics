# Reproducibility scripts and configuration

This directory contains portable figure-generation scripts, shared plotting
style, source matrices and the bundle audit. Scripts resolve all inputs from
their own location and write regenerated files to `regenerated_output/` by
default, or to the directory set through `RIA_FIGURE_OUTPUT`.

The original full-depth TaxProfiler QC provenance is retained under
`../04_CORE_ANALYSIS_DATA/03_READS_AND_QC/taxprofiler_20260430/`. Raw FASTQ
data are intentionally external to the repository and are described by a
portable filename manifest.
