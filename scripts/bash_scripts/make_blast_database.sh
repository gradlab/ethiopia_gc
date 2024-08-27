#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --mem=4G
#SBATCH	-p shared
#SBATCH -t 0-00:10
#SBATCH -o make_blast_database.out
#SBATCH -e make_blast_database.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=qinqinyu@hsph.harvard.edu
#SBATCH --account=grad_lab

# Make blast database
mkdir -p blastdb
cat assemblies/*.fa > blastdb/gc_contigs.fa
makeblastdb -dbtype nucl -in blastdb/gc_contigs.fa -out blastdb/gc