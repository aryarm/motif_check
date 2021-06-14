#!/usr/bin/env python

# ex usage:  cat nrf1.jaspar | ./jaspar2motif.py $(awk -F $'\t' '$9 < 0.01' lr_results.tsv | cut -d ' ' -f1 | paste -s -d ' ') | sed '/^>/ s/>/>\t/; /^>/ s/$/\t7.5/' > nrf1.motif

import sys
import argparse
import Bio.motifs.jaspar as jaspar
from Bio.motifs import clusterbuster


parser = argparse.ArgumentParser()
parser.add_argument('motifs', nargs='*', default=None)
args = parser.parse_args()


sys.stdout.write(
	jaspar.write([
		motif for motif in clusterbuster.read(
			sys.stdin
		) if (not args.motifs) or (motif.name in args.motifs)
	], format = 'jaspar')
)
