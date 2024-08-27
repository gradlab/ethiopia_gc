import pandas as pd
import numpy as np
from Bio import SeqIO
import glob
import os

results_all = pd.DataFrame()

# Load blast results
filenames = glob.glob('../data/ggi/blast_results/*.txt')
filenames = np.sort(filenames)

# Loop through files (one for each ggi query gene)
for filename in filenames:
    basename = os.path.basename(filename)
    gene = basename[:basename.find('.txt')]

    # Load blast result
    results = pd.read_csv('../data/ggi/blast_results/' + gene + '.txt', delimiter = '\t', names = ['query', 'subject', 'percent_identity', 'alignment_length', 'mismatches', 'gap_openings', 'query_start', 'query_end', 'subject_start', 'subject_end', 'evalue', 'bit_score'])

    # Get gene length and calculate percent of gene that was aligned in each hit
    records = list(SeqIO.parse("../data/ggi/MS11_ggi_cds/" + gene + ".fa", "fasta"))[0]
    results['strain'] = results['subject'].str.split('_', expand = True)[0]
    results['query_length'] = len(records.seq)
    results['alignment_percent'] = 100*results['alignment_length']/results['query_length']

    results_all = pd.concat([results_all, results])

results_all.reset_index(inplace = True, drop = True)

# Filter to only blast alignments that are >=50% the length of the gene
results_all = results_all[results_all['alignment_percent']>=50]
results_all.reset_index(inplace = True, drop = True)

# Get the percentage of ggi genes found for each strain
strains = []
num_ggi_genes = []
for strain, df in results_all.groupby('strain'):
    strains.append(strain)
    num_ggi_genes.append(len(np.unique(df['query'])))  
ggi_summary = pd.DataFrame({'strain':strains, 'num_ggi_genes':num_ggi_genes, 'percentage_ggi_genes':100*np.array(num_ggi_genes)/61})

# Save to file
ggi_summary.to_csv('../data/ggi/blast_results_summary.csv')