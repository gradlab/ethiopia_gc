#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --mem=4G
#SBATCH	-p shared
#SBATCH -t 1-00:00
#SBATCH -o run_pyngost.out
#SBATCH -e run_pyngost.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=qinqinyu@hsph.harvard.edu
#SBATCH --account=grad_lab

/n/home13/qinqinyu/.conda/envs/pyngoST/lib/python3.12/site-packages/pyngoST/pyngoST.py -d
/n/home13/qinqinyu/.conda/envs/pyngoST/lib/python3.12/site-packages/pyngoST/pyngoST.py -i /n/grad_lab2/Lab/gonococcus/datasets/*/assemblies/*_contigs_filtered.fa -p allelesDB -s MLST,NG-STAR -o mlst_ngstar_all_genomes.tsv