# MAG identifier reconciliation

## Current bundle identifier scheme

The current figure files and table files use the renumbered identifiers `SS-01` to `SS-29`. Some primary source tables use a different SS numbering scheme. The retained crosswalk links both schemes through original bin ID.

The three labels with the clearest potential for misinterpretation are:

| Label | Source-table meaning | Current bundle meaning |
|---|---|---|
| **SS-17** | **JABZFP01** (Desulfobacterota) | **CAJQQK01** (Pseudomonadota, Rhizobiales) |
| SS-01 | Marinihelvus | Site-B15 (Bacteroidota) |
| SS-03 | CAJQQK01 | JARQTN01 (Bacteroidota) |

The crosswalk contains source-table identifiers, original-bin IDs, source samples, GTDB taxonomy, completeness and contamination. It contains 29 joined records and zero genus mismatches.

## Files

- `figure_sources/taxonomy/MAG_ID_RECONCILIATION_AUTHORITATIVE.tsv`: complete 29-row identifier crosswalk and taxonomy.
- `figure_sources/taxonomy/Table_MAG29_full_catalogue_AUTHORITATIVE.tsv`: catalogue keyed and sorted by current bundle identifier.
- `Table_MAG29_functional_summary_AUTHORITATIVE.tsv`: functional summary keyed by current bundle identifier.
- `MAG_ID_TABLE_USAGE_FLAGS.tsv`: identifier scheme and join key for each listed artefact type.

Recruitment matrices are keyed by original bin ID. CoA4 uses the separate identifiers `CoA-1` to `CoA-4`. The cross-table MAG29 join key is original bin ID.
