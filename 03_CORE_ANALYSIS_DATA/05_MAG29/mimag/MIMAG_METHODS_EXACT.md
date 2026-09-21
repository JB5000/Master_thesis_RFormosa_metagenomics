# MIMAG post-hoc quality-assessment record

## Method and inputs

The final representatives were assessed post hoc against the strict high-quality draft criteria used in the canonical project report: detection of 16S, 23S and 5S rRNA genes, and tRNAs representing at least 18 of the 20 standard amino acids. This MIMAG screen did **not** determine MAG29 or CoA4 membership; membership was set earlier by CheckM2-based candidate selection and dRep.

All 29 MAG29 and four CoA4 representatives were subsequently reannotated successfully with Bakta v1.11.0 using the light v6 database in metagenome mode. The two Slurm arrays completed on 21 June 2026: array 18416 (29 MAG29 tasks) and array 18417 (four CoA4 tasks). The retained array scripts invoke Bakta with `--force --db <db-light> --output <dir> --prefix <id> --locus-tag <tag> --threads <n> --meta`. Each successful output includes a GFF3 file; the counts in `MIMAG_QC_33.tsv` were independently extracted from those GFF3 annotations.

The strict screen required at least one 16S, 23S and 5S feature, plus tRNAs representing at least 18 standard amino acids. The recorded counts are 26/29 strict passes for MAG29 and 3/4 for CoA4 (29/33 overall). The three non-strict MAG29 identifiers are SS-11, SS-17 and SS-29 in the current bundle crosswalk; CoA-1 is the non-strict CoA4 identifier. The feature counts are in `MIMAG_FAILURES.tsv`.

## Recorded workflow relation

The MIMAG assessment was performed after dereplication. MAG29 and CoA4 membership fields originate from the earlier CheckM2 and dRep records.

## Field boundaries

- MIMAG screening field: post-dereplication assessment; not a catalogue membership field.
- rRNA rule: presence of 16S, 23S and 5S; no exactly-one-copy rule.
- Source-table SS identifier relation: recorded in `MIMAG_ID_RESOLUTION.md` and joined through the retained crosswalk.
