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
print(unique_paths)
unique_paths = np.append(unique_paths, '/n/grad_lab2/Lab/gonococcus/datasets/ethiopia_isolates')

print(unique_paths)

resistance_paths = []
for path in unique_paths:
    resistance_paths = resistance_paths + glob.glob(path + '/resistance/*gc_resistance_alleles.tsv')

# Add the path to the resistance allele information that used to be stored elsewhere

resistance_paths.append('/n/grad_lab2/Lab/gonococcus/analyses/resistance_alleles/2021-10-07_gc_resistance_alleles.tsv')

resistance_df = pd.DataFrame()
for path in resistance_paths:
    resistance_df = pd.concat([resistance_df, pd.read_csv(path, sep = '\t')], ignore_index = True)
    
resistance_df = resistance_df[['wgs_id', 'GyrA_91', 'PBP1_421']]

ethiopia_isolates = pd.read_csv('../data/ethiopia_isolates.txt', sep = '\t', header = None, names = ['wgs_id'])
contemp_global_isolates = pd.read_csv('../data/gubbins/ethiopia_representative_isolates/representative_isolates.txt', sep = '\t', header = None, names = ['wgs_id'])
isolates = pd.concat([ethiopia_isolates, contemp_global_isolates])

print(isolates)

merged = isolates.merge(resistance_df, on = 'wgs_id', how = 'left')

merged.drop_duplicates(inplace = True, ignore_index = True)

merged['GyrA_91'] = merged['GyrA_91'].fillna(value = 'NA')
merged['PBP1_421'] = merged['PBP1_421'].fillna(value = 'NA')

merged['wgs_id'] = merged['wgs_id'].str.replace('#', '_')

print(merged)
# Write itol for GyrA_91

legend = merged[['wgs_id', 'GyrA_91']]
annotation = 'GyrA_91'
sample_name = 'wgs_id'
output_filename = 'itol_representative_isolates_GyrA_91.txt'
output_path = '../data/itol/'

unique_annotations = np.unique(legend[annotation])
unique_annotations = unique_annotations[unique_annotations!='NA']
color_palette = 'PiYG'
colors = sns.color_palette(color_palette, len(unique_annotations)).as_hex()
colors_dict = dict(zip(unique_annotations, colors))
colors_dict['NA'] = '#808080'

# Write itol for PBP1_421

fnc.itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path)

legend = merged[['wgs_id', 'PBP1_421']]
annotation = 'PBP1_421'
sample_name = 'wgs_id'
output_filename = 'itol_representative_isolates_PBP1_421.txt'
output_path = '../data/itol/'

unique_annotations = np.unique(legend[annotation])
unique_annotations = unique_annotations[unique_annotations!='NA']
color_palette = 'BrBG'
colors = sns.color_palette(color_palette, len(unique_annotations)).as_hex()
colors_dict = dict(zip(unique_annotations, colors))
colors_dict['NA'] = '#808080'

fnc.itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path)

# # Save as csv

# merged.to_csv('../data/isolate_info/representative_isolates_resistance_alleles.csv')