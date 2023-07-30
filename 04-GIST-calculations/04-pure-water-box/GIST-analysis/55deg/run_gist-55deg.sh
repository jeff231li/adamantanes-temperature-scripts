#!/bin/bash

# Options
folder=../../simulation/55deg
topology=tip3p_box.prmtop
temperature=328.15
refdens=0.0320

# Run GIST Analysis
cpptraj.cuda <<EOF > cpptraj.log
# Load Topology and Trajectory
parm ${folder}/${topology}
trajin ${folder}/production.dcd

# Do GIST on shifted trajectories
gist temp ${temperature} refdens ${refdens} gridspacn 0.5 gridcntr 19.807374954223633 19.639026641845703 19.884397506713867 griddim 60 60 60

go

quit
EOF
