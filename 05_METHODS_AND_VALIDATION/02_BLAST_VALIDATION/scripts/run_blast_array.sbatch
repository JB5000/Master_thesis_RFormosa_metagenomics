#!/bin/bash
#SBATCH -J ria_blast
#SBATCH -p all
#SBATCH -N 1
#SBATCH -n 56
#SBATCH --mem=100G
#SBATCH -t 3-00:00:00
#SBATCH --array=1-69%5
set -euo pipefail
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=${RIA_BLAST_WORKDIR:-$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)}
MAN=${RIA_SUBSAMPLE_TASK_MANIFEST:?Set RIA_SUBSAMPLE_TASK_MANIFEST to the 69-task manifest}
SUBSAMPLE_DIR=${RIA_SUBSAMPLE_FASTQ_DIR:?Set RIA_SUBSAMPLE_FASTQ_DIR to the equal-depth FASTQ directory}
DB=$ROOT/reference/pathogen_combined
line=$(sed -n "$((SLURM_ARRAY_TASK_ID+1))p" "$MAN")
IFS=$'\t' read -r task sample rep seed fastq depth oldout <<< "$line"
subfastq=$SUBSAMPLE_DIR/${sample}__sub${depth}__rep${rep}.fastq.gz
out=$ROOT/hits/${sample}__sub${depth}__rep${rep}.blast6.gz
mkdir -p "$ROOT/hits" "$ROOT/logs"
[ -s "$out" ] && exit 0
gzip -cd "$subfastq" | awk 'NR%4==1 {sub(/^@/,">"); print; next} NR%4==2 {print}' | \
  /share/apps/opt/ncbi-blast+/bin/blastn -query - -db "$DB" -evalue 1e-5 -max_target_seqs 1 -max_hsps 1 -num_threads 56 \
  -outfmt '6 qseqid sseqid pident length qlen qstart qend sstart send evalue bitscore qcovs' | gzip -c > "$out"
