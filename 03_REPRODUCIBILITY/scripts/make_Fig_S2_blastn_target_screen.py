#!/usr/bin/env python3
"""Supplementary Fig. S2 — BLASTn targeted screen, 20 reference targets."""
from pathlib import Path
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys; sys.path.insert(0, str(Path(__file__).parent))
from fig_style import ZSCORE_CMAP, save3

DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)
TABLE = Path(__file__).resolve().parents[2] / "06_METHODS_AND_VALIDATION" / "17_BLAST_VALIDATION" / "blast_sample_mean.tsv"

d = pd.read_csv(TABLE, sep="\t")
mat = d.pivot(index="target", columns="sample", values="mean_rpm").fillna(0.0)
samples = sorted(mat.columns)
targets = [
    "Bonamia ostreae", "Escherichia coli", "Lactococcus garvieae", "Mycobacterium marinum",
    "Ostreavirus ostreidmalaco1 / Ostreid herpesvirus 1 / OsHV-1", "Perkinsus olseni",
    "Photobacterium damselae", "Photobacterium damselae subsp. piscicida", "Pseudo-nitzschia",
    "Salmonella enterica", "Tenacibaculum maritimum", "Tenacibaculum soleae", "Vibrio aestuarianus",
    "Vibrio alginolyticus", "Vibrio anguillarum", "Vibrio cholerae", "Vibrio harveyi",
    "Vibrio parahaemolyticus", "Vibrio tapetis", "Vibrio vulnificus",
]
RPM = mat.loc[targets, samples]
sd = RPM.std(axis=1).replace(0, np.nan)
Z = RPM.sub(RPM.mean(axis=1), axis=0).div(sd, axis=0).fillna(0.0)
vlim = float(np.nanmax(np.abs(Z.values)))

fig, ax = plt.subplots(figsize=(15, 10))
im = ax.imshow(Z.values, aspect="auto", cmap=ZSCORE_CMAP, vmin=-vlim, vmax=vlim)
ax.set_xticks(range(len(samples))); ax.set_xticklabels(samples, rotation=55, ha="right", fontsize=8)
ax.set_yticks(range(len(targets))); ax.set_yticklabels(targets, fontsize=9)
for lab, target in zip(ax.get_yticklabels(), targets):
    lab.set_style("normal" if target.startswith("Ostreavirus") else "italic")
ax.set_xlabel("Sample date (S_YY_MM_DD)")
ax.set_title("BLASTn screen — all 20 reference targets (row-wise z-score)")
ax.set_xticks(np.arange(-.5, len(samples), 1), minor=True); ax.set_yticks(np.arange(-.5, len(targets), 1), minor=True)
ax.grid(which="minor", color="white", linewidth=0.6); ax.tick_params(which="minor", length=0)
cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
cb.set_label("Row-wise z-score of mean BLASTn RPM", fontsize=9); cb.ax.tick_params(labelsize=8)
fig.tight_layout()
save3(fig, OUT, "Fig_S2_blastn_target_screen")
RPM.round(3).to_csv(OUT / "Fig_S2_blastn_target_screen_RAW_RPM.tsv", sep="\t")
Z.round(4).to_csv(OUT / "Fig_S2_blastn_target_screen_ZSCORES.tsv", sep="\t")
