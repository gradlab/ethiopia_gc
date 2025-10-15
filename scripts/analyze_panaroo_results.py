import pandas as pd

# Read in panaroo results
panaroo = pd.read_csv('../data/panaroo/gene_presence_absence.csv')

# Get all of the wgs id's
wgs_id_all = panaroo.columns.drop(['Gene', 'Non-unique Gene name', 'Annotation'])

# Get all of the Ethiopia isolate wgs id's
wgs_id_eth = wgs_id_all[wgs_id_all.str.contains('Eth')]

# Get all of the non-Ethiopia isolate wgs id's
wgs_id_rep = wgs_id_all[~wgs_id_all.str.contains('Eth')]

# Checking if there are any genes where the representative isolates don't have the accessory genes but the Ethiopian isolates do
print(panaroo[panaroo[wgs_id_rep].isnull().all(axis = 'columns')][wgs_id_eth].values)