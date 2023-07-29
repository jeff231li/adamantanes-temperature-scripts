import json
import logging
import sys
import time
from copy import deepcopy
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
    filename="analysis-mpi.log",
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


def get_energy(simulation, xyz, box, force_group=0):
    box_vectors = unit.Quantity(
        value=[Vec3(box[0], 0, 0), Vec3(0, box[1], 0), Vec3(0, 0, box[2])],
        unit=unit.angstrom,
    )

    simulation.context.setPositions(xyz * unit.angstrom)
    simulation.context.setPeriodicBoxVectors(*box_vectors)

    energy = simulation.context.getState(getEnergy=True, groups={force_group})
    energy = energy.getPotentialEnergy().value_in_unit(unit.kilocalories_per_mole)

    return energy


def turn_parm_off(
    nb_force, atom_list, parm_type="all", parm_off=True, exception_off=True
):
    if parm_off:
        for atom in range(nb_force.getNumParticles()):
            if atom in atom_list:
                charge, sigma, epsilon = nb_force.getParticleParameters(atom)
                if parm_type == "all":
                    nb_force.setParticleParameters(atom, 0.0, sigma, 0.0)
                elif parm_type == "elec":
                    nb_force.setParticleParameters(atom, 0.0, sigma, epsilon)
                elif parm_type == "vdw":
                    nb_force.setParticleParameters(atom, charge, sigma, 0.0)

    if exception_off:
        for exception in range(nb_force.getNumExceptions()):
            atomi, atomj, charge, sigma, epsilon = nb_force.getExceptionParameters(
                exception
            )
            if atomi in atom_list or atomj in atom_list:
                if parm_type == "all":
                    nb_force.setExceptionParameters(
                        exception, atomi, atomj, 0.0, sigma, 0.0
                    )
                elif parm_type == "elec":
                    nb_force.setExceptionParameters(
                        exception, atomi, atomj, 0.0, sigma, epsilon
                    )
                elif parm_type == "vdw":
                    nb_force.setExceptionParameters(
                        exception, atomi, atomj, charge, sigma, 0.0
                    )


# Load Coordinates and XML file
if rank == 0:
    logger.info("Loading XML and PDB files...")

window = sys.argv[1]
temperature = float(sys.argv[2])

pdbfile = PDBFile(f"../../simulations/{window}/restrained.pdb")
with open(f"../../simulations/{window}/restrained.xml", "r") as f:
    system = XmlSerializer.deserialize(f.read())

# Atom indices
if rank == 0:
    logger.info("Defining atom indices of molecules in system...")

guest_resname = "AMT"
host_resname = "CB7"
solvent_resname = "HOH"
guest_indices = [
    atom.index
    for atom in pdbfile.topology.atoms()
    if atom.residue.name == guest_resname
]
host_indices = [
    atom.index for atom in pdbfile.topology.atoms() if atom.residue.name == host_resname
]
solvent_indices = [
    atom.index
    for atom in pdbfile.topology.atoms()
    if atom.residue.name == solvent_resname
]

# Split forces
if rank == 0:
    logger.info("Splitting Forces to different Force Groups...")

# Valence terms
harmonic_bond = [
    force for force in system.getForces() if isinstance(force, HarmonicBondForce)
][0]
harmonic_angle = [
    force for force in system.getForces() if isinstance(force, HarmonicAngleForce)
][0]
periodic_torsion = [
    force for force in system.getForces() if isinstance(force, PeriodicTorsionForce)
][0]
harmonic_bond.setForceGroup(5)
harmonic_angle.setForceGroup(6)
periodic_torsion.setForceGroup(7)

# Nonbonded forces
nonbonded_all = [
    force for force in system.getForces() if isinstance(force, NonbondedForce)
][0]
nonbonded_all.setForceGroup(8)
nonbonded_solvent = deepcopy(nonbonded_all)
nonbonded_complex = deepcopy(nonbonded_all)

# solvent-solvent
nonbonded_solvent.setForceGroup(1)
turn_parm_off(
    nonbonded_solvent,
    (guest_indices + host_indices),
    parm_type="all",
    parm_off=True,
    exception_off=True,
)
system.addForce(nonbonded_solvent)

# solute-solute
nonbonded_complex.setForceGroup(2)
turn_parm_off(
    nonbonded_complex,
    solvent_indices,
    parm_type="all",
    parm_off=True,
    exception_off=True,
)
system.addForce(nonbonded_complex)

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
    "bond": np.zeros(n_frames),
    "angle": np.zeros(n_frames),
    "dihedral": np.zeros(n_frames),
    "nonbonded": np.zeros(n_frames),
    "solvent": np.zeros(n_frames),
    "complex": np.zeros(n_frames),
}
potential_chunk = {
    "bond": np.zeros(num_per_rank),
    "angle": np.zeros(num_per_rank),
    "dihedral": np.zeros(num_per_rank),
    "nonbonded": np.zeros(num_per_rank),
    "solvent": np.zeros(num_per_rank),
    "complex": np.zeros(num_per_rank),
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
    start = time.time()

comm.Barrier()

for i, frame in enumerate(tqdm(universe.trajectory[lower_bound:upper_bound])):
    if rank == 0 and i % report_freq == 0:
        logger.info(f"Completed: {i/num_per_rank*100:5.2f}%")

    xyz = frame.positions
    box = frame.dimensions

    # Total nonbonded
    potential_chunk["nonbonded"][i] = get_energy(simulation, xyz, box, force_group=8)

    # solvent-solvent nonbonded
    potential_chunk["solvent"][i] = get_energy(simulation, xyz, box, force_group=1)

    # solute-solute nonbonded
    potential_chunk["complex"][i] = get_energy(simulation, xyz, box, force_group=2)

    # Host-Guest valence interactions
    potential_chunk["bond"][i] = get_energy(simulation, xyz, box, force_group=5)
    potential_chunk["angle"][i] = get_energy(simulation, xyz, box, force_group=6)
    potential_chunk["dihedral"][i] = get_energy(simulation, xyz, box, force_group=7)

comm.Barrier()

if rank == 0:
    end = time.time()
    logger.info("Completed: 100.00%")
    logger.info(f"Total time taken: {end-start} sec")

# Combine data back from child node
for decomp in potential.keys():
    comm.Allgather(
        [potential_chunk[decomp], MPI.DOUBLE], [potential[decomp], MPI.DOUBLE]
    )

# Save results to JSON
if rank == 0:
    logger.info("Saving results to JSON file...")
    with open(f"potential-decomposition-{window}.json", "w") as f:
        dumped = json.dumps(potential, cls=NumpyEncoder)
        f.write(dumped)

    logger.info("Analysis completed.")
