#!/usr/bin/env python3
"""Figure 3.4 — CheckM2 bin recovery, quality and per sample distribution.

All plotted bins come directly from CHECKM2_PRIMARY_RESULTS.tsv. The HQ subset retained as final
dRep representatives is obtained from CHECKM2_TO_DREP_CROSSWALK.tsv. DASToolUnbinned entries are
excluded upstream and are explicitly rejected here. No values are simulated or resampled.
"""

from pathlib import Path
import os
import sys

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from fig_style import mg_to_sid, save3


# Clean-bundle root; core source data are stored under 04_CORE_ANALYSIS_DATA.
ROOT = Path(__file__).resolve().parents[2] / "04_CORE_ANALYSIS_DATA"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)

PRIMARY = (
    ROOT
    / "05_ASSEMBLY_BINNING_QC_DREP"
    / "quality"
    / "CHECKM2_PRIMARY_RESULTS.tsv"
)
CROSSWALK = (
    ROOT
    / "05_ASSEMBLY_BINNING_QC_DREP"
    / "quality"
    / "CHECKM2_TO_DREP_CROSSWALK.tsv"
)

bins = pd.read_csv(PRIMARY, sep="\t")
drep = pd.read_csv(CROSSWALK, sep="\t")

required_bin_columns = {
    "source_sample",
    "source_run",
    "bin_id",
    "completeness_checkm2",
    "contamination_checkm2",
    "operational_category",
}
required_drep_columns = {
    "bin_id",
    "selected_by_initial_CheckM2",
    "dRep_winner",
}
assert required_bin_columns <= set(bins.columns)
assert required_drep_columns <= set(drep.columns)
assert len(bins) == 1408, f"expected 1,408 retained bins, found {len(bins)}"
assert bins["source_sample"].nunique() == 23
assert bins["bin_id"].is_unique
assert not bins["bin_id"].str.contains("DASToolUnbinned", case=False, na=False).any()

category_counts = bins["operational_category"].value_counts()
expected_counts = {"HQ_candidate": 56, "MQ": 561, "LQ": 791}
assert category_counts.to_dict() == expected_counts, category_counts.to_dict()

hq_bins = set(bins.loc[bins["operational_category"] == "HQ_candidate", "bin_id"])
assert set(drep["bin_id"]) == hq_bins
assert (drep["selected_by_initial_CheckM2"] == "YES").all()
assert len(drep) == 56
drep_winners = int((drep["dRep_winner"] == "YES").sum())
assert drep_winners == 29

category_label = {"HQ_candidate": "HQ", "MQ": "MQ", "LQ": "LQ"}
bins["quality_class"] = bins["operational_category"].map(category_label)
bins["sample_id"] = bins["source_sample"].map(mg_to_sid)

sample_order = sorted(bins["sample_id"].unique())
per_sample = (
    bins.pivot_table(
        index="sample_id",
        columns="quality_class",
        values="bin_id",
        aggfunc="count",
        fill_value=0,
    )
    .reindex(index=sample_order, columns=["HQ", "MQ", "LQ"], fill_value=0)
    .astype(int)
)
per_sample["total"] = per_sample.sum(axis=1)

focus = per_sample.loc["S_24_04_16", ["HQ", "MQ", "LQ", "total"]].to_dict()
assert focus == {"HQ": 38, "MQ": 243, "LQ": 241, "total": 522}, focus
assert per_sample[["HQ", "MQ", "LQ"]].sum().to_dict() == {
    "HQ": 56,
    "MQ": 561,
    "LQ": 791,
}

c_hq = "#4CAF50"
c_hq_drep = "#2E7D32"
c_mq = "#FFB300"
c_lq = "#E53935"

fig = plt.figure(figsize=(16, 11))
grid = fig.add_gridspec(
    2,
    2,
    hspace=0.30,
    wspace=0.35,
    height_ratios=[1.0, 0.9],
)

# Panel A — authoritative CheckM2 class counts, with the 29 final dRep representatives visible.
ax_a = fig.add_subplot(grid[0, 0])
categories = [
    "HQ\n(≥90% comp,\n≤5% cont)",
    "MQ\n(≥50% comp,\n≤10% cont)",
    "LQ\n(below MQ)",
]
counts = [56, 561, 791]
bars = ax_a.bar(
    categories,
    counts,
    color=[c_hq, c_mq, c_lq],
    width=0.55,
    edgecolor="#333333",
    linewidth=0.5,
)
for bar, value in zip(bars, counts):
    ax_a.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 10,
        str(value),
        ha="center",
        fontweight="bold",
        fontsize=13,
    )
ax_a.bar(
    categories[0],
    drep_winners,
    color=c_hq_drep,
    width=0.55,
    edgecolor="#333333",
    linewidth=0.5,
)
ax_a.text(
    bars[0].get_x() + bars[0].get_width() / 2,
    drep_winners / 2,
    str(drep_winners),
    ha="center",
    va="center",
    color="white",
    fontweight="bold",
    fontsize=12,
)
legend_a = [
    mpatches.Patch(
        facecolor=c_hq_drep,
        edgecolor="#333333",
        label="HQ retained as dRep representative",
    ),
    mpatches.Patch(
        facecolor=c_hq,
        edgecolor="#333333",
        label="HQ not retained as representative",
    ),
    mpatches.Patch(facecolor=c_mq, edgecolor="#333333", label="MQ"),
    mpatches.Patch(facecolor=c_lq, edgecolor="#333333", label="LQ"),
]
ax_a.legend(handles=legend_a, loc="upper left", fontsize=9, framealpha=0.9)
ax_a.set_ylabel("Bin count", fontsize=12)
ax_a.set_title(
    "A  QC-filtered MAG classes and HQ retention into dRep",
    fontsize=11,
    fontweight="bold",
    loc="left",
)

# Panel B — all 1,408 retained CheckM2 bins; no simulated points.
ax_b = fig.add_subplot(grid[0, 1])
point_style = {
    "LQ": (c_lq, 0.30, 12, 2),
    "MQ": (c_mq, 0.40, 15, 3),
    "HQ": (c_hq, 0.70, 25, 4),
}
for quality_class in ["LQ", "MQ", "HQ"]:
    colour, alpha, size, zorder = point_style[quality_class]
    subset = bins[bins["quality_class"] == quality_class]
    ax_b.scatter(
        subset["contamination_checkm2"],
        subset["completeness_checkm2"],
        c=colour,
        s=size,
        alpha=alpha,
        label=quality_class,
        zorder=zorder,
    )
ax_b.axhline(50, color="grey", ls="--", lw=0.5, alpha=0.5)
ax_b.axhline(90, color="grey", ls="--", lw=0.5, alpha=0.5)
ax_b.axvline(5, color="grey", ls=":", lw=0.5, alpha=0.5)
ax_b.axvline(10, color="grey", ls=":", lw=0.5, alpha=0.5)
ax_b.set_xlim(0, 100)
ax_b.set_ylim(0, 100)
ax_b.set_xlabel("Estimated contamination (%)", fontsize=11)
ax_b.set_ylabel("Estimated completeness (%)", fontsize=11)
ax_b.legend(title="Quality class", loc="lower right", fontsize=9)
ax_b.set_title(
    "B  Completeness vs contamination across HQ/MQ/LQ bins",
    fontsize=11,
    fontweight="bold",
    loc="left",
)

# Panel C — exact per sample counts from the same 1,408-bin table.
ax_c = fig.add_subplot(grid[1, :])
x = np.arange(len(sample_order))
width = 0.25
bars_hq = ax_c.bar(
    x - width,
    per_sample["HQ"],
    width,
    color=c_hq,
    edgecolor="#333333",
    linewidth=0.3,
    label="HQ",
)
bars_mq = ax_c.bar(
    x,
    per_sample["MQ"],
    width,
    color=c_mq,
    edgecolor="#333333",
    linewidth=0.3,
    label="MQ",
)
bars_lq = ax_c.bar(
    x + width,
    per_sample["LQ"],
    width,
    color=c_lq,
    edgecolor="#333333",
    linewidth=0.3,
    label="LQ",
)
for group_index, bar_group in enumerate([bars_hq, bars_mq, bars_lq]):
    for bar in bar_group:
        value = int(bar.get_height())
        if value > 0:
            # Separate labels on adjacent, similarly tall bars without changing data.
            x_offset = (-3, 0, 3)[group_index] if value >= 200 else 0
            ax_c.annotate(
                str(value),
                xy=(bar.get_x() + bar.get_width() / 2, value),
                xytext=(x_offset, 2),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=5.5,
                color="#333333",
            )
ax_c.set_xticks(x)
ax_c.set_xticklabels(sample_order, rotation=90, ha="center", fontsize=8)
ax_c.set_ylabel("Bin count", fontsize=12)
ax_c.set_xlabel("Sample date (S_YY_MM_DD)", fontsize=12)
ax_c.legend(loc="upper right", fontsize=10)
ax_c.set_title(
    "C  Per-sample MAG recovery by quality class",
    fontsize=11,
    fontweight="bold",
    loc="left",
)

paths = save3(fig, OUT, "Fig_3.4_bin_recovery")

panel_a = pd.DataFrame(
    {
        "quality_class": ["HQ", "MQ", "LQ"],
        "CheckM2_bin_count": counts,
        "final_dRep_representative_subset": [drep_winners, 0, 0],
    }
)
panel_b = bins[
    [
        "sample_id",
        "source_sample",
        "source_run",
        "bin_id",
        "quality_class",
        "completeness_checkm2",
        "contamination_checkm2",
    ]
].sort_values(["sample_id", "quality_class", "bin_id"])
panel_c = per_sample.reset_index()

panel_a.to_csv(OUT / "Fig_3.4A_category_counts_PLOTTED_VALUES.tsv", sep="\t", index=False)
panel_b.to_csv(OUT / "Fig_3.4B_bin_quality_PLOTTED_VALUES.tsv", sep="\t", index=False)
panel_c.to_csv(OUT / "Fig_3.4C_per_sample_counts_PLOTTED_VALUES.tsv", sep="\t", index=False)

print(
    "Figure 3.4 outputs: 1,408 bins; HQ/MQ/LQ=56/561/791; "
    "dRep representatives=29; S_24_04_16=38/243/241 (522); "
    f"saved {paths['png'].name}"
)
