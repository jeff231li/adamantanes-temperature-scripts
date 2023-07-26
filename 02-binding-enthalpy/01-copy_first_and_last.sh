#!/bin/bash

# Create simulations folder
mkdir -p simulations

# Create bound and unbound folder
mkdir -p simulations/a000
mkdir -p simulations/r014

# Copy XML and PDB Files
cp ../01-binding-free-energy/simulations/a000/restrained.* simulations/a000/
cp ../01-binding-free-energy/simulations/r014/restrained.* simulations/r014/
