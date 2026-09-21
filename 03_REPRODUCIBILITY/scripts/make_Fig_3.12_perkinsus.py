#!/usr/bin/env python3
"""Fig 3.12 — Perkinsus olseni BLASTn-derived RPM through time.
Mean BLASTn RPM per date with conventional point-wise SD error bars across the three equal-depth subsets.
One neutral line colour; NO special red/highlighted point and no marker emphasis on the maximum.
Chronological dates. RPM is computed from BLASTn hits per 315,147-read subset."""
from pathlib import Path
import os
import pandas as pd
import matplotlib.pyplot as plt
import sys; sys.path.insert(0, str(Path(__file__).parent))
from fig_style import save3


SOURCE = Path(__file__).resolve().parents[1] / "figure_sources"
BLAST_TABLE = Path(__file__).resolve().parents[2] / "06_METHODS_AND_VALIDATION" / "17_BLAST_VALIDATION" / "Perkinsus_olseni_BLAST_hits_timeseries.tsv"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)
TOTAL = 315147
LINE = "#33547a"   # single neutral colour

df = pd.read_csv(BLAST_TABLE, sep="\t").rename(columns={"sample": "sample_id"}).sort_values("sample_id")
x = range(len(df)); labels = list(df["sample_id"])
rpm = df["mean_rpm"].astype(float).values
sd  = df["sd_rpm"].astype(float).values

def draw(figsize, name):
    fig, ax = plt.subplots(figsize=figsize)
    ax.errorbar(list(x), rpm, yerr=sd, fmt="-o", color=LINE, ecolor=LINE,
                lw=1.6, elinewidth=1.0, capsize=3, capthick=1.0,
                ms=4.5, mfc="white", mew=1.1, zorder=3)
    ax.set_xticks(list(x)); ax.set_xticklabels(labels, rotation=90, fontsize=8)
    ax.set_ylabel("$\\it{Perkinsus\\ olseni}$  BLASTn-derived RPM", fontsize=10)
    ax.set_xlabel("Sample date (S_YY_MM_DD)", fontsize=10)
    ax.set_ylim(0, (rpm + sd).max() * 1.12)
    for sp in ("top","right"): ax.spines[sp].set_visible(False)
    ax.yaxis.grid(True, color="#e6e6e6", lw=0.7); ax.set_axisbelow(True); ax.margins(x=0.02)
    fig.tight_layout(); return save3(fig, OUT, name)

draw((11.0, 5.0), "Fig_3.12_perkinsus_landscape")
draw((7.4, 6.4), "Fig_3.12_perkinsus_wide_portrait")
out = df[["sample_id", "mean_hits", "sd_hits", "mean_rpm", "sd_rpm"]].copy()
out.to_csv(OUT/"Fig_3.12_perkinsus_PLOTTED_VALUES.tsv", sep="\t", index=False)
print("BLASTn RPM line + point-wise SD error bars; no highlighted point; chronological | saved landscape + wide-portrait")
