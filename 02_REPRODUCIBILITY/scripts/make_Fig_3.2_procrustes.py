#!/usr/bin/env python3
"""Fig 3.2 — full-depth (non-subsampled) vs equal-depth Bray-Curtis ordinations, Procrustes-aligned.
Scientific values preserved (PC1=50.9%, PC2=14.2%, Procrustes correlation ~0.995). Fonts/line weights
harmonised with the other figures. No statistical textbox. Reproduced from the source 5-axis coordinates."""
from pathlib import Path
import os
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import sys; sys.path.insert(0, str(Path(__file__).parent))
from fig_style import OKABE_ITO, save3


SOURCE = Path(__file__).resolve().parents[1] / "figure_sources"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "regenerated_output"
OUT = Path(os.environ.get("RIA_FIGURE_OUTPUT", DEFAULT_OUT))
OUT.mkdir(parents=True, exist_ok=True)
INP = SOURCE/"pcoa"
PC = ["PC1","PC2","PC3","PC4","PC5"]


def procrustes_numpy(reference, target):
    """SciPy-compatible unit-norm Procrustes alignment using only NumPy."""
    reference = np.asarray(reference, dtype=float)
    target = np.asarray(target, dtype=float)
    ref0 = reference - reference.mean(axis=0)
    target0 = target - target.mean(axis=0)
    ref_std = ref0 / np.linalg.norm(ref0)
    target_std = target0 / np.linalg.norm(target0)
    u, singular_values, vt = np.linalg.svd(ref_std.T @ target_std)
    rotation = u @ vt
    aligned_target = target_std @ rotation.T * singular_values.sum()
    disparity = np.sum((ref_std - aligned_target) ** 2)
    return ref_std, aligned_target, disparity

meta = pd.read_csv(INP/"sample_classification_metrics.tsv", sep="\t").set_index("sample")
f6 = pd.read_csv(INP/"fig6_pcoa_coordinates.tsv", sep="\t")
def coords(ds):
    d=f6[f6["dataset"]==ds].set_index("date_tag")[PC]; return d.reindex([s for s in meta.index if s in d.index])
raw5, eq5 = coords("raw_bray"), coords("eqdepth_bray")
order=[s for s in eq5.index if s in raw5.index]; eq5,raw5=eq5.loc[order],raw5.loc[order]
# Authoritative all-dimension explained-variance values retained by the source analysis.
pc1v, pc2v = 50.9, 14.2
eqM,rawM=eq5.values.astype(float),raw5.values.astype(float)
_,aligned_raw_std,disp=procrustes_numpy(eqM,rawM); proc=float(np.sqrt(max(0,1-disp)))
mu=eqM.mean(0); nrm=np.linalg.norm(eqM-mu); ar=aligned_raw_std*nrm+mu

fig, ax = plt.subplots(figsize=(8.6, 6.6))
for i in range(len(order)):
    ax.plot([ar[i,0],eqM[i,0]],[ar[i,1],eqM[i,1]], color="#b0b0b0", lw=0.8, zorder=1)
ax.scatter(ar[:,0],ar[:,1], s=80, c=OKABE_ITO[0], edgecolors="black", linewidths=0.5,
           label="Full-depth profiles", zorder=4)
ax.scatter(eqM[:,0],eqM[:,1], s=80, c=OKABE_ITO[1], edgecolors="black", linewidths=0.5,
           label="Equal-depth mean profiles", zorder=5)
ax.set_xlabel(f"Equal-depth PCoA1 ({pc1v:.1f}%)", fontsize=10)
ax.set_ylabel(f"Equal-depth PCoA2 ({pc2v:.1f}%)", fontsize=10)
ax.legend(fontsize=8.5, loc="upper right")
for sp in ("top","right"): ax.spines[sp].set_visible(False)
fig.tight_layout()
paths=save3(fig, OUT, "Fig_3.2_fulldepth_vs_eqdepth")
pd.DataFrame({"sample":order,"eq_PC1":eqM[:,0],"eq_PC2":eqM[:,1],
              "fulldepth_aligned_PC1":ar[:,0],"fulldepth_aligned_PC2":ar[:,1]}).to_csv(
    OUT/"Fig_3.2_PLOTTED_VALUES.tsv", sep="\t", index=False)
print(f"PC1={pc1v:.1f}% PC2={pc2v:.1f}% Procrustes={proc:.3f}")
