# Storage retention and provenance gates

This repository is the retained scientific reproduction bundle. It is not a
complete copy of the large HPC workflow trees, raw sequencing libraries, or
every intermediate output. Large external outputs may still be required for
provenance, audit, or future reruns.

## MAG workflow retention gates

- `05_nfccoremag_all_samples` is the canonical source named by the canonical
  MAG database and abundance workflow.
- `30_nfccoremag_all_samples` is an audit and provenance mirror. It must not be
  treated as disposable simply because it is an alternate numbered layer. The
  retained CheckM2 provenance records refer to this tree, including the
  `MG240416` run used by the authoritative MAG catalogue.
- `45_mag_db_abundance_69subsamples` is the canonical entry point for the
  validated MAG-only Kraken2/Bracken abundance rebuild. Its validation outputs,
  manifests, final tables, and documented legacy-retirement gate must be
  preserved together.
- The legacy MAG database trees must remain available until the canonical
  rebuild and its downstream abundance validation have been accepted.

## Raw-read retention gate

The 23 merged Oxford Nanopore FASTQ libraries are represented here by a
portable filename manifest rather than by the large FASTQ files themselves.
The raw libraries must not be deleted from external storage until an equivalent
long-term copy has been located, verified, and documented.

## Cleanup rule

A large directory is not disposable merely because it is old, large, named as
an archive, or absent from this repository. Before removal, confirm that its
contents are either reproducibly regenerated or represented by retained
evidence, and record the replacement path or archive location.
