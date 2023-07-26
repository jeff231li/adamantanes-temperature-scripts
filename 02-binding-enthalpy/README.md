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
5) Change in water molecules upon binding inside the cavity upon binding..

## Binding Enthalpy
The binding enthalpy is simply the change in potential energy between the bound and unbound states of the host-guest complex in water.

$$\Delta H_{b} = \langle U_{bound} \rangle - \langle U_{pulled} \rangle$$


## Decomposition of binding enthalpy -- force field terms
In this case, the total binding enthalpy is decomposed to the sum of force field terms. This is possible because we used an additive force field. We decomposed the binding enthalpy to

* $\Delta H_{val}$ - sum of bond, angles and torsions
* $\Delta H_{LJ}$ - Lennard-Jones interactions
* $\Delta H_{elec}$ - electrostatic interactions


## Decomposition of binding enthalpy -- Host-Guest and Desolvation
In the second decomposition of the binding enthalpy, we split the interactions involving host-guest interactions and desolvation. The decomposition follows the procedure from [Tang and Chang](https://doi.org/10.1021/acs.jctc.7b00899)

* $\Delta H_{H-G}$ - change upon binding of Host-Guest interactions only (solute-solute)
* $\Delta H_{desolv}$ - change upon binding of interactions involving the solvent (solute-water and water-water)

## Change in the number of H-bonds upon binding
A hydrogen bond is considered when the donor-acceptor-distance is less than 3.0 Å and the donor-hydrogen-acceptor angle is less than 150°. We count the number of H-bonds using the [MDAnalysis](https://github.com/MDAnalysis/mdanalysis) Python package.

## Change in the number of water molecules in cavity
We also estimated the change in the number of water molecules inside the host cavity upon binding