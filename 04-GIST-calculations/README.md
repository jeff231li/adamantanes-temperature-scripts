# Heat Capacity $\Delta C_{p,b}$ from GIST analysis

## Total Solvation Energy Grid from GIST
This folder contains the scripts to estimate the heat capacity $\Delta C_{p,b}$ from GIST analysis. Briefly, the solvation free energy in GIST is given by

$$\Delta A_{i} = \Delta E_{i} - T\Delta S_{i}$$

The total solvation energy in each voxel is

$$\Delta E_{i}^{total} = E_{i}^{sw} + \left(E_{i}^{ww} - \frac{n_{i}}{n_{i,bulk}} E_{i,bulk}^{ww} \right)$$

where 
* $E_{i}^{sw}$ -- solute-water energy in voxel $i$
* $E_{i}^{ww}$ -- water-water energy in voxel $i$
* $n_{i}$ -- average number of water molecules voxel $i$
* $n_{i,bulk}$ -- average number of water molecules in a pure bulk environment in voxel $i$

The water-water contribution is referenced with the bulk in order to make voxels far away from the solutes have zero values. To simplify things, I calculate the reference value by estimating the average energy in each voxel for a water box simulation at two temperatures. The average $E_{bulk}^{ww}$ for 298.15 K and 328.15 K are 9.562 kcal/mol and 9.173 kcal/mol, respectively. The water densities at these two temperatures are 0.0334 $\unicode{x212B}^{-3}$ and 0.0320 $\unicode{x212B}^{-3}$, respectively. The simulation and analysis scripts for pure water is available in [04-pure-water-box](04-pure-water-box)

## Heat Capacity Grid from GIST
The heat capacity in each voxel $C_{p,i}$ is estimated by taking the difference in energy at two temperatures divided by the difference in temperature:

$$C_{p,i} = \frac{\Delta E_{i}^{total}(T_2)-\Delta E_{i}^{total}(T_1)}{T_2 - T_1}$$

The change in heat capacity upon binding $\Delta C_{p,i}$ is then obtained by subtracting the grid of the free solutes from the identically aligned bound complex

$$\Delta C_{p,i} = C_{p,i}^{complex} - C_{p,i}^{host} - C_{p,i}^{guest}$$

This folder contains three folders corresponding to the simulations and analysis for the three components above. The heat capacity for each system is estimated with the script [calculate_heat_capacity-GIST.sh](calculate_heat_capacity-GIST.sh), which uses [GISTPP](https://github.com/KurtzmanLab/Gist-Post-Processing/tree/master) to perform the GRID operations above. 

## Integrating Heat Capacity Grid
Finally, we want to estimate the change in the heat capacity upon binding and integrate the GIST voxels to obtain some numerical values. This is done with the Python script [estimate_change_in_heat_capacity.py](estimate_change_in_heat_capacity.py) that the `gridData` module, which you will need to install this first using the command
```bash
pip install gridDataFormats
```
The Python script will subtract the free host and guest heat capacity from the bound complex state.