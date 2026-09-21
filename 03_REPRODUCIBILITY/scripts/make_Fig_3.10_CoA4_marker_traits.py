#!/usr/bin/env python3
"""Figure 3.10 — CoA4 counterpart to Figure 3.8.
Panel A shows curated marker gene/functional group counts for CoA-1..CoA-4.
Panel B uses the same names, row order, formatting and column structure as Figure 3.8 and shows
marker-derived predicted metabolic traits. No values are inferred."""
from pathlib import Path
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import sys; sys.path.insert(0, str(Path(__file__).parent))
from fig_style import COUNT_CMAP, phylum_color, save3

SOURCE = Path(__file__).resolve().parents[1] / "figure_sources"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)
SEL = ["CoA-1","CoA-2","CoA-3","CoA-4"]
PHY = {"CoA-1":"Pseudomonadota","CoA-2":"Pseudomonadota",
       "CoA-3":"Cyanobacteriota","CoA-4":"Cyanobacteriota"}

t36 = pd.read_csv(SOURCE/"functional/Table_3_6_curated_functional_comparison_SOURCE.tsv",
                  sep="\t", index_col=0)
CAT = [
 ("Sulfur cycling",["Dissimilatory sulfate reduction (dsrAB)","Sulfate activation (sat/aprA)",
                    "Thiosulfate oxidation (soxB)","Sulfide:quinone oxidoreductase (sqr)"]),
 ("Nitrogen cycling",["Nitrate reduction (narG)","Denitrification (nirS/nirK)",
                      "Nitrogen fixation (nifH)","Urease (ureC)"]),
 ("Carbon & photosynthesis",["RuBisCO (rbcL)","Photosystem II (psbA)","Photosystem I (psaA)"]),
 ("Organic matter",["Glycoside hydrolases (GH)","Glycosyltransferases (GT)",
                    "Formate dehydrogenase (fdhA)","Acetyl-CoA synthetase (acs)"]),
 ("Electron transport",["Cytochrome c oxidase (coxA)","Cytochrome bd oxidase (cydA)",
                        "Fumarate reductase (frdA)"]),
 ("Motility & stress",["Flagellar motility (fliC/motA)","Type IV pili (pilA)",
                       "Copper resistance (copA)","Oxidative stress (sodB/katE)"]),
 ("Biosynthetic gene clusters",["BGC: NRP (GECCO)","BGC: Polyketide (GECCO)",
                                "BGC: RiPP (GECCO)","BGC: Terpene (GECCO)"])
]
mk_rows=[m for _,ms in CAT for m in ms if m in t36.index]
Amat=t36.loc[mk_rows,SEL].apply(pd.to_numeric).values.astype(float)

TRAITS=[
 ("Sulfate reduction (dsrAB)",["Dissimilatory sulfate reduction (dsrAB)"]),
 ("Sulfur oxidation (soxB/sqr)",["Thiosulfate oxidation (soxB)","Sulfide:quinone oxidoreductase (sqr)"]),
 ("Nitrogen fixation (nifH)",["Nitrogen fixation (nifH)"]),
 ("Denitrification (nirS/nirK)",["Denitrification (nirS/nirK)"]),
 ("Carbon fixation (rbcL)",["RuBisCO (rbcL)"]),
 ("Photosynthesis (psbA/psaA)",["Photosystem II (psbA)","Photosystem I (psaA)"]),
 ("Flagellar motility (fliC/motA)",["Flagellar motility (fliC/motA)"]),
 ("Aerobic respiration (coxA)",["Cytochrome c oxidase (coxA)"])
]
present=np.array([[int(sum(float(t36.loc[m,s]) for m in ms if m in t36.index)>0)
                   for s in SEL] for _,ms in TRAITS])

def draw_A(ax):
    # Raw counts are printed in the cells; colour is deliberately normalised
    # within each functional row so profiles can be compared across the four MAGs.
    cmap=plt.get_cmap(COUNT_CMAP)
    rgba=np.zeros(Amat.shape+(4,))
    for i,row in enumerate(Amat):
        lo, hi = row.min(), row.max()
        rgba[i]=cmap(Normalize(lo, hi if hi>lo else lo+1)(row))
    for i in range(Amat.shape[0]):
        for j in range(Amat.shape[1]):
            ax.add_patch(Rectangle((j-.5,i-.5),1,1,facecolor=rgba[i,j],
                                   edgecolor="none"))
    for i in range(Amat.shape[0]):
        for j in range(len(SEL)):
            v=int(Amat[i,j])
            lum=0.299*rgba[i,j,0]+0.587*rgba[i,j,1]+0.114*rgba[i,j,2]
            ax.text(j,i,str(v),ha="center",va="center",fontsize=7.2,
                    color="#777777" if v==0 else ("white" if lum<0.5 else "black"))
    ax.set_yticks(range(len(mk_rows))); ax.set_yticklabels(mk_rows,fontsize=7.0)
    ax.set_xticks(range(len(SEL))); ax.set_xticklabels(SEL,fontsize=9)
    for lab,s in zip(ax.get_xticklabels(),SEL):
        lab.set_color(phylum_color(PHY[s])); lab.set_fontweight("normal")
    ax.set_xlim(-.5,len(SEL)-.5); ax.set_ylim(len(mk_rows)-.5,-.5)
    ax.set_xticks(np.arange(-.5,len(SEL),1),minor=True)
    ax.set_yticks(np.arange(-.5,len(mk_rows),1),minor=True)
    ax.grid(which="minor",color="white",lw=0.6); ax.tick_params(which="minor",length=0)
    ax.set_title("A  Curated marker-gene / functional-group counts",
                 fontsize=10.5,fontweight="bold",loc="left")

def draw_B(ax):
    ax.axis("off")
    off=0
    for i,(name,_) in enumerate(TRAITS):
        for j in range(len(SEL)):
            ax.add_patch(Rectangle((j,-off-i),1,1,
                                   facecolor="#3a3a3a" if present[i,j] else "#ededed",
                                   edgecolor="white"))
        ax.text(-0.2,-off-i+0.5,name,ha="right",va="center",fontsize=8)
    bottom=-(off+len(TRAITS)-1)
    ax.add_patch(Rectangle((0,bottom),len(SEL),1-bottom,fill=False,
                           edgecolor="#666666",linewidth=0.8,zorder=6))
    for j in range(1,len(SEL)):
        ax.plot([j,j],[bottom,1],color="#666666",linewidth=0.65,zorder=6)
    for j,s in enumerate(SEL):
        ax.text(j+0.5,bottom-0.10,s,ha="center",va="top",fontsize=9,
                color=phylum_color(PHY[s]),fontweight="normal")
    ax.set_xlim(-2.0,len(SEL)); ax.set_ylim(bottom-0.62,1.4)
    ax.text(2/6, 1.02, "B  Marker-derived metabolic traits", transform=ax.transAxes,
            ha="left", va="bottom", fontsize=10.5, fontweight="bold")

leg=[Line2D([0],[0],marker='s',color='none',markerfacecolor=phylum_color(PHY[s]),
            markersize=8,label=f"{s}: {PHY[s]}") for s in SEL]
leg += [Line2D([0],[0],marker='s',color='none',markerfacecolor='#3a3a3a',markersize=8,label='trait present'),
        Line2D([0],[0],marker='s',color='none',markerfacecolor='#ededed',
               markeredgecolor='#ccc',markersize=8,label='trait absent')]

fig,(axA,axB)=plt.subplots(1,2,figsize=(12.8,8.6),
                           gridspec_kw={"width_ratios":[1.0,1.05],"wspace":0.55})
draw_A(axA); draw_B(axB)
scale=fig.colorbar(ScalarMappable(norm=Normalize(0,1),cmap=plt.get_cmap(COUNT_CMAP)), ax=axA,
                   orientation="horizontal", fraction=0.045, pad=0.14)
scale.set_ticks([0,1]); scale.set_ticklabels(["minimum","maximum"])
scale.ax.tick_params(labelsize=7,length=0,pad=1)
scale.ax.set_title("Colour scale within each row",fontsize=8,pad=3)
fig.legend(handles=leg,loc="lower center",bbox_to_anchor=(0.5,0.005),
           ncol=4,fontsize=7.1,frameon=False)
fig.subplots_adjust(left=0.19,right=0.99,top=0.95,bottom=0.19)
save3(fig,OUT,"Fig_3.10_CoA4_marker_traits")
pd.DataFrame(Amat,index=mk_rows,columns=SEL).to_csv(
    OUT/"Fig_3.10_CoA4_marker_counts_PLOTTED_VALUES.tsv",sep="\t")
pd.DataFrame(present,index=[t[0] for t in TRAITS],columns=SEL).to_csv(
    OUT/"Fig_3.10_CoA4_marker_traits_presence_PLOTTED_VALUES.tsv",sep="\t")
print(f"CoA4 counterpart: markers {Amat.shape}, marker-derived traits {present.shape}")
