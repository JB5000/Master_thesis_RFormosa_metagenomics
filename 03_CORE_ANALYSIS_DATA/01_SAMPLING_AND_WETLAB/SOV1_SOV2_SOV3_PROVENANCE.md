# SOV1 / SOV2 / SOV3 sequencing provenance

## Established from retained records

- Twenty-two barcoded libraries were sequenced on PromethION 2 Solo unit
  P2S-02226, using MinKNOW 26.01.15, across loadings labelled RFormosa_SOV1,
  SOV2 and SOV3.
- Basecalling used Dorado v1.4.0 with
  `dna_r10.4.1_e8.2_400bps_sup@v5.2.0`; demultiplexing used
  `dorado demux --kit-name SQK-NBD114-24`; unclassified reads were excluded
  and sample FASTQs were merged by sample identity.
- Sample S_24_04_16 was sequenced separately and is the deepest dataset
  (approximately 21.6 million reads).

## Missing run-level evidence

The retained merged FASTQs contain read UUIDs only, without flow-cell ID,
run ID or start time. Sequencing-summary files, run-level BAM files, POD5
files and MinKNOW run folders were not retained. Therefore, assignment of the
second barcoded sample in SOV1 and the exact procedure for that loading cannot
be verified from this bundle alone.

## Additional run metadata

A sequencing-summary file or MinKNOW run report would add the flow-cell ID,
run ID, barcode arrangement and per-read timing to the retained metadata.
