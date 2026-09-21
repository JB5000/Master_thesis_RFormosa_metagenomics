# Quality-layer file record

CheckM2 ran inside the nf-core/mag v5.4.1 workflows (`--run_checkm2`), with legacy CheckM disabled (`--run_checkm false`). The retained process record reports **CheckM2 v1.1.0**, a supplied `uniref100.KO.1.dmnd` database, and successful completion. The database path is recorded; its release/hash is not recorded.

The 23 final per-sample `bin_summary.tsv` outputs contain 1,450 entries. Forty-two entries are explicitly named `DASToolUnbinned` and are excluded from the retained binned set. Applying the operational categories to the 1,408 retained rows reproduces 56 high-completeness/low-contamination candidates (completeness ≥90%; contamination ≤5%), 561 medium-quality entries (not HQ; completeness ≥50%; contamination ≤10%), and 791 remaining lower-quality entries.

The 56 CheckM2-selected bins are the input set documented in the final single-sample dRep run. dRep then performed its own internal CheckM filtering because the command used `-comp 90 -con 5` without a pre-supplied dRep genomeInfo table: 38/56 passed that internal dRep CheckM step and 29 representatives were chosen. This internal dRep CheckM result does not replace the preceding CheckM2 classification.

GUNC was enabled in nf-core/mag and primary GUNC summaries exist. The 56-input manifest is defined by CheckM2 completeness/contamination. Among these 56 inputs, 42 have `pass.GUNC=True`; 14 have no GUNC result in the retained records. No GUNC exclusion field is present in the retained 56-input manifest. GUNC version and complete final coverage are not recorded for every input.
