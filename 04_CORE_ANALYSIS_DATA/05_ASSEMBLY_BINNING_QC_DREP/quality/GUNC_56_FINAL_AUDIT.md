# §5 — GUNC audit (56 HQ candidates)

**Audit mode.** Date 2026-07-13. **Updated 2026-07-14 after institutional HPC source verification (see `verification_report/10_institutional HPC_SOURCE_VERIFICATION_20260714.tsv`).**

## Key finding — GUNC was a complementary QC layer, NOT an exclusion filter
`GUNC_56_FINAL_COMPLETE.tsv` (56 rows): **56 PASS · 0 excluded by GUNC** (was 42 PASS + 14 NO_RECOVERED_OUTPUT before the 2026-07-14 recovery).
- All 56 carry `selection_effect = "none; retained by CheckM2 criteria"`.
- The formerly-missing 14 were **recovered from institutional HPC** on 2026-07-14: `MG240416/results/run_20260601_144953/GenomeBinning/QC/gunc_summary.tsv` (523 rows; the file sat under a symlinked path the first audit did not traverse). **All 14 target bins have pass.GUNC = True** (evidence copied to `GUNC_MG240416_recovered_evidence/`).
- Therefore **no bin among the 56 was removed by GUNC**; the HQ selection was driven entirely by **CheckM2**
  (≥90 % completeness, ≤5 % contamination). GUNC provides chimerism/clade-separation context only.

## Version / database
- **Database:** `progenomes_2.1` (raw filename `GUNC.progenomes_2.1.maxCSS_level.tsv`; work-dir DB `gunc_db_progenomes2.1.dmnd`).
- **GUNC version:** **1.0.6** — RESOLVED 2026-07-14: nf-core/mag install is **v5.4.1** (git 0c370baf) and its GUNC module pins `bioconda::gunc=1.0.6` (container `gunc:1.0.6--pyhdfd78af_0`). This is a deterministic pipeline pin, consistent with every per-sample GUNC output.
- Scope: single-sample nf-core/mag QC; **1213 GUNC result records** registered — coverage is **incomplete** relative
  to the 1408 retained bins (`GUNC_RUNS.tsv`).

## The 14 — RECOVERED 2026-07-14
All 14 belong to **MG240416 / run_20260601_144953**:
`FLYE-…240416.{29,290,034,100,203,419,579,71,722,82,820,833}` + `METAMDBG-MetaBinnerRefined-…240416.{5,6}`.
- **Recovered:** the run's `GenomeBinning/QC/gunc_summary.tsv` (523 rows) exists at
  `${PROJECT_HOME}/final_results/00_heavy_base_outputs/30_nfccoremag_all_samples/MG240416/results/run_20260601_144953/`
  (a symlinked path the first audit did not traverse). Copied to `GUNC_MG240416_recovered_evidence/`.
- **All 14 target bins: pass.GUNC = True.** (Full sample: 463 True / 59 False across 522 bins.)
- **Impact: none on selection** — GUNC was not a filter; CheckM2 remained the sole driver. The recovery simply
  completes the record to **56/56 with a GUNC result, all PASS**.

## Wording to use in the thesis
- "MAG selection used CheckM2 completeness/contamination thresholds; GUNC (v1.0.6, database progenomes_2.1, run within
  nf-core/mag v5.4.1) was applied as a **complementary chimerism/contamination QC** and did not act as an additional
  exclusion filter. All 56 high-quality candidates that entered dereplication passed the GUNC clade-separation check."
- You may now state GUNC **v1.0.6** and that all 56 candidates passed GUNC.

## Files
- `GUNC_56_FINAL_COMPLETE.tsv` (this folder) — per-candidate PASS / NO_RECOVERED_OUTPUT, `GUNC_acted_as_filter=No`,
  `selection_driver=CheckM2`.
- Existing: `GUNC_EFFECT_ON_SELECTION.tsv`, `GUNC_PRIMARY_RESULTS.tsv` (1213), `GUNC_RUNS.tsv`.

## Status: **PASS** — role (QC, not filter) resolved; **all 14 outputs recovered (56/56 PASS)**; **version resolved = GUNC 1.0.6** (nf-core/mag v5.4.1). See `verification_report/10_institutional HPC_SOURCE_VERIFICATION_20260714.tsv`.
