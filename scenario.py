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

from data.config import MODEL_SETUPS, WT_MODULES, BT_PARAMS, pv_model_params

sim_config = {
        'OutputSim': {
                    'python': 'mosaik_csv_writer:CSVWriter',
        },
        'InputSim': {
                    'python': 'mosaik_csv:CSV',
        },  
        'WTSim': {
            'python': 'mosaik_components.wind:Simulator', #'simulators.wind:Simulator'
        },
        'PVSim': {
            'python': 'pysimmods.mosaik.pysim_mosaik:PysimmodsSimulator',
        },
        #'FlexSim': {
        #        'python': 'simulators.flexible:Simulator',
        #},
        'BTSim': {
            'python': 'simulators.flexible.battery:Simulator',#'pysimmods.mosaik.pysim_mosaik:PysimmodsSimulator',
        },
        'GridSim': {
                'python': 'mosaik_components.pandapower:Simulator',
        },
        'CtrlSim': {
                'python': 'simulators.flexible:CtrlSimulator',
        },
    }

    ## Preperation
SCENARIO_TYPE = 'A'
END = 60 * 60 * 1 # one day in seconds
START_DATE = '2023-03-01 00:00:00' # '2023-04-26 00:00:00
DATE_FORMAT = 'mixed' # 'YYYY-MM-DD hh:mm:ss'
STEP_SIZE = 15 * 60 # 15 minutes in seconds
WEATHER_DATA = 'weather_data_bremen_2020_2023.csv'
STEEL_PLANT_DATA = 'steel_plant_consumption_2023.csv'
POWER_PLANT_DATA = 'power_plant_generation_2023.csv'
GRID_FILE = 'hybit_egrid_cell1.json'

base_dir = os.path.dirname(__file__)
output_file = f'results_{SCENARIO_TYPE}.csv'
data_dir = os.path.join(base_dir, 'data')
results_dir = os.path.join(base_dir, 'results')
output_file = os.path.join(results_dir, output_file)
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

world = mosaik.World(sim_config)

output_sim = world.start('OutputSim', sim_id="OutputSim", start_date=START_DATE, output_file=output_file)
outputs = output_sim.CSVWriter(buff_size=STEP_SIZE)

weater_input = world.start("InputSim", 
                            sim_id='WeaterSim',
                            sim_start=START_DATE, 
                            date_format=DATE_FORMAT,
                            datafile=os.path.join(data_dir, WEATHER_DATA))
weather = weater_input.WeatherData.create(1)[0]

pv_sim = world.start('PVSim', sim_id="PVSim", step_size=STEP_SIZE, start_date=f"{START_DATE}Z")
wt_sim = world.start("WTSim", sim_id=f"WTSim", step_size=STEP_SIZE, gen_neg=False)

steel_plant_input = world.start("InputSim", 
                            sim_id='SteelPlantSim',
                            sim_start=START_DATE, 
                            date_format=DATE_FORMAT,
                            datafile=os.path.join(data_dir, STEEL_PLANT_DATA))
steel_plant = steel_plant_input.SteelPlant.create(1)[0]

power_plant_input = world.start("InputSim", 
                            sim_id='PowerPlantSim',
                            sim_start=START_DATE, 
                            date_format=DATE_FORMAT,
                            datafile=os.path.join(data_dir, POWER_PLANT_DATA))
power_plant = power_plant_input.PowerPlant.create(1)[0]

## Electricity grid model
grid_sim = world.start('GridSim', sim_id='GridSim', step_size=None) # step_size=None is important to have the grid model triggered by any input
grid_model = grid_sim.Grid(json=grid_file)
power_units = {v['name'] : (e, v) for k, v in grid_sim.get_extra_info().items()
                                for e in grid_model.children
                                    if e.eid == k and\
                                        ('ExternalGrid' in v['name'] or\
                                         'StaticGen' in v['name'] or\
                                         'Load' in v['name'] or\
                                         'Bus' in v['name'])}

def get_power_unit(key, type='Bus', first=True):
    units = []
    for k, v in power_units.items():
         if (f'-{key}-' in k) and (f'-{type}-' in k):
            if first:
                return v[0] 
            units.append(v[0])
    return units

ctrl_attributes = {}
for i, v in enumerate(get_power_unit('SteelPlant', first=False)):
    ctrl_attributes[f'SteelPlant-{i+1}-P[MW]'] = {'output': v, 'input': steel_plant}
    
for i, v in enumerate(get_power_unit('PowerPlant', first=False)):
    ctrl_attributes[f'PowerPlant-{i+1}-P[MW]'] = {'output': v, 'input': power_plant}

pv, wt = [], []
for id, setup in MODEL_SETUPS.items():
        if 'PV' in id:
            pv += [pv_sim.Photovoltaic(**pv_model_params(**setup))]
            world.connect(weather, pv[-1], 't_air_deg_celsius', 'bh_w_per_m2', 'dh_w_per_m2')
            ctrl_attributes[f'PV-{len(pv)}-P[MW]'] = {'output': get_power_unit(id), 'input': pv[-1]}
        elif 'WT' in id:
            wt += [wt_sim.WT(max_power=setup['max_power'], 
                                  power_curve_csv=os.path.join(data_dir, WT_MODULES[setup["module_type"]]))]
            world.connect(weather, wt[-1], 'wind_speed')
            ctrl_attributes[f'WT-{len(wt)}-P[MW]'] = {'output': get_power_unit(id), 'input': wt[-1]}

if SCENARIO_TYPE == 'A':

    # control cycle
    with world.group():

        bt_sim = world.start('BTSim', sim_id="BTSim", step_size=STEP_SIZE, start_date=f"{START_DATE}Z")
        bt = bt_sim.Battery(**BT_PARAMS)
        ctrl_attributes[f'Battery-1-P[MW]'] = {'output': get_power_unit('Battery'), 'input': bt}
        ctrl_attributes[f'Battery-1-SET-P[MW]'] = ctrl_attributes[f'Battery-1-P[MW]']

    #world.connect(batModel, controller, ('soc_percent', 'soc_bat'))
    #world.connect(controller, batModel, ('p_out_toBat', 'p_set_mw'), weak=True)
    #world.connect(batModel, nodes_load[162], ('p_mw', 'p_mw'))
    #world.connect(nodes_load[65], monitor, 'p_mw')
    #world.connect(batModel, monitor,  'p_mw', 'soc_percent')



    #    Battery
    #    pass

        ctrl_sim = world.start("CtrlSim", sim_id="CtrlSim", step_size=STEP_SIZE, sim_params=dict(ctrl_attributes=ctrl_attributes, 
                                                                                                scenario_type=SCENARIO_TYPE,
                                                                                                gen_neg=False))
        ctrl = ctrl_sim.Ctrl.create(1)[0]



world.connect(power_units['ExternalGrid'][0], outputs, ('P[MW]', 'ExternalGrid-P[MW]'))
world.connect(bt, outputs, 'p_mw')
world.connect(bt, outputs, 'soc_percent')


for k, v in ctrl_attributes.items():
    if 'PV' in k:
        world.connect(v['input'], ctrl, ('p_mw', k))
        #world.connect(v['input'], outputs, 'p_mw')
        world.connect(ctrl, v['output'], (k, 'P_gen[MW]'))
    elif 'WT' in k:
        world.connect(v['input'], ctrl, ('P_gen', k))
        world.connect(ctrl, v['output'], (k, 'P_gen[MW]'))
    elif 'SteelPlant' in k:
        world.connect(v['input'], ctrl, (f"L{k.split('-')[1]}-P[MW]", k))
        world.connect(ctrl, v['output'], (k, 'P_load[MW]'))
    elif 'PowerPlant' in k:
        world.connect(v['input'], ctrl, (f"G{k.split('-')[1]}-P[MW]", k))
        world.connect(ctrl, v['output'], (k, 'P_gen[MW]'))
    elif 'Battery' in k:
        if 'SET' in k:
            world.connect(ctrl, v['input'], (k, 'p_set_mw'))
        else:
            world.connect(v['input'], ctrl, ('p_mw', k), weak=True, initial_data={'p_mw': 0})
            #world.connect(v['input'], v['output'], ('p_mw', 'P_load[MW]'))
            #world.connect(ctrl, v['output'], (k, 'P_load[MW]'))

    world.connect(ctrl, outputs, k)

print(f'Power grid elements created: {len(power_units)}')
print(f'Controlled units: {len(ctrl_attributes)}')

mosaik.util.plot_dataflow_graph(world, hdf5path=os.path.join(results_dir, '.hdf5'), show_plot=False)
world.run(until=END, print_progress=True)#'individual')

print(f'Results were saved: {output_file}')