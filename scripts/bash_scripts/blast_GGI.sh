#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --mem=4G
#SBATCH	-p shared
#SBATCH -t 0-04:00
#SBATCH -o blast_GGI.out
#SBATCH -e blast_GGI.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=qinqinyu@hsph.harvard.edu
#SBATCH --account=grad_lab
#SBATCH --array=0-61

readarray -t f < ggi_genes.txt

# Blast genes
mkdir -p blast_results
blastn -db blastdb/gc -query "reference_sequences/${f[${SLURM_ARRAY_TASK_ID}]}.fa" -out "blast_results/${f[${SLURM_ARRAY_TASK_ID}]}.txt" -num_threads 1 -max_target_seqs 30000 -outfmt 6