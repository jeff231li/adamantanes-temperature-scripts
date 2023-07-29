import json
import logging
import sys
from importlib import reload

import numpy as np
import simtk.unit as unit
from MDAnalysis import Universe
from mpi4py import MPI
from paprika.io import NumpyEncoder
from simtk.openmm import (
    HarmonicAngleForce,
    HarmonicBondForce,
    LangevinIntegrator,
    NonbondedForce,
    PeriodicTorsionForce,
    Platform,
    Vec3,
    XmlSerializer,
)
from simtk.openmm.app import PDBFile, Simulation
from tqdm import tqdm

reload(logging)

logger = logging.getLogger()
logging.basicConfig(
    filename="enthalpy-analysis.log",
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
    level=logging.INFO,
)

# MPI Settings
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    logger.info("Starting full analysis of Binding Enthalpy.")


def get_energy(simulation, xyz, box, force_group=None):
    box_vectors = unit.Quantity(
        value=[Vec3(box[0], 0, 0), Vec3(0, box[1], 0), Vec3(0, 0, box[2])],
        unit=unit.angstrom,
    )

    simulation.context.setPositions(xyz * unit.angstrom)
    simulation.context.setPeriodicBoxVectors(*box_vectors)

    if force_group is not None:
        energy = simulation.context.getState(getEnergy=True, groups={force_group})
    else:
        energy = simulation.context.getState(getEnergy=True)
    energy = energy.getPotentialEnergy().value_in_unit(unit.kilocalories_per_mole)

    return energy


# Load Coordinates and XML file
if rank == 0:
    logger.info("Loading XML and PDB files...")

window = sys.argv[1]
temperature = float(sys.argv[2])

# Load XML and PDB file
pdbfile = PDBFile(f"../../simulations/{window}/restrained.pdb")
with open(f"../../simulations/{window}/restrained.xml", "r") as f:
    system = XmlSerializer.deserialize(f.read())

# Preparation
if rank == 0:
    logger.info("Creating OpenMM `Simulation` object...")

# Simulation Object
thermostat = LangevinIntegrator(
    temperature * unit.kelvin,
    1.0 / unit.picosecond,
    2.0 * unit.femtosecond,
)
simulation = Simulation(
    pdbfile.topology,
    system,
    thermostat,
    Platform.getPlatformByName("CPU"),
    {"Threads": "1"},
)

# Load 1 microsecond long trajectory
if rank == 0:
    logger.info("Loading Trajectories...")

universe = Universe(
    f"../../simulations/{window}/restrained.pdb",
    f"../../simulations/{window}/production.dcd",
    in_memory=False,
)
n_frames = universe.trajectory.n_frames

# Specify array sizes for MPI nodes
if rank == 0:
    logger.info(f"Total number of frames {n_frames}")

num_per_rank = int(n_frames / size)
lower_bound = rank * num_per_rank
upper_bound = (rank + 1) * num_per_rank
report_freq = int(num_per_rank / 100)

potential = {
    "potential": np.zeros(n_frames),
    "all": np.zeros(n_frames),
}
potential_chunk = {
    "potential": np.zeros(num_per_rank),
    "all": np.zeros(num_per_rank),
}

# Scatter array to child node
for decomp in potential.keys():
    comm.Scatter(
        [potential[decomp], num_per_rank, MPI.DOUBLE],
        [potential_chunk[decomp], num_per_rank, MPI.DOUBLE],
        root=0,
    )

# Calculate Potential Energy
if rank == 0:
    logger.info("Calculating Potential Energy...")

comm.Barrier()

for i, frame in enumerate(tqdm(universe.trajectory[lower_bound:upper_bound])):
    if rank == 0 and i % report_freq == 0:
        logger.info(f"Completed: {i/num_per_rank*100:5.2f}%")

    xyz = frame.positions
    box = frame.dimensions

    # Nonbonded interactions
    potential_chunk["potential"][i] = get_energy(simulation, xyz, box, force_group=0)
    potential_chunk["all"][i] = get_energy(simulation, xyz, box, force_group=None)

comm.Barrier()

if rank == 0:
    logger.info("Completed: 100.00%")

# Combine data back from child node
for decomp in potential.keys():
    comm.Allgather(
        [potential_chunk[decomp], MPI.DOUBLE], [potential[decomp], MPI.DOUBLE]
    )

# Save results to JSON
if rank == 0:
    logger.info("Saving results to JSON file...")
    with open(f"potential-{window}.json", "w") as f:
        dumped = json.dumps(potential, cls=NumpyEncoder)
        f.write(dumped)

    logger.info("Analysis completed.")
