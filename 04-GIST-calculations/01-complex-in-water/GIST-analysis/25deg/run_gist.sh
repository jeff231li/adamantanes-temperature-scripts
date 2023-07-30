#!/bin/bash

# Options
folder=../../simulation-25deg
topology=CB7-AMT-sol.prmtop
host_resname=CB7
temperature=298.15
refdens=0.0334

# Run GIST Analysis
cpptraj.cuda <<EOF > cpptraj.log
# Load Topology and Trajectory
parm ${folder}/${topology}
trajin ${folder}/production.dcd

# Center coordinates
center :${host_resname} origin

# Do GIST on shifted trajectories
gist temp ${temperature} refdens ${refdens} gridspacn 0.5 gridcntr 0.0 0.0 0.0 griddim 60 60 60

go

quit
EOF
