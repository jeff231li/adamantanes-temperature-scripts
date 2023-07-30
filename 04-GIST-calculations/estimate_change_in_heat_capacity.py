from copy import deepcopy

import numpy as np
from gridData import Grid

# Load in GRIDs for each component
complex_grid = Grid("01-complex-in-water/GIST-analysis/gist-Cptot-norm.dx")
host_grid = Grid("02-host-in-water/GIST-analysis/gist-Cptot-norm.dx")
guest_grid = Grid("03-guest-in-water/GIST-analysis/gist-Cptot-norm.dx")

# Change in Heat Capacity upon binding
delta_Cpb = complex_grid - host_grid - guest_grid
delta_Cpb.export("grid_dCp.dx")

# Total heat capacity of GRID
heat_capacity_total = np.sum(delta_Cpb.grid)

# Integrate heat capacity in cavity
cavity_radius = 7.0
z_min = -3.2
z_max = 3.2

# GRID centers
dx, dy, dz = delta_Cpb.delta
nx, ny, nz = delta_Cpb.grid.shape
cx, cy, cz = nx // 2, ny // 2, nz // 2

# Search Volume (Cylindrical)
circular_land = np.zeros_like(delta_Cpb.grid)

for i in range(nx):
    for j in range(ny):
        distance = ((dx * (i - cx)) ** 2 + (dy * (j - cy)) ** 2) ** 0.5
        circular_land[i, j, :] = distance

z_land = np.zeros_like(delta_Cpb.grid)
for k in range(nz):
    distance = dz * (k - cz)
    z_land[:, :, k] = distance

vol_cavity = deepcopy(delta_Cpb)
vol_cavity.grid = deepcopy(circular_land)
vol_cavity.grid[circular_land <= cavity_radius] = 1
vol_cavity.grid[circular_land > cavity_radius] = 0
location = list(np.where(vol_cavity.grid == 1))
for x in range(len(location[0])):
    i = location[0][x]
    j = location[1][x]
    k = location[2][x]
    if z_land[i, j, k] <= z_min or z_land[i, j, k] >= z_max:
        vol_cavity.grid[i, j, k] = 0

vol_cavity = vol_cavity.grid.astype(dtype=bool)

# Sum of voxels in cavity
heat_capacity_cavity = np.sum(delta_Cpb.grid[vol_cavity])
heat_capacity_portal = heat_capacity_total - heat_capacity_cavity

# Print results
print(f"Heat Capacity in Cavity: {heat_capacity_cavity:.2f} cal/mol/K")
print(f"Heat Capacity in Portal: {heat_capacity_portal:.2f} cal/mol/K")
print("-------------------------------------------")
print(f"Total Heat Capacity: {heat_capacity_total:.2f} cal/mol/K")
