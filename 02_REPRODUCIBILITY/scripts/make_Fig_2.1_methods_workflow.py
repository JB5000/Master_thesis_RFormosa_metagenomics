#!/usr/bin/env python3
"""Generate Figure 2.1, the overview of laboratory and analytical methods."""

from pathlib import Path
import os
import sys

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).parent))
from fig_style import save3


DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
COLOURS = {
    "input": "#d9d9d9",
    "wetlab": "#e8e8e8",
    "read": "#fdbf6f",
    "genome": "#a6cee3",
    "catalogue": "#8fce8f",
    "coassembly": "#66c2a5",
    "blast": "#cbaacb",
    "characterisation": "#c9dcef",
}
EDGE = "#3a3a3a"


def add_box(ax, x, y, width, height, text, colour, fontsize=10.2):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), width, height,
            boxstyle="round,pad=0.55,rounding_size=2.2",
            linewidth=1.4, edgecolor=EDGE, facecolor=colour, zorder=2,
        )
    )
    ax.text(
        x + width / 2, y + height / 2, text,
        ha="center", va="center", fontsize=fontsize, color="#111111", zorder=3,
    )
    return {
        "cx": x + width / 2,
        "cy": y + height / 2,
        "top": y + height,
        "bottom": y,
        "left": x,
        "right": x + width,
    }


def add_arrow(ax, start, end):
    ax.add_patch(
        FancyArrowPatch(
            start, end, arrowstyle="-|>", mutation_scale=14,
            linewidth=1.45, color=EDGE, shrinkA=0, shrinkB=0, zorder=1,
        )
    )


def add_elbow(ax, points):
    for start, end in zip(points[:-2], points[1:-1]):
        ax.plot(
            [start[0], end[0]], [start[1], end[1]],
            color=EDGE, linewidth=1.45, solid_capstyle="butt", zorder=1,
        )
    add_arrow(ax, points[-2], points[-1])


def main():
    fig, ax = plt.subplots(figsize=(13.2, 11.7))
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 163)
    ax.axis("off")

    sample = add_box(
        ax, 39, 152, 42, 8,
        "23 sediment samples\nOctober 2021–November 2025",
        COLOURS["input"], fontsize=10.5,
    )
    dna = add_box(ax, 43, 140, 34, 7, "DNA extraction", COLOURS["wetlab"])
    library = add_box(
        ax, 43, 128, 34, 7, "ONT library preparation", COLOURS["wetlab"]
    )
    sequencing = add_box(
        ax, 43, 116, 34, 7, "PromethION sequencing", COLOURS["input"]
    )
    dorado = add_box(
        ax, 41, 103, 38, 8,
        "Dorado basecalling and\ndemultiplexing", COLOURS["input"],
    )
    qc = add_box(
        ax, 41, 90, 38, 8,
        "Read quality control and filtering", COLOURS["input"], fontsize=9.8,
    )
    for upper, lower in zip(
        (sample, dna, library, sequencing, dorado),
        (dna, library, sequencing, dorado, qc),
    ):
        add_arrow(ax, (upper["cx"], upper["bottom"]), (lower["cx"], lower["top"]))

    ax.text(
        29, 84.5, "Genome-resolved analysis",
        ha="center", va="center", fontsize=11.5, color="#111111", zorder=4,
    )
    ax.text(
        91, 84.5, "Read-level context and targeted follow-up",
        ha="center", va="center", fontsize=10.8, color="#111111", zorder=4,
    )

    genome1 = add_box(
        ax, 10, 70, 38, 9,
        "Per-sample assembly\nFlye + metaMDBG", COLOURS["genome"],
    )
    genome2 = add_box(ax, 10, 57, 38, 8, "Binning + DAS Tool", COLOURS["genome"])
    genome3 = add_box(ax, 10, 44, 38, 8, "CheckM2 + GUNC", COLOURS["genome"])
    genome4 = add_box(
        ax, 10, 31, 38, 8,
        "dRep dereplication\n95% secondary ANI", COLOURS["catalogue"],
    )
    genome5 = add_box(
        ax, 8, 15, 42, 11,
        "MAG characterisation\nGTDB-Tk taxonomy · minimap2 recruitment\nfunctional annotation",
        COLOURS["characterisation"], fontsize=9.6,
    )

    read1 = add_box(
        ax, 72, 70, 38, 9,
        "KrakenUniq\nFull-depth profiles", COLOURS["read"],
    )
    read2 = add_box(
        ax, 72, 55, 38, 10,
        "Equal-depth subsampling\n3 subsets per sampling date",
        COLOURS["read"], fontsize=9.6,
    )
    read3 = add_box(
        ax, 72, 41, 38, 9,
        "Bray–Curtis dissimilarity\nand PCoA", COLOURS["read"],
    )
    read4 = add_box(
        ax, 72, 27, 38, 9, "PERMANOVA and PERMDISP", COLOURS["read"]
    )

    split_y = 81.5
    add_elbow(ax, [
        (qc["cx"], qc["bottom"]), (qc["cx"], split_y),
        (genome1["cx"], split_y), (genome1["cx"], genome1["top"]),
    ])
    add_elbow(ax, [
        (qc["cx"], qc["bottom"]), (qc["cx"], split_y),
        (read1["cx"], split_y), (read1["cx"], read1["top"]),
    ])
    for upper, lower in zip(
        (genome1, genome2, genome3, genome4),
        (genome2, genome3, genome4, genome5),
    ):
        add_arrow(ax, (upper["cx"], upper["bottom"]), (lower["cx"], lower["top"]))
    for upper, lower in zip((read1, read2, read3), (read2, read3, read4)):
        add_arrow(ax, (upper["cx"], upper["bottom"]), (lower["cx"], lower["top"]))

    blast = add_box(
        ax, 51, 55.5, 18, 9,
        "Selected-reference\nBLASTn screen", COLOURS["blast"], fontsize=8.8,
    )
    add_arrow(ax, (read2["left"], read2["cy"]), (blast["right"], blast["cy"]))

    coassembly = add_box(
        ax, 72, 1.5, 38, 8, "Targeted coassembly",
        COLOURS["coassembly"], fontsize=9.8,
    )
    add_elbow(ax, [
        (read3["right"], read3["cy"]), (115, read3["cy"]),
        (115, 12), (coassembly["cx"], 12),
        (coassembly["cx"], coassembly["top"]),
    ])

    legend_items = [
        ("Sampling / sequencing", COLOURS["input"]),
        ("Laboratory preparation", COLOURS["wetlab"]),
        ("Read-level analysis", COLOURS["read"]),
        ("Genome-resolved analysis", COLOURS["genome"]),
        ("Dereplication", COLOURS["catalogue"]),
        ("Targeted follow-up", COLOURS["coassembly"]),
    ]
    handles = [
        Line2D(
            [0], [0], marker="s", color="none", markerfacecolor=colour,
            markeredgecolor=EDGE, markersize=10, label=label,
        )
        for label, colour in legend_items
    ]
    fig.legend(
        handles=handles, loc="lower center", ncol=3, fontsize=8.5,
        frameon=True, bbox_to_anchor=(0.5, 0.012),
    )
    fig.subplots_adjust(left=0.025, right=0.975, top=0.985, bottom=0.075)
    paths = save3(fig, OUT, "Fig_2.1_methods_workflow")
    print("saved", paths["png"])


if __name__ == "__main__":
    main()
