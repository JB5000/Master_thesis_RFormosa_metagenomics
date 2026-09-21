#!/usr/bin/env python3
"""Plot selected sumTraits phenotypes with annotation coverage made explicit.

Panel A shows the conditional positive fraction among robust assignments:
100 * consensus_true / (consensus_true + consensus_false).
Panel B shows robust annotation coverage:
100 * (consensus_true + consensus_false).
"""

from __future__ import annotations

from pathlib import Path
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

matplotlib.rcParams["svg.hashsalt"] = (
    "ria-formosa-sumtraits-selected-traits-final"
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "community_trait_annotations.tsv"
VALUES = ROOT / "values"
FIGURES = ROOT / "figures"

# Display label, exact sumTraits trait, exact positive feature.
# "oxidation in darkness: sulfide" was selected instead of thiosulfate
# oxidation because its robust annotation coverage is substantially higher.
TRAITS = [
    (
        "Reduction: sulfate",
        "reduction: sulfate",
        "reduction_sulfate.true",
    ),
    (
        "Oxidation in darkness: sulfide",
        "oxidation in darkness: sulfide",
        "oxidation_in_darkness_sulfide.true",
    ),
    (
        "Denitrification pathway",
        "denitrification pathway",
        "denitrification_pathway.true",
    ),
    (
        "Nitrogen fixation",
        "nitrogen fixation",
        "nitrogen_fixation.true",
    ),
    (
        "Growth: photoautotrophy",
        "growth: photoautotrophy",
        "growth_photoautotrophy.true",
    ),
]

FIGURE_TRAITS = {
    "reduction: sulfate",
    "oxidation in darkness: sulfide",
    "denitrification pathway",
    "nitrogen fixation",
    "growth: photoautotrophy",
}
ZSCORE_COLOUR_LIMIT = 3.0
FIGURE_DISPLAY_LABELS = {
    "reduction: sulfate": "Reduction:\nsulfate",
    "oxidation in darkness: sulfide": "Oxidation in darkness:\nsulfide",
    "denitrification pathway": "Denitrification\npathway",
    "nitrogen fixation": "Nitrogen fixation",
    "growth: photoautotrophy": "Growth:\nphotoautotrophy",
}


def parse_profile(column: str) -> tuple[str, int]:
    match = re.fullmatch(r"(S_\d{2}_\d{2}_\d{2})__rep([123])", column)
    if not match:
        raise ValueError(f"Unexpected profile column: {column}")
    return match.group(1), int(match.group(2))


def aggregate(
    values: pd.Series, profile_columns: list[str], sample_order: list[str]
) -> tuple[pd.Series, pd.Series]:
    long = pd.DataFrame(
        {
            "profile": profile_columns,
            "value": pd.to_numeric(values[profile_columns]).to_numpy(float),
        }
    )
    parsed = long["profile"].map(parse_profile)
    long["sample"] = parsed.map(lambda item: item[0])
    long["replicate"] = parsed.map(lambda item: item[1])
    replicate_counts = long.groupby("sample")["replicate"].nunique()
    if not replicate_counts.reindex(sample_order).eq(3).all():
        raise ValueError("Every sample must have three independent replicates")
    grouped = long.groupby("sample")["value"]
    return (
        grouped.mean().reindex(sample_order),
        grouped.std(ddof=1).reindex(sample_order),
    )


def rowwise_zscore(values: np.ndarray) -> np.ndarray:
    means = np.nanmean(values, axis=1, keepdims=True)
    standard_deviations = np.nanstd(values, axis=1, ddof=0, keepdims=True)
    if np.any(np.isclose(standard_deviations, 0)):
        raise ValueError("Cannot calculate a row-wise z-score for a constant row")
    return (values - means) / standard_deviations


def save_figure(fig: plt.Figure, stem: str) -> None:
    for suffix in ("png", "pdf", "svg"):
        metadata = None
        if suffix == "pdf":
            metadata = {
                "Creator": "Ria Formosa MSc reproducible figure script",
                "CreationDate": None,
                "ModDate": None,
            }
        elif suffix == "svg":
            metadata = {
                "Creator": "Ria Formosa MSc reproducible figure script",
                "Date": None,
            }
        fig.savefig(
            FIGURES / f"{stem}.{suffix}",
            dpi=300 if suffix == "png" else None,
            bbox_inches="tight",
            pad_inches=0.05,
            facecolor="white",
            metadata=metadata,
        )


def main() -> None:
    # A freshly extracted bundle does not contain generated-output folders.
    # Create both destinations before any TSV or figure is written.
    FIGURES.mkdir(parents=True, exist_ok=True)
    VALUES.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(SOURCE, sep="\t")
    profile_columns = list(frame.columns[3:])
    sample_order: list[str] = []
    for column in profile_columns:
        sample, _ = parse_profile(column)
        if sample not in sample_order:
            sample_order.append(sample)
    if len(sample_order) != 23 or len(profile_columns) != 69:
        raise ValueError(
            f"Expected 23 samples and 69 profiles; found "
            f"{len(sample_order)} and {len(profile_columns)}"
        )

    prevalence_records = []
    coverage_records = []
    diagnostic_records = []
    conditional_means = []
    conditional_standard_deviations = []
    robust_coverages = []

    for display, trait, positive_feature in TRAITS:
        selected = frame.loc[frame["trait"].eq(trait)].copy()
        if set(selected["summary_type"]) != {
            "consensus_true",
            "consensus_false",
            "no_majority",
            "unannotated",
            "unclassified",
        }:
            raise ValueError(f"Unexpected summary components for {trait}")
        selected = selected.set_index("summary_type")
        positive = selected.loc["consensus_true"]
        if positive["feature"] != positive_feature:
            raise ValueError(
                f"Positive feature mismatch for {trait}: {positive['feature']}"
            )

        components = selected.loc[
            [
                "consensus_true",
                "consensus_false",
                "no_majority",
                "unannotated",
                "unclassified",
            ],
            profile_columns,
        ].astype(float)
        component_sum = components.sum(axis=0)
        if not np.allclose(component_sum, 1.0, atol=2e-9):
            raise ValueError(
                f"Trait fractions do not sum to one for {trait}: "
                f"range={component_sum.min()}–{component_sum.max()}"
            )

        prevalence_percent = positive[profile_columns].astype(float) * 100.0
        prevalence_mean, prevalence_sd = aggregate(
            prevalence_percent, profile_columns, sample_order
        )

        # Robustly interpretable = robust consensus true or false.
        # Database annotated also includes lineages with no robust majority.
        robust_percent = (
            components.loc["consensus_true"]
            + components.loc["consensus_false"]
        ) * 100.0
        conditional_percent = (
            components.loc["consensus_true"]
            / (
                components.loc["consensus_true"]
                + components.loc["consensus_false"]
            )
            * 100.0
        )
        if not np.isfinite(conditional_percent).all():
            raise ValueError(f"Undefined conditional positive fraction for {trait}")
        database_annotated_percent = (
            robust_percent + components.loc["no_majority"] * 100.0
        )
        no_majority_percent = components.loc["no_majority"] * 100.0
        unannotated_percent = components.loc["unannotated"] * 100.0
        unclassified_percent = components.loc["unclassified"] * 100.0

        robust_mean, robust_sd = aggregate(
            robust_percent, profile_columns, sample_order
        )
        conditional_mean, conditional_sd = aggregate(
            conditional_percent, profile_columns, sample_order
        )
        conditional_mean_zscore = (
            conditional_mean - conditional_mean.mean()
        ) / conditional_mean.std(ddof=0)
        robust_mean_zscore = (
            robust_mean - robust_mean.mean()
        ) / robust_mean.std(ddof=0)
        db_mean, db_sd = aggregate(
            database_annotated_percent, profile_columns, sample_order
        )
        no_majority_mean, no_majority_sd = aggregate(
            no_majority_percent, profile_columns, sample_order
        )
        unannotated_mean, unannotated_sd = aggregate(
            unannotated_percent, profile_columns, sample_order
        )
        unclassified_mean, unclassified_sd = aggregate(
            unclassified_percent, profile_columns, sample_order
        )

        conditional_means.append(conditional_mean.to_numpy())
        conditional_standard_deviations.append(conditional_sd.to_numpy())
        robust_coverages.append(robust_mean.to_numpy())

        for sample in sample_order:
            prevalence_records.append(
                {
                    "display_trait": display,
                    "sumtraits_trait": trait,
                    "positive_feature": positive_feature,
                    "sample": sample,
                    "replicate_n": 3,
                    "included_in_main_figure": trait in FIGURE_TRAITS,
                    "inferred_prevalence_percent_mean": prevalence_mean[sample],
                    "inferred_prevalence_percent_sd": prevalence_sd[sample],
                    "conditional_positive_fraction_percent_mean": conditional_mean[
                        sample
                    ],
                    "conditional_positive_fraction_percent_sd": conditional_sd[
                        sample
                    ],
                    "conditional_positive_fraction_rowwise_zscore": (
                        conditional_mean_zscore[sample]
                    ),
                    "robust_interpretable_coverage_percent_mean": robust_mean[
                        sample
                    ],
                    "robust_interpretable_coverage_percent_sd": robust_sd[sample],
                    "robust_coverage_rowwise_zscore": robust_mean_zscore[sample],
                }
            )
            coverage_records.append(
                {
                    "display_trait": display,
                    "sumtraits_trait": trait,
                    "sample": sample,
                    "replicate_n": 3,
                    "database_annotated_percent_mean": db_mean[sample],
                    "database_annotated_percent_sd": db_sd[sample],
                    "robust_interpretable_percent_mean": robust_mean[sample],
                    "robust_interpretable_percent_sd": robust_sd[sample],
                    "no_robust_majority_percent_mean": no_majority_mean[sample],
                    "no_robust_majority_percent_sd": no_majority_sd[sample],
                    "unannotated_percent_mean": unannotated_mean[sample],
                    "unannotated_percent_sd": unannotated_sd[sample],
                    "unclassified_percent_mean": unclassified_mean[sample],
                    "unclassified_percent_sd": unclassified_sd[sample],
                }
            )

        raw_values = prevalence_percent.to_numpy(float)
        coverage_values = robust_percent.to_numpy(float)
        conditional_values = conditional_percent.to_numpy(float)
        raw_coverage_rho, raw_coverage_p = spearmanr(
            raw_values, coverage_values
        )
        sample_index = np.arange(len(sample_order), dtype=float)
        raw_time_rho, raw_time_p = spearmanr(
            sample_index, prevalence_mean.to_numpy(float)
        )
        conditional_time_rho, conditional_time_p = spearmanr(
            sample_index, conditional_mean.to_numpy(float)
        )
        between_sd = float(conditional_mean.std(ddof=1))
        mean_replicate_sd = float(conditional_sd.mean())
        signal_noise_ratio = (
            between_sd / mean_replicate_sd
            if mean_replicate_sd > 0
            else np.nan
        )
        pre_2025 = np.array([sample < "S_25" for sample in sample_order])
        post_2025 = ~pre_2025
        mean_coverage = float(coverage_values.mean())
        if mean_coverage < 1:
            interpretation = (
                "Not interpretable: extremely low robust annotation coverage"
            )
        elif (
            abs(conditional_time_rho) >= 0.5
            and conditional_time_p < 0.05
            and signal_noise_ratio >= 2
        ):
            interpretation = (
                "Exploratory conditioned temporal pattern remains"
            )
        else:
            interpretation = (
                "Raw temporal pattern does not remain after conditioning"
            )
        diagnostic_records.append(
            {
                "display_trait": display,
                "sumtraits_trait": trait,
                "mean_robust_coverage_percent": mean_coverage,
                "min_robust_coverage_percent": float(coverage_values.min()),
                "max_robust_coverage_percent": float(coverage_values.max()),
                "mean_conditional_positive_fraction_percent": float(
                    conditional_values.mean()
                ),
                "min_conditional_positive_fraction_percent": float(
                    conditional_values.min()
                ),
                "max_conditional_positive_fraction_percent": float(
                    conditional_values.max()
                ),
                "mean_replicate_sd_conditional_percent": mean_replicate_sd,
                "between_sample_sd_conditional_percent": between_sd,
                "between_to_within_sd_ratio": signal_noise_ratio,
                "profiles_with_consensus_false_gt_zero": int(
                    (components.loc["consensus_false"] > 0).sum()
                ),
                "raw_prevalence_vs_coverage_spearman_rho": raw_coverage_rho,
                "raw_prevalence_vs_coverage_spearman_p": raw_coverage_p,
                "sample_order_vs_raw_prevalence_spearman_rho": raw_time_rho,
                "sample_order_vs_raw_prevalence_spearman_p": raw_time_p,
                "sample_order_vs_conditional_fraction_spearman_rho": (
                    conditional_time_rho
                ),
                "sample_order_vs_conditional_fraction_spearman_p": (
                    conditional_time_p
                ),
                "pre_2025_conditional_fraction_percent_mean": float(
                    conditional_mean.to_numpy()[pre_2025].mean()
                ),
                "year_2025_conditional_fraction_percent_mean": float(
                    conditional_mean.to_numpy()[post_2025].mean()
                ),
                "pre_2025_robust_coverage_percent_mean": float(
                    robust_mean.to_numpy()[pre_2025].mean()
                ),
                "year_2025_robust_coverage_percent_mean": float(
                    robust_mean.to_numpy()[post_2025].mean()
                ),
                "interpretation": interpretation,
            }
        )

    conditional_array = np.asarray(conditional_means)
    conditional_sd_array = np.asarray(conditional_standard_deviations)
    coverage_array = np.asarray(robust_coverages)
    figure_indices = [
        index
        for index, (_, trait, _) in enumerate(TRAITS)
        if trait in FIGURE_TRAITS
    ]
    figure_traits = [TRAITS[index] for index in figure_indices]
    figure_conditional_array = conditional_array[figure_indices]
    figure_coverage_array = coverage_array[figure_indices]
    figure_conditional_zscore = rowwise_zscore(figure_conditional_array)

    plotted_values = pd.DataFrame(prevalence_records)
    plotted_values.to_csv(
        VALUES / "sumtraits_sediment_biogeochemistry_PLOTTED_VALUES.tsv",
        sep="\t",
        index=False,
        float_format="%.10g",
    )
    pd.DataFrame(coverage_records).to_csv(
        VALUES / "sumtraits_sediment_biogeochemistry_COVERAGE_COMPONENTS.tsv",
        sep="\t",
        index=False,
        float_format="%.10g",
    )
    pd.DataFrame(diagnostic_records).to_csv(
        VALUES / "sumtraits_sediment_biogeochemistry_TRAIT_DIAGNOSTIC.tsv",
        sep="\t",
        index=False,
        float_format="%.10g",
    )
    fig = plt.figure(figsize=(7.0, 3.9), dpi=300, layout="constrained")
    fig.get_layout_engine().set(
        w_pad=0.02,
        h_pad=0.02,
        hspace=0.06,
        rect=(0.0, 0.0, 1.0, 1.0),
    )
    grid = fig.add_gridspec(
        2,
        2,
        height_ratios=[0.14, 1.0],
        width_ratios=[1.0, 0.025],
    )
    title_ax = fig.add_subplot(grid[0, :])
    conditional_ax = fig.add_subplot(grid[1, 0])
    conditional_cax = fig.add_subplot(grid[1, 1])
    title_ax.axis("off")
    title_ax.text(
        0.5,
        0.55,
        "Relative temporal patterns in selected taxonomically inferred\n"
        "community phenotypes",
        ha="center",
        va="center",
        fontsize=10.5,
        fontweight="bold",
        transform=title_ax.transAxes,
    )

    conditional_image = conditional_ax.imshow(
        figure_conditional_zscore,
        aspect="auto",
        interpolation="none",
        cmap="RdBu_r",
        vmin=-ZSCORE_COLOUR_LIMIT,
        vmax=ZSCORE_COLOUR_LIMIT,
    )
    conditional_ax.set_yticks(
        range(len(figure_traits)),
        [FIGURE_DISPLAY_LABELS[item[1]] for item in figure_traits],
        fontsize=8,
    )
    conditional_ax.set_xticks(
        np.arange(-0.5, len(sample_order), 1), minor=True
    )
    conditional_ax.set_yticks(
        np.arange(-0.5, len(figure_traits), 1), minor=True
    )
    conditional_ax.grid(which="minor", color="white", linewidth=0.7)
    conditional_ax.tick_params(which="minor", length=0)
    conditional_ax.tick_params(axis="y", length=0)
    conditional_ax.set_xticks(range(len(sample_order)))
    conditional_ax.set_xticklabels(
        sample_order, rotation=90, ha="center", va="top", fontsize=7.5
    )
    conditional_ax.set_xlabel(
        "Sample date (S_YY_MM_DD)", fontsize=8, labelpad=6
    )
    conditional_colourbar = fig.colorbar(
        conditional_image, cax=conditional_cax
    )
    conditional_colourbar.set_label("Row-wise z-score", fontsize=7.5)
    conditional_colourbar.ax.tick_params(labelsize=7.5)

    save_figure(fig, "sumTraits_sediment_biogeochemistry_selected_traits")
    plt.close(fig)

    supplement = plt.figure(
        figsize=(7.0, 4.1), dpi=300, layout="constrained"
    )
    supplement.get_layout_engine().set(
        w_pad=0.02,
        h_pad=0.02,
        hspace=0.06,
        rect=(0.0, 0.0, 1.0, 1.0),
    )
    supplement_grid = supplement.add_gridspec(
        2,
        2,
        height_ratios=[0.14, 1.0],
        width_ratios=[1.0, 0.025],
    )
    supplement_title_ax = supplement.add_subplot(supplement_grid[0, :])
    supplement_ax = supplement.add_subplot(supplement_grid[1, 0])
    supplement_cax = supplement.add_subplot(supplement_grid[1, 1])
    supplement_title_ax.axis("off")
    supplement_title_ax.text(
        0.5,
        0.55,
        "Trait-specific robust annotation coverage",
        ha="center",
        va="center",
        fontsize=10.5,
        fontweight="bold",
        transform=supplement_title_ax.transAxes,
    )
    supplement_image = supplement_ax.imshow(
        figure_coverage_array,
        aspect="auto",
        interpolation="none",
        cmap="YlGnBu",
        vmin=0,
        vmax=35,
    )
    for row in range(figure_coverage_array.shape[0]):
        for column in range(figure_coverage_array.shape[1]):
            value = figure_coverage_array[row, column]
            supplement_ax.text(
                column,
                row,
                (
                    f"{value:.3f}"
                    if figure_traits[row][1] == "reduction: sulfate"
                    else f"{value:.1f}"
                ),
                ha="center",
                va="center",
                fontsize=6.5,
                color="white" if value > 24 else "black",
            )
    supplement_ax.set_yticks(
        range(len(figure_traits)),
        [FIGURE_DISPLAY_LABELS[item[1]] for item in figure_traits],
        fontsize=8,
    )
    supplement_ax.set_xticks(range(len(sample_order)))
    supplement_ax.set_xticklabels(
        sample_order, rotation=90, ha="center", va="top", fontsize=7.5
    )
    supplement_ax.set_xticks(
        np.arange(-0.5, len(sample_order), 1), minor=True
    )
    supplement_ax.set_yticks(
        np.arange(-0.5, len(figure_traits), 1), minor=True
    )
    supplement_ax.grid(which="minor", color="white", linewidth=0.7)
    supplement_ax.tick_params(which="minor", length=0)
    supplement_ax.tick_params(axis="y", length=0)
    supplement_ax.set_xlabel(
        "Sample date (S_YY_MM_DD)", fontsize=8, labelpad=6
    )
    supplement_colourbar = supplement.colorbar(
        supplement_image, cax=supplement_cax
    )
    supplement_colourbar.set_ticks([0, 5, 10, 15, 20, 25, 30, 35])
    supplement_colourbar.set_label(
        "Coverage (% of complete profile)", fontsize=7.5
    )
    supplement_colourbar.ax.tick_params(labelsize=7.5)
    save_figure(
        supplement,
        "sumTraits_trait_specific_annotation_coverage_supplementary",
    )
    plt.close(supplement)

    print(
        "Generated selected-trait figure: "
        f"{len(figure_traits)} displayed traits, {len(TRAITS)} audited traits, "
        f"{len(sample_order)} samples, "
        "three replicates per sample."
    )
    for row, (display, _, _) in enumerate(TRAITS):
        print(
            f"{display}: mean robust coverage="
            f"{coverage_array[row].mean():.6g}%; mean conditional positive="
            f"{conditional_array[row].mean():.6g}%; "
            f"mean replicate SD={conditional_sd_array[row].mean():.6g}"
        )


if __name__ == "__main__":
    main()
