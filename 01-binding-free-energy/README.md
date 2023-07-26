# Standard APR calculation to estimate H-G binding $$\Delta G_{b}$$

In this step, we perform the binding free energy calculation with the attach-pull-release (APR) method.

* [01-pAPRika_prepare_system.ipynb](01-pAPRika_prepare_system.ipynb) - prepares the files for the whole APR workflow. Running the notebook will create the folder `simulation` with all the individual APR windows. 
* [02-openmm_simulation.py](02-openmm_simulation.py) - a Python script that performs MD simulations first doing an energy minimization, 100 ps of thermalization with 1 fs, 2.5 ns of equilibration with 2 fs and 30.0 ns of production with 2 fs.
* [03-pAPRika_analysis.ipynb](03-pAPRika_analysis.ipynb) - a Jupyter notebook that analysis the APR simulations that extracts the standard binding free energy. The binding free energy will be printed in the Notebook and the results are saved to a JSON file.