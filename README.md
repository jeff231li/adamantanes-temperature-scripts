# Temperature-dependence of host-guest binding thermodynamics

## Introduction
This repository contains most of the scripts used in the "Simulation Analysis" from the paper "The Temperature-Dependence of Host-Guest Binding Thermodynamics: Experimental and Simulation Studies". The files provided are either Python or bash scripts, that performs the different analysis. 

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
I've prepared some of the script to use Jupyter notebook/lab, so we will need to install this in conda (either the notebook or lab versions will work). The simulations use OpenMM version 7.5.1 and MDAnalysis. To install these libraries run the following in the `paprika` conda environment
```bash
conda install -c conda-forge jupyterlab mdanalysis openmm=7.5.1
```

For some of the analysis scripts in the binding enthalpies section I implemented the code in parallel since the trajectories are large (1-$\mu$s long trajectories). Thus, a version of MPI (OpenMPI or MPIVEC) needs to be installed first on your workstation/HPC and then we need the Python wrapper MPI4Py
```Python
conda install -c conda-forge mpi4py
```

For GIST calculations, you will need the [CPPTRAJ](https://github.com/Amber-MD/cpptraj) program, which can be installed through conda (AmberTools) or compiled manually if you want to run the GPU version. The other program I used is [gisttools](https://github.com/liedllab/gisttools/tree/master), which I used to post-process the GIST output file.

# Manifest
* `01-binding-free-energy/`: Contains Jupyter Notebooks and Python scripts to build, simulate and analyze an APR calculation for CB7 with 1-AdOH. 
* `02-binding-enthalpy/`: Contains Jupyter Notebooks and Python scripts to copy initial files from APR calculations, simulate and analyze the trajectories. The analysis includes binding enthalpy, decomposition of binding enthalpy, and the change in the number of hydrogen bonds upon binding.
* `03-heat-capacity/`: Contains Jupyter Notebooks that estimates the heat capacities from binding enthalpies.
* `04-GIST-calculations/`: Contains bash and Python scripts that runs GIST calculations from MD simulations, and post-process the grid files to extract the heat capacities from GIST. An analysis script is also provided that integrates the heat capacities.