#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd
from meirlop.io import read_fasta

# Set half-width for sequence and DNase-seq coverage
# for meirlop: 150
# for scanMotifsGenomeWide: 650
# for calculating confusion matrix: 50
dhs_width = int(sys.argv[3])

concat_chrom=bool(int(sys.argv[4]))

# Read DHS intercals and set genome fasta
genome_fa_filepath = sys.argv[2]
dnase_bed_df = pd.read_csv(
    sys.argv[1],
    sep = '\t', 
    header = None, 
    low_memory = False,
    names = (
        'chrom '
        'start '
        'end '
        'name '
        'score '
        'strand '
        'signal '
        'pval '
        'qval '
        'peak'
    ).split(' ')
)

# Center DHS
dnase_bed_df['original_start'] = dnase_bed_df['start']
dnase_bed_df['original_end'] = dnase_bed_df['end']
dnase_bed_df['center'] = dnase_bed_df['original_start'] + dnase_bed_df['peak']

# Rename DHS
dnase_bed_df['score'] = dnase_bed_df['signal']
dnase_bed_df['dhs_signal'] = dnase_bed_df['score']

# These are unstanded so we stick to + strand
dnase_bed_df['strand'] = '+'

# Get interval for sequence and DNase-seq coverage
dnase_bed_df['start'] = dnase_bed_df['center'] - dhs_width
dnase_bed_df['end'] = dnase_bed_df['center'] + dhs_width

if concat_chrom:
    dnase_bed_df['name'] = dnase_bed_df['chrom'].astype(str) + ':'  + dnase_bed_df['center'].astype(str)
else:
    dnase_bed_df['name'] = dnase_bed_df['chrom'].astype(str) + ' '  + dnase_bed_df['start'].astype(str) + ' ' + dnase_bed_df['end'].astype(str)

# Sort and preview
dnase_bed_df = dnase_bed_df.sort_values(by = ['chrom', 'start']).reset_index(drop = True).copy()

with open(genome_fa_filepath) as genome_fa_file:
    genome_fa_dict = read_fasta(genome_fa_file)
mask_softmasked_sequence = lambda sequence: ''.join([nuc if nuc in list('ACGT') else 'N' for nuc in sequence])
get_sequence = lambda chromosome, start, end: mask_softmasked_sequence(genome_fa_dict[chromosome][start:end]) if chromosome in genome_fa_dict else np.nan

# Name DHS and assign sequence
dnase_bed_df['peak_id'] = dnase_bed_df['name']
dnase_bed_df['sequence'] = dnase_bed_df['chrom start end'.split(' ')].apply(tuple, axis = 1).apply(lambda x: get_sequence(*x))
dnase_bed_df.dropna(subset=['sequence'], inplace=True)


# Helper function to create a scored FASTA entry
get_scored_fa_entry = lambda peak_id, score, sequence: f'>{peak_id} {score}\n{sequence}'

# Write both histone ratios into scored FASTA files
with sys.stdout as scored_fasta_file:
    scored_fasta_file.write(
        '\n'.join(
            list(
    	        dnase_bed_df[
                    f'peak_id signal sequence'.split(' ')
                ]
                .apply(tuple, axis = 1)
                .apply(lambda x: get_scored_fa_entry(*x))
            )
	    ) + '\n'
    )
