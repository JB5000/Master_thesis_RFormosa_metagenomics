# MIMAG identifier resolution

## Identifier relation

The source catalogue and the locked thesis use different SS identifier schemes. Original bin ID is the stable join key. The three non-strict MIMAG results resolve as follows:

| Original bin ID | Source HQMAG | Source-table ID | Current bundle ID | MIMAG limitation |
|---|---|---:|---:|---|
| `METAMDBG-MetaBAT2Refined-group-group_240304.160` | HQMAG_005 | SS-17 | SS-11 | 17/20 standard tRNA amino acids |
| `FLYE-MetaBAT2Refined-group-group_240416.203` | HQMAG_009 | SS-03 | SS-17 | 16S and 23S rRNA absent; 20/20 tRNA amino acids |
| `FLYE-CONCOCTRefined-group-group_240416.290` | HQMAG_008 | SS-01 | SS-29 | 23S and 5S rRNA absent; 18/20 tRNA amino acids |

The current bundle identifiers for these records are SS-11, SS-17 and SS-29. Audit tables also retain the source-table identifier and original bin ID.

## Evidence

- `MAG_ID_renumbering_map.tsv`: source-table to current bundle identifier mapping.
- `MIMAG_QC_rRNA_tRNA.tsv`: source HQMAG/original-bin rRNA and tRNA outcomes.
- `MIMAG_QC_33.tsv` and `MIMAG_FAILURES.tsv`: reconciled MIMAG assessment records.
