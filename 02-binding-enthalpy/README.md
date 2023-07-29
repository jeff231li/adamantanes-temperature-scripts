# Binding enthalpy $\Delta H_{b}$

The binding enthalpy is simply the difference in total potential energy between the bound and unbound states. For this we copy the OpenMM XML and PDB file for window `a000` and `r014` from the [01-binding-free-energy](../01-binding-free-energy/simulations) folder.

The calculations for binding enthalpy require a much longer simulation than the binding free energy. The file [02-openmm_enthalpy_simulation.py](02-openmm_enthalpy_simulation.py) is similar to the simulation file in [01-binding-free-energy](../01-binding-free-energy) but with a longer production run of 1000 ns.

> **_NOTE:_** Similar to the binding free energy, you will need to run separate simulations for different temperatures. The heat capacity $\Delta C_{p,b}$ is obtained from the slope of $\Delta H_{b}$ vs T.

# Analysis
With the binding enthalpy simulations, we perform a number of analysis as showcased in the paper.

1) Binding enthalpy
2) Decomposition of binding enthalpy in terms of force field terms
3) Decomposition of binding enthalpy in terms of Host-Guest interaction and Desolvation energy.
4) Change in number of H-bonds in the system upon binding.

## Binding Enthalpy
The binding enthalpy is simply the change in potential energy between the bound and unbound states of the host-guest complex in water.

$$\Delta H_{b} = \langle U_{bound} \rangle - \langle U_{unbound} \rangle$$

The energy $\langle U \rangle$ is estimated by recalculating the total potential energy without the restraint potentials. There are two files available in [analysis/enthalpy](analysis/enthalpy) that is used to estimate the enthalpy. To recalculate the potential energy run the Python script
```bash
mpirun -np 4 python calculate_total_potential_energy-MPI.py a000
mpirun -np 4 python calculate_total_potential_energy-MPI.py r014
```
The Jupyter Notebook [estimate_enthalpy.ipynb](analysis/enthalpy/estimate_enthalpy.ipynb) post-processes the raw potential energy and estimates the binding enthalpy with the SEM.

## Decomposition of binding enthalpy -- force field terms
In this case, the total binding enthalpy is decomposed to the sum of force field terms. This is possible because we used an additive force field. We decomposed the binding enthalpy to

* $\Delta H_{val}$ - sum of bond, angles and torsions
* $\Delta H_{LJ}$ - Lennard-Jones interactions
* $\Delta H_{elec}$ - electrostatic interactions

The scripts to estimate the enthalpy based on the FF terms above are available at [analysis/enthalpy-force-field-decomposition](analysis/enthalpy-force-field-decomposition).

```bash
mpirun -np 4 python calculate_potential_ff_decomposition-MPI.py a000
mpirun -np 4 python calculate_potential_ff_decomposition-MPI.py r014
```
The Jupyter Notebook [enthalpy_ff_decomposition.ipynb](analysis/enthalpy-force-field-decomposition/enthalpy_ff_decomposition.ipynb) post-processes the raw individual potential energy and estimates the binding enthalpy with the SEM for each force field components.

## Decomposition of binding enthalpy -- $\Delta H_{H-G}$ and $\Delta H_{Desolv}$
In the second decomposition of the binding enthalpy, we split the interactions involving host-guest interactions and desolvation. The decomposition follows the procedure from [Tang and Chang](https://doi.org/10.1021/acs.jctc.7b00899)

* $\Delta H_{H-G}$ - change upon binding of Host-Guest interactions only (solute-solute)
* $\Delta H_{desolv}$ - change upon binding of interactions involving the solvent (solute-water and water-water)
* 
The scripts to decompose the enthalpy for host-guest and desolvation are located int [analysis/enthalpy-decomposition](analysis/enthalpy-decomposition).

```bash
mpirun -np 4 python calculate_potential_decomposition-MPI.py a000
mpirun -np 4 python calculate_potential_decomposition-MPI.py r014
```

The Jupyter Notebook [enthalpy_decomposition.ipynb](analysis/enthalpy-decomposition/enthalpy_decomposition.ipynb) post-processes the raw individual potential energy and estimates the binding enthalpy with the SEM for the host-guest and desolvation terms.


## Change in the number of H-bonds upon binding
A hydrogen bond is considered when the donor-acceptor-distance is less than 3.0 Å and the donor-hydrogen-acceptor angle is less than 150°. We count the number of H-bonds using the [MDAnalysis](https://github.com/MDAnalysis/mdanalysis) Python package. The analysis is summarized in the Jupyter Notebook [hbond_analysis.ipynb](analysis/hydrogen-bonds/hbond_analysis.ipynb).
