import pandas as pd
import numpy as np
import seaborn as sns
import functions as fnc

# Load in information about Ethiopia isolates
ethiopia_isolates = pd.read_csv('../data/ethiopia_isolates.txt', header = None, names = ['wgs_id'])

# Load in information about representative isolates
contemp_global_isolates = pd.read_csv('../data/gubbins/ethiopia_representative_isolates/representative_isolates.txt', header = None, names = ['wgs_id'])

isolates = pd.concat([ethiopia_isolates, contemp_global_isolates])

# Load information about MLST
mlst = pd.read_csv('../data/mlst_ngstar_all_genomes.tsv', sep = '\t')[['strain', 'MLST']]
mlst['wgs_id'] = mlst['strain'].str.split('_', expand = True)[0]
mlst.drop('strain', axis = 'columns', inplace = True)

# Merge with isolates of interest
merged = isolates.merge(mlst, on = 'wgs_id')

# Only show MLST 7827 and 1587 (most common MLSTs in Ethiopian isolates)
merged.at[(merged['MLST']!='7827')&(merged['MLST']!='1587'),'MLST'] = 'NA'

# Write itol
legend = merged.copy()
annotation = 'MLST'
sample_name = 'wgs_id'
output_filename = 'itol_representative_isolates_st.txt'
output_path = '../data/itol/'

unique_annotations = np.unique(legend[annotation])
unique_annotations = unique_annotations[unique_annotations!='NA']
colors_dict = {'1587':'violet', '7827':'darkgoldenrod', 'NA':'white'}

fnc.itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path)