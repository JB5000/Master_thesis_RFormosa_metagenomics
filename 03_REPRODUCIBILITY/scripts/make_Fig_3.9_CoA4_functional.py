#!/usr/bin/env python3
"""Fig 3.9 — CoA4 FUNCTIONAL summary only, same visual template as Fig 3.7 (no taxonomy table in the figure).
A "Annotation-derived protein counts": COG, KEGG, CAZy, VFDB.
B "FuncScan screening outputs": AMP, ARG, GECCO, antiSMASH.
Rows CoA-1..CoA-4; CoA IDs on both panels. Blue(low)->red(high), normalised independently from the
displayed minimum to maximum of each column. Raw counts in cells.
No quantitative GenomeSPOT traits. The taxonomy/quality is provided separately as Table 3.3 (external TSV)."""
from pathlib import Path
import os
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.lines import Line2D
import sys; sys.path.insert(0, str(Path(__file__).parent))
from fig_style import COUNT_CMAP, phylum_color, save3


SOURCE = Path(__file__).resolve().parents[1] / "figure_sources"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)
reps = ["CoA-1","CoA-2","CoA-3","CoA-4"]
PHY = {"CoA-1":"Pseudomonadota","CoA-2":"Pseudomonadota","CoA-3":"Cyanobacteriota","CoA-4":"Cyanobacteriota"}

fun = pd.read_csv(SOURCE/"functional/CoA4_functional_values_PRIMARY_DERIVED.tsv", sep="\t").set_index("CoA_ID").loc[reps]
PANELS = [("A  Annotation-derived protein counts", fun[["COG","KEGG","CAZy","VFDB"]].astype(int).values, ["COG","KEGG","CAZy","VFDB"]),
          ("B  FuncScan screening outputs", fun[["AMP","ARG","GECCO","antiSMASH"]].astype(int).values, ["AMP","ARG","GECCO","antiSMASH"])]

fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.4), gridspec_kw={"wspace":0.30})
cmap = plt.get_cmap(COUNT_CMAP)
for ax, (title, A, labels) in zip(axes, PANELS):
    A = A.astype(float); assert A.shape == (4,4)
    rgba = np.zeros(A.shape+(4,))
    for c in range(A.shape[1]):
        lo, hi = A[:,c].min(), A[:,c].max()
        norm = Normalize(lo, hi if hi>lo else lo+1)
        rgba[:,c] = cmap(norm(A[:,c]))
    for i in range(A.shape[0]):
        for c in range(A.shape[1]):
            ax.add_patch(plt.Rectangle((c-.5,i-.5),1,1,facecolor=rgba[i,c],
                                       edgecolor="none"))
    for i in range(4):
        for c in range(4):
            lum=0.299*rgba[i,c,0]+0.587*rgba[i,c,1]+0.114*rgba[i,c,2]
            ax.text(c,i,f"{int(A[i,c])}",ha="center",va="center",fontsize=8.5,color="white" if lum<0.5 else "black")
    ax.set_xticks(range(4)); ax.set_xticklabels(labels, fontsize=9)
    ax.set_yticks(range(4)); ax.set_yticklabels(reps, fontsize=9.5)
    ax.set_xlim(-.5,3.5); ax.set_ylim(3.5,-.5)
    for tick,r in zip(ax.get_yticklabels(), reps): tick.set_color(phylum_color(PHY[r]))
    ax.set_xticks(np.arange(-.5,4,1),minor=True); ax.set_yticks(np.arange(-.5,4,1),minor=True)
    ax.grid(which="minor",color="white",lw=0.7); ax.tick_params(which="minor",length=0)
    ax.set_title(title, fontsize=10.5, fontweight="bold", loc="left")
keys=[Line2D([0],[0],marker='s',color='none',markerfacecolor=phylum_color(p),markersize=9,label=p) for p in ["Cyanobacteriota","Pseudomonadota"]]
for ax in axes:
    scale = fig.colorbar(ScalarMappable(norm=Normalize(0, 1), cmap=cmap), ax=ax,
                         orientation="horizontal", fraction=0.045, pad=0.16)
    scale.set_ticks([0, 1])
    scale.set_ticklabels(["minimum", "maximum"])
    scale.ax.tick_params(labelsize=7, length=0, pad=1)
    scale.ax.set_title("Colour scale within each column", fontsize=8, pad=3)
fig.legend(handles=keys, loc="lower center", ncol=2, fontsize=8, frameon=False, bbox_to_anchor=(0.5,0.01),
           title="Row label colour = phylum", title_fontsize=8.5)
fig.subplots_adjust(left=0.09, right=0.98, top=0.93, bottom=0.34)
paths = save3(fig, OUT, "Fig_3.9_CoA4_functional")
fun.to_csv(OUT/"Fig_3.9_CoA4_functional_PLOTTED_VALUES.tsv", sep="\t")

# external Table 3.3 — CoA4 taxonomy & genome quality (NOT embedded in the figure)
cat = pd.read_csv(SOURCE/"coa4/Table_CoA4_catalogue.tsv", sep="\t").set_index("CoA_ID").loc[reps]
STRICT = {"CoA-1":"no (23S and 5S absent; tRNA criterion met)","CoA-2":"yes","CoA-3":"yes","CoA-4":"yes"}
# CoA-3 CheckM2 values are retained in a separate report (catalogue has NA) -> use the authoritative report
coa3 = pd.read_csv(SOURCE/"coa4/CoA-3_CheckM2_quality_report.tsv", sep="\t").iloc[0]
COMPL = {r: cat.loc[r,"Completeness"] for r in reps}; CONT = {r: cat.loc[r,"Contamination"] for r in reps}
COMPL["CoA-3"] = coa3["Completeness"]; CONT["CoA-3"] = coa3["Contamination"]   # 97.01 / 2.71
def q(x):
    try: return f"{float(x):.2f}"
    except: return "n.d."
t33 = pd.DataFrame({
    "CoA_ID": reps,
    "Phylum":[cat.loc[r,"GTDB_Phylum"] for r in reps],
    "Family":[cat.loc[r,"GTDB_Family"] for r in reps],
    "Genus_lowest_GTDB_taxon":[cat.loc[r,"GTDB_Genus"] for r in reps],
    "Genome_size_Mb":[cat.loc[r,"Genome_size_Mb"] for r in reps],
    "N_contigs":[cat.loc[r,"N_contigs"] for r in reps],
    "Completeness_pct":[q(COMPL[r]) for r in reps],
    "Contamination_pct":[q(CONT[r]) for r in reps],
    "Strict_MIMAG_HQ":[STRICT[r] for r in reps],
})
t33.to_csv(OUT/"CoA4_taxonomy_quality.tsv", sep="\t", index=False)
print("CoA4 functional 4x4+4x4, column-min-to-column-max colour + taxonomy quality table | saved", paths['png'].name)
