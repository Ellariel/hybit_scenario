'''
Test scenario for the Simulators used.
'''

import os
import sys
import mosaik
import mosaik.util
import pandas as pd
import pandapower as pp

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

GRID_FILE = 'hybit_egrid_cell1.json'
base_dir = './'
output_file = 'results.csv'
data_dir = os.path.join(base_dir, 'data')
results_dir = os.path.join(base_dir, 'results')
output_file = os.path.join(results_dir, f'test_{output_file}')
os.makedirs(data_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

    ## grid model check
grid_file = os.path.join(data_dir, GRID_FILE)
grid_model = pp.from_json(grid_file)
pp.runpp(grid_model, numba=False)
print(f"Grid model of {len(grid_model.load)} loads,\
 {len(grid_model.sgen)} sgens,\
 {len(grid_model.bus)} buses,\
 {len(grid_model.line)} lines,\
 {len(grid_model.trafo)} trafos,\
 {len(grid_model.ext_grid)} ext_grids")

buses = grid_model.bus[grid_model.bus.name.str.contains('SteelPlant')]
print(buses)

for b in buses:
    for
pp.runpp(grid_model, numba=False)