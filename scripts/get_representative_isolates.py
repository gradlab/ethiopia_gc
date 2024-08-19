import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# Load data

df = pd.read_csv('/n/grad_lab2/Lab/gonococcus/analyses/gc_clusters/gc_clusters_clusters.csv')
metadata = pd.read_csv('/n/holylfs05/LABS/grad_lab/Lab/repos/gc_genomics/metadata/Ng-Combined-Metadata.txt', delimiter = '\t')

print('Number of clusters in poppunk database: ', len(np.unique(df['Cluster'])))

representative_isolates = []
clusters = []
query_cols = ['wgs_id', 'accession', 'names']
i = 0
did_not_meet_qc = 0
no_isolates_found = 0
did_not_meet_qc_array = np.array([])
no_isolates_found_array = np.array([])

for cluster, df_cluster in df.groupby('Cluster'):
    
    # Get the metadata rows corresponding to the isolates in the cluster
    metadata_cluster = metadata[metadata['wgs_id'].isin(df_cluster['Taxon'])]
    
    # Basic filtering of QC
    metadata_cluster_qc = metadata_cluster[
    (metadata_cluster['reference_coverage']>40)&
    (metadata_cluster['reference_percentage_mapped']>80)&
    (metadata_cluster['assembly_length']>1.75*10**6)&
    (metadata_cluster['assembly_length']<2.5*10**6)&
    (metadata_cluster['percent_missing']<12)]

    # Sort based on fewest contigs and prioritizing isolates in the lab
    metadata_cluster_qc = metadata_cluster_qc.sort_values(by = ['isolate_in_lab', 'contigs'], ascending=[False, True])
    metadata_cluster_qc.reset_index(inplace = True, drop = True)
    
    if len(metadata_cluster_qc)>0:
        representative_isolate = metadata_cluster_qc.iloc[0]['wgs_id']
        representative_isolates.append(representative_isolate)
        clusters.append(cluster)
    elif len(metadata_cluster)>0:
        did_not_meet_qc_array=np.concatenate((did_not_meet_qc_array, metadata_cluster['wgs_id'].values))
        did_not_meet_qc+=1
    else:
        no_isolates_found_array=np.concatenate((no_isolates_found_array, df_cluster['Taxon'].values))
        no_isolates_found+=1
        
print('Clusters with no isolates that met QC: ', did_not_meet_qc)
print('Clusters with no isolates found in metadata table (using wgs_id column): ', no_isolates_found)
print(no_isolates_found_array)
print('Number of clusters with representative isolates found: ', len(representative_isolates))

isolates = representative_isolates.copy()
# Remove duplicates
print('Number of isolates before removing duplicates: ', len(isolates))
isolates = np.unique(isolates)
print('Number of isolates after removing duplicates: ', len(isolates))

# Remove duplicates of WHO strains that are under a different name
who_alternate_names = np.array(['SRR1661324', 'SRR1661325', 'SRR1661326', 'SRR1661327', 'SRR1661328', 'SRR1661329', 'SRR1661330', 'SRR1661331'])
isolates = np.setdiff1d(isolates, who_alternate_names, assume_unique=True)
print('Number of isolates after removing WHO strains that are under a different name: ', len(isolates))

# Remove Ethiopian isolates that our lab sequenced
print(len(isolates))
isolates = [x for x in isolates if x.find('GCs')<0]
print('Final number of isolates after removing Ethiopian isolates that our lab sequenced: ', len(isolates))

# Get the paths for the pseudogenomes

paths = []

# Priority of locations if a sequence is found in multiple folders
# Ordering of publications is based off of the publication that referenced in metadata table for the isolates that are found in "duplicate" paths
# Put refseq at end because those were using simulated reads
# Note that I did simulate reads for all the WHO strains, which are the ones used here

priority_folders = np.array(['lab_strains', 'sss_project', 'umass_dgi', 'unemo_2016_WHO', 'golparian_2020_historic', 'sanchez_buso_2018_global', 'eyre_2017_brighton', 'desilva_2017_brighton', 'demczuk_2015_canada_cro', 'demczuk_2016_canada_azi', 'refseq'])
for isolate in isolates: 
    isolate_paths = glob.glob('/n/grad_lab2/Lab/gonococcus/datasets/*/pseudogenomes/' + isolate + '_pseudogenome.fasta')
    isolate_paths = isolate_paths + glob.glob('/n/grad_lab2/Lab/gonococcus/datasets/*/pseudogenomes/' + isolate + '.fasta')
    if len(isolate_paths)==1:
        paths.append(isolate_paths[0])
    elif len(isolate_paths)==0:
        print(isolate)
        print('no path found for pseudogenome')
    elif len(isolate_paths)>1:
        path_orders = []
        for isolate_path in isolate_paths:
            folder = isolate_path.split('/')[6]
            path_orders.append(np.where(priority_folders==folder)[0][0])
        paths.append(isolate_paths[np.argmin(path_orders)])
        
# Write the isolate names and pseudogenome locations to file

with open('../data/gubbins/ethiopia_representative_isolates/representative_isolates.txt', "w") as outfile:
    for isolate in isolates:
        outfile.write(isolate + "\n")
        
with open('../data/gubbins/ethiopia_representative_isolates/representative_isolates_pseudogenome_paths.txt', "w") as outfile:
    for path in paths:
        outfile.write(path + "\n")