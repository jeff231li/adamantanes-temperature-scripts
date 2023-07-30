#!/bin/bash

# Options
folder=../../simulation/55deg
topology=CB7-sol.prmtop
host_resname=CB7
temperature=328.15
refdens=0.0320

# Run GIST Analysis
cpptraj.cuda <<EOF > cpptraj.log
# Load Topology and Trajectory
parm ${folder}/${topology}
trajin ../host-equil-aligned.pdb
trajin ${folder}/production.dcd

# Center coordinates
center :${host_resname} origin

# Do GIST on shifted trajectories
gist temp ${temperature} refdens ${refdens} gridspacn 0.5 gridcntr 19.807374954223633 19.639026641845703 19.884397506713867 griddim 60 60 60

go

quit
EOF
