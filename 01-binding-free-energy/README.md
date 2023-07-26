# Standard APR calculation to estimate H-G binding $\Delta G_{b}$

In this step, we perform the binding free energy calculation with the attach-pull-release (APR) method. The binding free energy is the sum of the APR free energies

$$\Delta G_{b} = W_{attach} + W_{pull} + W_{release-host} + W_{release-guest}^{0}$$

* [01-pAPRika_prepare_system.ipynb](01-pAPRika_prepare_system.ipynb) - prepares the files for the whole APR workflow. Running the notebook will create the folder `simulation` with all the individual APR windows. 
* [02-openmm_simulation.py](02-openmm_simulation.py) - a Python script that performs MD simulations first doing an energy minimization, 100 ps of thermalization with 1 fs, 2.5 ns of equilibration with 2 fs and 30.0 ns of production with 2 fs. You will need to copy this file to each APR window and run them individually. Recommended to run these on a HPC cluster with GPU resources.
* [03-pAPRika_analysis.ipynb](03-pAPRika_analysis.ipynb) - a Jupyter notebook that analysis the APR simulations that extracts the standard binding free energy. The binding free energy will be printed in the Notebook and the results are saved to a JSON file.

## Running Simulations at different temperatures
The current OpenMM simulation is configured to run at a temperature of 298 K. To estimate the binding free energy at different temperatures, simply change line **26** in [02-openmm_simulation.py](02-openmm_simulation.py) 
```python
temperature = 298.15 * unit.kelvin
```
In the analysis notebook, set the temperature accordingly
```python
free_energy = fe_calc()
free_energy.temperature = 298.15  #<-- Change temperature here
```