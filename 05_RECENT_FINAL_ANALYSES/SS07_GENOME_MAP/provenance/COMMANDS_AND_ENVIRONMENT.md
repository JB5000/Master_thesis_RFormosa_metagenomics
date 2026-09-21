# Commands and environment

## Software

- Proksee Batch 0.6.6
- Python 3.12.3
- Biopython 1.87
- gffutils 0.12
- Selenium 4.46.0
- Google Chrome 143.0.7499.40
- Bakta annotation v1.11.0 with light database v6.0
- eggNOG-mapper v2.1.13 with eggNOG v5.0.2 and DIAMOND v2.2.0

## Installation

```bash
pipx install 'proksee-batch==0.6.6'
```

## Build and run

```bash
python3 scripts/build_curated_markers.py
proksee-batch --input proksee_input --output proksee_output
python3 scripts/style_cgview_map.py
python3 scripts/export_styled_map.py
python3 scripts/build_bakta_and_mimag_variants.py
<proksee-batch-python> scripts/export_variant_maps.py
```

The two variant exports reuse the local CGView map created by Proksee Batch.
They do not upload new data or change the retained raw Proksee output. The
export script temporarily loads each variant into the local report and restores
the original report JavaScript before exiting.

`proksee-batch 0.6.6` excludes GFF feature types `gene`, `exon` and `region`. The additional curated marker track therefore uses `CDS` features, with the original Bakta CDS coordinates retained in the attributes.

## CETA source locators

`CETA_RESULTS` denotes the site-specific base directory containing the retained
analysis outputs. The complete files needed for this bundle entry are included
under `source/` and `proksee_input/`; the locators below document their origin
and are not portable rerun configuration.

Final Bakta directory:

```text
${CETA_RESULTS}/34_MAG_RERUN_REANNOTATION_AND_RECRUITMENT/01_single_sample_drep/03_bakta/individual_results/METAMDBG-MetaBAT2Refined-group-group_240416.257/
```

Final eggNOG annotations:

```text
${CETA_RESULTS}/34_MAG_RERUN_REANNOTATION_AND_RECRUITMENT/01_single_sample_drep/05_eggnog/results/single_sample_reps_eggnog.emapper.annotations
```

## Proksee project

The final styled-project identifier and URL are stored in `proksee_project_response.json`. Creating the project uploads the styled CGView JSON to the Proksee service. The local report and all local JSON/export files remain usable independently of that URL.
