# sumTraits phenotype asset

| Item | Path or value |
|---|---|
| Final figure | `01_FIGURES/final/Fig_S9_selected_taxonomically_inferred_phenotypes.png` |
| Generation script | `scripts/make_sumtraits_sediment_biogeochemistry_figure.py` |
| Samples | 23 |
| Equal-depth replicates | 3 per sample; 315,147 reads per replicate |
| Input annotations | `source/community_trait_annotations.tsv` |
| Plotted values | `values/` |
| Retained source table | `source/community_trait_annotations.tsv` |

The script calculates replicate means and standard deviations from the retained
sumTraits table and writes the row-standardised figure. Machine-readable values
are retained for reproduction.
