#!/usr/bin/env python3
"""Build the SS-07 Proksee marker track from retained coordinate evidence."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
SOURCE_GFF = ROOT / "source" / "SS-07_Bakta.gff3"
EVIDENCE_TSV = ROOT / "source" / "SS-07_curated_marker_evidence.tsv"
OUTPUT_GFF = ROOT / "proksee_input" / "SS-07" / "gff" / "SS-07_curated_markers.gff3"

EXPECTED_COUNTS = {
    "nifH": 1,
    "psaA": 1,
    "psbA": 5,
    "rbcL": 1,
    "sat": 1,
    "sqr": 1,
    "ureC": 1,
}


def parse_attributes(value: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for item in value.rstrip().split(";"):
        if "=" in item:
            key, entry = item.split("=", 1)
            parsed[key] = entry
    return parsed


def encode(value: str) -> str:
    return quote(str(value), safe="._:-")


def main() -> None:
    with EVIDENCE_TSV.open(newline="", encoding="utf-8") as handle:
        evidence = list(csv.DictReader(handle, delimiter="\t"))

    by_locus = {row["locus_tag"]: row for row in evidence}
    if len(by_locus) != len(evidence):
        raise ValueError("Duplicate locus tags in marker evidence")

    coordinates: dict[str, tuple[str, str, str, str, str]] = {}
    sequence_regions: list[str] = []
    with SOURCE_GFF.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("##FASTA"):
                break
            if line.startswith("##sequence-region"):
                sequence_regions.append(line.rstrip())
                continue
            if line.startswith("#") or not line.strip():
                continue
            fields = line.rstrip().split("\t")
            if len(fields) != 9:
                continue
            attributes = parse_attributes(fields[8])
            locus_tag = attributes.get("locus_tag")
            if locus_tag not in by_locus:
                continue
            if locus_tag in coordinates:
                raise ValueError(f"Multiple coordinate features found for {locus_tag}")
            coordinates[locus_tag] = (fields[0], fields[3], fields[4], fields[6], fields[2])

    missing = sorted(set(by_locus) - set(coordinates))
    if missing:
        raise ValueError(f"Marker loci absent from Bakta GFF3: {', '.join(missing)}")

    observed_counts = Counter(row["display_marker"] for row in evidence)
    if dict(sorted(observed_counts.items())) != EXPECTED_COUNTS:
        raise ValueError(f"Unexpected marker counts: {dict(observed_counts)}")

    OUTPUT_GFF.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_GFF.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("##gff-version 3\n")
        for region in sequence_regions:
            handle.write(f"{region}\n")
        for index, row in enumerate(evidence, start=1):
            seqid, start, end, strand, original_type = coordinates[row["locus_tag"]]
            attributes = {
                "ID": f"SS-07_marker_{index:02d}",
                "Name": row["display_marker"],
                "gene": row["display_marker"],
                "locus_tag": row["locus_tag"],
                "KEGG_KO": row["KEGG_KO"],
                "eggNOG_preferred_name": row["eggnog_preferred_name"],
                "seed_ortholog": row["seed_ortholog"],
                "evalue": row["evalue"],
                "score": row["score"],
                "coordinate_source": f"Bakta_{original_type}",
                "annotation_source": "eggNOG-mapper_2.1.13_eggNOG_5.0.2",
            }
            attribute_text = ";".join(f"{key}={encode(value)}" for key, value in attributes.items())
            handle.write(
                "\t".join(
                    [seqid, "curated_marker_evidence", "CDS", start, end, ".", strand, ".", attribute_text]
                )
                + "\n"
            )

    print(f"Wrote {len(evidence)} coordinate-confirmed markers to {OUTPUT_GFF}")
    print("Counts: " + ", ".join(f"{marker}={count}" for marker, count in sorted(observed_counts.items())))


if __name__ == "__main__":
    main()
