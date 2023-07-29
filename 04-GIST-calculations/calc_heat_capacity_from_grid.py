#!/usr/bin/env python
#
# Dependencies to read *.dx files
#   -> pip install gridDataFormats
#
import numpy as np
from gridData import Grid

T_initial = 25
T_final = 55
dT = T_final - T_initial

#--------------------------------------------------------------------#
# Water-Water
#--------------------------------------------------------------------#
# Load density dx files
grid_Eww_dens_25 = Grid("25deg/gist-Eww-dens.dx")
grid_Eww_dens_55 = Grid("55deg/gist-Eww-dens.dx")

# Convert density to norm
grid_Eww_norm_25 = grid_Eww_dens_25 * np.prod(grid_Eww_dens_25.delta)
grid_Eww_norm_55 = grid_Eww_dens_55 * np.prod(grid_Eww_dens_55.delta)

# Calculate the heat capacity - unit of cal/mol/K
grid_dEww_norm = grid_Eww_norm_55 - grid_Eww_norm_25
grid_Cpww_norm = grid_dEww_norm / dT * 1000

# Save to file
grid_Cpww_norm.export("grid_Cpww_norm.dx")

#--------------------------------------------------------------------#
# Solute-Water
#--------------------------------------------------------------------#
# Load density dx files
grid_Esw_dens_25 = Grid("25deg/gist-Esw-dens.dx")
grid_Esw_dens_55 = Grid("55deg/gist-Esw-dens.dx")

# Convert density to norm
grid_Esw_norm_25 = grid_Esw_dens_25 * np.prod(grid_Esw_dens_25.delta)
grid_Esw_norm_55 = grid_Esw_dens_55 * np.prod(grid_Esw_dens_55.delta)

# Calculate the heat capacity - unit of cal/mol/K
grid_dEsw_norm = grid_Esw_norm_55 - grid_Esw_norm_25
grid_Cpsw_norm = grid_dEsw_norm / dT * 1000

# Save to file
grid_Cpsw_norm.export("grid_Cpsw_norm.dx")

#--------------------------------------------------------------------#
# Total
#--------------------------------------------------------------------#
grid_Cp_norm = grid_Cpsw_norm + grid_Cpww_norm
grid_Cp_norm.export("grid_Cp_norm.dx")
