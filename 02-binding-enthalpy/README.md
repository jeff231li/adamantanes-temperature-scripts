## Binding enthalpy $$\Delta H_{b}$$

The binding enthalpy is simply the difference in total potential energy between the bound and unbound states. For this we copy the OpenMM XML and PDB file for window `a000` and `r014` from the [01-binding-free-energy](../01-binding-free-energy/simulations) folder.

The calculations for binding enthalpy require a much longer simulation than the binding free energy. The file [02-openmm_enthalpy_simulation.py](02-openmm_enthalpy_simulation.py) is similar to the simulation file in [01-binding-free-energy](../01-binding-free-energy) but with a longer production run of 1000 ns.

> **_NOTE:_** Similar to the binding free energy, you will need to run separate simulations for different temperatures. The heat capacity is obtained from the gradient of dH vs T.

## Analysis
With the binding enthalpy simulations, we can perform a number of analysis

* Binding enthalpy
* Decomposition of binding enthalpy in terms of force field parameters
* Decomposition of binding enthalpy in terms of Host-Guest interaction and Desolvation energy.
* Change in water molecules upon binding inside the cavity.