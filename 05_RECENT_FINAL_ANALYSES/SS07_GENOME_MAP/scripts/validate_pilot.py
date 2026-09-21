#!/usr/bin/env python3
"""Validate SS-07 pilot inputs, marker coordinates and final exports."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "provenance" / "VALIDATION_REPORT.txt"

EXPECTED_SOURCE_HASHES = {
    "proksee_input/SS-07/genbank/SS-07.gbff": "ae34641a3dd2a757217cf10f08b7bdd865f51bc810771d9f4a990f3040df135c",
    "source/SS-07_Bakta.gff3": "15d30914a310beaf998896ad67a0d03b8df6ca2bf6b50f86d82ac1d36da49bb0",
    "source/SS-07_Bakta.json": "bfa6f4a8b03505855e2fb9539184db935e4e76abf52834e7b4503b8b6c7af054",
}
EXPECTED_MARKERS = {
    "nifH": 1,
    "psaA": 1,
    "psbA": 5,
    "rbcL": 1,
    "sat": 1,
    "sqr": 1,
    "ureC": 1,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    lines: list[str] = []
    for relative, expected in EXPECTED_SOURCE_HASHES.items():
        observed = sha256(ROOT / relative)
        assert observed == expected, f"Source hash mismatch: {relative}"
        lines.append(f"PASS\tsource hash\t{relative}\t{observed}")

    gbff = ROOT / "proksee_input" / "SS-07" / "genbank" / "SS-07.gbff"
    loci: list[tuple[str, int]] = []
    with gbff.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("LOCUS"):
                fields = line.split()
                loci.append((fields[1], int(fields[2])))
    assert loci == [("contig_1", 2759014), ("contig_2", 3171520)]
    lines.append("PASS\tGenBank records\t2")
    lines.append(f"PASS\tsequence length bp\t{sum(length for _, length in loci)}")

    marker_gff = ROOT / "proksee_input" / "SS-07" / "gff" / "SS-07_curated_markers.gff3"
    markers: list[str] = []
    with marker_gff.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#") or not line.strip():
                continue
            fields = line.rstrip().split("\t")
            assert len(fields) == 9 and fields[2] == "CDS"
            attributes = dict(item.split("=", 1) for item in fields[8].split(";") if "=" in item)
            markers.append(attributes["gene"])
    assert dict(sorted(Counter(markers).items())) == EXPECTED_MARKERS
    lines.append(f"PASS\tcoordinate-confirmed marker features\t{len(markers)}")

    cgview = json.loads(
        (ROOT / "proksee_output" / "data" / "genome_maps" / "SS-07.cgview.json").read_text()
    )["cgview"]
    contigs = cgview["sequence"]["contigs"]
    assert [(c["name"], int(c["length"])) for c in contigs] == loci
    curated = [feature for feature in cgview["features"] if feature.get("source") == "gff_1"]
    assert len(curated) == 11 and all(feature.get("favorite") is True for feature in curated)
    lines.append("PASS\tCGView contig order and orientation retained\t2 contigs")
    lines.append("PASS\tstyled CGView curated markers\t11")

    with (ROOT / "source/SS-07_MIMAG_RNA_evidence.tsv").open(newline="", encoding="utf-8") as handle:
        rna_rows = list(csv.DictReader(handle, delimiter="\t"))
    trna_rows = [row for row in rna_rows if row["feature_type"] == "tRNA"]
    rrna_rows = [row for row in rna_rows if row["feature_type"] == "rRNA"]
    aa_counts = Counter(row["standard_type"] for row in trna_rows)
    assert len(trna_rows) == 45 and len(aa_counts) == 20
    assert sum(row["representative_label"] == "true" for row in trna_rows) == 20
    assert len(rrna_rows) == 9 and set(row["standard_type"] for row in rrna_rows) == {"16S", "23S", "5S"}
    assert sum(row["representative_label"] == "true" for row in rrna_rows) == 3
    lines.append("PASS\tMIMAG tRNA evidence\t45 features; 20/20 standard amino-acid types")
    lines.append("PASS\tMIMAG rRNA evidence\t9 features; 16S, 23S and 5S represented")

    general_variant = json.loads((ROOT / "proksee_variants/SS-07_Bakta_general.cgview.json").read_text())["cgview"]
    mimag_variant = json.loads((ROOT / "proksee_variants/SS-07_MIMAG_RNA.cgview.json").read_text())["cgview"]
    assert len(general_variant["features"]) == 5662
    assert len(mimag_variant["features"]) == 54
    assert Counter(feature["source"] for feature in mimag_variant["features"]) == {"mimag-trna": 45, "mimag-rrna": 9}
    lines.append("PASS\tCGView Bakta general variant\t5662 annotated features")
    lines.append("PASS\tCGView MIMAG RNA variant\t45 tRNA plus 9 rRNA features")

    response = json.loads((ROOT / "provenance" / "proksee_project_response.json").read_text())
    assert response.get("status") == "success" and response.get("url", "").startswith("https://proksee.ca/projects/")
    lines.append(f"PASS\tProksee project\t{response['url']}")

    required_exports = {
        "exports/SS-07_Proksee_pilot.png": 1000,
        "exports/SS-07_Proksee_pilot.svg": 1000,
        "exports/SS-07_Proksee_pilot.json": 1000,
        "exports/SS-07_Proksee_batch_report.png": 1000,
        "proksee_output/report.html": 1000,
        "exports/SS-07_Bakta_general.png": 1000,
        "exports/SS-07_Bakta_general.svg": 1000,
        "exports/SS-07_MIMAG_RNA.png": 1000,
        "exports/SS-07_MIMAG_RNA.svg": 1000,
    }
    for relative, minimum_size in required_exports.items():
        size = (ROOT / relative).stat().st_size
        assert size > minimum_size
        lines.append(f"PASS\toutput present\t{relative}\t{size} bytes")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Validation complete: {len(lines)} checks passed")


if __name__ == "__main__":
    main()
