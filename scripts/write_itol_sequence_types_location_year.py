import pandas as pd
import numpy as np
import math
import seaborn as sns

import functions as fnc

isolates_filename = '../data/gubbins/mlst/1587/isolates.txt'
st_label = 'mlst_1587'
fnc.write_itol_sequence_types(isolates_filename, st_label)

isolates_filename = '../data/gubbins/mlst/7827/isolates.txt'
st_label = 'mlst_7827'
fnc.write_itol_sequence_types(isolates_filename, st_label)

isolates_filename = '../data/gubbins/ngstar/1203/isolates.txt'
st_label = 'ngstar_1203'
fnc.write_itol_sequence_types(isolates_filename, st_label)
