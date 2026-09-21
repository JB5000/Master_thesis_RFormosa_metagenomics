# Genus rarefaction relative to each sample's full-depth profile

## Definition

For each of the 23 samples, the observed genus richness in its original
full-depth read-level KrakenUniq profile is defined as 100%. Each rarefied
subsample is expressed as:

`100 × observed genera in subsample / observed genera in the corresponding full-depth profile`

The analysis contains eight depths (1,000; 5,000; 10,000; 25,000; 50,000;
100,000; 250,000; and 315,147 reads) and three independent subsamples per
sample and depth.

Genus was used because the sample-specific full-depth genus
richness table is retained. The equivalent full-depth species denominator
was not retained, so a species-percentage version was not generated.

## Contents

- `figures/`: per-sample and overall figures in PNG, PDF, and SVG.
- `tables/`: all repeat-level values, sample/depth summaries, overall
  summaries, and the 23-sample full-depth baseline.
- `scripts/`: executable analysis and figure-generation script.
- `provenance/`: source record and machine-readable provenance record.

The 552 raw KrakenUniq report files and the upstream scheduler/subsampling
scripts are retained at the CETA location recorded below and were not copied
into this bundle. The bundle retains every extracted repeat-level value,
seed where recorded, source class, report locator and report SHA-256.

## Heatmap at 315,147 reads

`heatmap_315147_vs_full_depth_genus` compares the mean genus richness from
the three 315,147-read reports with the archived full-depth genus richness
for each sample. Samples are shown chronologically and cell labels give the
percentage to one decimal place. The displayed values are preserved in
`tables/heatmap_315147_vs_full_depth_genus_values.tsv`.

This heatmap deliberately uses the archived full-depth baseline requested
for this comparison. The archived baseline reports and the new subsamples
represent different read-processing stages; this is recorded here so that
the provenance remains explicit.

## Recorded checks

- 23 samples.
- 8 depths.
- 3 replicates per sample and depth.
- 552 repeat-level observations.
- 184 sample-by-depth summaries.
- Zero discrepancies between the newly parsed 315,147-read endpoint and the
  previously archived endpoint means.
- TSV and PNG outputs reproduced with identical SHA-256 hashes on rerun.

Three endpoint observations for `S_21_12_20` reach 100.0546%. Its archived
full-depth denominator came from a report containing 296,287 processed reads,
whereas the rarefaction endpoint contains 315,147 reads. The values are
retained without clipping.

## Canonical CETA location

`${CETA_RESULTS}/00_heavy_base_outputs/02_krakenuniq_subsamples/19_alpha_rarefaction_krakenuniq_all23_real`

`CETA_RESULTS` is a site-specific base directory. These source locators are
retained for provenance and are not portable rerun configuration.
