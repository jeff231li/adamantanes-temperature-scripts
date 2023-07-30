#!/usr/bin/env python
#
# Dependencies to read *.dx files
#   -> pip install gridDataFormats
#
import numpy as np
from gridData import Grid

# Temperature(s) of simulations
T_init = 298.15
T_fina = 328.15

Eww_ref_T_init = 9.562
Eww_ref_T_fina = 9.172

# 01) Process GIST grid for 25deg
# Load Density Grid
grid_Esw_dens_25 = Grid("25deg/gist-Esw-dens.dx")
grid_Eww_dens_25 = Grid("25deg/gist-Eww-dens.dx")

# Convert Density to Normalized Voxels
grid_Esw_norm_25 = grid_Esw_dens_25 * np.prod(grid_Esw_dens_25.delta)
grid_Eww_norm_25 = grid_Eww_dens_25 * np.prod(grid_Eww_dens_25.delta)

# Reference Eww
grid_Eww_norm_25 += Eww_ref_T_init

# Total Solvation Energy
grid_Etot_norm_25 = grid_Esw_norm_25 + grid_Eww_norm_25

# 01) Process GIST grid for 55deg
# Load Density Grid
grid_Esw_dens_55 = Grid("55deg/gist-Esw-dens.dx")
grid_Eww_dens_55 = Grid("55deg/gist-Eww-dens.dx")

# Convert Density to Normalized Voxels
grid_Esw_norm_55 = grid_Esw_dens_55 * np.prod(grid_Esw_dens_55.delta)
grid_Eww_norm_55 = grid_Eww_dens_55 * np.prod(grid_Eww_dens_55.delta)

# Reference Eww
grid_Eww_norm_55 += Eww_ref_T_fina

# Total Solvation Energy
grid_Etot_norm_55 = grid_Esw_norm_55 + grid_Eww_norm_55

# 03) Total Heat Capacity
# Heat capacity (E(T2) - E(T1)) / (T2 - T1)
grid_Cp_norm = (grid_Etot_norm_55 - grid_Etot_norm_25) / (T_fina - T_init)

# Convert to kcal/mol/K to cal/mol/K
grid_Cp_norm *= 1000

# Save total Grid to file
grid_Cp_norm.export("grid_Cptot_norm.dx")
