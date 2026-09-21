# GUNC QC summary (56 high-quality candidates)

GUNC was used as a complementary chimerism and clade-separation QC layer, not
as an additional exclusion filter. `GUNC_56_FINAL_COMPLETE.tsv` contains 56
candidate records; all 56 passed the retained GUNC check and selection remained
driven by the CheckM2 thresholds (at least 90% completeness and at most 5%
contamination).

The run used GUNC 1.0.6 with the `progenomes_2.1` database in nf-core/mag
v5.4.1. The per-candidate and run-level records are retained in this directory,
including the evidence records for the 14 candidates whose first source scan
did not traverse a symlinked HPC path. Those records show no change to the
selection set.

The complete evidence is in:

- `GUNC_56_FINAL_COMPLETE.tsv`;
- `GUNC_EFFECT_ON_SELECTION.tsv`;
- `GUNC_PRIMARY_RESULTS.tsv`;
- `GUNC_RUNS.tsv`;
- `GUNC_MG240416_evidence/`.
