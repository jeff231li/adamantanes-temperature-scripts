#!/bin/nash

# 01) Process 25deg
# Extract Normalized Esw and Eww
gistpp -i 25deg/gist-output.dat -i2 25deg/gist-gO.dx -op makedx -opt const 14 -o 25deg/gist-Esw-norm.dx
gistpp -i 25deg/gist-output.dat -i2 25deg/gist-gO.dx -op makedx -opt const 16 -o 25deg/gist-Eww-unref-norm.dx

# Get Total Energy Etot = Esw + Eww
gistpp -i 25deg/gist-Eww-unref-norm.dx -i2 25deg/gist-Esw-norm.dx -o 25deg/gist-Etot-unref-norm.dx -op add

# Calculate Average Etot per Voxel
gistpp -i 25deg/gist-Etot-unref-norm.dx -op sum

# 02) Process 55deg
# Extract Normalized Esw and Eww
gistpp -i 55deg/gist-output.dat -i2 55deg/gist-gO.dx -op makedx -opt const 14 -o 55deg/gist-Esw-norm.dx
gistpp -i 55deg/gist-output.dat -i2 55deg/gist-gO.dx -op makedx -opt const 16 -o 55deg/gist-Eww-unref-norm.dx

# Get Total Energy Etot = Esw + Eww
gistpp -i 55deg/gist-Eww-unref-norm.dx -i2 55deg/gist-Esw-norm.dx -o 55deg/gist-Etot-unref-norm.dx -op add

# Calculate Average Etot per Voxel
gistpp -i 55deg/gist-Etot-unref-norm.dx -op sum
