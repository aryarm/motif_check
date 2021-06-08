#!/usr/bin/env bash

# extracts coordinates from chrom column

# usage: ./fix_bed.bash broken_bed.tsv > fixed.bed

paste <(cut -d ' ' -f1 "$1") <(paste <(cut -d ' ' -f2 "$1") <(cut -f 2,3 "$1") | awk -F $'\t' -v 'OFS=\t' '{print $1 + $2 - 1, $1 + $3 - 1;}') <(cut -f4- "$1")
