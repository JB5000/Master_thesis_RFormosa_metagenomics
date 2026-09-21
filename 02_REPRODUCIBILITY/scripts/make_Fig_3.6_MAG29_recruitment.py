#!/usr/bin/env python3
"""Fig 3.6 — MAG29 temporal recruitment (row-wise z-score heatmap).
Rows ordered SS-01..SS-29 (numerical); MAG-label axis shows ONLY the canonical SS IDs.
Each MAG's assembly-source-sample cell is outlined in fluorescent yellow (#FFFF00, ~2.7 pt).
No "Assembly source" column and no source-date text inside the image (explained in the caption only).
Matrix unchanged (29 x 23); source assignments via the authoritative reconciliation table."""
from pathlib import Path
import os
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import sys; sys.path.insert(0, str(Path(__file__).parent))
from fig_style import ZSCORE_CMAP, YELLOW, mg_to_sid, save3, FULLPAGE_LAND


SOURCE = Path(__file__).resolve().parents[1] / "figure_sources"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)
VMIN, VMAX = -3.0, 3.0

Z = pd.read_csv(SOURCE/"recruitment/MAG29_row_zscore_23samples.tsv", sep="\t", index_col=0)
recon = pd.read_csv(SOURCE/"taxonomy/MAG_ID_RECONCILIATION_AUTHORITATIVE.tsv", sep="\t")
src_of = dict(zip(recon["authoritative_ID"], recon["source_sample"]))

rows = sorted(Z.index, key=lambda s: int(s.split("-")[1]))   # SS-01..SS-29
Z = Z.loc[rows]
samples = list(Z.columns)
M = Z.values
assert M.shape == (29, 23), f"expected 29x23, got {M.shape}"
src_sid = {r: mg_to_sid(src_of.get(r, "")) for r in rows}

fig, ax = plt.subplots(figsize=FULLPAGE_LAND)
im = ax.imshow(M, aspect="auto", cmap=ZSCORE_CMAP, vmin=VMIN, vmax=VMAX)
ax.set_xticks(range(len(samples))); ax.set_xticklabels(samples, rotation=90, fontsize=8)
ax.set_yticks(range(len(rows))); ax.set_yticklabels(rows, fontsize=8)
ax.set_xlabel("Sample date (S_YY_MM_DD)")
ax.set_xticks(np.arange(-.5, len(samples), 1), minor=True)
ax.set_yticks(np.arange(-.5, len(rows), 1), minor=True)
ax.grid(which="minor", color="white", linewidth=0.6); ax.tick_params(which="minor", length=0)

n_out = 0
for i, r in enumerate(rows):
    sid = src_sid[r]
    if sid in samples:
        j = samples.index(sid)
        ax.add_patch(Rectangle((j-.5, i-.5), 1, 1, fill=False, edgecolor=YELLOW, linewidth=2.7, zorder=6))
        n_out += 1

cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
cb.set_label("Row-wise z-score of length-weighted mean coverage", fontsize=9)
cb.ax.tick_params(labelsize=8)
fig.tight_layout()
paths = save3(fig, OUT, "Fig_3.6_MAG29_recruitment")

# plotted values + a SEPARATE source-map TSV (kept out of the image)
Z.to_csv(OUT/"Fig_3.6_MAG29_recruitment_PLOTTED_VALUES.tsv", sep="\t")
pd.DataFrame({"MAG_ID": rows, "assembly_source_sample": [src_sid[r] for r in rows]}).to_csv(
    OUT/"Fig_3.6_MAG29_source_map.tsv", sep="\t", index=False)
print(f"matrix {M.shape} | rows SS-01..SS-29 | yellow source outlines: {n_out}/29 | saved {paths['png'].name}")
