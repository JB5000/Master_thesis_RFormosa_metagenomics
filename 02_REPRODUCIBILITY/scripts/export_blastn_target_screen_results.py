#!/usr/bin/env python3
"""Export the BLASTn result matrix and exact plotted-value matrices.

The result matrix contains the 20 reference targets used in the selected-reference BLASTn
screen and the 23 date-level mean RPM values (three equal-depth subsamples per
date).  It deliberately rejects any source table that does not contain exactly
the declared targets and complete target-by-date coverage.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "06_RESULT_TABLES"
SOURCE = ROOT / "05_METHODS_AND_VALIDATION" / "02_BLAST_VALIDATION" / "blast_sample_mean.tsv"
REFERENCE_MAPPING = TABLES / "data" / "blastn_target_reference_mapping_20_targets.tsv"
TARGETS = [
    "Bonamia ostreae", "Escherichia coli", "Lactococcus garvieae", "Mycobacterium marinum",
    "Ostreavirus ostreidmalaco1 / Ostreid herpesvirus 1 / OsHV-1", "Perkinsus olseni",
    "Photobacterium damselae", "Photobacterium damselae subsp. piscicida", "Pseudo-nitzschia",
    "Salmonella enterica", "Tenacibaculum maritimum", "Tenacibaculum soleae", "Vibrio aestuarianus",
    "Vibrio alginolyticus", "Vibrio anguillarum", "Vibrio cholerae", "Vibrio harveyi",
    "Vibrio parahaemolyticus", "Vibrio tapetis", "Vibrio vulnificus",
]


def main() -> None:
    d = pd.read_csv(SOURCE, sep="\t")
    required = {"sample", "target", "mean_hits", "mean_rpm"}
    assert required.issubset(d.columns), f"Missing source columns: {required - set(d.columns)}"
    observed = set(d["target"])
    assert observed == set(TARGETS), f"Expected 20 BLASTn targets; found {len(observed)}"
    samples = sorted(d["sample"].unique())
    # The upstream aggregator records target/date rows only when a hit exists.
    # Missing target/date combinations therefore denote zero BLASTn hits and are
    # made explicit as 0 RPM, exactly as in the Supplementary Figure S2 script.
    rpm = d.pivot(index="target", columns="sample", values="mean_rpm").reindex(index=TARGETS, columns=samples)
    zero_filled = int(rpm.isna().sum().sum())
    rpm = rpm.fillna(0.0)
    assert rpm.shape == (20, 23) and not rpm.isna().any().any(), f"Incomplete matrix: {rpm.shape}"
    z = rpm.sub(rpm.mean(axis=1), axis=0).div(rpm.std(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    (TABLES / "data").mkdir(parents=True, exist_ok=True)
    (TABLES / "figure_plotted_values").mkdir(parents=True, exist_ok=True)
    rpm.round(3).to_csv(TABLES / "data" / "blastn_target_screen_RPM_20_targets.tsv", sep="\t")
    rpm.round(3).to_csv(TABLES / "figure_plotted_values" / "Fig_S2_blastn_target_screen_RAW_RPM.tsv", sep="\t")
    z.round(4).to_csv(TABLES / "figure_plotted_values" / "Fig_S2_blastn_target_screen_ZSCORES.tsv", sep="\t")
    refs = pd.read_csv(REFERENCE_MAPPING, sep="\t")
    refs = refs.loc[refs["included_as_reference"].astype(str).str.upper().eq("YES")].copy()
    assert len(refs) == 20 and set(refs["target_name"]) == set(TARGETS), "Reference mapping is not the 20-target BLASTn set"
    refs = refs.set_index("target_name").loc[TARGETS].reset_index()
    refs.to_csv(TABLES / "data" / "blastn_target_reference_mapping_20_targets.tsv", sep="\t", index=False)
    print(f"Exported BLASTn target matrix: {rpm.shape[0]} targets × {rpm.shape[1]} sampling dates from {SOURCE.name}; {zero_filled} no-hit cells written as 0 RPM")


if __name__ == "__main__":
    main()
