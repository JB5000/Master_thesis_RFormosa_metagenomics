# Data availability

This repository contains the retained figure assets (23 final figures and one
candidate), figure-level source data, result tables, scripts, configuration and
workflow records needed to regenerate and verify the analyses represented in
the bundle.

The original 23 merged Oxford Nanopore FASTQ libraries are not included because
they are large primary-sequencing files. Their portable filename inventory is
retained at
`03_CORE_ANALYSIS_DATA/02_READS_AND_QC/taxprofiler_20260430/raw_fastq_manifest.tsv`.
The raw reads must be deposited in, or made available through, an appropriate
long-term sequencing repository before claiming that a public user can rerun
the complete workflow from raw reads.

The retained figures can be regenerated or verified without those large files,
because their plotted tables and retained QC outputs are included. Reanalysis
from raw FASTQs additionally requires:

- an accessible copy of the 23 FASTQs listed in the manifest;
- nf-core/taxprofiler 1.2.4 and its documented software environment;
- the `krakenuniq_standard` database build dated 2022-06-16, or a documented
  replacement database if an exact historical rerun is not required.
