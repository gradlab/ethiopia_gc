import pandas as pd
import numpy as np
import glob
import os

# Read in tree file
f = open("../data/gubbins/ethiopia_representative_isolates/ethiopia_representative_isolates.final_tree.tre", "r")
tree = (f.read())

# Split the tree to get the subtree
subtree = tree.split('160.5578,')[1]
# subtree = subtree.split('392.235992')[0]
subtree = subtree.split('439.986481')[0]

# Get the isolates in subtree
subtree = subtree.replace('25818_3_234', '25818_3#234')
subtree = subtree.replace('25825_2_43', '25825_2#43')
subtree = subtree.replace('(', '').replace(')', '').split(',')

subtree_isolates = []
for i in subtree:
    isolate = i[:i.find(':')]
    subtree_isolates.append(isolate)
    
subtree_isolates_df = pd.DataFrame({'wgs_id':subtree_isolates})

# Get the pseudogenome_paths
# For representative genomes
isolates = pd.read_csv('../data/gubbins/ethiopia_representative_isolates/representative_isolates.txt', header = None, names = ['wgs_id'])
pseudogenome_paths = pd.read_csv('../data/gubbins/ethiopia_representative_isolates/representative_isolates_pseudogenome_paths.txt', header = None, names = ['pseudogenome_path'])
df1 = pd.DataFrame({'wgs_id':isolates['wgs_id'].values, 'pseudogenome_path':pseudogenome_paths['pseudogenome_path'].values})

# For Ethiopian isolates
pseudogenome_paths = glob.glob('/n/grad_lab2/Lab/gonococcus/datasets/ethiopia_isolates/pseudogenomes/*')
isolates = []
for pseudogenome_path in pseudogenome_paths:
    basename = os.path.basename(pseudogenome_path)
    isolates.append(basename[:basename.find('_pseudogenome')])
df2 = pd.DataFrame({'wgs_id':isolates, 'pseudogenome_path':pseudogenome_paths})
df = pd.concat([df1, df2])

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
metadata.loc[metadata['name']=='MA43', 'date'] = '2016-1-01'

date_split = metadata['date'].str.split('-', expand = True)
date_split['month'] = date_split.loc[~date_split[0].isnull(), 1].fillna('6').astype('int').astype('str')
date_split['day'] = date_split.loc[~date_split[0].isnull(), 2].fillna('01')
metadata['reformatted_date'] = date_split[0] + '-' + date_split['month'] + '-' + date_split['day']

# Save isolate names, pseudogenome_paths, and dates

metadata['name'].to_csv('../data/beast/representative_subtree_to_check_mlst_7827/isolates.txt', index = None, header = None)
metadata['pseudogenome_path'].to_csv('../data/beast/representative_subtree_to_check_mlst_7827/pseudogenomes.txt', index = None, header = None)

metadata_dates = metadata[['name', 'reformatted_date']].copy()
metadata_dates[metadata_dates['name'] == '25818_3#234'] = '25818_3_234'
metadata_dates[metadata_dates['name'] == '25825_2#43'] = '25825_2_43'
metadata_dates.to_csv('../data/beast/representative_subtree_to_check_mlst_7827/dates.dat', sep = '\t', header = False, index = False)