#!/usr/bin/env python3
"""Percent recovery of full-depth genus richness across read subsamples."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


PROJECT = Path(__file__).resolve().parents[1]
BASELINE = PROJECT / "tables/full_depth_genus_baseline_23.tsv"
ALL_REPEATS = PROJECT / "tables/rarefaction_percent_full_depth_genus_all_repeats.tsv"
VALUES_DIR = PROJECT / "tables"
FIGURE_DIR = PROJECT / "figures"
PROVENANCE_DIR = PROJECT / "provenance"

DEPTHS = (1000, 5000, 10000, 25000, 50000, 100000, 250000, 315147)
SELECTED_DEPTH = DEPTHS[-1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def save_figure(fig: plt.Figure, stem: str) -> dict[str, str]:
    paths = {}
    for suffix in ("png", "pdf", "svg"):
        path = FIGURE_DIR / f"{stem}.{suffix}"
        kwargs = {"bbox_inches": "tight"}
        if suffix == "png":
            kwargs["dpi"] = 450
        fig.savefig(path, **kwargs)
        paths[suffix] = str(path)
    return paths


def main() -> None:
    VALUES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    PROVENANCE_DIR.mkdir(parents=True, exist_ok=True)

    baseline_rows = read_tsv(BASELINE)
    repeat_rows = read_tsv(ALL_REPEATS)
    if len(baseline_rows) != 23:
        raise RuntimeError(f"Expected 23 full-depth baselines, found {len(baseline_rows)}")
    if len(repeat_rows) != 552:
        raise RuntimeError(f"Expected 552 rarefaction observations, found {len(repeat_rows)}")

    baseline = {}
    for row in baseline_rows:
        sample = row["date_tag"]
        if sample in baseline:
            raise RuntimeError(f"Duplicate full-depth baseline for {sample}")
        richness = int(row["raw_richness_genus"])
        total_reads = int(float(row["raw_total_reads"]))
        if richness <= 0 or total_reads <= 0:
            raise RuntimeError(f"Invalid full-depth baseline for {sample}")
        baseline[sample] = {
            "richness": richness,
            "total_reads": total_reads,
            "legacy_endpoint_mean": float(row["eqdepth_richness_mean"]),
            "legacy_endpoint_sd": float(row["eqdepth_richness_sd"]),
        }

    repeat_samples = {row["sample"] for row in repeat_rows}
    if repeat_samples != set(baseline):
        raise RuntimeError(
            f"Sample mismatch: rarefaction-only={sorted(repeat_samples-set(baseline))}; "
            f"baseline-only={sorted(set(baseline)-repeat_samples)}"
        )

    enriched_rows = []
    grouped = defaultdict(list)
    for row in repeat_rows:
        sample = row["sample"]
        depth = int(row["requested_depth"])
        repeat = int(row["repeat"])
        observed = int(row["observed_genera"])
        full_richness = baseline[sample]["richness"]
        percent = 100.0 * observed / full_richness
        enriched = {
            "sample": sample,
            "requested_depth": depth,
            "repeat": repeat,
            "seed": row["seed"],
            "source": row["source"],
            "observed_genera": observed,
            "full_depth_richness_genus_100pct": full_richness,
            "full_depth_processed_reads": baseline[sample]["total_reads"],
            "percent_full_depth_genera_recovered": f"{percent:.12g}",
            "rarefaction_report": row.get("rarefaction_report", row.get("report", "")),
            "rarefaction_report_sha256": row.get(
                "rarefaction_report_sha256", row.get("report_sha256", "")
            ),
        }
        enriched_rows.append(enriched)
        grouped[(sample, depth)].append(percent)

    if set(depth for _, depth in grouped) != set(DEPTHS):
        raise RuntimeError("Rarefaction depths do not match the expected eight depths")
    bad_groups = {key: len(vals) for key, vals in grouped.items() if len(vals) != 3}
    if bad_groups:
        raise RuntimeError(f"Expected three replicates per sample-depth: {bad_groups}")

    summary_rows = []
    summary_lookup = {}
    endpoint_mismatches = []
    for sample in sorted(baseline):
        for depth in DEPTHS:
            values = grouped[(sample, depth)]
            observed_values = [
                int(row["observed_genera"])
                for row in repeat_rows
                if row["sample"] == sample and int(row["requested_depth"]) == depth
            ]
            mean_observed = statistics.mean(observed_values)
            sd_observed = statistics.stdev(observed_values)
            mean_percent = statistics.mean(values)
            sd_percent = statistics.stdev(values)
            summary = {
                "sample": sample,
                "requested_depth": depth,
                "replicates": 3,
                "mean_observed_genera": f"{mean_observed:.12g}",
                "sd_observed_genera": f"{sd_observed:.12g}",
                "full_depth_richness_genus_100pct": baseline[sample]["richness"],
                "full_depth_processed_reads": baseline[sample]["total_reads"],
                "mean_percent_full_depth_genera_recovered": f"{mean_percent:.12g}",
                "sd_percent_full_depth_genera_recovered": f"{sd_percent:.12g}",
            }
            summary_rows.append(summary)
            summary_lookup[(sample, depth)] = (mean_percent, sd_percent)
            if depth == 315147 and not math.isclose(
                mean_observed,
                baseline[sample]["legacy_endpoint_mean"],
                rel_tol=0.0,
                abs_tol=1e-9,
            ):
                endpoint_mismatches.append(
                    {
                        "sample": sample,
                        "current": mean_observed,
                        "legacy": baseline[sample]["legacy_endpoint_mean"],
                    }
                )
    if endpoint_mismatches:
        raise RuntimeError(f"Legacy endpoint mismatch: {endpoint_mismatches}")

    overall_rows = []
    for depth in DEPTHS:
        sample_means = [summary_lookup[(sample, depth)][0] for sample in sorted(baseline)]
        overall_rows.append(
            {
                "requested_depth": depth,
                "samples": 23,
                "replicates_per_sample": 3,
                "mean_percent_full_depth_genera_recovered": f"{statistics.mean(sample_means):.12g}",
                "sd_across_sample_means": f"{statistics.stdev(sample_means):.12g}",
                "median_percent_full_depth_genera_recovered": f"{statistics.median(sample_means):.12g}",
                "min_percent_full_depth_genera_recovered": f"{min(sample_means):.12g}",
                "max_percent_full_depth_genera_recovered": f"{max(sample_means):.12g}",
            }
        )

    all_path = VALUES_DIR / "rarefaction_percent_full_depth_genus_all_repeats.tsv"
    sample_path = VALUES_DIR / "rarefaction_percent_full_depth_genus_by_sample_depth.tsv"
    overall_path = VALUES_DIR / "rarefaction_percent_full_depth_genus_overall.tsv"
    write_tsv(all_path, enriched_rows, list(enriched_rows[0]))
    write_tsv(sample_path, summary_rows, list(summary_rows[0]))
    write_tsv(overall_path, overall_rows, list(overall_rows[0]))

    samples = sorted(baseline)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 10,
            "axes.labelsize": 12,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 9,
        }
    )

    max_percent = max(
        float(row["percent_full_depth_genera_recovered"]) for row in enriched_rows
    )
    ymax = max(105.0, math.ceil((max_percent + 2.0) / 5.0) * 5.0)

    fig, axes = plt.subplots(5, 5, figsize=(15.8, 16.3), sharex=True, sharey=True)
    axes_flat = axes.ravel()
    line_handle = band_handle = baseline_handle = None
    for index, sample in enumerate(samples):
        ax = axes_flat[index]
        means = np.array([summary_lookup[(sample, depth)][0] for depth in DEPTHS])
        sds = np.array([summary_lookup[(sample, depth)][1] for depth in DEPTHS])
        line_handle = ax.plot(
            DEPTHS, means, color="#1769aa", marker="o", markersize=3.5, linewidth=1.7
        )[0]
        band_handle = ax.fill_between(
            DEPTHS,
            np.maximum(0.0, means - sds),
            np.minimum(ymax, means + sds),
            color="#90caf9",
            alpha=0.38,
            linewidth=0,
        )
        baseline_handle = ax.scatter(
            [baseline[sample]["total_reads"]],
            [100.0],
            marker="D",
            s=24,
            color="#c62828",
            edgecolor="white",
            linewidth=0.4,
            zorder=5,
        )
        ax.axhline(100.0, color="#555555", linestyle="--", linewidth=0.8)
        ax.set_ylim(0.0, ymax)
        ax.grid(True, alpha=0.20, linewidth=0.6)
        ax.set_title(sample)
    for ax in axes_flat[len(samples) :]:
        ax.axis("off")
    fig.supxlabel("Subsampled reads", y=0.035)
    fig.supylabel("Full-depth genera recovered (%)", x=0.025)
    fig.legend(
        [line_handle, band_handle, baseline_handle],
        ["Mean of three subsamples", "± SD", "Full-depth profile (100%)"],
        loc="upper center",
        ncol=3,
        frameon=False,
        bbox_to_anchor=(0.5, 0.995),
    )
    fig.subplots_adjust(left=0.07, right=0.99, top=0.965, bottom=0.07, wspace=0.20, hspace=0.32)
    facet_paths = save_figure(fig, "rarefaction_percent_full_depth_genus_all23")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    for sample in samples:
        sample_means = [summary_lookup[(sample, depth)][0] for depth in DEPTHS]
        ax.plot(DEPTHS, sample_means, color="#9e9e9e", alpha=0.42, linewidth=0.8)
    overall_means = np.array(
        [
            float(row["mean_percent_full_depth_genera_recovered"])
            for row in overall_rows
        ]
    )
    overall_sds = np.array(
        [float(row["sd_across_sample_means"]) for row in overall_rows]
    )
    ax.fill_between(
        DEPTHS,
        np.maximum(0.0, overall_means - overall_sds),
        np.minimum(ymax, overall_means + overall_sds),
        color="#90caf9",
        alpha=0.38,
        linewidth=0,
        label="± SD across samples",
    )
    ax.plot(
        DEPTHS,
        overall_means,
        color="#0d47a1",
        marker="o",
        linewidth=2.3,
        markersize=5,
        label="Mean across 23 samples",
    )
    ax.axvline(
        SELECTED_DEPTH,
        color="#455a64",
        linestyle=":",
        linewidth=1.1,
        label=f"Selected depth ({SELECTED_DEPTH:,} reads)",
    )
    ax.axhline(
        100.0,
        color="#c62828",
        linestyle="--",
        linewidth=1.1,
        label="Full-depth reference (100%)",
    )
    ax.set_ylim(0.0, ymax)
    ax.set_xlabel("Subsampled reads")
    ax.set_ylabel("Full-depth genus richness recovered (%)")
    ax.grid(True, alpha=0.22, linewidth=0.7)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    overall_paths = save_figure(fig, "rarefaction_percent_full_depth_genus_overall")
    plt.close(fig)

    provenance_record = {
        "status": "PASS",
        "rank": "genus",
        "full_depth_reference_definition": (
            "Observed genus richness derived from the original full-depth "
            "read-level KrakenUniq reports; 100% is sample-specific."
        ),
        "species_version_generated": False,
        "species_version_reason": (
            "The original full-depth species-richness denominator was not retained."
        ),
        "samples": 23,
        "depths": list(DEPTHS),
        "replicates_per_sample_depth": 3,
        "observations": len(enriched_rows),
        "sample_depth_groups": len(summary_rows),
        "legacy_315147_endpoint_mismatches": len(endpoint_mismatches),
        "baseline_source": str(BASELINE.relative_to(PROJECT)),
        "baseline_sha256": sha256(BASELINE),
        "rarefaction_source": str(ALL_REPEATS.relative_to(PROJECT)),
        "rarefaction_source_sha256": sha256(ALL_REPEATS),
        "outputs": {
            "all_repeats_tsv": str(all_path.relative_to(PROJECT)),
            "by_sample_depth_tsv": str(sample_path.relative_to(PROJECT)),
            "overall_tsv": str(overall_path.relative_to(PROJECT)),
            "facet_figure": {key: str(Path(value).relative_to(PROJECT)) for key, value in facet_paths.items()},
            "overall_figure": {key: str(Path(value).relative_to(PROJECT)) for key, value in overall_paths.items()},
        },
        "output_sha256": {
            str(path.relative_to(PROJECT)): sha256(path)
            for path in [
                all_path,
                sample_path,
                overall_path,
                *[Path(value) for value in facet_paths.values()],
                *[Path(value) for value in overall_paths.values()],
            ]
        },
        "maximum_observed_percent": max_percent,
        "observations_above_100_percent": sum(
            float(row["percent_full_depth_genera_recovered"]) > 100.0
            for row in enriched_rows
        ),
    }
    provenance_record_path = PROVENANCE_DIR / "percent_full_depth_genus_provenance.json"
    provenance_record_path.write_text(json.dumps(provenance_record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(provenance_record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
