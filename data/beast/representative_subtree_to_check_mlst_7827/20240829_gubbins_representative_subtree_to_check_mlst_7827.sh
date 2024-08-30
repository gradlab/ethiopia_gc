#!/bin/bash
#SBATCH -p shared
#SBATCH -c 12
#SBATCH -t 0-05:00
#SBATCH --mem-per-cpu=12G
#SBATCH -o 20240829_gubbins_representative_subtree_to_check_mlst_7827.out
#SBATCH -e 20240829_gubbins_representative_subtree_to_check_mlst_7827.err
#SBATCH --mail-type=END
#SBATCH --mail-user=qinqinyu@hsph.harvard.edu 

run_gubbins.py --first-tree-builder rapidnj --tree-builder raxmlng --first-model JC --model GTR --threads 12 pseudogenome_alignment.fa
