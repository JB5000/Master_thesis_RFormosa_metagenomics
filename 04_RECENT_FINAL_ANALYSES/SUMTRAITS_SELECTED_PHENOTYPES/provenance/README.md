# sumTraits equal-depth 23-sample figure

## Scope

This working asset summarises the successful sumTraits run for 69 KrakenUniq
profiles: 23 samples, three independent replicates per sample and 315,147 reads
per replicate.

The figure follows the environmental and metabolic themes used in the
porTraits/GenomeSPOT panels. It does not treat taxonomically inferred
sumTraits phenotypes as marker-gene observations. The exact sumTraits trait and
feature behind every displayed row are recorded in the long-form values table.

## Calculation

- Environmental optima: arithmetic mean and sample standard deviation of the
  three replicate `numeric_mean` results.
- Categorical phenotypes: the `consensus_true` fraction, or the aerobic
  `consensus_majority` fraction for oxygen preference, expressed as a
  percentage of the complete taxonomic profile; mean and sample standard
  deviation across three replicates.
- `unclassified` and `unannotated` fractions are not removed from the
  categorical denominator. This avoids inflating traits with sparse reference
  coverage.
- Trait-specific resolved annotation coverage is retained beside every value in
  `values/sumtraits_23samples_replicate_mean_sd_and_coverage.tsv`.
- Heatmap colour is scaled independently within each row. Printed cell values
  are the unstandardised replicate means.

## Source

Successful CloWM archive:

`source/sumtraits_run_c3665d18-453d-484f-9afc-c0073c0e7cb0.tar.gz`

The 69 KrakenUniq reports supplied to the workflow are retained in:

`source/krakenuniq_reports_69/`

The corrected combined input and the complete sumTraits outputs are retained
directly in `source/`.

SHA-256:

`158f0066329bcc94f4303ad4815f4405476539c483f37c32bbfd0e9abfb59fae`

This asset does not modify source archives or retained inputs.

## Selected sediment-biogeochemistry figure

`figures/sumTraits_sediment_biogeochemistry_selected_traits.*` is a focused
single-panel view of five traits, using their catalogue names:

- `reduction: sulfate`;
- `oxidation in darkness: sulfide`;
- `denitrification pathway`;
- `nitrogen fixation`;
- `growth: photoautotrophy`.

Dark sulfide oxidation (`oxidation in darkness: sulfide`) was selected instead
of thiosulfate oxidation because the mean robustly interpretable annotation
coverage was approximately 24.1%, compared with approximately 0.037% for
thiosulfate oxidation. This choice is based only on annotation coverage and is
recorded in the executable script.

The main heatmap shows the abundance-weighted conditional positive fraction
among robust assignments:
`100 × consensus_true / (consensus_true + consensus_false)`. Colour represents
the z-score calculated independently along each trait row across the 23
sampling dates. Untransformed percentages are retained in the plotted-value
table rather than printed inside the heatmap cells.

Robustly interpretable coverage,
`100 × (consensus_true + consensus_false)`, is retained in the plotted-value,
coverage-component and diagnostic tables but is not displayed as a separate
panel because the four traits with usable coverage have nearly identical
temporal coverage patterns. The sulfate-reduction coverage is separately
visible in the complete supplementary heatmap. Robust coverage excludes the
`no_majority`, `unannotated` and `unclassified` fractions.

The complete five-row coverage heatmap is retained as:

- `figures/sumTraits_trait_specific_annotation_coverage_supplementary.*`.

The publication-ready export is approximately 180 mm wide at 300 dpi. Numerical
cell annotations are omitted to keep the 23 sampling dates visually separate;
the exact percentages and full explanatory caption are retained outside the
image.

The complete plotted values and coverage components are retained in:

- `values/sumtraits_sediment_biogeochemistry_PLOTTED_VALUES.tsv`;
- `values/sumtraits_sediment_biogeochemistry_COVERAGE_COMPONENTS.tsv`;
- `values/sumtraits_sediment_biogeochemistry_TRAIT_DIAGNOSTIC.tsv`.

The `reduction: sulfate` result has exceptionally sparse reference coverage
(mean robust coverage approximately 0.0129% of the complete taxonomic
profile), and its conditional fraction is therefore not interpretable. It is
displayed for completeness, but its row must be treated as diagnostic rather
than as a community-wide estimate. After conditioning, the apparent
generalized chronological decline does not remain. `growth: photoautotrophy`
retains an exploratory positive chronological association, but the traits
with usable coverage do not show a coherent community-wide temporal shift.
These remain database-dependent phenotype inferences and do not establish
biological function, activity or biogeochemical process rates.
