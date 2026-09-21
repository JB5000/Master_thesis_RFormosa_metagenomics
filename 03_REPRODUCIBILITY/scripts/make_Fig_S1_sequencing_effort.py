#!/usr/bin/env python3
"""Supplementary Fig S1 — raw sequencing effort across 23 samples.
Log-scaled bars with the equal-depth threshold and an explicit y-axis tick at the largest
library (S_24_04_16; 21,573,034 reads). All bars use the same colour."""
from pathlib import Path
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter
import sys; sys.path.insert(0, str(Path(__file__).parent))
from fig_style import save3


SOURCE = Path(__file__).resolve().parents[1] / "figure_sources"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)
SRC = SOURCE/"sequencing/S1_read_totals_source_fig2_sequencing_effort_qc_metrics.tsv"

df = pd.read_csv(SRC, sep="\t").sort_values("date_tag")
x = range(len(df))
reads = df["raw_reads_total"].astype(int)
imax = int(reads.idxmax())
max_reads = int(reads.max())
equal_depth = int(reads.min())

fig, ax = plt.subplots(figsize=(11.0, 4.6))
ax.bar(list(x), reads, color="#4C78B8", width=0.72)
ax.set_yscale("log")
ax.set_xticks(list(x))
ax.set_xticklabels(df["date_tag"], rotation=90, ha="center", va="top", fontsize=8)
ax.set_xlabel("Sample date (S_YY_MM_DD)")
ax.set_ylabel("Total reads (log scale)")
ax.axhline(equal_depth, color="#555", linestyle="--", linewidth=1.0)

ticks = sorted(set([equal_depth, 1_000_000, 10_000_000, max_reads]))
ax.yaxis.set_major_locator(FixedLocator(ticks))
def fmt(v, _):
    if int(v) == max_reads:
        return f"{v/1e6:.2f}M"
    if v >= 1_000_000:
        return f"{v/1e6:g}M"
    return f"{int(v):,}"
ax.yaxis.set_major_formatter(FuncFormatter(fmt))

for sp in ("top","right"): ax.spines[sp].set_visible(False)
ax.margins(x=0.01)
fig.subplots_adjust(left=0.09,right=0.99,top=0.97,bottom=0.34)
save3(fig, OUT, "Fig_S1_sequencing_effort")
df[["date_tag","raw_reads_total"]].to_csv(OUT/"Fig_S1_sequencing_effort_PLOTTED_VALUES.tsv", sep="\t", index=False)
print(f"23 samples | uniform bars | max y-axis tick={max_reads} | equal-depth={equal_depth}")
