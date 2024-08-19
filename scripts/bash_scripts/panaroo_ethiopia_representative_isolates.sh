#!/bin/bash
#SBATCH -p shared
#SBATCH -c 10
#SBATCH -t 1-00:00
#SBATCH --mem-per-cpu=12G
#SBATCH -o 20240626_ethiopia_representative_isolates_panaroo.out
#SBATCH -e 20240626_ethiopia_representative_isolates_panaroo.err
#SBATCH --mail-type=END
#SBATCH --mail-user=qinqinyu@hsph.harvard.edu

# Activate panaroo conda environment before running this
# Align all genes present in at least 98% of isolates
mkdir -p results
panaroo -i gffs/* -o results --clean-mode strict -a core --aligner mafft --core_threshold 0.98 -t 10
