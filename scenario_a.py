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

from data.config import MODEL_SETUPS, WT_MODULES, pv_model_params

sim_config = {
        'OutputSim': {
                    'python': 'mosaik_csv_writer:CSVWriter',
        },
        'InputSim': {
                    'python': 'mosaik_csv:CSV'
        },  
        'WTSim': {
            'python': 'mosaik_components.wind:Simulator'#'simulators.wind:Simulator'
        },
        'PVSim': {
            'python': 'pysimmods.mosaik.pysim_mosaik:PysimmodsSimulator'
        },
        #'FlexSim': {
        #        'python': 'simulators.flexible:Simulator',
        #},
        'GridSim': {
                'python': 'mosaik_components.pandapower:Simulator',
        },
        'CtrlSim': {
                'python': 'simulators.flexible:SimulatorA',
        },
    }

    ## Preperation
END = 24 * 60 * 60 * 1 # one day in seconds
START_DATE = '2023-03-01 00:00:00' # '2023-04-26 00:00:00
DATE_FORMAT = 'mixed' # 'YYYY-MM-DD hh:mm:ss'
STEP_SIZE = 15 * 60 # 15 minutes in seconds
WEATHER_DATA = 'weather_data_bremen_2020_2023.csv'
STEEL_PLANT_DATA = 'steel_plant_consumption_2023.csv'
POWER_PLANT_DATA = 'power_plant_generation_2023.csv'
GRID_FILE = 'hybit_egrid_cell1.json'
GEN_NEG = False

base_dir = os.path.dirname(__file__)
output_file = 'results.csv'
data_dir = os.path.join(base_dir, 'data')
results_dir = os.path.join(base_dir, 'results')
output_file = os.path.join(results_dir, f'a_{output_file}')
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

output_sim = world.start('OutputSim', sim_id="OutputSim", start_date = START_DATE,output_file=output_file)
outputs = output_sim.CSVWriter(buff_size=STEP_SIZE)

weater_input = world.start("InputSim", 
                            sim_id='WeaterSim',
                            sim_start=START_DATE, 
                            date_format=DATE_FORMAT,
                            datafile=os.path.join(data_dir, WEATHER_DATA))
weather = weater_input.WeatherData.create(1)[0]

pv_sim = world.start('PVSim', sim_id="PVSim", step_size=STEP_SIZE, start_date=f"{START_DATE}Z", gen_neg=GEN_NEG)
wt_sim = world.start("WTSim", sim_id=f"WTSim", step_size=STEP_SIZE, gen_neg=GEN_NEG)

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
grid_sim = world.start('GridSim', sim_id='GridSim', step_size=STEP_SIZE) # step_size=None is important to have the grid model triggered by any input
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

ctrl_sim = world.start("CtrlSim", sim_id="CtrlSim", step_size=STEP_SIZE, sim_params=dict(ctrl_attributes=ctrl_attributes))
ctrl = ctrl_sim.Ctrl.create(1)[0]

for k, v in ctrl_attributes.items():
    if 'PV' in k:
        world.connect(v['input'], ctrl, ('p_mw', k))
        world.connect(ctrl, v['output'], (k, 'P_gen[MW]'))
    elif 'WT' in k:
        world.connect(v['input'], ctrl, ('P_gen', k))
        world.connect(ctrl, v['output'], (k, 'P_gen[MW]'))
    elif 'SteelPlant' in k:
        world.connect(v['input'], ctrl, (f"L{k.split('-')[1]}-P[MW]", k))
        world.connect(ctrl, v['output'], (k, 'P_load[MW]'))
    elif 'PowerPlant' in k:
        world.connect(v['input'], ctrl, (f"G{k.split('-')[1]}-P[MW]", k))
        world.connect(ctrl, v['output'], (k, 'P_load[MW]'))
    world.connect(ctrl, outputs, k)

print(f'Power grid elements created: {len(power_units)}')
print(f'Controlled units: {len(ctrl_attributes)}')

mosaik.util.plot_dataflow_graph(world, hdf5path=os.path.join(results_dir, '.hdf5'), show_plot=False)
world.run(until=END, print_progress=True)#'individual')

print(f'Results were saved: {output_file}')

sys.exit()



flex_sim = world.start("FlexSim", sim_id="FlexSim", step_size=STEP_SIZE, sim_params=dict(gen_neg=False))




renewables = flex_sim.FLSim.create(1)[0] # summator for renewable power
conventionals = flex_sim.FLSim.create(1)[0] # summator for conventional power



units = {}
for id, setup in MODEL_SETUPS.items():
        if 'PV' in id:
            units[id] = pv_sim.Photovoltaic(**pv_model_params(**setup))
            world.connect(weather, units[id], 't_air_deg_celsius', 'bh_w_per_m2', 'dh_w_per_m2')
            world.connect(units[id], get_power_unit(id), ('p_mw', 'P_gen[MW]'))

            #switch_off.append(get_power_unit(id, 'StaticGen').eid)
            #world.connect(get_power_unit(id, 'StaticGen'), outputs, 'P[MW]')

            world.connect(units[id], renewables, ('p_mw', 'P[MW]'))
            #gens += 1
            #world.connect(units[id], outputs, ('p_mw', 'P[MW]'))
        elif 'WT' in id:
            units[id] = wt_sim.WT(max_power=setup['max_power'], 
                                  power_curve_csv=os.path.join(data_dir, WT_MODULES[setup["module_type"]]))
            world.connect(weather, units[id], 'wind_speed')
            world.connect(units[id], get_power_unit(id), ('P_gen', 'P_gen[MW]'))

            #switch_off.append(get_power_unit(id, 'StaticGen').eid)
            #world.connect(get_power_unit(id, 'StaticGen'), outputs, 'P[MW]')

            world.connect(units[id], renewables, ('P_gen', 'P[MW]'))
            #world.connect(units[id], outputs, ('P_gen', 'P[MW]'))
            #gens += 1

'''
for i, v in enumerate(get_power_unit('SteelPlant', first=False)):
    world.connect(steel_plant, v, (f'L{i+1}-P[MW]', 'P_load[MW]'))

world.connect(power_plant, conventionals, 'P[MW]')
for i, v in enumerate(get_power_unit('PowerPlant', first=False)):
    world.connect(power_plant, v, (f'G{i+1}-P[MW]', 'P_gen[MW]'))
'''




#world.connect(steel_plant, ctrl, 'P[MW]')
#for i, v in enumerate(get_power_unit('SteelPlant', first=False)):
#    print(ctrl_sim.meta)
#    world.connect(ctrl, v, (f'SteelPlant-{i+1}-P[MW]', 'P_load[MW]'))
#
#world.connect(power_plant, ctrl, 'P[MW]')


world.connect(power_units['ExternalGrid'][0], outputs, 'P[MW]')
world.connect(steel_plant, outputs, 'P[MW]')
world.connect(power_plant, outputs, 'P[MW]')
world.connect(renewables, outputs, 'P[MW]')
world.connect(conventionals, outputs, 'P[MW]')

#grid_sim.disable_elements(switch_off)

print(f'Renewable power units created: {len(units)}')
print(f'Power grid elements created: {len(power_units)}')

mosaik.util.plot_dataflow_graph(world, hdf5path=os.path.join(results_dir, '.hdf5'), show_plot=False)
world.run(until=END, print_progress=True)#'individual')

    ## testing part
print(f'Results were saved: {output_file}')
#r = pd.read_csv(output_file)
#s_test_sum = 0
#s_cols = ['WTSim-E82_2000kw.WT_2-P[MW]',
#            'WTSim-ANBONUS_2300kw.WT_3-P[MW]', 
#            'PVSim.Photovoltaic-15-P[MW]', 
#            'PVSim.Photovoltaic-6-P[MW]']
#
#for c in s_cols:
#        s_test_sum += r[c].sum()
#
#print(f'{s_test_sum:.2f}')
#
#print(f"{r['FlexSim.FLSim-0-P[MW]'].sum():.2f}")
#
#if __name__ == '__main__':
        
#        test_sims()
