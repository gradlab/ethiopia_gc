#!/bin/bash
#SBATCH -p shared
#SBATCH -c 12
#SBATCH -t 3-00:00
#SBATCH --mem-per-cpu=12G
#SBATCH -o 20240829_beast_representative_subtree_to_check_mlst_7827_gubbins.out
#SBATCH -e 20240829_beast_representative_subtree_to_check_mlst_7827_gubbins.err
#SBATCH --mail-type=END
#SBATCH --mail-user=qinqinyu@hsph.harvard.edu 

/n/holylfs05/LABS/grad_lab/Users/qinqinyu/software/beast/bin/beast -threads 12 representative_subtree_to_check_mlst_7827_gubbins.xml
