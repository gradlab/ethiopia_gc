import pandas as pd
import os

df = pd.read_csv('../data/gubbins/ethiopia_representative_isolates/representative_isolates_pseudogenome_paths.txt', sep = '\t', header = None, names = ['pseudogenome_path'])

for i, row in df.iterrows():
    pseudogenome_path = row['pseudogenome_path']
    dataset_folder = pseudogenome_path[:pseudogenome_path.find('pseudogenomes')]
    basename = os.path.basename(pseudogenome_path)
    if basename.find('_pseudogenome.fasta')>=0:
        wgs_id = basename[:basename.find('_pseudogenome.fasta')]
    else:
        wgs_id = basename[:basename.find('.fasta')]
    df.at[i,'annotation_path'] = dataset_folder + 'annotations/' + wgs_id + '.gff'
    
df['annotation_path'].to_csv('../data/panaroo/representative_isolates_annotation_paths.txt', index = None, header = None)