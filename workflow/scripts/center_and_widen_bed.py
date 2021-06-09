#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd
from meirlop.io import read_fasta

# Set half-width for sequence and DNase-seq coverage
# for meirlop: 150
# for scanMotifsGenomeWide: 650
# for calculating confusion matrix: 50
dhs_width = int(sys.argv[2])

# Read DHS intercals and set genome fasta
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
dnase_bed_df['name'] = dnase_bed_df['chrom'].astype(str) + ':' + dnase_bed_df['center'].astype(str)
# These are unstanded so we stick to + strand
dnase_bed_df['strand'] = '+'

# Get interval for sequence and DNase-seq coverage
dnase_bed_df['start'] = dnase_bed_df['center'] - dhs_width
dnase_bed_df['end'] = dnase_bed_df['center'] + dhs_width

# Sort and preview
dnase_bed_df = dnase_bed_df.sort_values(by = ['chrom', 'start']).reset_index(drop = True).copy()

dnase_bed_df.drop(['original_start', 'original_end', 'center'], axis=1, inplace=True)

dhs_wide_filename = 'temporary_data/dhs_wide.bed'
dnase_bed_df.to_csv(
    sys.stdout, 
    sep = '\t', 
    index = False, 
    header = None
)
