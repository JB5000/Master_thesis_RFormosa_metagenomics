#!/bin/bash
#SBATCH -J ss07_coverage
#SBATCH -p all
#SBATCH -N 1
#SBATCH -n 56
#SBATCH --mem=100G
#SBATCH -t 3-00:00:00
set -euo pipefail
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=${RIA_SS07_COVERAGE_WORKDIR:-$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)/coverage_regenerated}
REF=${RIA_SS07_REFERENCE_FASTA:?Set RIA_SS07_REFERENCE_FASTA to the SS-07 source MAG FASTA}
READS=${RIA_SS07_SOURCE_FASTQ:?Set RIA_SS07_SOURCE_FASTQ to the source long-read FASTQ}
MINIMAP2=/share/apps/opt/minimap2-2.17_x64-linux/minimap2
SAMTOOLS=/share/apps/bin/samtools
mkdir -p "$ROOT"/{reference,bam,tables,logs}
cp "$REF" "$ROOT/reference/SS-07_source_MAG.fna"
$MINIMAP2 -ax map-ont -t 56 "$ROOT/reference/SS-07_source_MAG.fna" "$READS" | $SAMTOOLS sort -@ 16 -o "$ROOT/bam/SS-07_S_24_04_16.sorted.bam" -
$SAMTOOLS index "$ROOT/bam/SS-07_S_24_04_16.sorted.bam"
$SAMTOOLS depth -aa "$ROOT/bam/SS-07_S_24_04_16.sorted.bam" | awk 'BEGIN{OFS="\t"} {w=int(($2-1)/10000); k=$1 FS w; sum[k]+=$3; n[k]++; if(!(k in start)){start[k]=w*10000+1; contig[k]=$1}} END{for(k in sum) print contig[k],start[k],start[k]+9999,sum[k]/n[k]}' | sort -k1,1 -k2,2n > "$ROOT/tables/SS-07_S_24_04_16_10kb_mean_depth.tsv"
$SAMTOOLS coverage "$ROOT/bam/SS-07_S_24_04_16.sorted.bam" > "$ROOT/tables/SS-07_S_24_04_16_contig_coverage.tsv"
