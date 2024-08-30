import pandas as pd
import shutil
import glob

# Copy representative pseudogenomes

paths = pd.read_csv('../data/beast/representative_subtree_to_check_mlst_7827/pseudogenomes.txt', header = None)[0].values
for path in paths:
    shutil.copy(path, '/n/holyscratch01/grad_lab/Users/qinqinyu/20240829_gubbins_representative_subtree_to_check_mlst_7827/pseudogenomes/')