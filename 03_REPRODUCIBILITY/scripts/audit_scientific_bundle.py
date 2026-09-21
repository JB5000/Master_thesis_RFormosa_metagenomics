#!/usr/bin/env python3
"""Audit scientific assets, provenance links and reproducibility constraints."""
from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "ASSET_MANIFEST.tsv"
REPORT = ROOT / "BUNDLE_AUDIT.md"


def read_tsv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def check(check_id, passed, details):
    return check_id, "PASS" if passed else "FAIL", details


def paths(field):
    return [ROOT / item.strip() for item in field.split(";") if item.strip()]


def main():
    rows = []
    manifest = read_tsv(MANIFEST)
    required = {"asset_filename", "asset_type", "description", "source_data", "generation_script", "upstream_analysis", "status", "notes"}
    rows.append(check("MANIFEST-01", bool(manifest) and set(manifest[0]) == required, f"manifest records={len(manifest)}; required columns present={bool(manifest) and set(manifest[0]) == required}"))

    figures = sorted((ROOT / "figures").glob("*.png"))
    figure_rows = [row for row in manifest if row["asset_type"] == "final_figure"]
    figure_assets = {ROOT / row["asset_filename"] for row in figure_rows}
    rows.append(check("FIGURES-01", len(figures) == 24 and set(figures) == figure_assets, f"figure PNGs={len(figures)}; manifest figure records={len(figure_rows)}"))

    missing_sources = []
    missing_scripts = []
    for row in figure_rows:
        missing_sources.extend(str(path.relative_to(ROOT)) for path in paths(row["source_data"]) if not path.exists())
        missing_scripts.extend(str(path.relative_to(ROOT)) for path in paths(row["generation_script"]) if not path.exists())
    rows.append(check("PROVENANCE-01", not missing_sources and not missing_scripts, f"missing figure source data={missing_sources}; missing generation scripts={missing_scripts}"))

    retained_scripts = sorted({path for row in manifest for path in paths(row["generation_script"])})
    nonportable_input_assumptions = []
    for path in retained_scripts:
        script_text = path.read_text(encoding="utf-8", errors="ignore")
        portable_entrypoint = "Path(__file__).resolve()" in script_text or "argparse.ArgumentParser" in script_text
        cwd_relative = "Path('.')" in script_text or 'Path(".")' in script_text
        if not portable_entrypoint or cwd_relative:
            nonportable_input_assumptions.append(str(path.relative_to(ROOT)))
    rows.append(check("SCRIPTS-01", not nonportable_input_assumptions, f"retained scripts with non-portable input assumptions={nonportable_input_assumptions}"))

    sumtraits_script = ROOT / "05_RECENT_FINAL_ANALYSES" / "SUMTRAITS_SELECTED_PHENOTYPES" / "scripts" / "make_sumtraits_sediment_biogeochemistry_figure.py"
    sumtraits_text = sumtraits_script.read_text(encoding="utf-8")
    output_dirs_created = "FIGURES.mkdir(parents=True, exist_ok=True)" in sumtraits_text and "VALUES.mkdir(parents=True, exist_ok=True)" in sumtraits_text
    rows.append(check("SCRIPTS-02", output_dirs_created, "sumTraits figure and values directories are created before output is written"))

    tables = sorted((ROOT / "results_tables" / "data").glob("*.tsv"))
    table_rows = [row for row in manifest if row["asset_type"] == "result_table"]
    rows.append(check("TABLES-01", len(tables) == 9 and {ROOT / row["asset_filename"] for row in table_rows} == set(tables), f"result tables={len(tables)}; manifest table records={len(table_rows)}"))

    perkinsus = read_tsv(ROOT / "results_tables" / "data" / "perkinsus_olseni_blastn_RPM_by_date.tsv")
    peak = max(perkinsus, key=lambda row: float(row["Mean BLASTn-derived RPM"]))
    peak_ok = peak["Sample"] == "S_22_06_29" and abs(float(peak["Mean BLASTn-derived RPM"]) - 720.2988) < 0.0001 and abs(float(peak["SD BLASTn-derived RPM"]) - 23.9565) < 0.0001
    rows.append(check("SCIENCE-01", peak_ok, f"Perkinsus peak={peak['Sample']}; mean={peak['Mean BLASTn-derived RPM']}; SD={peak['SD BLASTn-derived RPM']}"))

    blast_matrix = read_tsv(ROOT / "results_tables" / "data" / "blastn_target_screen_RPM_20_targets.tsv")
    refs = read_tsv(ROOT / "results_tables" / "data" / "blastn_target_reference_mapping_20_targets.tsv")
    mag29 = read_tsv(ROOT / "results_tables" / "data" / "MAG29_taxonomy_quality.tsv")
    coa4 = read_tsv(ROOT / "results_tables" / "data" / "CoA4_taxonomy_quality.tsv")
    rows.append(check("SCIENCE-02", len(blast_matrix) == 20 and len(blast_matrix[0]) == 24 and len(refs) == 20 and all(row["included_as_reference"] == "YES" for row in refs) and len(mag29) == 29 and len(coa4) == 4, "BLASTn=20 targets × 23 dates; references=20; MAG29=29; CoA4=4"))

    qc = read_tsv(ROOT / "03_REPRODUCIBILITY" / "figure_sources" / "sequencing" / "S1_read_totals_source_fig2_sequencing_effort_qc_metrics.tsv")
    subsets = read_tsv(ROOT / "04_CORE_ANALYSIS_DATA" / "03_READS_AND_QC" / "subsampling_tasks_69seeds_PORTABLE.tsv")
    subset_depths = {row.get("target_reads", "") for row in subsets}
    dates = {row.get("sample_id", row.get("sample", "")) for row in subsets}
    rows.append(check("SCIENCE-03", len(qc) == 23 and len(subsets) == 69 and subset_depths == {"315147"} and len(dates) == 23, f"QC dates={len(qc)}; equal-depth subsets={len(subsets)}; reads/subset={sorted(subset_depths)}; dates={len(dates)}"))

    taxprofiler = ROOT / "04_CORE_ANALYSIS_DATA" / "03_READS_AND_QC" / "taxprofiler_20260430"
    multiqc = read_tsv(taxprofiler / "source_data" / "multiqc_nanoq.tsv")
    raw_manifest = read_tsv(taxprofiler / "raw_fastq_manifest.tsv")
    nanoq_stats = list((taxprofiler / "nanoq_stats").glob("*.stats"))
    kraken_reports = [path for path in (taxprofiler / "krakenuniq_reports").rglob("*") if path.is_file()]
    required_taxprofiler = [
        taxprofiler / "README.md",
        taxprofiler / "config" / "nextflow.config",
        taxprofiler / "database_manifest.tsv",
        taxprofiler / "pipeline_info" / "taxprofiler_parameters.json",
        taxprofiler / "pipeline_info" / "software_versions.yml",
        taxprofiler / "pipeline_info" / "execution_trace.tsv",
    ]
    taxprofiler_ok = (len(multiqc) == 23 and len(raw_manifest) == 23 and len(nanoq_stats) == 23 and len(kraken_reports) == 23 and all(path.exists() for path in required_taxprofiler))
    rows.append(check("QC-PROVENANCE-01", taxprofiler_ok, f"TaxProfiler inputs: MultiQC rows={len(multiqc)}; FASTQ manifest rows={len(raw_manifest)}; nanoq stats={len(nanoq_stats)}; KrakenUniq reports={len(kraken_reports)}"))

    by_prefix = {str(row["Sample"]).rsplit("_run", 1)[0]: row for row in multiqc}
    qc_mismatches = []
    for row in qc:
        prefix = "RFormosa_" + str(row["MG"])[2:]
        source = by_prefix.get(prefix)
        if not source:
            qc_mismatches.append(prefix)
            continue
        checks = {
            "qc_reads": "Number of reads",
            "qc_bases": "Number of bases",
            "read_n50": "N50 read length",
            "read_median_len": "Median read length",
            "read_mean_len": "Mean read length",
        }
        if any(abs(float(row[left]) - float(source[right])) > 0.001 for left, right in checks.items()):
            qc_mismatches.append(prefix)
    rows.append(check("QC-PROVENANCE-02", not qc_mismatches, f"Figure S6 post-QC values match original nanoq/MultiQC table; mismatches={qc_mismatches[:5]}"))

    s6_script = ROOT / "03_REPRODUCIBILITY" / "scripts" / "make_Fig_S6_full_depth_read_QC.py"
    s6_portable = s6_script.exists() and "Path(__file__).resolve()" in s6_script.read_text(encoding="utf-8") and "OUT.mkdir(parents=True, exist_ok=True)" in s6_script.read_text(encoding="utf-8")
    rows.append(check("SCRIPTS-03", s6_portable, "Figure S6 script resolves bundle-relative inputs and creates its output directory"))

    source = read_tsv(ROOT / "06_METHODS_AND_VALIDATION" / "17_BLAST_VALIDATION" / "blast_sample_mean.tsv")
    source_targets = {row["target"] for row in source}
    matrix_targets = {row[next(iter(row))] for row in blast_matrix}
    rows.append(check("VALUES-01", source_targets == matrix_targets and len(matrix_targets) == 20, "BLASTn source target set matches exported plotted-value matrix"))
    matrix_by_target = {row["target"]: row for row in blast_matrix}
    mismatches = []
    for row in source:
        observed = float(matrix_by_target[row["target"]][row["sample"]])
        if abs(observed - round(float(row["mean_rpm"]), 3)) > 0.00001:
            mismatches.append(f"{row['target']}:{row['sample']}")
    rows.append(check("VALUES-02", not mismatches, f"BLASTn exported RPM matrix matches rounded source values; mismatches={mismatches[:5]}"))

    active_kraken = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*") if path.is_file() and re.search(r"kraken2.*target|target.*kraken2", str(path.relative_to(ROOT)), re.I)]
    rows.append(check("CLEAN-01", not active_kraken, f"active Kraken2 target-screen files={active_kraken}"))

    # Source reports may retain original runtime paths in their headers. Only
    # executable/configuration material is required to be path-portable.
    text_suffixes = {".py", ".sh", ".sbatch", ".config", ".json", ".yaml", ".yml"}
    private = []
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in text_suffixes:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "/" + "home" + "/" + "jonyb" in text or "/" + "home" + "/" + "jbentes" in text:
                private.append(str(path.relative_to(ROOT)))
    rows.append(check("PORTABLE-01", not private, f"private absolute paths in active scripts/configuration={private}"))

    cache = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*") if path.name == "__pycache__" or path.suffix in {".pyc", ".tmp", ".temp"}]
    rows.append(check("CLEAN-02", not cache, f"cache/temp artifacts={cache}"))

    github_docs = [ROOT / "DATA_AVAILABILITY.md", ROOT / ".gitignore", ROOT / "03_REPRODUCIBILITY" / "requirements.txt"]
    raw_fastqs = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*.fastq*") if path.is_file()]
    rows.append(check("GITHUB-01", all(path.exists() for path in github_docs) and not raw_fastqs, f"GitHub documentation present={all(path.exists() for path in github_docs)}; bundled raw FASTQs={raw_fastqs}"))

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    rows.append(check("DOC-01", "ASSET_MANIFEST.tsv" in readme and "24 retained high-resolution PNG figure assets" in readme and "taxprofiler_20260430" in readme and "nine descriptive result tables" in readme, "README scope and counts match manifest"))

    overall = all(status == "PASS" for _, status, _ in rows)
    lines = ["# Bundle integrity and reproducibility audit", "", f"**Overall status: {'PASS' if overall else 'FAIL'}**", "", "This audit checks scientific assets and reproducibility only; it does not assess thesis wording or interpretation.", "", "| Check | Status | Details |", "|---|---:|---|"]
    lines.extend(f"| {name} | {status} | {details} |" for name, status, details in rows)
    lines.extend(["", "## Scope notes", "", "- Figure S6 has recovered TaxProfiler/nanoq provenance: input inventory, QC matrices, nanoq statistics, KrakenUniq reports, parameters, versions and execution trace are retained.", "- Proksee and Bandage assets retain their inputs and documented interactive procedures.", "- Large original FASTQs are not duplicated; their portable filename manifest is in `04_CORE_ANALYSIS_DATA/03_READS_AND_QC/taxprofiler_20260430/raw_fastq_manifest.tsv`."])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT} — {'PASS' if overall else 'FAIL'}")
    raise SystemExit(0 if overall else 1)


if __name__ == "__main__":
    main()
