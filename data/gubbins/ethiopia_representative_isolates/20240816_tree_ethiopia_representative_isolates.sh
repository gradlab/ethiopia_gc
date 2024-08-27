#!/bin/bash
#SBATCH -p intermediate
#SBATCH -c 12
#SBATCH -t 14-00:00
#SBATCH --mem-per-cpu=12G
#SBATCH -o 20240816_tree_ethiopia_representative_isolates.out
#SBATCH -e 20240816_tree_ethiopia_representative_isolates.err
#SBATCH --mail-type=END
#SBATCH --mail-user=qinqinyu@hsph.harvard.edu 

run_gubbins.py --first-tree-builder rapidnj --tree-builder raxmlng --first-model JC --model GTR --threads 12 ethiopia_representative_isolates.fa
