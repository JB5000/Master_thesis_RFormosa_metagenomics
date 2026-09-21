#!/usr/bin/env python3
"""Build general-Bakta and MIMAG-RNA CGView variants from the Proksee Batch map."""

from __future__ import annotations

import csv
import copy
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "proksee_output/data/genome_maps/SS-07.cgview.raw.json"
VARIANTS = ROOT / "proksee_variants"
VALUES = ROOT / "source/SS-07_MIMAG_RNA_evidence.tsv"

STANDARD_AA = {
    "Ala", "Arg", "Asn", "Asp", "Cys", "Gln", "Glu", "Gly", "His", "Ile",
    "Leu", "Lys", "Met", "Phe", "Pro", "Ser", "Thr", "Trp", "Tyr", "Val",
}
AA_GROUP = {
    "Ala": "Nonpolar", "Val": "Nonpolar", "Leu": "Nonpolar", "Ile": "Nonpolar",
    "Met": "Nonpolar", "Pro": "Nonpolar", "Gly": "Nonpolar",
    "Phe": "Aromatic", "Tyr": "Aromatic", "Trp": "Aromatic",
    "Ser": "Polar", "Thr": "Polar", "Cys": "Polar", "Asn": "Polar", "Gln": "Polar",
    "Lys": "Basic", "Arg": "Basic", "His": "Basic",
    "Asp": "Acidic", "Glu": "Acidic",
}
GROUP_STYLE = {
    "Nonpolar": "rgba(59,130,246,1)",
    "Aromatic": "rgba(139,92,246,1)",
    "Polar": "rgba(16,185,129,1)",
    "Basic": "rgba(239,68,68,1)",
    "Acidic": "rgba(245,158,11,1)",
}
RRNA_STYLE = {
    "16S": "rgba(8,145,178,1)",
    "23S": "rgba(14,116,144,1)",
    "5S": "rgba(21,94,117,1)",
}


def aa_from_product(product: str) -> str:
    match = re.match(r"tRNA-([A-Za-z0-9]+)", product)
    if not match:
        raise ValueError(f"Cannot parse tRNA product: {product}")
    aa = match.group(1)
    return {"fMet": "Met", "Ile2": "Ile"}.get(aa, aa)


def rna_kind(product: str) -> str:
    for kind in ("16S", "23S", "5S"):
        if product.startswith(kind):
            return kind
    raise ValueError(f"Cannot parse rRNA product: {product}")


def base_variant(raw: dict, caption: str) -> dict:
    data = copy.deepcopy(raw)
    cgv = data["cgview"]
    cgv["captions"][0].update({
        "name": caption,
        "font": "sans-serif,bold,17",
        "fontColor": "rgba(0,0,0,1)",
        "backgroundColor": "rgba(255,255,255,0.82)",
    })
    cgv["features"] = [f for f in cgv["features"] if f.get("source") == "genbank-features"]
    cgv["tracks"] = [t for t in cgv["tracks"] if t.get("dataKeys") != "gff_1"]
    cgv["legend"]["items"] = [
        item for item in cgv["legend"]["items"]
        if item["name"] != "SS-07_curated_markers.gff3"
    ]
    cgv["legend"]["position"] = "top-right"
    cgv["legend"]["defaultFont"] = "sans-serif,plain,10"
    cgv["annotation"]["font"] = "sans-serif,plain,10"
    return data


def main() -> None:
    VARIANTS.mkdir(parents=True, exist_ok=True)
    raw = json.loads(RAW.read_text(encoding="utf-8"))

    general = base_variant(
        raw,
        "SS-07 | Bakta v1.11.0 annotation | 5.93 Mb | 2 contigs",
    )
    general["cgview"]["annotation"]["onlyDrawFavorites"] = True
    (VARIANTS / "SS-07_Bakta_general.cgview.json").write_text(
        json.dumps(general, indent=2) + "\n", encoding="utf-8"
    )

    mimag = base_variant(
        raw,
        "SS-07 | MIMAG RNA evidence | 20/20 amino-acid types | 45 tRNA features",
    )
    cgv = mimag["cgview"]
    cgv["annotation"]["onlyDrawFavorites"] = True

    trnas = [f for f in cgv["features"] if f.get("type") == "tRNA"]
    rrnas = [f for f in cgv["features"] if f.get("type") == "rRNA"]
    counts = Counter(aa_from_product(f["meta"]["product"]) for f in trnas)
    if len(trnas) != 45 or set(counts) != STANDARD_AA:
        raise ValueError(f"Expected 45 tRNAs and 20 standard AA types, found {len(trnas)} and {sorted(counts)}")

    # This is an RNA-evidence view, not a second general annotation view.
    # Retain sequence-derived GC plots but remove the dense GenBank feature
    # track so the RNA loci and the 20 represented amino-acid types are legible.
    cgv["features"] = []
    cgv["tracks"] = [
        track for track in cgv["tracks"]
        if track.get("dataKeys") != "genbank-features"
    ]

    representatives: set[str] = set()
    evidence_rows: list[dict[str, object]] = []
    added: list[dict] = []
    for feature in trnas:
        aa = aa_from_product(feature["meta"]["product"])
        duplicate = copy.deepcopy(feature)
        duplicate["source"] = "mimag-trna"
        duplicate["legend"] = f"tRNA {AA_GROUP[aa]}"
        duplicate["name"] = aa
        duplicate["favorite"] = aa not in representatives
        if duplicate["favorite"]:
            representatives.add(aa)
        duplicate["meta"]["standard_amino_acid"] = aa
        duplicate["meta"]["amino_acid_group"] = AA_GROUP[aa]
        duplicate["meta"]["representative_label"] = str(duplicate["favorite"]).lower()
        added.append(duplicate)
        evidence_rows.append({
            "feature_type": "tRNA", "standard_type": aa,
            "amino_acid_group": AA_GROUP[aa], "gene": feature.get("name", ""),
            "product": feature["meta"]["product"], "locus_tag": feature["meta"]["locus_tag"],
            "contig": feature["contig"], "start": feature["start"], "stop": feature["stop"],
            "strand": feature["strand"], "representative_label": str(duplicate["favorite"]).lower(),
        })

    represented_rrna: set[str] = set()
    for feature in rrnas:
        kind = rna_kind(feature["meta"]["product"])
        duplicate = copy.deepcopy(feature)
        duplicate["source"] = "mimag-rrna"
        duplicate["legend"] = f"rRNA {kind}"
        duplicate["name"] = f"{kind} rRNA"
        duplicate["favorite"] = kind not in represented_rrna
        represented_rrna.add(kind)
        added.append(duplicate)
        evidence_rows.append({
            "feature_type": "rRNA", "standard_type": kind,
            "amino_acid_group": "NOT_APPLICABLE", "gene": feature.get("name", ""),
            "product": feature["meta"]["product"], "locus_tag": feature["meta"]["locus_tag"],
            "contig": feature["contig"], "start": feature["start"], "stop": feature["stop"],
            "strand": feature["strand"], "representative_label": str(duplicate["favorite"]).lower(),
        })

    cgv["features"].extend(added)
    cgv["tracks"].extend([
        {"name": "MIMAG tRNA evidence", "separateFeaturesBy": "none", "position": "outside", "thicknessRatio": 2.2, "dataType": "feature", "dataMethod": "source", "dataKeys": "mimag-trna", "drawOrder": "score"},
        {"name": "MIMAG rRNA evidence", "separateFeaturesBy": "none", "position": "outside", "thicknessRatio": 1.5, "dataType": "feature", "dataMethod": "source", "dataKeys": "mimag-rrna", "drawOrder": "score"},
    ])
    cgv["legend"]["items"] = [
        {"name": f"tRNA {group}", "swatchColor": colour, "decoration": "arc"}
        for group, colour in GROUP_STYLE.items()
    ] + [
        {"name": f"rRNA {kind}", "swatchColor": colour, "decoration": "arc"}
        for kind, colour in RRNA_STYLE.items()
    ]

    (VARIANTS / "SS-07_MIMAG_RNA.cgview.json").write_text(
        json.dumps(mimag, indent=2) + "\n", encoding="utf-8"
    )
    with VALUES.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(evidence_rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(evidence_rows)

    print(f"Bakta features: {len(general['cgview']['features'])}")
    print(f"MIMAG evidence: {len(trnas)} tRNAs, {len(counts)}/20 AA types, {len(rrnas)} rRNAs")
    print("tRNA counts: " + ", ".join(f"{aa}={counts[aa]}" for aa in sorted(counts)))


if __name__ == "__main__":
    main()
