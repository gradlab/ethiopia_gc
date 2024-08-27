from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

records = list(SeqIO.parse("../data/ggi/MS11_ggi_cds_all.fa", "fasta"))

genes = []

for record in records:
    description = record.description
    gene = description.split(' ')[1].split('=')[1][:-1]
    seq = record.seq
    new_record = SeqRecord(seq, id=gene, description = '')
    SeqIO.write(new_record, "../data/ggi/MS11_ggi_cds/" + gene + ".fa", "fasta")
    genes.append(gene)
    
f = open("../data/ggi/ggi_genes.txt", "w")
f.write('\n'.join(genes))
f.close()