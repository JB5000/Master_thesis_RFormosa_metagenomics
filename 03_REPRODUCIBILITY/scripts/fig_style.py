#!/usr/bin/env python3
"""Shared visual style for the Ria Formosa MSc figure rebuild (FINAL_REBUILD_20260716).
One font family, >= 8 pt everywhere, colour-blind-friendly palettes, A4-landscape-safe sizing,
and a 3-format writer (PNG 600 dpi + vector PDF + SVG). No figure numbers / long captions in images."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt

# ---- one consistent font family, minimum 8 pt ----
mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8.5,
    "legend.title_fontsize": 9,
    "figure.dpi": 150,
    "savefig.dpi": 600,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "pdf.fonttype": 42,   # embed as TrueType (editable text in vector output)
    "svg.fonttype": "none",
})

# ---- Okabe-Ito colour-blind-safe qualitative palette ----
OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9",
             "#D55E00", "#F0E442", "#000000", "#999999"]

# phylum -> CB-safe colour (fixed, reused across figures)
PHYLUM_COLORS = {
    "Bacteroidota":    "#E69F00",   # orange
    "Actinomycetota":  "#D55E00",   # vermillion
    "Cyanobacteriota": "#009E73",   # bluish green
    "Desulfobacterota":"#CC79A7",   # reddish purple
    "Pseudomonadota":  "#0072B2",   # blue
}
def phylum_color(p): return PHYLUM_COLORS.get(str(p).strip(), "#999999")

# ---- colormaps ----
ZSCORE_CMAP = "RdBu_r"        # diverging blue<->red (row z-scores, e.g. recruitment / S2)
SEQ_CMAP    = "cividis"       # sequential, colour-blind-safe (kept for reference)
# TRUE SEQUENTIAL blue(low) -> red(high) for COUNT heatmaps (monotonic luminosity, NO white centre;
# NOT a diverging map). Figures 3.7/3.9 normalise each displayed column independently from its minimum
# to its maximum, so colour intensity is comparable within a column but not between columns.
# No yellow (reserved for outlines).
from matplotlib.colors import LinearSegmentedColormap as _LSC
COUNT_CMAP = _LSC.from_list("blue_red_seq", [
    "#eaf1fb",  # very light blue (low)
    "#a9cbe8",
    "#5d94c8",
    "#3f6fae",
    "#7d5aa0",  # blue->purple transition (no white)
    "#c0392b",
    "#7d0a12",  # dark red (high)
])
YELLOW = "#FFFF00"           # fluorescent-yellow source/input cell outline (~2.5-3 pt)

# A4 landscape usable area with 2.5 cm margins ~= 9.65 x 6.30 in; "full-page" figures use ~11.0 x 7.2
A4_LAND = (9.6, 6.3)
FULLPAGE_LAND = (11.0, 7.2)

def mg_to_sid(mg):
    """MG240905 -> S_24_09_05 (source_sample id -> full sample id)."""
    d = str(mg).strip().replace("MG", "")
    return f"S_{d[0:2]}_{d[2:4]}_{d[4:6]}" if len(d) == 6 and d.isdigit() else str(mg)

def save3(fig, outdir, name, pad=0.03):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for ext in ("png", "pdf", "svg"):
        p = outdir / f"{name}.{ext}"
        fig.savefig(p, bbox_inches="tight", pad_inches=pad)
        paths[ext] = p
    plt.close(fig)
    return paths
