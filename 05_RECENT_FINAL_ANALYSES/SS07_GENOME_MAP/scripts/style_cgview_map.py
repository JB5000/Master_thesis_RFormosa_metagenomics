#!/usr/bin/env python3
"""Apply the reproducible SS-07 pilot styling to Proksee Batch CGView JSON."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_JSON = ROOT / "proksee_output" / "data" / "genome_maps" / "SS-07.cgview.raw.json"
STYLED_JSON = ROOT / "proksee_output" / "data" / "genome_maps" / "SS-07.cgview.json"
REPORT_JS = ROOT / "proksee_output" / "data" / "genome_maps" / "genome_1.js"

MARKER_STYLE = {
    "sat": ("Sulfur: sat", "rgba(148,103,189,1)"),
    "sqr": ("Sulfur: sqr", "rgba(106,61,154,1)"),
    "nifH": ("Nitrogen: nifH", "rgba(44,160,44,1)"),
    "ureC": ("Nitrogen: ureC", "rgba(125,190,85,1)"),
    "rbcL": ("Carbon fixation: rbcL", "rgba(230,159,0,1)"),
    "psaA": ("Photosystem I: psaA", "rgba(213,94,0,1)"),
    "psbA": ("Photosystem II: psbA", "rgba(240,110,50,1)"),
}


def main() -> None:
    data = json.loads(RAW_JSON.read_text(encoding="utf-8"))
    cgview = data["cgview"]

    cgview["annotation"]["onlyDrawFavorites"] = True
    cgview["annotation"]["font"] = "sans-serif,plain,11"
    cgview["captions"][0].update(
        {
            "name": "SS-07 | Waterburya-related | 5.93 Mb | 2 contigs",
            "font": "sans-serif,bold,18",
            "fontColor": "rgba(0,0,0,1)",
            "backgroundColor": "rgba(255,255,255,0.75)",
        }
    )

    legend = cgview["legend"]
    legend["position"] = "top-right"
    legend["defaultFont"] = "sans-serif,plain,11"
    legend["items"] = [
        item for item in legend["items"] if item["name"] != "SS-07_curated_markers.gff3"
    ]
    for marker in ("sat", "sqr", "nifH", "ureC", "rbcL", "psaA", "psbA"):
        legend_name, colour = MARKER_STYLE[marker]
        legend["items"].insert(
            0,
            {"name": legend_name, "swatchColor": colour, "decoration": "arc"},
        )

    marker_count = 0
    for feature in cgview["features"]:
        if feature.get("source") != "gff_1":
            continue
        marker = feature["name"]
        if marker not in MARKER_STYLE:
            raise ValueError(f"No style configured for curated marker {marker}")
        legend_name, _ = MARKER_STYLE[marker]
        feature["legend"] = legend_name
        feature["favorite"] = True
        marker_count += 1

    if marker_count != 11:
        raise ValueError(f"Expected 11 curated features, found {marker_count}")

    for track in cgview["tracks"]:
        if track.get("dataKeys") == "gff_1":
            track.update(
                {
                    "name": "Curated functional markers",
                    "position": "outside",
                    "thicknessRatio": 2,
                    "drawOrder": "score",
                }
            )

    rendered = json.dumps(data, indent=2)
    STYLED_JSON.write_text(rendered + "\n", encoding="utf-8")
    REPORT_JS.write_text("json = " + json.dumps(data, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(f"Styled {marker_count} curated markers in {STYLED_JSON}")


if __name__ == "__main__":
    main()
