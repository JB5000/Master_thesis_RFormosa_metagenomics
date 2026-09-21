# Ria Formosa scientific data and figure-reproduction bundle

Created and audited: 2026-09-02.

This is a scientific analysis bundle, not a thesis copy. It contains final
figures, their source data, result tables, figure-generation scripts, upstream
workflows and technical provenance. Interpretation, thesis prose, captions,
bibliography-management material and supervisor comments are deliberately
excluded.

## Start here

- `ASSET_MANIFEST.tsv` maps each final figure and result table to its source
  data, generation script and upstream analysis.
- `figures/` contains 24 retained high-resolution PNG figure assets.
- `results_tables/data/` contains nine descriptive result tables without
  thesis table numbering.
- `03_REPRODUCIBILITY/` contains portable plotting and audit scripts plus
  source matrices and plotted-value tables.
- `04_CORE_ANALYSIS_DATA/` and `05_RECENT_FINAL_ANALYSES/` retain sampling,
  QC, taxonomy, assembly/binning, MAG29, CoA4, recruitment, functional,
  rarefaction, porTraits/sumTraits, Proksee and Bandage evidence.
- `06_METHODS_AND_VALIDATION/` retains BLASTn outputs, workflow parameters,
  versions, commands and reproducibility reports.

## Canonical analysis constants

- 23 sampling dates; three equal-depth subsets per date; 315,147 reads per
  subset; 69 equal-depth FASTQ datasets.
- Final BLASTn target screen: 20 incorporated reference targets. *Perkinsus
  olseni* maximum: `S_22_06_29`, mean 720.2988 RPM, SD 23.9565.
- MAG29: 29 representatives. CoA4: four representatives.

## Reproduction notes

All active scripts use bundle-relative paths or documented environment
variables. Historical absolute commands, when scientifically useful, are kept
only as clearly labelled provenance. The original full-depth TaxProfiler QC run
for Figure S6 is retained in
`04_CORE_ANALYSIS_DATA/03_READS_AND_QC/taxprofiler_20260430/`; its raw FASTQs
are represented by a portable manifest rather than copied into this repository.
Proksee and Bandage figures retain their inputs and documented interactive
procedures. Run `03_REPRODUCIBILITY/scripts/audit_scientific_bundle.py` to
regenerate `BUNDLE_AUDIT.md`.

Install plotting dependencies with:

```bash
python3 -m pip install -r 03_REPRODUCIBILITY/requirements.txt
```

See `DATA_AVAILABILITY.md` for the boundary between the included
figure-reproduction data and the external raw sequencing data required for a
complete raw-read rerun.
