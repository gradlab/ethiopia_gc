import pandas as pd
import shutil
import glob

# Copy representative gffs

paths = pd.read_csv('../data/panaroo/representative_isolates_annotation_paths.txt', header = None)[0].values
for path in paths:
    shutil.copy(path, '/n/holyscratch01/grad_lab/Users/qinqinyu/20240626_ethiopia_representative_isolates_panaroo/gffs/')
    
# Copy Ethiopian isolates

paths = glob.glob('/n/grad_lab2/Lab/gonococcus/datasets/ethiopia_isolates/annotations/*.gff')

# Remove the reference genome
paths.remove('/n/grad_lab2/Lab/gonococcus/datasets/ethiopia_isolates/annotations/Eth14-2022.gff')

for path in paths:
    shutil.copy(path, '/n/holyscratch01/grad_lab/Users/qinqinyu/20240626_ethiopia_representative_isolates_panaroo/gffs/')