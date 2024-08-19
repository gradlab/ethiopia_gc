import glob
import os
import shutil
import numpy as np

# Create folder if it doesn't exist yet
fastqs_folder = '/n/holyscratch01/grad_lab/Users/qinqinyu/20240611_assemble_all_ethiopia_isolates/fastqs/'
if not os.path.exists(fastqs_folder):
    os.mkdir(fastqs_folder)
    
# Rename files
path = '/n/holyscratch01/grad_lab/Users/qinqinyu/20240611_assemble_all_ethiopia_isolates/fastqs_original_names/*.fastq.gz'
filenames = glob.glob(path)
filenames = np.sort(filenames)
for filename in filenames:
    basename = os.path.basename(filename)
    idx = basename.find('_merged')
    idx2 = basename.find('_001')
    new_basename = basename[:idx] + '_' + basename[idx2-1] + '.fastq.gz'
    shutil.copy(filename, fastqs_folder + new_basename)
    
# Rename files that had a different naming convention
os.rename(fastqs_folder + 'ETH12-GCS12L_1.fastq.gz', fastqs_folder + 'Eth12-2021_1.fastq.gz')
os.rename(fastqs_folder + 'ETH12-GCS12L_2.fastq.gz', fastqs_folder + 'Eth12-2021_2.fastq.gz')

os.rename(fastqs_folder + 'ETH21-GCS21U_1.fastq.gz', fastqs_folder + 'Eth21-2022_1.fastq.gz')
os.rename(fastqs_folder + 'ETH21-GCS21U_2.fastq.gz', fastqs_folder + 'Eth21-2022_2.fastq.gz')

os.rename(fastqs_folder + 'ETH32-GCS32F_1.fastq.gz', fastqs_folder + 'Eth32-2022_1.fastq.gz')
os.rename(fastqs_folder + 'ETH32-GCS32F_2.fastq.gz', fastqs_folder + 'Eth32-2022_2.fastq.gz')

os.rename(fastqs_folder + 'ETH52-GCS52Z_1.fastq.gz', fastqs_folder + 'Eth52-2022_1.fastq.gz')
os.rename(fastqs_folder + 'ETH52-GCS52Z_2.fastq.gz', fastqs_folder + 'Eth52-2022_2.fastq.gz')

os.rename(fastqs_folder + 'ETH69-GCS69_1.fastq.gz', fastqs_folder + 'Eth69-2023_1.fastq.gz')
os.rename(fastqs_folder + 'ETH69-GCS69_2.fastq.gz', fastqs_folder + 'Eth69-2023_2.fastq.gz')

os.rename(fastqs_folder + 'ETH78-GCS78_1.fastq.gz', fastqs_folder + 'Eth78-2023_1.fastq.gz')
os.rename(fastqs_folder + 'ETH78-GCS78_2.fastq.gz', fastqs_folder + 'Eth78-2023_2.fastq.gz')