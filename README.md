[![Snakemake](https://img.shields.io/badge/snakemake-6.4.1-brightgreen.svg?style=flat-square)](https://snakemake.readthedocs.io/)
[![License](https://img.shields.io/apm/l/vim-mode.svg)](LICENSE)

# motif_check
Evaluate de novo motif finding tools. Create precision/recall plots and compute performance metrics, by labeling motifs around ChIP-seq summits as positives.

# download
Execute the following command or download the [latest release](https://github.com/aryarm/motif_check/releases/latest) manually.
```
git clone https://github.com/aryarm/motif_check.git
```
Also consider downloading the [example data](https://github.com/aryarm/motif_check/releases/latest/download/data.tar.gz).
```
cd motif_check
wget -O- -q https://github.com/aryarm/motif_check/releases/latest/download/data.tar.gz | tar xvzf -
```

# setup
The pipeline is written as a Snakefile which can be executed via [Snakemake](https://snakemake.readthedocs.io). We recommend installing version 6.4.1:
```
conda create -n snakemake -c bioconda -c conda-forge --no-channel-priority 'snakemake==6.4.1'
```
We highly recommend you install [Snakemake via conda](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html#installation-via-conda) like this so that you can use the `--use-conda` flag when calling `snakemake` to let it [automatically handle all dependencies](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html#integrated-package-management) of the pipeline. Otherwise, you must manually install the dependencies listed in the [env files](envs).

# execution
1. Activate snakemake via `conda`:
    ```
    conda activate snakemake
    ```
2. Execute the pipeline on the example data

    Locally:
    ```
    ./run.bash &
    ```
#### Output
VarCA will place all of its output in a new directory (`out/`, by default). Log files describing the progress of the pipeline will also be created there: the `log` file contains a basic description of the progress of each step, while the `qlog` file is more detailed and will contain any errors or warnings.

#### Executing the pipeline on your own data
You must modify [the config.yaml file](config#configyaml) to specify paths to your data. The config file is currently configured to run the pipeline on the example data provided.

### If this is your first time using Snakemake
We recommend that you run `snakemake --help` to learn about Snakemake's options. For example, to check that the pipeline will be executed correctly before you run it, you can call Snakemake with the `-n -p -r` flags. This is also a good way to familiarize yourself with the steps of the pipeline and their inputs and outputs (the latter of which are inputs to the first rule in each workflow -- ie the `all` rule).

Note that Snakemake will not recreate output that it has already generated, unless you request it. If a job fails or is interrupted, subsequent executions of Snakemake will just pick up where it left off. This can also apply to files that *you* create and provide in place of the files it would have generated.

By default, the pipeline will automatically delete some files it deems unnecessary (ex: unsorted copies of a BAM). You can opt to keep these files instead by providing the `--notemp` flag to Snakemake when executing the pipeline.
