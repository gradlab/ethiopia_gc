#!/bin/bash
#SBATCH -p shared
#SBATCH -c 12
#SBATCH -t 2-00:00
#SBATCH --mem-per-cpu=12G
#SBATCH -o 20240627_mlst_7827_subtree_beast.out
#SBATCH -e 20240627_mlst_7827_subtree_beast.err
#SBATCH --mail-type=END
#SBATCH --mail-user=qinqinyu@hsph.harvard.edu 

/n/holylfs05/LABS/grad_lab/Users/qinqinyu/software/beast/bin/beast -threads 12 mlst_7827_subtree.xml
