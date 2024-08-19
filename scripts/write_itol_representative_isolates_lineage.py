import pandas as pd
import numpy as np
import seaborn as sns
import functions as fnc

# Read in tree file
f = open("../data/gubbins/ethiopia_representative_isolates/ethiopia_representative_isolates.final_tree.tre", "r")
tree = (f.read())

# Split the tree at the most basal branch into lineages A and B
linA_str = tree.split('18.283104,')[0]
linB_str = tree.split('18.283104,')[1]

# Get the isolates in lineage A
linA_str = linA_str.replace('(', '').replace(')', '').split(',')

linA_isolates = []
for i in linA_str:
    isolate = i[:i.find(':')]
    linA_isolates.append(isolate)

# Get the isolates in lineage B
linB_str = linB_str.replace('(', '').replace(')', '').split(',')

linB_isolates = []
for i in linB_str:
    isolate = i[:i.find(':')]
    linB_isolates.append(isolate)
    
# Save into a dataframe
linA_df = pd.DataFrame(linA_isolates, columns = ['wgs_id'])
linA_df['lineage'] = 'A'

linB_df = pd.DataFrame(linB_isolates, columns = ['wgs_id'])
linB_df['lineage'] = 'B'

lin_df = pd.concat([linA_df, linB_df], ignore_index = True)

# Write itol file
legend = lin_df.copy()
annotation = 'lineage'
sample_name = 'wgs_id'
output_filename = 'itol_representative_isolates_lineage.txt'
output_path = '../data/itol/'

unique_annotations = np.unique(legend[annotation])
unique_annotations = unique_annotations[unique_annotations!='NA']
color_palette = 'Paired'
colors = sns.color_palette(color_palette, len(unique_annotations)).as_hex()
colors_dict = dict(zip(unique_annotations, colors))

fnc.itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path)