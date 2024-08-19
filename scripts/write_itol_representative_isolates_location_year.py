import pandas as pd
import numpy as np
import math
import seaborn as sns

import functions as fnc

# Load in information about Ethiopia isolates
ethiopia_isolates = pd.read_csv('../data/ethiopia_isolates.txt', header = None, names = ['wgs_id'])

# Load in information about representative isolates
contemp_global_isolates = pd.read_csv('../data/gubbins/ethiopia_representative_isolates/representative_isolates.txt', header = None, names = ['wgs_id'])

isolates = pd.concat([ethiopia_isolates, contemp_global_isolates])

# Load in metadata
gc_metadata = pd.read_csv('/n/holylfs05/LABS/grad_lab/Lab/repos/gc_genomics/metadata/Ng-Combined-Metadata.txt', sep = '\t')

# Merge with information about location and year
merged = isolates.merge(gc_metadata, on = 'wgs_id', how = 'left', indicator = True)
merged = merged[['wgs_id', 'date', 'continent', 'country']]
merged['year'] = merged['date'].str.split('-', expand = True)[0]
# merged['decade'] = round(merged['year'].astype('float'), ndigits = -1)
merged['decade'] = merged['year'].astype('float') - (merged['year'].astype('float')%10)

merged.drop('date', axis = 'columns', inplace = True)
merged.fillna('NA', inplace = True)
decades_str = []
for i in merged['decade']:
    if i!='NA':
        print(i)
        decades_str.append(str(int(i)))
    else:
        decades_str.append('NA')
merged['decade'] = decades_str

print(np.unique(merged['decade']))

metadata = merged.copy()

metadata['wgs_id'] = metadata['wgs_id'].str.replace('#', '_')
                   
# Write itol for country
legend = metadata[['wgs_id', 'continent']]
annotation = 'continent'
sample_name = 'wgs_id'
output_filename = 'itol_representative_isolates_continent.txt'
output_path = '../data/itol/'

unique_annotations = np.unique(metadata[annotation])
unique_annotations = unique_annotations[unique_annotations!='NA']
color_palette = 'Paired'
colors = sns.color_palette(color_palette, len(unique_annotations)).as_hex()
colors_dict = dict(zip(unique_annotations, colors))
colors_dict['NA'] = '#808080'

fnc.itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path)

# Write itol for whether an isolate is from Ethiopia
metadata['ethiopia'] = 'Representative genomes'
metadata.loc[metadata['country'] == 'Ethiopia', 'ethiopia'] = 'Ethiopia'
legend = metadata[['wgs_id', 'ethiopia']]
annotation = 'ethiopia'
sample_name = 'wgs_id'
output_filename = 'itol_representative_isolates_ethiopia.txt'
output_path = '../data/itol/'

color_palette = 'Paired'
colors = sns.color_palette(color_palette).as_hex()
colors_dict = {'Ethiopia':colors[6], 'Representative genomes':'#808080'}

fnc.itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path)

# Write itol for year                   
legend = metadata[['wgs_id', 'year']]
annotation = 'year'
sample_name = 'wgs_id'
output_filename = 'itol_representative_isolates_year.txt'
output_path = '../data/itol/'

unique_annotations = np.unique(metadata[annotation])
unique_annotations = unique_annotations[unique_annotations!='NA']
color_palette = 'mako'
colors = sns.color_palette(color_palette, len(unique_annotations)).as_hex()
colors_dict = dict(zip(unique_annotations, colors))
colors_dict['NA'] = '#808080'

fnc.itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path)

# Write itol for decade                   
legend = metadata[['wgs_id', 'decade']]
annotation = 'decade'
sample_name = 'wgs_id'
output_filename = 'itol_representative_isolates_decade.txt'
output_path = '../data/itol/'

unique_annotations = np.unique(metadata[annotation])
unique_annotations = unique_annotations[unique_annotations!='NA']
color_palette = 'mako'
colors = sns.color_palette(color_palette, len(unique_annotations)).as_hex()
colors_dict = dict(zip(unique_annotations, colors))
colors_dict['NA'] = '#808080'

fnc.itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path)
