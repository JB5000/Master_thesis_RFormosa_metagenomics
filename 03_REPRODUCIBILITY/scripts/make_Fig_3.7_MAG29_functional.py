#!/usr/bin/env python3
"""Fig 3.7 — MAG29 functional summary, two panels, one coherent template.
A "Annotation-derived protein counts": COG, KEGG, CAZy, VFDB.
B "FuncScan screening outputs": AMP, ARG, GECCO, antiSMASH (GECCO clusters & antiSMASH regions kept separate).
Rows SS-01..SS-29 (numerical); SS IDs on BOTH panels. Blue(low)->red(high) colour, normalised independently
from the displayed minimum to maximum of each column.
Raw counts in every cell. Phylum legend; no crowded footer."""
from pathlib import Path
import os
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.lines import Line2D
import sys; sys.path.insert(0, str(Path(__file__).parent))
from fig_style import COUNT_CMAP, phylum_color, PHYLUM_COLORS, save3


SOURCE = Path(__file__).resolve().parents[1] / "figure_sources"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)

vals = pd.read_csv(SOURCE/"functional/MAG29_functional_values_SOURCE.tsv", sep="\t").set_index("SS_ID")
fsc  = pd.read_csv(SOURCE/"functional/FUNCSCAN_PER_MAG_AUTHORITATIVE_AMP_ARG_BGC.tsv", sep="\t")
fsc  = fsc[fsc["branch"]=="MAG29"].set_index("authoritative_ID")
rows = sorted(vals.index, key=lambda s: int(s.split("-")[1]))   # SS-01..SS-29
vals, fsc = vals.loc[rows], fsc.loc[rows]
phy = vals["Phylum"]

PANELS = [("A  Annotation-derived protein counts", vals[["COG","KEGG","CAZymes","VFDB"]].astype(int).values, ["COG","KEGG","CAZy","VFDB"]),
          ("B  FuncScan screening outputs", fsc[["AMP_ampir_p0.5","ARG_hamronization","BGC_GECCO","BGC_antiSMASH"]].astype(int).values, ["AMP","ARG","GECCO","antiSMASH"])]

fig, axes = plt.subplots(1, 2, figsize=(11.6, 8.8), gridspec_kw={"width_ratios":[1,1], "wspace":0.30})
cmap = plt.get_cmap(COUNT_CMAP)
for ax, (title, A, labels) in zip(axes, PANELS):
    A = A.astype(float); assert A.shape == (29, 4), f"{title}: expected 29x4, got {A.shape}"
    rgba = np.zeros(A.shape+(4,))
    for c in range(A.shape[1]):
        lo, hi = A[:,c].min(), A[:,c].max()
        norm = Normalize(lo, hi if hi>lo else lo+1)
        rgba[:,c] = cmap(norm(A[:,c]))
    for i in range(A.shape[0]):
        for c in range(A.shape[1]):
            ax.add_patch(plt.Rectangle((c-.5,i-.5),1,1,facecolor=rgba[i,c],
                                       edgecolor="none"))
    for i in range(29):
        for c in range(4):
            lum=0.299*rgba[i,c,0]+0.587*rgba[i,c,1]+0.114*rgba[i,c,2]
            ax.text(c,i,f"{int(A[i,c])}",ha="center",va="center",fontsize=7.2,color="white" if lum<0.5 else "black")
    ax.set_xticks(range(4)); ax.set_xticklabels(labels, fontsize=9)
    ax.set_yticks(range(29)); ax.set_yticklabels(rows, fontsize=7.4)     # SS IDs on BOTH panels
    ax.set_xlim(-.5,3.5); ax.set_ylim(28.5,-.5)
    for tick,r in zip(ax.get_yticklabels(), rows): tick.set_color(phylum_color(phy.loc[r]))
    ax.set_xticks(np.arange(-.5,4,1),minor=True); ax.set_yticks(np.arange(-.5,29,1),minor=True)
    ax.grid(which="minor",color="white",lw=0.7); ax.tick_params(which="minor",length=0)
    ax.set_title(title, fontsize=10.5, fontweight="bold", loc="left")

# One identical horizontal scale below each panel. Colours are normalised
# independently within every column, while the exact count remains printed in-cell.
for ax in axes:
    scale = fig.colorbar(ScalarMappable(norm=Normalize(0, 1), cmap=cmap), ax=ax,
                         orientation="horizontal", fraction=0.035, pad=0.085)
    scale.set_ticks([0, 1])
    scale.set_ticklabels(["minimum", "maximum"])
    scale.ax.tick_params(labelsize=7, length=0, pad=1)
    scale.ax.set_title("Colour scale within each column", fontsize=8, pad=3)
# Tidy phylum legend (single row, below both colour scales).
keys=[Line2D([0],[0],marker='s',color='none',markerfacecolor=c,markersize=9,label=p) for p,c in PHYLUM_COLORS.items()]
fig.legend(handles=keys, loc="lower center", ncol=5, fontsize=8, frameon=False, bbox_to_anchor=(0.5,0.005),
           title="Row label colour = phylum", title_fontsize=8.5)
fig.subplots_adjust(left=0.10, right=0.98, top=0.97, bottom=0.17)
paths = save3(fig, OUT, "Fig_3.7_MAG29_functional")

out = vals[["Phylum","COG","KEGG","CAZymes","VFDB"]].copy()
out["AMP"]=fsc["AMP_ampir_p0.5"].values; out["ARG"]=fsc["ARG_hamronization"].values
out["GECCO"]=fsc["BGC_GECCO"].values; out["antiSMASH"]=fsc["BGC_antiSMASH"].values
out.to_csv(OUT/"Fig_3.7_MAG29_functional_PLOTTED_VALUES.tsv", sep="\t")
print("panels 29x4 + 29x4 | rows SS-01..SS-29 | blue-red column-min-to-column-max | saved", paths['png'].name)
