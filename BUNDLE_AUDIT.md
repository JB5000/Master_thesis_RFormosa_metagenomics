# Bundle integrity and reproducibility audit

**Overall status: PASS**

This audit checks scientific assets and reproducibility only; it does not assess thesis wording or interpretation.

| Check | Status | Details |
|---|---:|---|
| MANIFEST-01 | PASS | manifest records=33; required columns present=True |
| FIGURES-01 | PASS | figure PNGs=24; manifest figure records=24 |
| PROVENANCE-01 | PASS | missing figure source data=[]; missing generation scripts=[] |
| SCRIPTS-01 | PASS | retained scripts with non-portable input assumptions=[] |
| SCRIPTS-02 | PASS | sumTraits figure and values directories are created before output is written |
| TABLES-01 | PASS | result tables=9; manifest table records=9 |
| SCIENCE-01 | PASS | Perkinsus peak=S_22_06_29; mean=720.2988; SD=23.9565 |
| SCIENCE-02 | PASS | BLASTn=20 targets × 23 dates; references=20; MAG29=29; CoA4=4 |
| SCIENCE-03 | PASS | QC dates=23; equal-depth subsets=69; reads/subset=['315147']; dates=23 |
| QC-PROVENANCE-01 | PASS | TaxProfiler inputs: MultiQC rows=23; FASTQ manifest rows=23; nanoq stats=23; KrakenUniq reports=23 |
| QC-PROVENANCE-02 | PASS | Figure S6 post-QC values match original nanoq/MultiQC table; mismatches=[] |
| SCRIPTS-03 | PASS | Figure S6 script resolves bundle-relative inputs and creates its output directory |
| VALUES-01 | PASS | BLASTn source target set matches exported plotted-value matrix |
| VALUES-02 | PASS | BLASTn exported RPM matrix matches rounded source values; mismatches=[] |
| CLEAN-01 | PASS | active Kraken2 target-screen files=[] |
| PORTABLE-01 | PASS | private absolute paths in active scripts/configuration=[] |
| CLEAN-02 | PASS | cache/temp artifacts=[] |
| GITHUB-01 | PASS | GitHub documentation present=True; bundled raw FASTQs=[] |
| DOC-01 | PASS | README scope and counts match manifest |

## Scope notes

- Figure S6 has recovered TaxProfiler/nanoq provenance: input inventory, QC matrices, nanoq statistics, KrakenUniq reports, parameters, versions and execution trace are retained.
- Proksee and Bandage assets retain their inputs and documented interactive procedures.
- Large original FASTQs are not duplicated; their portable filename manifest is in `04_CORE_ANALYSIS_DATA/03_READS_AND_QC/taxprofiler_20260430/raw_fastq_manifest.tsv`.
