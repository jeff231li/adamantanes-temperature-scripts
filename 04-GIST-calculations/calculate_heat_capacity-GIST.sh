#!/bin/bash

# Extract Average Number of Water in Each Voxel
gistpp -i 25deg/gist-output.dat -i2 25deg/gist-gO.dx -op makedx -opt const 4 -o 25deg/numwat.dx
gistpp -i 55deg/gist-output.dat -i2 55deg/gist-gO.dx -op makedx -opt const 4 -o 55deg/numwat.dx

# Extract SW and WW Normalized Densities - 25deg
gistpp -i 25deg/gist-output.dat -i2 25deg/gist-gO.dx -op makedx -opt const 14 -o 25deg/gist-Esw-norm.dx
gistpp -i 25deg/gist-output.dat -i2 25deg/gist-gO.dx -op makedx -opt const 16 -o 25deg/gist-Eww-unref-norm.dx

# Reference the E^{WW} to bulk values at 25 deg
gistpp -i 25deg/gist-Eww-unref-norm.dx -op addconst -opt const 9.562 -o 25deg/gist-Eww-ref-norm.dx

# Extract SW and WW Normalized Densities - 55deg
gistpp -i 55deg/gist-output.dat -i2 55deg/gist-gO.dx -op makedx -opt const 14 -o 55deg/gist-Esw-norm.dx
gistpp -i 55deg/gist-output.dat -i2 55deg/gist-gO.dx -op makedx -opt const 16 -o 55deg/gist-Eww-unref-norm.dx

# Reference the E^{WW} to bulk values at 55 deg
gistpp -i 55deg/gist-Eww-unref-norm.dx -op addconst -opt const 9.173 -o 55deg/gist-Eww-ref-norm.dx

# Add Total Energy (SW + WW)
gistpp -i 25deg/gist-Esw-norm.dx -i2 25deg/gist-Eww-ref-norm.dx -op add -o 25deg/gist-Etot-norm.dx
gistpp -i 55deg/gist-Esw-norm.dx -i2 55deg/gist-Eww-ref-norm.dx -op add -o 55deg/gist-Etot-norm.dx

# Take the Change in E Between Different Temperatures - dE = E(T2)-E(T1)
gistpp -i 55deg/gist-Etot-norm.dx -i2 25deg/gist-Etot-norm.dx -o gist-Etot-diff.dx -op sub

# Calculate Heat Capacity - dE/dT --> dE x 1/dT --> dE * 0.033333 --> 1 / (328.15 - 298.15)
gistpp -i gist-Etot-diff.dx -o gist-Etot-diff-divided.dx -op multconst -opt const 0.033333

# dE/dT * 1000 - convert to cal/mol/K
gistpp -i gist-Etot-diff-divided.dx -o gist-Cptot-norm.dx -op multconst -opt const 1000
