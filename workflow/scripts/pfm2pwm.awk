#!/usr/bin/env awk -f

# usage: ./pfm2pwm.awk -F $'\t' -v 'OFS=\t' pfm.motif > pwm.motif

$0 ~ /^>/ {print;next;}

{sum=0; for(i=1; i<=NF; i++) sum += $i; print $1/sum, $2/sum, $3/sum, $4/sum;}
