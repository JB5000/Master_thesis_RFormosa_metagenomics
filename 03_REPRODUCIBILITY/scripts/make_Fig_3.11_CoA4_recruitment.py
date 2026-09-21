#!/usr/bin/env python3
"""Fig 3.11 — CoA4 temporal recruitment (row-wise z-score heatmap), same styling as Fig 3.6.
Rows ordered CoA-1..CoA-4; label axis shows only canonical CoA IDs. For EVERY CoA row, the four coassembly
INPUT dates (S_25_04_30/07_10/09_12/11_25) are outlined in fluorescent yellow (#FFFF00, ~2.7 pt) — the same
outline style as Fig 3.6. No "Coassembly input samples" text and no source legend inside the image.
Matrix unchanged (4 x 23); row-wise z-score."""
from pathlib import Path
import os
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import sys; sys.path.insert(0, str(Path(__file__).parent))
from fig_style import ZSCORE_CMAP, YELLOW, save3


SOURCE = Path(__file__).resolve().parents[1] / "figure_sources"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)
VMIN, VMAX = -3.0, 3.0
INPUTS = ["S_25_04_30","S_25_07_10","S_25_09_12","S_25_11_25"]

Z = pd.read_csv(SOURCE/"recruitment/CoA4_row_zscore_23samples.tsv", sep="\t", index_col=0)
rows = sorted(Z.index, key=lambda s: int(s.split("-")[1]))   # CoA-1..CoA-4
Z = Z.loc[rows]; samples = list(Z.columns); M = Z.values
assert M.shape == (4, 23), f"expected 4x23, got {M.shape}"

# Extra vertical room keeps the long colour-bar label fully inside the figure.
fig, ax = plt.subplots(figsize=(11.0, 4.4))
im = ax.imshow(M, aspect="auto", cmap=ZSCORE_CMAP, vmin=VMIN, vmax=VMAX)
ax.set_xticks(range(len(samples))); ax.set_xticklabels(samples, rotation=90, fontsize=8)
ax.set_yticks(range(len(rows))); ax.set_yticklabels(rows, fontsize=10)
ax.set_xlabel("Sample date (S_YY_MM_DD)")
ax.set_xticks(np.arange(-.5,len(samples),1),minor=True); ax.set_yticks(np.arange(-.5,len(rows),1),minor=True)
ax.grid(which="minor", color="white", linewidth=0.6); ax.tick_params(which="minor", length=0)

jin = [samples.index(s) for s in INPUTS if s in samples]
assert len(jin) == 4, "coassembly input columns not all found"
assert jin == list(range(min(jin), min(jin)+4)), "coassembly input columns must be contiguous"
# One independent rectangle per CoA row shows the same four input samples without enclosing a 4x4 block.
for i in range(len(rows)):
    ax.add_patch(Rectangle((min(jin)-.5, i-.5), 4, 1, fill=False,
                           edgecolor=YELLOW, linewidth=2.7, zorder=6))
cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
cb.set_label("Row-wise z-score of length-weighted mean coverage", fontsize=9)
cb.ax.tick_params(labelsize=8)
fig.tight_layout()
paths = save3(fig, OUT, "Fig_3.11_CoA4_recruitment")
Z.to_csv(OUT/"Fig_3.11_CoA4_recruitment_PLOTTED_VALUES.tsv", sep="\t")
print(f"matrix {M.shape} | four row-specific yellow rectangles span {[samples[j] for j in jin]} | saved {paths['png'].name}")
