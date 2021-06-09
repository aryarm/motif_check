#!/usr/bin/env bash

# An example bash script demonstrating how to run the entire snakemake pipeline
# This script creates two separate log files:
# 	1) log - the basic snakemake log of completed rules
# 	2) qlog - a more detailed log of the progress of each rule and any errors

# Before running the snakemake pipeline, remember to complete the config.yaml
# file in the config/ folder with the required input info.
# Make sure that this script is executed from the directory that it lives in!

# you should specify a directory for all output here, rather than in the config
# this will override whichever output directory appears in the config
out_path="out"
mkdir -p "$out_path"/log

# clear leftover log files
if [ -f "$out_path/log" ]; then
	echo ""> "$out_path/log/log";
fi
if [ -f "$out_path/qlog" ]; then
	echo ""> "$out_path/log/qlog";
fi

snakemake \
--config out="$out_path" \
--latency-wait 60 \
--conda-frontend conda \
--use-conda \
-k \
-j 12 \
"$@" 2>"$out_path/log/log" >"$out_path/log/qlog"

# message the user on slack if possible
exit_code="$?"
if command -v 'slack' &>/dev/null; then
    if [ "$exit_code" -eq 0 ]; then
        slack "flower-mapping pipeline finished successfully" &>/dev/null
    else
        slack "flower-mapping pipeline exited with error code $exit_code"
    fi
fi
exit "$exit_code"
