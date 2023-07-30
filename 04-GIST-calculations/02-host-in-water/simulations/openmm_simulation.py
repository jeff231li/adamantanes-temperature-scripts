import logging
import sys
from importlib import reload

import simtk.unit as openmm_unit
from simtk.openmm import LangevinIntegrator, MonteCarloBarostat, Platform, XmlSerializer
from simtk.openmm.app import (
    CheckpointReporter,
    DCDReporter,
    PDBFile,
    Simulation,
    StateDataReporter,
)

reload(logging)

logger = logging.getLogger()
logging.basicConfig(
    filename="openmm.log",
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
    level=logging.INFO,
)

# Init
properties = {"CudaPrecision": "mixed"}
temperature = float(sys.argv[1]) * openmm_unit.kelvin
pressure = 1.01325 * openmm_unit.bar
kT = temperature * openmm_unit.BOLTZMANN_CONSTANT_kB * openmm_unit.AVOGADRO_CONSTANT_NA
dt_therm = 1.0 * openmm_unit.femtoseconds
dt_equil = 2.0 * openmm_unit.femtoseconds
dt_prod = 2.0 * openmm_unit.femtoseconds
therm_steps = 50000
equil_steps = 1500000
prod_steps = 50000000
out_freq = 1000

# Open system
with open("system.xml", "r") as file:
    system = XmlSerializer.deserialize(file.read())
coords = PDBFile("system.pdb")

# Add a barostat
barostat = MonteCarloBarostat(pressure, temperature, 100)
system.addForce(barostat)

# Minimization and Thermalisation
# --------------------------------------------------------------------#
logger.info("Minimizing and Thermalisation ...")

# Thermostat
integrator = LangevinIntegrator(temperature, 1.0 / openmm_unit.picoseconds, dt_therm)

# Simulation Object
simulation = Simulation(
    coords.topology, system, integrator, Platform.getPlatformByName("CUDA"), properties,
)
simulation.context.setPositions(coords.positions)

# Minimize Energy
simulation.minimizeEnergy(
    tolerance=1.0 * openmm_unit.kilojoules_per_mole, maxIterations=5000
)

# Reporters
check_reporter = CheckpointReporter("thermalisation.chk", out_freq * 10)
dcd_reporter = DCDReporter("thermalisation.dcd", out_freq * 10)
state_reporter = StateDataReporter(
    "thermalisation.log",
    out_freq * 10,
    step=True,
    kineticEnergy=True,
    potentialEnergy=True,
    totalEnergy=True,
    temperature=True,
    volume=True,
    speed=True,
    separator=",",
)
simulation.reporters.append(check_reporter)
simulation.reporters.append(dcd_reporter)
simulation.reporters.append(state_reporter)

# MD Step
simulation.step(therm_steps)
simulation.saveState("thermalisation.xml")

# Equilibration
# --------------------------------------------------------------------#
logging.info("Running equilibration ...")

# Thermostat
integrator = LangevinIntegrator(temperature, 1.0 / openmm_unit.picoseconds, dt_equil)

# Simulation object
simulation = Simulation(
    coords.topology, system, integrator, Platform.getPlatformByName("CUDA"), properties,
)
with open("thermalisation.chk", "rb") as file:
    simulation.context.loadCheckpoint(file.read())

# Reporters
check_reporter = CheckpointReporter("equilibration.chk", out_freq * 10)
dcd_reporter = DCDReporter("equilibration.dcd", out_freq * 10)
state_reporter = StateDataReporter(
    "equilibration.log",
    out_freq * 10,
    step=True,
    kineticEnergy=True,
    potentialEnergy=True,
    totalEnergy=True,
    temperature=True,
    volume=True,
    speed=True,
    separator=",",
)
simulation.reporters.append(check_reporter)
simulation.reporters.append(dcd_reporter)
simulation.reporters.append(state_reporter)

# MD step
simulation.step(equil_steps)
simulation.saveState("equilibration.xml")

# Production
# --------------------------------------------------------------------#
logging.info("Running production ...")

# Thermostat
integrator = LangevinIntegrator(temperature, 1.0 / openmm_unit.picoseconds, dt_prod)

# Create simulation object
simulation = Simulation(
    coords.topology, system, integrator, Platform.getPlatformByName("CUDA"), properties,
)
with open("equilibration.chk", "rb") as file:
    simulation.context.loadCheckpoint(file.read())

# Reporters
check_reporter = CheckpointReporter("production.chk", out_freq * 100)
dcd_reporter = DCDReporter("production.dcd", out_freq, append=False)
state_reporter = StateDataReporter(
    "production.log",
    out_freq * 10,
    step=True,
    kineticEnergy=True,
    potentialEnergy=True,
    totalEnergy=True,
    temperature=True,
    volume=True,
    speed=True,
    separator=",",
)
simulation.reporters.append(check_reporter)
simulation.reporters.append(dcd_reporter)
simulation.reporters.append(state_reporter)

# MD step
simulation.step(prod_steps)
simulation.saveState("production.xml")
