#!/usr/bin/env python3
"""Create the requested Figure 3.3 alternatives from the authoritative 23-sample inputs.

Outputs:
  * Fig_3.3A_phylum_stacked_barplot — former panel A as a standalone figure.
  * Fig_3.3B_top10_genus_barplot_and_heatmap — top-10 genus composition alongside
    the former genus z-score heatmap, using the same chronological sample order.

Top-10 genera are selected by mean relative abundance across all equal-depth samples
after removal of Homo and synthetic-construct labels.  Each stacked bar is then
renormalised within those ten selected genera, so it sums to 100%.
"""
from pathlib import Path
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from fig_style import ZSCORE_CMAP, save3


SOURCE = Path(__file__).resolve().parents[1] / "figure_sources"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)

PH_COL = {
    "Proteobacteria": "#1f77b4", "Actinobacteria": "#2ca02c",
    "Cyanobacteria": "#4bb5b0", "Bacteroidetes": "#ff7f0e",
    "Firmicutes": "#f4d03f", "Planctomycetes": "#9467bd",
    "Other taxa": "#bfbfbf",
}


ph = pd.read_csv(
    SOURCE / "read_level/krakenuniq_phylum_relative_classified_23samples_SOURCE.tsv",
    sep="\t",
)
ph = ph.loc[ph["taxon_rank"].eq("phylum")]
P = ph.pivot_table(
    index="sample_id", columns="taxon_name",
    values="mean_relative_abundance_classified_only", aggfunc="sum",
).fillna(0).sort_index() * 100.0
top_ph = [
    p for p in ["Proteobacteria", "Actinobacteria", "Cyanobacteria", "Bacteroidetes",
                "Firmicutes", "Planctomycetes"] if p in P.columns
]
comp_a = P[top_ph].copy()
comp_a["Other taxa"] = (100.0 - comp_a.sum(axis=1)).clip(lower=0)
assert np.allclose(comp_a.sum(axis=1), 100.0, atol=1e-6)

g = pd.read_csv(
    SOURCE / "pcoa/eqdepth_mean23_genus_relative_abundance_matrix.tsv",
    sep="\t", index_col=0,
).loc[comp_a.index]
g = g[[c for c in g if str(c).strip().lower() not in {"homo", "synthetic construct"}]]
top10 = g.mean(axis=0).nlargest(10).index.tolist()
top10_comp = g[top10].div(g[top10].sum(axis=1), axis=0).mul(100.0)
top31 = g.mean(axis=0).nlargest(31).index.tolist()
z = g[top31].T
z = z.sub(z.mean(axis=1), axis=0).div(z.std(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
vlim = float(np.nanmax(np.abs(z.values)))

# Former panel A, isolated.
fig, ax = plt.subplots(figsize=(8.8, 6.8))
x = np.arange(len(comp_a))
bottom = np.zeros(len(comp_a))
for taxon in top_ph + ["Other taxa"]:
    ax.bar(x, comp_a[taxon], bottom=bottom, width=0.82, color=PH_COL[taxon],
           edgecolor="white", linewidth=0.3, label=taxon)
    bottom += comp_a[taxon].to_numpy()
ax.set_title("Phylum-level stacked barplot", loc="left", fontsize=11, fontweight="bold")
ax.set_ylabel("Relative abundance among classified reads (%)")
ax.set_xlabel("Sample date (S_YY_MM_DD)")
ax.set_xticks(x); ax.set_xticklabels(comp_a.index, rotation=90, fontsize=7.7)
ax.set_ylim(0, 100); ax.margins(x=0.01)
ax.legend(ncol=2, fontsize=7.5, loc="lower left", frameon=True, facecolor="white",
          edgecolor="#cccccc", framealpha=0.96)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
fig.tight_layout()
save3(fig, OUT, "Fig_3.3A_phylum_stacked_barplot")

# Requested combination: former Panel B heatmap joined to the top-10 genus barplot.
fig, (ax_a, ax_b) = plt.subplots(
    1, 2, figsize=(14.4, 6.8), gridspec_kw={"width_ratios": [1.0, 1.22], "wspace": 0.28}
)
bottom = np.zeros(len(top10_comp))
for colour, genus in zip(plt.cm.tab10.colors, top10):
    ax_a.bar(x, top10_comp[genus], bottom=bottom, width=0.82, color=colour,
             edgecolor="white", linewidth=0.3, label=genus)
    bottom += top10_comp[genus].to_numpy()
ax_a.set_title("A  Top-10 genus stacked barplot", loc="left", fontsize=10.5, fontweight="bold")
ax_a.set_ylabel("Relative abundance within the top 10 genera (%)")
ax_a.set_xticks(x); ax_a.set_xticklabels(comp_a.index, rotation=90, fontsize=7.2)
ax_a.set_ylim(0, 100); ax_a.margins(x=0.01)
ax_a.legend(ncol=2, fontsize=7.0, loc="lower left", frameon=True, facecolor="white",
            edgecolor="#cccccc", framealpha=0.96)
for side in ("top", "right"):
    ax_a.spines[side].set_visible(False)

im = ax_b.imshow(z.values, aspect="auto", cmap=ZSCORE_CMAP, vmin=-vlim, vmax=vlim)
ax_b.set_title("B  Genus-level heatmap", loc="left", fontsize=10.5, fontweight="bold")
ax_b.set_xticks(range(len(comp_a))); ax_b.set_xticklabels(comp_a.index, rotation=90, fontsize=7.2)
ax_b.set_yticks(range(len(top31))); ax_b.set_yticklabels(top31, fontsize=6.5)
for label in ax_b.get_yticklabels():
    label.set_style("italic")
ax_b.set_xticks(np.arange(-.5, len(comp_a), 1), minor=True)
ax_b.set_yticks(np.arange(-.5, len(top31), 1), minor=True)
ax_b.grid(which="minor", color="white", linewidth=0.4); ax_b.tick_params(which="minor", length=0)
cb = fig.colorbar(im, ax=ax_b, fraction=0.03, pad=0.02)
cb.set_label("Row-wise z-score of mean relative abundance", fontsize=8)
cb.ax.tick_params(labelsize=7)
fig.text(0.5, 0.005, "Sample date (S_YY_MM_DD)", ha="center", fontsize=10)
fig.subplots_adjust(left=0.06, right=0.98, top=0.95, bottom=0.17)
save3(fig, OUT, "Fig_3.3B_top10_genus_barplot_and_heatmap")

comp_a.round(4).to_csv(OUT / "Fig_3.3A_phylum_stacked_barplot_VALUES.tsv", sep="\t")
top10_comp.round(4).to_csv(OUT / "Fig_3.3B_top10_genus_barplot_VALUES.tsv", sep="\t")
z.round(4).to_csv(OUT / "Fig_3.3B_genus_heatmap_zscore_VALUES.tsv", sep="\t")
print(f"Standalone phylum barplot + top-10 genus barplot/heatmap pair; top 10: {', '.join(top10)}")
