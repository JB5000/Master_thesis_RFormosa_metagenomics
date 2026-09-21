# Full-depth long-read QC and KrakenUniq profiling (2026-04-30)

This directory preserves the lightweight, primary outputs and configuration of
the nf-core/taxprofiler run that supplied the full-depth QC metrics used by
`figures/Fig_S6_archived_full_depth_read_QC.png`.

## Run identity

- Workflow: `nf-core/taxprofiler` v1.2.4 (Nextflow 25.04.4)
- Long-read QC: `nanoq` v0.10.0
- Taxonomic profiler: `krakenuniq` v1.0.4
- Input: 23 merged Oxford Nanopore FASTQ libraries, one per sampling date
- Database: `krakenuniq_standard`, built on 2022-06-16

## QC parameters

Long-read quality filtering used a minimum read length of 1,000 bp, a minimum
read quality of Q7 and a retained-base target of 90%. Adapter trimming was
explicitly skipped in this run. The exact workflow parameters and software
versions are stored under `pipeline_info/`.

## Contents

- `source_data/`: MultiQC/nanoq tables used to verify the plotted QC values.
- `nanoq_stats/`: the 23 per-library nanoq statistics files.
- `krakenuniq_reports/`: the 23 full-depth KrakenUniq reports.
- `pipeline_info/`: exact parameters, software versions and Nextflow trace.
- `config/`: retained workflow configuration.
- `raw_fastq_manifest.tsv`: portable inventory of the 23 input FASTQs.

The large FASTQ files are intentionally not duplicated in this GitHub-ready
bundle. To rerun from raw reads, set `RIA_RAW_FASTQ_ROOT` to the directory that
contains the filenames in `raw_fastq_manifest.tsv`, then generate a local
TaxProfiler samplesheet. The source QC matrix required to regenerate Figure S6
is already included in this bundle.
