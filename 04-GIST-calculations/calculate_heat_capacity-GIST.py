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

# 01) Process Water-Water GIST-Grid
# Load Density Grid
grid_Eww_dens_25 = Grid("25deg/gist-Eww-dens.dx")
grid_Eww_dens_55 = Grid("55deg/gist-Eww-dens.dx")

# Convert Density to Normalized Voxels
grid_Eww_norm_25 = grid_Eww_dens_25 * np.prod(grid_Eww_dens_25.delta)
grid_Eww_norm_55 = grid_Eww_dens_55 * np.prod(grid_Eww_dens_55.delta)

# Calculate the heat capacity - unit of cal/mol/K
grid_dEww_norm = grid_Eww_norm_55 - grid_Eww_norm_25
grid_Cpww_norm = grid_dEww_norm / (T_fina - T_init) * 1000

# 02) Process Solute-Water GIST-Grid
# Load Density Grid
grid_Esw_dens_25 = Grid("25deg/gist-Esw-dens.dx")
grid_Esw_dens_55 = Grid("55deg/gist-Esw-dens.dx")

# Convert Density to Normalized Voxels
grid_Esw_norm_25 = grid_Esw_dens_25 * np.prod(grid_Esw_dens_25.delta)
grid_Esw_norm_55 = grid_Esw_dens_55 * np.prod(grid_Esw_dens_55.delta)

# Calculate the heat capacity - unit of cal/mol/K
grid_dEsw_norm = grid_Esw_norm_55 - grid_Esw_norm_25
grid_Cpsw_norm = grid_dEsw_norm / (T_fina - T_init) * 1000

# 03) Calculate the Total Heat Capacity
# Add SW and WW Grids
grid_Cp_norm = grid_Cpsw_norm + grid_Cpww_norm

# Save total Grid to file
grid_Cp_norm.export("grid_Cp_norm.dx")