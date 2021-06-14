#!/usr/bin/env awk -f

# usage: ./pfm2pwm.awk -F $'\t' -v 'OFS=\t' pfm.motif > pwm.motif

$0 ~ /^>/ {print;next;}

{print $1*100, $2*100, $3*100, $4*100;}
