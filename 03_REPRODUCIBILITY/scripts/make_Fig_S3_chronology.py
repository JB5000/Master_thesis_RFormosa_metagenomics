#!/usr/bin/env python3
"""Supplementary Figure S3 — chronological genus clade-read PCoA.
Points are numbered 1..23 in chronological order, with a compact chronological key
(number -> S_YY_MM_DD) beside the plot. No connecting arrows or season encoding are used.
The input is mean genus clade-read counts across three equal-depth replicates,
not a relative-abundance matrix."""
from pathlib import Path
import os
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import sys; sys.path.insert(0, str(Path(__file__).parent))
from fig_style import save3


SOURCE = Path(__file__).resolve().parents[1] / "figure_sources"
# These two clade-read PCoA inputs are retained locally as active Figure S3 sources.
HISTORICAL = SOURCE / "pcoa"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)
coords = pd.read_csv(HISTORICAL/"historical_genus_clade_read_pcoa_coordinates.tsv", sep="\t").set_index("sample_id")
metrics = pd.read_csv(HISTORICAL/"historical_pcoa_method_metrics.tsv", sep="\t").iloc[0]
eq = coords[["PC1", "PC2"]]
pc1v = float(metrics["PC1_percent_positive_eigenvalues"])
pc2v = float(metrics["PC2_percent_positive_eigenvalues"])
chrono=sorted(eq.index); rank={s:i+1 for i,s in enumerate(chrono)}
POINT_COLOR="#56B4E9"

fig, (ax, axk) = plt.subplots(1, 2, figsize=(11.6, 7.2), gridspec_kw={"width_ratios":[3.0,1.0], "wspace":0.05})
# Numbered points; chronology is read from the point numbers and key.
ax.scatter(eq.loc[chrono,"PC1"], eq.loc[chrono,"PC2"], s=250, c=POINT_COLOR,
           edgecolors="#333", linewidths=1.0, zorder=4)
for s in chrono:
    ax.text(eq.loc[s,"PC1"], eq.loc[s,"PC2"], str(rank[s]), ha="center", va="center", fontsize=8.5,
            fontweight="bold", color="white", zorder=5)
ax.axhline(0, color="#ececec", lw=0.6, zorder=0); ax.axvline(0, color="#ececec", lw=0.6, zorder=0)
ax.set_xlabel(f"PC1 ({pc1v:.1f}% var)"); ax.set_ylabel(f"PC2 ({pc2v:.1f}% var)")
for sp in ("top","right"): ax.spines[sp].set_visible(False)
# chronological key
axk.axis("off")
axk.text(0.0, 1.0, "Chronological order", fontsize=9, fontweight="bold", va="top")
for i,s in enumerate(chrono):
    axk.text(0.0, 0.955 - i*0.041, f"{rank[s]:>2}: {s}", fontsize=8, va="top", family="monospace")

fig.tight_layout()
paths = save3(fig, OUT, "Fig_S3_chronology")
pd.DataFrame({"from":chrono[:-1],"to":chrono[1:],"step":range(1,len(chrono))}).to_csv(OUT/"Fig_S3_chronology_EDGE_LIST.tsv", sep="\t", index=False)
coords.assign(chrono_rank=[rank[s] for s in coords.index]).to_csv(OUT/"Fig_S3_chronology_PLOTTED_VALUES.tsv", sep="\t")
print(f"genus clade reads | PC1={pc1v:.1f}% PC2={pc2v:.1f}% | 23 numbered points + chronological key; no arrows or seasons")
