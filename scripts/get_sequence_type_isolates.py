import pandas as pd
import numpy as np
import glob
import os
import shutil

# Load MLST and NG-STAR typing results
results = pd.read_csv('../data/mlst_ngstar_all_genomes.tsv', sep = '\t')
results['wgs_id'] = results['strain'].str.split('_contigs_filtered.fa', expand = True)[0]
results.drop('strain', axis = 'columns', inplace = True)

# Load metadata
ng_metadata = pd.read_csv('/n/holylfs05/LABS/grad_lab/Lab/repos/gc_genomics/metadata/Ng-Combined-Metadata.txt', sep = '\t')

# Get all assembly filenames
assembly_filenames = glob.glob('/n/grad_lab2/Lab/gonococcus/datasets/*/assemblies/*_contigs_filtered.fa')

# Merge the assembly filenames with the typing results
strains = []
for filename in assembly_filenames:
    basename = os.path.basename(filename)
    strain = basename[:basename.find('_contigs_filtered.fa')]
    strains.append(strain)
assembly_df = pd.DataFrame({'wgs_id':strains, 'assembly_path':assembly_filenames})

results = results.merge(assembly_df, on = 'wgs_id')

# Merge with metadata
merged_indicator = results.merge(ng_metadata, on = 'wgs_id', how = 'outer', indicator = True)
merged = results.merge(ng_metadata, on = 'wgs_id')

# Drop duplicates
merged_indicator.drop_duplicates(subset = 'wgs_id', inplace = True, ignore_index = True)
merged.drop_duplicates(subset = 'wgs_id', inplace = True, ignore_index = True)

# Remove the Ethiopian isolates sequenced by our lab
merged_indicator.drop(merged_indicator[merged_indicator['reference']=='ethiopia_isolates_grad_lab'].index, inplace = True)
merged_indicator.reset_index(inplace = True, drop = True)

merged.drop(merged[merged['reference']=='ethiopia_isolates_grad_lab'].index, inplace = True)
merged.reset_index(inplace = True, drop = True)

# Get the NG-STAR and MLST types represented in the Ethiopian isolates
ngstars = []
num_isolates = []
for ngstar, df in merged[merged['reference'] == 'ethiopia_isolates'].groupby('NG-STAR'):
    ngstars.append(ngstar)
    num_isolates.append(len(df))
ethiopia_ngstar = pd.DataFrame({'NG-STAR':ngstars, 'num_isolates':num_isolates})
ethiopia_ngstar.sort_values('num_isolates', ascending = False, ignore_index = True, inplace = True)

mlsts = []
num_isolates = []
for mlst, df in merged[merged['reference'] == 'ethiopia_isolates'].groupby('MLST'):
    mlsts.append(mlst)
    num_isolates.append(len(df))
ethiopia_mlst = pd.DataFrame({'MLST':mlsts, 'num_isolates':num_isolates})
ethiopia_mlst.sort_values('num_isolates', ascending = False, ignore_index = True, inplace = True)

# Check that the genomes with ST results are in the metadata table (do manually for each of the STs that I'm interested in)

global_mlst = merged_indicator[merged_indicator['MLST'] == '7827']
for i, row in global_mlst[global_mlst['_merge'] == 'left_only'][['wgs_id', 'reference', 'assembly_path']].iterrows():
    print(row.values)
    
# Get the top 2 MLST types from Ethiopian isolates
top_ethiopia_mlst = ethiopia_mlst.iloc[0:2]

# Get the top 3 NG-STAR types from Ethiopian isolates
top_ethiopia_ngstar = ethiopia_ngstar.iloc[0:3]

# Copy pseudogenomes for MLST types
for i, row in top_ethiopia_mlst.iterrows():
    global_mlst = merged[merged['MLST'] == row['MLST']]
    assembly_path_split = global_mlst['assembly_path'].str.split('/', expand = True)
    pseudogenome_path_split = assembly_path_split[[1, 2, 3, 4, 5, 6]]
    pseudogenome_path_split[7] = 'pseudogenomes/' + global_mlst['wgs_id']
    global_mlst['pseudogenome_path'] = '/' + pseudogenome_path_split[1] + '/' + pseudogenome_path_split[2] + '/' + pseudogenome_path_split[3] + '/' + pseudogenome_path_split[4] + '/' + pseudogenome_path_split[5] + '/' + pseudogenome_path_split[6] + '/' + pseudogenome_path_split[7] + '_pseudogenome.fasta'
    global_mlst['alternate_pseudogenome_path'] = '/' + pseudogenome_path_split[1] + '/' + pseudogenome_path_split[2] + '/' + pseudogenome_path_split[3] + '/' + pseudogenome_path_split[4] + '/' + pseudogenome_path_split[5] + '/' + pseudogenome_path_split[6] + '/' + pseudogenome_path_split[7] + '.fasta'
    print('MLST:', row['MLST'], ', num genomes:', len(global_mlst))
    mlst_scratch_path = '/n/holyscratch01/grad_lab/Users/qinqinyu/20240620_tree_ethiopia_isolates_sequence_types/' + 'mlst_' + row['MLST']
    if not os.path.exists(mlst_scratch_path):
        os.mkdir(mlst_scratch_path)
        os.mkdir(mlst_scratch_path + '/pseudogenomes')
    wgs_ids = []
    pseudogenome_paths = []
    for j, row2 in global_mlst.iterrows():
        if os.path.exists(row2['pseudogenome_path']):
            shutil.copy(row2['pseudogenome_path'], mlst_scratch_path + '/pseudogenomes')
            pseudogenome_paths.append(row2['pseudogenome_path'])
        else:
            shutil.copy(row2['alternate_pseudogenome_path'], mlst_scratch_path + '/pseudogenomes')
            pseudogenome_paths.append(row2['alternate_pseudogenome_path'])
        wgs_ids.append(row2['wgs_id'])
    
    if not os.path.exists('../data/gubbins/mlst/' + row['MLST']):
        os.mkdir('../data/gubbins/mlst/' + row['MLST'])
    pd.DataFrame(wgs_ids).to_csv('../data/gubbins/mlst/' + row['MLST'] + '/isolates.txt', index = False, header = False)
    pd.DataFrame(pseudogenome_paths).to_csv('../data/gubbins/mlst/' + row['MLST'] + '/pseudogenome_paths.txt', index = False, header = False)
    
# Copy pseudogenomes for NG-STAR types
for i, row in top_ethiopia_ngstar.iterrows():
    global_ngstar = merged[merged['NG-STAR'] == row['NG-STAR']]
    assembly_path_split = global_ngstar['assembly_path'].str.split('/', expand = True)
    pseudogenome_path_split = assembly_path_split[[1, 2, 3, 4, 5, 6]]
    pseudogenome_path_split[7] = 'pseudogenomes/' + global_ngstar['wgs_id']
    global_ngstar['pseudogenome_path'] = '/' + pseudogenome_path_split[1] + '/' + pseudogenome_path_split[2] + '/' + pseudogenome_path_split[3] + '/' + pseudogenome_path_split[4] + '/' + pseudogenome_path_split[5] + '/' + pseudogenome_path_split[6] + '/' + pseudogenome_path_split[7] + '_pseudogenome.fasta'
    global_ngstar['alternate_pseudogenome_path'] = '/' + pseudogenome_path_split[1] + '/' + pseudogenome_path_split[2] + '/' + pseudogenome_path_split[3] + '/' + pseudogenome_path_split[4] + '/' + pseudogenome_path_split[5] + '/' + pseudogenome_path_split[6] + '/' + pseudogenome_path_split[7] + '.fasta'
    print('NG-STAR:', row['NG-STAR'], ', num genomes:', len(global_ngstar))
    ngstar_scratch_path = '/n/holyscratch01/grad_lab/Users/qinqinyu/20240620_tree_ethiopia_isolates_sequence_types/' + 'ngstar_' + row['NG-STAR']
    if not os.path.exists(ngstar_scratch_path):
        os.mkdir(ngstar_scratch_path)
        os.mkdir(ngstar_scratch_path + '/pseudogenomes')
    wgs_ids = []
    pseudogenome_paths = []
    for j, row2 in global_ngstar.iterrows():
        if os.path.exists(row2['pseudogenome_path']):
            shutil.copy(row2['pseudogenome_path'], ngstar_scratch_path + '/pseudogenomes')
            pseudogenome_paths.append(row2['pseudogenome_path'])
        else:
            shutil.copy(row2['alternate_pseudogenome_path'], ngstar_scratch_path + '/pseudogenomes')
            pseudogenome_paths.append(row2['alternate_pseudogenome_path'])
        wgs_ids.append(row2['wgs_id'])
    
    if not os.path.exists('../data/gubbins/ngstar/' + row['NG-STAR']):
        os.mkdir('../data/gubbins/ngstar/' + row['NG-STAR'])
    pd.DataFrame(wgs_ids).to_csv('../data/gubbins/ngstar/' + row['NG-STAR'] + '/isolates.txt', index = False, header = False)
    pd.DataFrame(pseudogenome_paths).to_csv('../data/gubbins/ngstar/' + row['NG-STAR'] + '/pseudogenome_paths.txt', index = False, header = False)