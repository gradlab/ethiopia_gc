import pandas as pd
import shutil
import glob

# Copy representative pseudogenomes

paths = pd.read_csv('../data/gubbins/ethiopia_representative_isolates/representative_isolates_pseudogenome_paths.txt', header = None)[0].values
for path in paths:
    shutil.copy(path, '/n/netscratch/grad_lab/Lab/qinqinyu/20251009_tree_ethiopia_representative_isolates/pseudogenomes/')
    
# Copy Ethiopian isolates

paths = glob.glob('/n/grad_lab2/Lab/gonococcus/datasets/ethiopia_isolates/pseudogenomes/*_pseudogenome.fasta')

# Remove the reference genome
paths.remove('/n/grad_lab2/Lab/gonococcus/datasets/ethiopia_isolates/pseudogenomes/Eth14-2022_pseudogenome.fasta')

for path in paths:
    shutil.copy(path, '/n/netscratch/grad_lab/Lab/qinqinyu/20251009_tree_ethiopia_representative_isolates/pseudogenomes/')