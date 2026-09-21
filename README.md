# Ria Formosa scientific data and figure-reproduction bundle

This repository is a scientific data and reproducibility package. It contains
the final figure assets, the data used to make them, relevant result tables,
analysis inputs and portable scripts.

## Repository map

- `01_FIGURES/final/` — the 24 final PNG figure assets.
- `01_FIGURES/gallery/` — a local HTML viewer for those same assets. It is
  only an index; it is not a second figure collection.
- `02_REPRODUCIBILITY/` — figure source matrices, plotted-value tables,
  generation scripts, software/database versions and recovered commands.
- `03_CORE_ANALYSIS_DATA/` — sampling, read QC, taxonomy, assembly/binning,
  MAG29, recruitment, functional and CoA4 data.
- `04_RECENT_FINAL_ANALYSES/` — the recent rarefaction, sumTraits, Proksee
  and Flye/Bandage analyses with their inputs and provenance.
- `05_METHODS_AND_VALIDATION/` — BLASTn target-screen outputs and relevant
  workflow/provenance records.
- `06_RESULT_TABLES/` — descriptive result tables and exact plotted-value
  matrices.
- `ASSET_MANIFEST.tsv` — one row per final figure or result table, linking it
  to source data and (where applicable) its generation script.

## Canonical analysis constants

- 23 sampling dates; three equal-depth subsets per date; 315,147 reads per
  subset; 69 equal-depth FASTQ datasets.
- Final BLASTn target screen: 20 incorporated reference targets. *Perkinsus
  olseni* maximum: `S_22_06_29`, mean 720.2988 RPM, SD 23.9565.
- MAG29: 29 representatives. CoA4: four representatives.

## Reproduction notes

Active figure scripts resolve inputs from the bundle or from documented
environment variables and create their own output directories. Install the
plotting dependencies with:

```bash
python3 -m pip install -r 02_REPRODUCIBILITY/requirements.txt
```

The original full-depth TaxProfiler QC provenance for Figure S6 is retained
under `03_CORE_ANALYSIS_DATA/02_READS_AND_QC/taxprofiler_20260430/`; the raw
FASTQs themselves are represented by a portable filename manifest rather than
copied into this repository. Proksee and Bandage figures retain their inputs
and documented interactive procedures. See `DATA_AVAILABILITY.md` for the
boundary between the included reproduction data and external raw sequencing
data required for a complete raw-read rerun.
