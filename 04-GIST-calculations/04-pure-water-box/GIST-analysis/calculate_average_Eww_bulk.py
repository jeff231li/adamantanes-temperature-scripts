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

# 01) Process GIST grid for 25deg
# Load Density Grid
grid_Esw_dens_25 = Grid("25deg/gist-Esw-dens.dx")
grid_Eww_dens_25 = Grid("25deg/gist-Eww-dens.dx")

# Convert Density to Normalized Voxels
grid_Esw_norm_25 = grid_Esw_dens_25 * np.prod(grid_Esw_dens_25.delta)
grid_Eww_norm_25 = grid_Eww_dens_25 * np.prod(grid_Eww_dens_25.delta)

# Total Solvation Energy
grid_Etot_unref_norm_25 = grid_Esw_norm_25 + grid_Eww_norm_25

# Print Average Etot per Voxel
print(grid_Etot_unref_norm_25.grid.mean())

# 01) Process GIST grid for 55deg
# Load Density Grid
grid_Esw_dens_55 = Grid("55deg/gist-Esw-dens.dx")
grid_Eww_dens_55 = Grid("55deg/gist-Eww-dens.dx")

# Convert Density to Normalized Voxels
grid_Esw_norm_55 = grid_Esw_dens_55 * np.prod(grid_Esw_dens_55.delta)
grid_Eww_norm_55 = grid_Eww_dens_55 * np.prod(grid_Eww_dens_55.delta)

# Total Solvation Energy
grid_Etot_unref_norm_55 = grid_Esw_norm_55 + grid_Eww_norm_55

# Print Average Etot per Voxel
print(grid_Etot_unref_norm_55.grid.mean())
