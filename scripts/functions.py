import numpy as np
import os
import pandas as pd
import math
import seaborn as sns

def itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path):
    # Write itol file

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    i = 0
    # legend_labels = []
    # legend_colors = []
    for value, df in legend.groupby(annotation):
        legend.loc[df.index, 'color'] = colors_dict[value]
        # legend_labels.append(str(value))
        # legend_colors.append(colors_dict[value])
        i = i+1
    
    legend_labels = []
    legend_colors = []
    for i in colors_dict:
        legend_labels.append(str(i))
        legend_colors.append(colors_dict[i])

    with open(output_path + output_filename, "w") as itol_file:
        itol_file.write("DATASET_COLORSTRIP\n\n")
        itol_file.write("SEPARATOR TAB\n\n")
        itol_file.write("DATASET_LABEL\t{0}\nCOLOR\t{1}\n\n".format(annotation, list(colors_dict.values())[-1]))
        itol_file.write("LEGEND_TITLE\t{0}\nLEGEND_SHAPES\t{1}\nLEGEND_COLORS\t{2}\nLEGEND_LABELS\t{3}\n\n".format(annotation,
                                                                                                                   "\t".join(['1']*len(legend_labels)),
                                                                                                                    "\t".join(legend_colors),
                                                                                                                    "\t".join(legend_labels)))
        itol_file.write("BORDER_WIDTH\t0.25\nBORDER_COLOR\t#CCCCCC\n\n")
        itol_file.write("DATA\n")
        for i,row in legend.iterrows():
            itol_file.write("{0}\t{1}\t{2}\n".format(row[sample_name], row['color'], row[annotation]))
            
def write_itol_sequence_types(isolates_filename, st_label):
    # Load in information about isolates from sequence type
    isolates = pd.read_csv(isolates_filename, header = None, names = ['wgs_id'])

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
            decades_str.append(str(int(i)))
        else:
            decades_str.append('NA')
    merged['decade'] = decades_str

    metadata = merged.copy()

    metadata['wgs_id'] = metadata['wgs_id'].str.replace('#', '_')

    # Write itol for country
    legend = metadata[['wgs_id', 'continent']]
    annotation = 'continent'
    sample_name = 'wgs_id'
    output_filename = 'itol_' + st_label + '_continent.txt'
    output_path = '../data/itol/'

    unique_annotations = np.unique(metadata[annotation])
    unique_annotations = unique_annotations[unique_annotations!='NA']
    color_palette = 'Paired'
    colors = sns.color_palette(color_palette, len(unique_annotations)).as_hex()
    colors_dict = dict(zip(unique_annotations, colors))
    colors_dict['NA'] = '#808080'

    itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path)

    # Write itol for whether an isolate is from Ethiopia
    metadata['ethiopia'] = 'Not Ethiopia'
    metadata.loc[metadata['country'] == 'Ethiopia', 'ethiopia'] = 'Ethiopia'
    legend = metadata[['wgs_id', 'ethiopia']]
    annotation = 'ethiopia'
    sample_name = 'wgs_id'
    output_filename = 'itol_' + st_label + '_ethiopia.txt'
    output_path = '../data/itol/'

    color_palette = 'Paired'
    colors = sns.color_palette(color_palette).as_hex()
    colors_dict = {'Ethiopia':colors[6], 'Not Ethiopia':'#808080'}

    itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path)

    # Write itol for year                   
    legend = metadata[['wgs_id', 'year']]
    annotation = 'year'
    sample_name = 'wgs_id'
    output_filename = 'itol_' + st_label + '_year.txt'
    output_path = '../data/itol/'

    unique_annotations = np.unique(metadata[annotation])
    unique_annotations = unique_annotations[unique_annotations!='NA']
    color_palette = 'mako'
    colors = sns.color_palette(color_palette, len(unique_annotations)).as_hex()
    colors_dict = dict(zip(unique_annotations, colors))
    colors_dict['NA'] = '#808080'

    itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path)

    # Write itol for decade                   
    legend = metadata[['wgs_id', 'decade']]
    annotation = 'decade'
    sample_name = 'wgs_id'
    output_filename = 'itol_' + st_label + '_decade.txt'
    output_path = '../data/itol/'

    unique_annotations = np.unique(metadata[annotation])
    unique_annotations = unique_annotations[unique_annotations!='NA']
    color_palette = 'mako'
    colors = sns.color_palette(color_palette, len(unique_annotations)).as_hex()
    colors_dict = dict(zip(unique_annotations, colors))
    colors_dict['NA'] = '#808080'

    itol_colorstrip(legend, annotation, sample_name, colors_dict, output_filename, output_path)