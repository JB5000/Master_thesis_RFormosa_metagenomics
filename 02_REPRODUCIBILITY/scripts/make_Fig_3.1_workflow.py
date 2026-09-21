#!/usr/bin/env python3
"""Fig 3.1 — analytical workflow (rebuilt). No figure numbers cited inside the image; the
'Cyanobacteriota pattern (Figure 3.3A)' text is removed and replaced by a clean connector. Eight
distinguished stages: (1) sample collection & ONT sequencing; (2) read-level taxonomy & equal-depth
validation; (3) per-sample assembly & binning; (4) CheckM2/GUNC & dRep; (5) MAG29; (6) targeted
four-sample coassembly, separate dRep & CoA4; (7) custom BLAST database & the P. olseni follow-up; (8) downstream taxonomy,
recruitment & functional screening. MAG29 and CoA4 undergo comparable downstream analyses but remain
separate. Connectors are routed outside boxes and do not cross text."""
from pathlib import Path
import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
import sys; sys.path.insert(0, str(Path(__file__).parent))
from fig_style import save3

SOURCE = Path(__file__).resolve().parents[1] / "figure_sources"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)
C = dict(input="#d9d9d9", read="#fdbf6f", assembly="#a6cee3", catalogue="#8fce8f",
         coassembly="#66c2a5", target="#cbaacb", perk="#f08a6c", downstream="#c9dcef")
EDGE = "#3a3a3a"

fig, ax = plt.subplots(figsize=(12.4, 8.4))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

def box(x, y, w, h, text, color, fs=9.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=2",
                 linewidth=1.3, edgecolor=EDGE, facecolor=color))
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=fs,
            fontweight="normal", zorder=5)
    return dict(cx=x+w/2, top=y+h, bot=y, l=x, r=x+w, cy=y+h/2)

def arrow(a, b, rad=0.0):
    ax.add_patch(FancyArrowPatch((a[0], a[1]), (b[0], b[1]), arrowstyle="-|>", mutation_scale=14,
                 lw=1.4, color=EDGE, connectionstyle=f"arc3,rad={rad}", zorder=1))

def elbow_arrow(points):
    """Route a connector through explicit waypoints, with the arrowhead on the final segment."""
    for a, b in zip(points[:-2], points[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=EDGE, lw=1.4, zorder=1)
    arrow(points[-2], points[-1])

# (1) input: collection + ONT sequencing
inp = box(34, 89, 32, 7, "Sediment sampling and\nOxford Nanopore sequencing (23 metagenomes)", C["input"], fs=10)

# column headers
ax.text(19, 83, "Genome-resolved analysis", ha="center", fontsize=11.5, fontweight="normal")
ax.text(64, 83, "Read-level context and targeted follow-up", ha="left", fontsize=11.5, fontweight="normal")

DW = ("Downstream characterisation:\nMIMAG · GTDB-Tk taxonomy\nseparate read recruitment\n"
      "functional annotation and screening\nporTraits submission")

# LEFT column (3,4,5,8)
LC = 19
l1 = box(LC-14, 69, 28, 7, "Per-sample assembly and binning", C["assembly"])
l2 = box(LC-14, 58, 28, 7, "CheckM2 quality classes\n+ complementary GUNC", C["assembly"])
l3 = box(LC-14, 47, 28, 7, "dRep dereplication (ANI 95%)\n→ MAG29 (29 representatives)", C["catalogue"])
l4 = box(LC-15, 28, 30, 11, "MAG29 —\n"+DW, C["downstream"], fs=9)
arrow((l1['cx'], l1['bot']), (l2['cx'], l2['top']))
arrow((l2['cx'], l2['bot']), (l3['cx'], l3['top']))
arrow((l3['cx'], l3['bot']), (l4['cx'], l4['top']))

# RIGHT column (2,6,8)
RC = 58
r1 = box(RC-15, 69, 30, 7, "Equal-depth subsampling\n(23 dates × 3 subsets)", C["read"])
r2 = box(RC-15, 58, 30, 7, "KrakenUniq read-level taxonomy\nand equal-depth validation", C["read"])
r3 = box(RC-15, 47, 30, 7, "Read-level taxonomic composition\nBray–Curtis PCoA", C["read"])
r4 = box(RC-15, 33, 30, 8, "Targeted coassembly of non-subsampled\nsample-level read datasets (four 2025 dates)", C["coassembly"], fs=9)
r5 = box(RC-15, 22.5, 30, 7.5, "Separate dRep dereplication\n→ CoA4 (4 representatives)", C["catalogue"], fs=9)
r6 = box(RC-15, 5, 30, 11, "CoA4 —\n"+DW, C["downstream"], fs=9)
arrow((r1['cx'], r1['bot']), (r2['cx'], r2['top']))
arrow((r2['cx'], r2['bot']), (r3['cx'], r3['top']))
arrow((r3['cx'], r3['bot']), (r4['cx'], r4['top']))   # clean connector (no in-image figure citation)
arrow((r4['cx'], r4['bot']), (r5['cx'], r5['top']))
arrow((r5['cx'], r5['bot']), (r6['cx'], r6['top']))

# (7) custom BLAST database branch (kept separate)
k1 = box(78, 58, 20, 7, "Custom BLAST database\n(BLASTn target screen)", C["target"])
k2 = box(78, 46, 20, 8, r"$\it{Perkinsus\ olseni}$"+"\nBLASTn-derived signal", C["perk"], fs=9)
elbow_arrow([(r1['r'], r1['cy']), (k1['cx'], r1['cy']), (k1['cx'], k1['top'])])
arrow((k1['cx'], k1['bot']), (k2['cx'], k2['top']))

# input split: orthogonal routes remain fully outside the headers and boxes.
elbow_arrow([(inp['cx']-8, inp['bot']), (inp['cx']-8, 79.5),
             (l1['cx'], 79.5), (l1['cx'], l1['top'])])
arrow((r1['cx'], inp['bot']), (r1['cx'], r1['top']))

leg = [Line2D([0],[0], marker='s', color='none', markerfacecolor=c, markeredgecolor=EDGE, markersize=11, label=lab)
       for lab, c in [("Input / sequencing",C["input"]),("Read-level analysis",C["read"]),
                      ("Assembly / quality",C["assembly"]),("Genome catalogue",C["catalogue"]),
                      ("Coassembly",C["coassembly"]),("BLAST target screen",C["target"]),
                      ("Downstream characterisation",C["downstream"])]]
fig.legend(handles=leg, loc="lower center", ncol=4, fontsize=8.5, frameon=True, bbox_to_anchor=(0.5, 0.02))
# (the "comparable downstream / GenomeSPOT MAG29-only" note lives in the thesis caption, not in the image)
fig.subplots_adjust(left=0.02, right=0.98, top=0.97, bottom=0.08)
paths = save3(fig, OUT, "Fig_3.1_workflow")
print("saved", paths['png'].name)
