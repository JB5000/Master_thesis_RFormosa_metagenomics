# Supplementary Methods — recovered commands and parameters

This appendix records only command text recovered from scripts/logs. Private absolute paths are intentionally replaced with placeholders. A command being listed does not prove that every later table or figure was derived from that run; such limits are recorded in the layer-specific provenance tables.

## Single-sample nf-core/mag (23 independent runs)

```bash
nextflow run nf-core/mag -r 5.4.1 \
  -profile apptainer -c <nextflow.config> --input <samples_longread.csv> \
  -w <work_dir> --outdir <out_dir> --keep_lambda \
  --longread_filtering_tool chopper --skip_megahit --skip_spades \
  --skip_spadeshybrid --skip_comebin --skip_gtdbtk --skip_prokka \
  --run_checkm false --coassemble_group --run_checkm2 --run_gunc \
  --run_busco false --refine_bins_dastool \
  --postbinning_input refined_bins_only --bin_domain_classification \
  --tiara_min_length 2000 --longreads_min_length 2000 \
  --checkm2_db <uniref100.KO.1.dmnd>
```

The MG240416 variant additionally used `-resume`, `--exclude_unbins_from_postbinning`, and `--max_time 5.d`.

## Final MAG29 dRep

```bash
dRep dereplicate <drep_out> -g <56_genome_FASTAs> -p <cpus> \
  -comp 90 -con 5 -l 50000 -pa 0.9 -sa 0.95 -nc 0.1 \
  --S_algorithm fastANI
```

## GTDB-Tk

```bash
gtdbtk classify_wf --batchfile <gtdbtk_batchfile.tsv> \
  --out_dir <gtdbtk_out> --cpus 16
```

The recovered environment used GTDB-Tk 2.5.2 with GTDB r226.

## Mapping-based recruitment

```bash
minimap2 -t 50 -ax map-ont <LEGACY39_reference.fna> <equal_depth.fastq> |
  samtools view -@2 -b -F 2308 -q 10 - |
  samtools sort -o <sample.bam>
samtools index <sample.bam>
samtools idxstats <sample.bam>
```

No percent-identity or aligned-fraction threshold occurs in the recovered mapping command.

## VFDB similarity screening

```bash
diamond blastp -d <VFDB_setB_pro.dmnd> -q <all_reps.faa> --threads 16 \
  -o <single_sample_reps_vfdb_hits.tsv> \
  --outfmt 6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen qcovhsp scovhsp \
  --sensitive -e 1e-5 --max-target-seqs 5 --id 30 --query-cover 50
```

The completed run used DIAMOND 2.2.0. The database was named `VFDB_setB_pro`; no release label was retained.

## Bakta and eggNOG-mapper

```bash
bakta --force --db <db-light> --output <output_dir> --prefix <id> \
  --locus-tag <tag> --threads <n> --meta <genome.fasta>

emapper.py -i <LEGACY39_all_Bakta_proteins.faa> --itype proteins -m diamond \
  --data_dir <eggnog_db> --cpu 16 -o LEGACY39_eggnog \
  --output_dir <output_dir> --override
```

## FuncScan

```bash
nextflow run nf-core/funcscan -r 3.0.0 -profile apptainer \
  -params-file LEGACY39_funcscan_params.yaml --run_amp_screening \
  --run_arg_screening --run_bgc_screening -resume
```

## Equal-depth TaxProfiler/KrakenUniq

```bash
seqkit sample -s <seed> -n 315147 <input.fastq> | gzip -c > <subsample.fastq.gz>

nextflow run nf-core/taxprofiler -r 1.2.4 -profile apptainer \
  --input <samplesheet> --databases <dbsheet> --outdir <outdir> \
  --run_krakenuniq --run_krona --run_profile_standardisation \
  --max_cpus <n> --max_memory 80.GB --max_time 2.d -resume
```

## Full-depth TaxProfiler QC and KrakenUniq

The recovered 23-library run used nf-core/taxprofiler 1.2.4 with Nextflow
25.04.4, nanoq 0.10.0 and KrakenUniq 1.0.4. Its portable equivalent is:

```bash
nextflow run nf-core/taxprofiler -r 1.2.4 -profile apptainer \
  -c <taxprofiler_config> --input <samplesheet.csv> \
  --databases <database_sheet.csv> --outdir <outdir> \
  --perform_longread_qc --longread_qc_skipadaptertrim \
  --longread_qc_qualityfilter_minlength 1000 \
  --longread_qc_qualityfilter_minquality 7 \
  --longread_qc_qualityfilter_keeppercent 90 \
  --run_krakenuniq --run_krona --run_profile_standardisation -resume
```

The preserved source outputs and portable raw-FASTQ manifest are in
`03_CORE_ANALYSIS_DATA/02_READS_AND_QC/taxprofiler_20260430/`.

## Coassembly and selected-reference BLASTn screening

The coassembly used the MAG command above with the four `group_2025_4samples` entries, plus `--exclude_unbins_from_postbinning -resume`.

```bash
dRep dereplicate <coa_drep_out> -g <four_FASTAs> -p <cpus> \
  --ignoreGenomeQuality --S_algorithm fastANI

gzip -cd <equal_depth.fastq.gz> | awk 'NR%4==1 {sub(/^@/,">"); print; next} NR%4==2 {print}' | \
  blastn -query - -db <selected_reference_database> -evalue 1e-5 \
  -max_target_seqs 1 -max_hsps 1 -num_threads <cpus> \
  -outfmt '6 qseqid sseqid pident length qlen qstart qend sstart send evalue bitscore qcovs' \
  | gzip -c > <hits.blast6.gz>
```

The active target-screening command is also retained at
`05_METHODS_AND_VALIDATION/02_BLAST_VALIDATION/scripts/run_blast_array.sbatch`.
