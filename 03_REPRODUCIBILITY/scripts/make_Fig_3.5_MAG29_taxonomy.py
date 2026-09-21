#!/usr/bin/env python3
"""Fig 3.5 — GTDB-Tk r226 taxonomic cladogram of the 29 MAG29 representatives.
Uses the retained recursive cladogram drawing logic with the authoritative taxonomy and print-legible fonts.
Nested rank membership (Phylum..Genus); NOT an independently inferred phylogeny."""
from pathlib import Path
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys; sys.path.insert(0, str(Path(__file__).parent))
from fig_style import save3


SOURCE = Path(__file__).resolve().parents[1] / "figure_sources"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)
RANK_NAMES = ["Phylum","Class","Order","Family","Genus"]
PHYLUM_COLORS = {"Pseudomonadota":"#4575b4","Desulfobacterota":"#d73027","Actinomycetota":"#fdae61",
                 "Cyanobacteriota":"#1a9850","Bacteroidota":"#9e6ebd"}

cat = pd.read_csv(SOURCE/"taxonomy/Table_MAG29_full_catalogue_AUTHORITATIVE.tsv", sep="\t")
cat = cat.set_index("MAG_ID").loc[[f"SS-{i:02d}" for i in range(1,30)]]
def clean(v, fallback=""):
    v=str(v).strip(); return v if v and v.lower() not in ("nan","unclassified","") else fallback
TAXONOMY = {}
for mid, r in cat.iterrows():
    # Use the same explicit missing-genus wording as the MAG29 taxonomy table rather than
    # repeating the family name at the terminal leaf.
    lin = ";".join([clean(r["Phylum"]), clean(r["Class"]), clean(r["Order"]), clean(r["Family"]),
                    clean(r["Genus"], "genus not assigned")])
    TAXONOMY[mid] = ("", lin)

def build(tax):
    tree={}
    for mid,(_,lin) in tax.items():
        node=tree
        for rank in lin.split(";"):
            node=node.setdefault(rank, {})
        node[f"__LEAF__{mid}"]={}
    return tree
def nleaf(node):
    return sum(1 if k.startswith("__LEAF__") else nleaf(v) for k,v in node.items())

def draw(ax, node, x, y0, y1, depth, xs, leaves, blabels):
    items=[(k,node[k],nleaf(node[k])) for k in node if not k.startswith("__LEAF__")] + \
          [(k,{},1) for k in node if k.startswith("__LEAF__")]
    total=sum(n for *_,n in items)
    if total==0: return
    yps=[]; cum=y0
    for name,sub,nl in items:
        span=(y1-y0)*nl/total; ym=cum+span/2
        ax.plot([x,x+xs],[ym,ym], color="#9a9a9a", lw=0.9, solid_capstyle="round")
        if name.startswith("__LEAF__"):
            mid=name.replace("__LEAF__",""); phy=TAXONOMY[mid][1].split(";")[0]; gen=TAXONOMY[mid][1].split(";")[-1]
            leaves.append((x+xs, ym, mid, gen, phy))
        else:
            if depth<4 and nl>=2:
                blabels.append((x+xs*0.5, ym, name, max(7.5, 10-depth)))
            draw(ax, sub, x+xs, cum, cum+span, depth+1, xs, leaves, blabels)
        yps.append(ym); cum+=span
    if len(yps)>=2: ax.plot([x,x],[yps[0],yps[-1]], color="#9a9a9a", lw=0.9, solid_capstyle="round")

tree=build(TAXONOMY); n=nleaf(tree)
fig, ax = plt.subplots(figsize=(13.5, 12.5)); ax.set_axis_off()
leaves=[]; blabels=[]; xs=1.0
draw(ax, tree, 0, 0, n, 0, xs, leaves, blabels)
for lx,ly,mid,gen,phy in leaves:
    ax.plot(lx,ly,"o",color=PHYLUM_COLORS.get(phy,"#999"),markersize=11,markeredgecolor="white",markeredgewidth=0.9,zorder=5)
    ax.text(lx+0.14, ly, f"{mid}  {gen}", va="center", fontsize=11.0, color="#222", fontstyle="italic")
for bx,by,name,fs in blabels:
    ax.text(bx, by+0.22, name, ha="center", va="bottom", fontsize=fs, color="#555", fontstyle="italic",
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85))
for i,rn in enumerate(RANK_NAMES):
    ax.text(i*xs+xs*0.5, -0.8, rn, ha="center", va="bottom", fontsize=11, color="#555", fontweight="bold")
counts=cat["Phylum"].value_counts()
patches=[mpatches.Patch(color=c,label=f"{p} ({int(counts.get(p,0))})") for p,c in PHYLUM_COLORS.items() if p in counts.index]
fig.legend(handles=patches, title="Phylum (n MAGs)", loc="lower center", ncol=5,
           fontsize=10, title_fontsize=10.5, frameon=False, bbox_to_anchor=(0.5, 0.01))
maxx=max(lx for lx,*_ in leaves)+4.5
ax.set_xlim(-0.5, maxx); ax.set_ylim(-1.2, n+0.8)
ax.invert_yaxis()  # SS-01 at the top, followed by SS-02 ... SS-29
fig.subplots_adjust(left=0.02, right=0.99, top=0.98, bottom=0.08)
paths=save3(fig, OUT, "Fig_3.5_MAG29_taxonomy")
cat.reset_index()[["MAG_ID"]+RANK_NAMES].to_csv(OUT/"Fig_3.5_MAG29_taxonomy_PLOTTED_VALUES.tsv", sep="\t", index=False)
print(f"{n} leaves SS-01..SS-29 (retained cladogram logic, source taxonomy) | phyla {dict(counts)}")
