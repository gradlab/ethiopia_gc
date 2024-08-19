import glob
import os
import numpy as np
import pandas as pd

filenames = glob.glob('/n/grad_lab2/Lab/gonococcus/datasets/ethiopia_isolates/annotations/*.gff')

isolates = []
for filename in filenames:
    basename = os.path.basename(filename)
    isolate = basename.split('.')[0]
    isolates.append(isolate)
    
pd.DataFrame(np.sort(isolates)).to_csv('../data/ethiopia_isolates.txt', index = False, header = False)