#!/bin/bash
#SBATCH -J ria_blastdb
#SBATCH -p all
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --mem=20G
#SBATCH -t 02:00:00
set -euo pipefail
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=${RIA_BLAST_WORKDIR:-$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)}
REFERENCE_FASTA=${RIA_BLAST_REFERENCE_FASTA:?Set RIA_BLAST_REFERENCE_FASTA to the selected-reference FASTA}
REFERENCE_MAP=${RIA_BLAST_REFERENCE_MAP:?Set RIA_BLAST_REFERENCE_MAP to the contig-to-target TSV}
mkdir -p "$ROOT/reference" "$ROOT/logs" "$ROOT/hits"
cp "$REFERENCE_FASTA" "$ROOT/reference/pathogen_combined.fna"
cp "$REFERENCE_MAP" "$ROOT/reference/contig_to_organism.tsv"
/share/apps/opt/ncbi-blast+/bin/makeblastdb -in "$ROOT/reference/pathogen_combined.fna" -dbtype nucl -out "$ROOT/reference/pathogen_combined"
