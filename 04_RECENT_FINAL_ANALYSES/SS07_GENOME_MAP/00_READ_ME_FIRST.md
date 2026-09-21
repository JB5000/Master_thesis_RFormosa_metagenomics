# Proksee MAG pilot: SS-07

This directory contains a reproducible Proksee/CGView pilot for one final MAG29 representative. Original files on CETA were not modified; the files here are copies or derived outputs.

## Selected genome

- Final identifier: `SS-07`
- Original bin identifier: `METAMDBG-MetaBAT2Refined-group-group_240416.257`
- Source sample: `MG240416` / thesis sample identifier `S_24_04_16`
- Taxonomy: Cyanobacteriota; Cyanobacteriia; Cyanobacteriales; Xenococcaceae; Waterburya
- CheckM2 completeness: 100.0%
- CheckM2 contamination: 0.1%
- Sequence length: 5,930,534 bp
- Contigs / GenBank records: 2
- Bakta: v1.11.0, light database v6.0

The circular layout places the two contigs consecutively for visualization. It does not represent a closed circular chromosome or confirmed adjacency between the contigs. Their order and orientation were not changed.

## Contents

- `proksee_input/`: exact input structure used with Proksee Batch.
- `proksee_output/report.html`: local interactive Proksee Batch report.
- `proksee_output/data/genome_maps/SS-07.cgview.raw.json`: unstyled CGView output from Proksee Batch.
- `proksee_output/data/genome_maps/SS-07.cgview.json`: reproducibly styled CGView project.
- `exports/SS-07_Proksee_pilot.png`: 2400 × 2400 raster export.
- `exports/SS-07_Proksee_pilot.svg`: vector export.
- `exports/SS-07_Proksee_pilot.json`: exported editable CGView JSON.
- `exports/SS-07_Proksee_batch_report.png`: screenshot of the local interactive report.
- `exports/SS-07_Bakta_general.{png,svg}`: general display of the retained
  Bakta annotation, without the later curated functional-marker overlay.
- `exports/SS-07_MIMAG_RNA.{png,svg}`: focused RNA-evidence display. All 45
  Bakta tRNA features are drawn; one representative of each of the 20 standard
  amino-acid types is labelled. The nine rRNA features are also drawn, with one
  representative label for each of 16S, 23S and 5S.
- `proksee_variants/`: editable CGView JSON for the general Bakta and focused
  MIMAG RNA displays.
- `source/SS-07_MIMAG_RNA_evidence.tsv`: exact feature coordinates and labels
  used by the focused RNA display.
- `source/`: retained Bakta coordinate files and the curated eggNOG marker-evidence table.
- `scripts/`: scripts that build the marker track, style the CGView map and export it.
- `provenance/`: versions, commands, project response, manifest and checksums.

## Curated marker track

The marker track contains 11 coordinate-confirmed features:

- `sat`: 1
- `sqr`: 1
- `nifH`: 1
- `ureC`: 1
- `rbcL` (`cbbL`): 1
- `psaA`: 1
- `psbA`: 5

Coordinates come from the final Bakta GFF3. Functional labels come from the final eggNOG-mapper output by preferred name and/or the recorded KEGG orthologue. No missing marker was inferred.

## MIMAG RNA-evidence variant

The retained post-hoc strict screen required 16S, 23S and 5S rRNA plus tRNAs
representing at least 18 of the 20 standard amino acids. SS-07 contains all
three rRNA types and tRNAs for 20/20 standard amino-acid types (45 tRNA
features total). The circular arrangement concatenates the two contigs for
display only and does not assert genome closure or contig adjacency.

## Open the results

Open `proksee_output/report.html` through a local HTTP server, for example:

```bash
cd proksee_output
python3 -m http.server 8765
```

Then open `http://127.0.0.1:8765/report.html`.

The styled project created through the Proksee API is recorded in `provenance/proksee_project_response.json`.
