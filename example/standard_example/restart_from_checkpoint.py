# Import OpenMM library
# Import sbmOpenMM library
import os
import sys
import time
from sys import stdout

from simtk.openmm import *
from simtk.openmm.app import *
from simtk.unit import *

import sbmOpenMM

# MD parameter
# let's decide here now long we want to run the simulation and the file writing period
mdsteps = 10000  # 5 ns at 2 fs timestep
dcdperiod = 1000  # 10 ps at 2 fs timestep
logperiod = 100  # 10 ps at 2 fs timestep

# stage of simulation equil, prod
prev_stage = 'equil'
stage = 'prod'
# which platform to run simulation: CPU/GPU
device = 'CPU'

pdbname = 'asyn_ext_pymol'
protein_code = 'asyn'
pdb_file = f'{pdbname}.pdb'

# Create an sbmOpenMM.system() object and store it in "sbmCAModelModel" variable.
cgModel = sbmOpenMM.models.getCGModel(pdb_file)

if device == 'GPU':
    # Run simulation on CUDA
    platform = Platform.getPlatformByName('CUDA')
    properties = {'CudaPrecision': 'mixed'}
    # in case of many GPUs present, we can select which one to use
    # properties["DeviceIndex"] = "0"

elif device == 'CPU':
    platform = Platform.getPlatformByName('CPU')
    properties = {'Threads': str(8)}

integrator = LangevinIntegrator(298 * kelvin, 0.01 / picosecond, 10 * femtoseconds)
simulation = Simulation(cgModel.topology, cgModel.system, integrator, platform, properties)

# Set initial positions
simulation.context.setPositions(cgModel.positions)
# set velocity by temperature
# simulation.context.setVelocitiesToTemperature(298 * kelvin)

# Add a DCD reporter that writes coordinates every 100 steps.
simulation.reporters.append(DCDReporter(f'{protein_code}_{stage}.dcd', dcdperiod))

# If we don't need too details, we can use the default reporter from OpenMM
simulation.reporters.append(
    StateDataReporter(stdout, logperiod, step=True, time=True, potentialEnergy=True, kineticEnergy=True,
                      totalEnergy=True, temperature=True, progress=True, remainingTime=True, speed=True,
                      totalSteps=mdsteps, separator='\t'))
simulation.reporters.append(
    StateDataReporter(f'{protein_code}_{stage}.log', logperiod, step=True, time=True, potentialEnergy=True,
                      kineticEnergy=True,
                      totalEnergy=True, temperature=True, progress=True, remainingTime=True, speed=True,
                      totalSteps=mdsteps, separator='\t'))

# load binary checkpoint from previous stage (equilibrium)
with open(f'checkpoint_{prev_stage}.chk', 'rb') as f:
    simulation.context.loadCheckpoint(f.read())

print('Simulation started')
start_time = time.time()
# for i in range(1000):
simulation.step(mdsteps)

# write the last frame
lastframe = simulation.context.getState(getPositions=True).getPositions()
PDBFile.writeFile(cgModel.topology, lastframe, open(f'{protein_code}_{stage}_final.pdb', 'w'))
simulation.saveCheckpoint(f'checkpoint_{stage}.chk')

print("--- Finished in %s seconds ---" % (time.time() - start_time))