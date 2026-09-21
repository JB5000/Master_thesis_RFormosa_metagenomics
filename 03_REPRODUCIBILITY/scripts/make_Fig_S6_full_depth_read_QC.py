#!/usr/bin/env python3
"""Regenerate full-depth read QC figure from the retained 23-library matrix.

The exact plotted values are in the bundle. The original TaxProfiler/nanoq
outputs, parameters and software versions are retained under
04_CORE_ANALYSIS_DATA/03_READS_AND_QC/taxprofiler_20260430/.
"""
from pathlib import Path
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from fig_style import save3


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "03_REPRODUCIBILITY" / "figure_sources" / "sequencing" / "S1_read_totals_source_fig2_sequencing_effort_qc_metrics.tsv"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", ROOT / "03_REPRODUCIBILITY" / "regenerated_output"))
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    df = pd.read_csv(SOURCE, sep="\t").sort_values("date_tag")
    x = range(len(df))
    labels = df["date_tag"].str.replace("S_", "", regex=False)

    fig, axes = plt.subplots(3, 1, figsize=(13.2, 10.0), sharex=True)
    fig.suptitle("Initial sequencing and read quality metrics across 23 full-depth profiles", y=0.995, fontsize=15)

    axes[0].plot(x, df["raw_reads_total"], "o-", color="#9aa7b4", mfc="white", lw=2, label="Raw reads")
    axes[0].plot(x, df["qc_reads"], "o-", color="#2878b5", lw=2, label="Reads retained after QC")
    axes[0].set_yscale("log")
    axes[0].set_ylabel("Number of reads\n(log scale)")
    axes[0].set_title("A   Read counts", loc="center")
    axes[0].legend(frameon=False, ncol=2, loc="upper left")

    axes[1].plot(x, df["raw_bases_total"] / 1e9, "o-", color="#9aa7b4", mfc="white", lw=2, label="Raw bases")
    axes[1].plot(x, df["qc_bases"] / 1e9, "o-", color="#2878b5", lw=2, label="Bases retained after QC")
    axes[1].set_yscale("log")
    axes[1].set_ylabel("Total bases (Gb)\n(log scale)")
    axes[1].set_title("B   Sequence yield", loc="center")
    axes[1].legend(frameon=False, ncol=2, loc="upper left")

    axes[2].plot(x, df["read_n50"] / 1000, "o-", color="#d55e4b", lw=2, label="Read N50")
    axes[2].plot(x, df["read_mean_len"] / 1000, "s-", color="#2878b5", lw=2, label="Mean read length")
    axes[2].plot(x, df["read_median_len"] / 1000, "^-", color="#4c9f62", lw=2, label="Median read length")
    axes[2].set_ylabel("Read length (kb)")
    axes[2].set_title("C   Read-length metrics", loc="center")
    axes[2].legend(frameon=False, ncol=3, loc="upper right")

    for ax in axes:
        ax.grid(axis="y", alpha=0.25)
        ax.spines[["top", "right"]].set_visible(False)
    axes[2].set_xticks(list(x))
    axes[2].set_xticklabels(labels, rotation=90)
    axes[2].set_xlabel("Sample date (S_YY_MM_DD)")
    fig.tight_layout()
    save3(fig, OUT, "Fig_S6_full_depth_read_QC")
    print(f"Wrote Figure S6 formats to {OUT}")


if __name__ == "__main__":
    main()
