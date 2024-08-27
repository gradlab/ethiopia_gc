import pandas as pd
import numpy as np

# Read in tree file
f = open("../data/gubbins/mlst/7827/pseudogenome_alignment_mlst_7827.final_tree.tre", "r")
tree = (f.read())

# Split the tree to get the subtree
subtree = tree.split('431.070801,')[1]

# Get the isolates in subtree
subtree = subtree.replace('25825_2_121', '25825_2#121')
subtree = subtree.replace('(', '').replace(')', '').split(',')

subtree_isolates = []
for i in subtree:
    isolate = i[:i.find(':')]
    subtree_isolates.append(isolate)
    
subtree_isolates_df = pd.DataFrame({'wgs_id':subtree_isolates})

# Get the pseudogenome_paths
isolates = pd.read_csv('../data/gubbins/mlst/7827/isolates.txt', header = None, names = ['wgs_id'])
pseudogenome_paths = pd.read_csv('../data/gubbins/mlst/7827/pseudogenome_paths.txt', header = None, names = ['pseudogenome_path'])
df = pd.DataFrame({'wgs_id':isolates['wgs_id'].values, 'pseudogenome_path':pseudogenome_paths['pseudogenome_path'].values})

subtree_isolates_pseudogenomes = df.merge(subtree_isolates_df, on = 'wgs_id', how = 'right')

# Get dates
# Load in metadata
gc_metadata = pd.read_csv('/n/holylfs05/LABS/grad_lab/Lab/repos/gc_genomics/metadata/Ng-Combined-Metadata.txt', sep = '\t')

# Merge with information about date
merged = subtree_isolates_pseudogenomes.merge(gc_metadata, on = 'wgs_id', how = 'left', indicator = True)   
metadata = merged[['wgs_id', 'date', 'pseudogenome_path']].copy()
metadata.rename({'wgs_id':'name'}, axis = 'columns', inplace = True)

# Drop the isolates without dates
metadata.dropna(subset = ['date'], inplace = True, ignore_index = True)

# Replace weird date
metadata.loc[metadata['name']=='MA67', 'date'] = '2016-1-01'

date_split = metadata['date'].str.split('-', expand = True)
date_split['month'] = date_split.loc[~date_split[0].isnull(), 1].fillna('6').astype('int').astype('str')
date_split['day'] = date_split.loc[~date_split[0].isnull(), 2].fillna('01')
metadata['reformatted_date'] = date_split[0] + '-' + date_split['month'] + '-' + date_split['day']

# Save isolate names, pseudogenome_paths, and dates

metadata['name'].to_csv('../data/beast/mlst_7827_subtree_isolates.txt', index = None, header = None)
metadata['pseudogenome_path'].to_csv('../data/beast/mlst_7827_subtree_pseudogenomes.txt', index = None, header = None)
metadata[['name', 'reformatted_date']].to_csv('../data/beast/mlst_7827_subtree_dates.dat', sep = '\t', header = False, index = False)