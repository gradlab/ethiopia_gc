import pandas as pd
import numpy as np
import math
import glob
import seaborn as sns
import functions as fnc

pseudogenome_paths = pd.read_csv('../data/gubbins/ethiopia_representative_isolates/representative_isolates_pseudogenome_paths.txt', header = None, names = ['pseudogenome'])['pseudogenome'].values

paths = []
for path in pseudogenome_paths:
    paths.append("/".join(path.split('/')[:-2]))
    
unique_paths = np.unique(paths)
unique_paths = np.append(unique_paths, '/n/grad_lab2/Lab/gonococcus/datasets/ethiopia_isolates')

# Get the porB1b strains
porB1b_paths = []
for path in unique_paths:
    porB1b_paths = porB1b_paths + glob.glob(path + '/resistance/porB1b_SNPs.txt')

# Add the path to the resistance allele information that used to be stored elsewhere
porB1b_paths.append('/n/grad_lab2/Lab/gonococcus/analyses/resistance_alleles/2021-10-07_porB1b_SNPs.txt')

porB1b_df = pd.DataFrame()
for path in porB1b_paths:
    porB1b_df = pd.concat([porB1b_df, pd.read_csv(path, sep = '\t')], ignore_index = True)
    
porB1b_df['porB'] = 'porB1b'

# Get the porB1b strains

porB1a_paths = []
for path in unique_paths:
    porB1a_paths = porB1a_paths + glob.glob(path + '/resistance/porB1a_SNPs.txt')

# Add the path to the resistance allele information that used to be stored elsewhere
porB1a_paths.append('/n/grad_lab2/Lab/gonococcus/analyses/resistance_alleles/2021-10-07_porB1a_SNPs.txt')

porB1a_df = pd.DataFrame()
for path in porB1a_paths:
    porB1a_df = pd.concat([porB1a_df, pd.read_csv(path, sep = '\t')], ignore_index = True)

porB1a_df['porB'] = 'porB1a'

resistance_df = pd.concat([porB1a_df, porB1b_df])
    
resistance_df = resistance_df[['wgs_id', 'porB']]

ethiopia_isolates = pd.read_csv('../data/ethiopia_isolates.txt', sep = '\t', header = None, names = ['wgs_id'])
contemp_global_isolates = pd.read_csv('../data/gubbins/ethiopia_representative_isolates/representative_isolates.txt', sep = '\t', header = None, names = ['wgs_id'])
isolates = pd.concat([ethiopia_isolates, contemp_global_isolates])
    
merged = isolates.merge(resistance_df, on = 'wgs_id', how = 'left')

merged.drop_duplicates(inplace = True, ignore_index = True)

merged['porB'] = merged['porB'].fillna(value = 'NA')
# merged['PBP1_421'] = merged['PBP1_421'].fillna(value = 'NA')

merged['wgs_id'] = merged['wgs_id'].str.replace('#', '_')

# Write itol for porB

legend = merged[['wgs_id', 'porB']]
annotation = 'porB'
sample_name = 'wgs_id'
output_filename = 'itol_representative_isolates_porB.txt'
output_path = '../data/itol/'

unique_annotations = np.unique(legend[annotation])
unique_annotations = unique_annotations[unique_annotations!='NA']
color_palette = 'viridis'
colors = sns.color_palette(color_palette, len(unique_annotations)).as_hex()
colors_dict = dict(zip(unique_annotations, colors))
colors_dict['NA'] = '#808080'

fnc.itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path)