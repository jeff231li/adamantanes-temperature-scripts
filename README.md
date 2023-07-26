# Temperature-dependence of host-guest binding thermodynamics
This repository contains scripts (mostly Python) used to configure and perform analysis in the paper "The Temperature-Dependence of Host-Guest Binding Thermodynamics: Experimental and Simulation Studies".

# Introduction


# Dependencies
The scripts provided here require some libraries, which I will and describe the installation process

> **_NOTE:_** The libraries we will use will only work on Linux and MacOS. For Windows, you will need to install [WSL](https://learn.microsoft.com/en-us/windows/wsl/).

If you don't already have Anaconda installed in your machine, then go to https://anaconda.org and install version 3. Most of the dependencies will be included when we install pAPRika. I recommend installing pAPRika in a fresh `conda` environment. 

### Installing pAPRika
Follow these steps to install pAPRika version 1.1.0 straight from conda (change the commands below from `conda` to `mamba` if you have it installed):
1. Create a new environment `conda create --name paprika python=3.8`
2. Activate the new environment `conda activate paprika`
3. Install paprika v1.1.0 `conda install -c conda-forge paprika=1.1.0`

### Installing other dependencies
One of the main libraries I used for analysis is MDAnalysis and it is not installed by default with the `conda` command above. To install MDAnalysis run the following command
```Python
conda install -c conda-forge mdanalysis
```

Optionally, I provide a parallel version of the analysis script for processing long trajectories. For running the parallel code we need the MPI4Py.
```Python
conda install -c conda-forge mpi4py
```
With the parallel version, you will need to have openmpi installed in your Linux machine. Below is an example on running the python script in parallel 
```bash
mpirun -np 4 python analyze_water.py
```


# Manifest