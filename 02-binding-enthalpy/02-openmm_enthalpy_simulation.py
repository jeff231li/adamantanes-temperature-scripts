import logging
from importlib import reload

import simtk.unit as unit
from simtk.openmm import LangevinIntegrator, MonteCarloBarostat, Platform, XmlSerializer
from simtk.openmm.app import (
    CheckpointReporter,
    DCDReporter,
    PDBFile,
    Simulation,
    StateDataReporter,
)

# Initialize Logger
reload(logging)

logger = logging.getLogger()
logging.basicConfig(
    filename="paprika_openmm.log",
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
    level=logging.INFO,
)

# User Options -- Time steps etc.
temperature = 298.15 * unit.kelvin
pressure = 1.01325 * unit.bar

dt_therm = 1.0 * unit.femtoseconds
dt_equil = 2.0 * unit.femtoseconds
dt_prod = 2.0 * unit.femtoseconds

time_therm = 100 * unit.picoseconds
time_equil = 2.5 * unit.nanoseconds
time_prod = 30.0 * unit.nanoseconds
time_output = 10 * unit.picoseconds

therm_steps = int(time_therm / dt_therm) + 1
equil_steps = int(time_equil / dt_equil) + 1
prod_steps = int(time_prod / dt_prod) + 1
n_output = int(time_output / dt_prod)

# Load OpenMM System and PDB file
with open("restrained.xml", "r") as file:
    system = XmlSerializer.deserialize(file.read())
coords = PDBFile("restrained.pdb")

# Add Barostat
barostat = MonteCarloBarostat(pressure, temperature, 101)
system.addForce(barostat)

# ------------------------------------------------------------------ #
# Run Energy Minimization and initial Thermialization
# ------------------------------------------------------------------ #
# Thermostat
integrator = LangevinIntegrator(temperature, 1.0 / unit.picoseconds, dt_therm)

# Simulation Object
simulation = Simulation(
    coords.topology,
    system,
    integrator,
    Platform.getPlatformByName("CUDA"),
    {"CudaPrecision": "mixed"},
)
simulation.context.setPositions(coords.positions)

# Minimize Energy
simulation.minimizeEnergy()

# Reporters
check_reporter = CheckpointReporter("thermalization.chk", n_output * 10)
dcd_reporter = DCDReporter("thermalization.dcd", n_output * 10)
state_reporter = StateDataReporter(
    "thermalization.log",
    n_output * 10,
    step=True,
    kineticEnergy=True,
    potentialEnergy=True,
    totalEnergy=True,
    temperature=True,
    speed=True,
    separator=",",
)
simulation.reporters.append(dcd_reporter)
simulation.reporters.append(state_reporter)
simulation.reporters.append(check_reporter)

# MD step
simulation.step(therm_steps)
simulation.saveState("thermalization.xml")

# ------------------------------------------------------------------ #
# Run Equilibration
# ------------------------------------------------------------------ #
# Thermostat
integrator = LangevinIntegrator(temperature, 1.0 / unit.picoseconds, dt_equil)

# Simulation Object
simulation = Simulation(
    coords.topology,
    system,
    integrator,
    Platform.getPlatformByName("CUDA"),
    {"CudaPrecision": "mixed"},
)
simulation.loadState("thermalization.xml")
simulation.currentStep = 0

# Reporters
check_reporter = CheckpointReporter("equilibration.chk", n_output * 10)
dcd_reporter = DCDReporter("equilibration.dcd", n_output * 10)
state_reporter = StateDataReporter(
    "equilibration.log",
    n_output * 10,
    step=True,
    kineticEnergy=True,
    potentialEnergy=True,
    totalEnergy=True,
    temperature=True,
    speed=True,
    separator=",",
)
simulation.reporters.append(dcd_reporter)
simulation.reporters.append(state_reporter)
simulation.reporters.append(check_reporter)

# MD step
simulation.step(equil_steps)
simulation.saveState("equilibration.xml")

# ------------------------------------------------------------------ #
# Run Production
# ------------------------------------------------------------------ #
# Thermostat
integrator = LangevinIntegrator(temperature, 1.0 / unit.picoseconds, dt_prod)

# Simulation Object
simulation = Simulation(
    coords.topology,
    system,
    integrator,
    Platform.getPlatformByName("CUDA"),
    {"CudaPrecision": "mixed"},
)
simulation.loadState("equilibration.xml")
simulation.currentStep = 0

# Reporters
check_reporter = CheckpointReporter("production.chk", n_output)
dcd_reporter = DCDReporter("production.dcd", n_output)
state_reporter = StateDataReporter(
    "production.log",
    n_output,
    step=True,
    kineticEnergy=True,
    potentialEnergy=True,
    totalEnergy=True,
    temperature=True,
    speed=True,
    separator=",",
)
simulation.reporters.append(dcd_reporter)
simulation.reporters.append(state_reporter)
simulation.reporters.append(check_reporter)

# MD step
simulation.step(prod_steps)
simulation.saveState("production.xml")
