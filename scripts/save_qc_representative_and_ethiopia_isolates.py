import pandas as pd

# Read in list of representative isolates and all metadata
rep_isolates = pd.read_csv('../data/gubbins/ethiopia_representative_isolates/representative_isolates.txt', header = None, names = ['wgs_id'])
metadata = pd.read_csv('/n/holylfs05/LABS/grad_lab/Lab/repos/gc_genomics/metadata/Ng-Combined-Metadata.txt', sep = '\t')

# Merge and save
rep_isolates_metadata = rep_isolates.merge(metadata, on = 'wgs_id', how = 'left')
rep_isolates_metadata = rep_isolates_metadata[['wgs_id', 'accession', 'names', 'reference', 'date', 'continent', 'assembly_length', 'assembly_coverage', 'contigs', 'reference_coverage', 'reference_percentage_mapped', 'percent_missing']]

rep_isolates_metadata.to_csv('../data/isolates_summary_and_qc/representative_isolates_accession_and_qc.csv', index = None)

# Save metadata for Ethiopia isolates
eth_metadata = metadata[metadata['reference'] == 'ethiopia_isolates']
eth_metadata = eth_metadata[['wgs_id', 'date', 'assembly_length', 'assembly_coverage', 'contigs', 'reference_coverage', 'reference_percentage_mapped', 'percent_missing']]
eth_metadata.to_csv('../data/isolates_summary_and_qc/ethiopia_isolates_qc.csv', index = None)