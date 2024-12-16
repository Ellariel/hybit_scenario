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

from data.params import MODEL_SETUPS, WT_MODULES, pv_model_params

sim_config = {
        'WTSim': {
            'python': 'simulators.wind:Simulator'
        },
        'PVSim': {
            'python': 'pysimmods.mosaik.pysim_mosaik:PysimmodsSimulator'
        },
        'FlexSim': {
                'python': 'simulators.flexible:Simulator',
        },
        'GridSim': {
                'python': 'mosaik_components.pandapower:Simulator',
        },
        'OutputSim': {
                    'python': 'mosaik_csv_writer:CSVWriter',
        },
        'InputSim': {
                    'python': 'mosaik_csv:CSV'
        },  
    }

    ## Preperation
END = 24 * 60 * 60 * 1# one day in seconds
START_DATE = '2023-05-01 00:00:00'
DATE_FORMAT = 'mixed' # 'YYYY-MM-DD hh:mm:ss'
STEP_SIZE = 15 * 60 # 15 minutes in seconds
WEATHER_DATA = 'weather_data_2023.csv'
STEEL_PLANT_DATA = 'steel_plant_consumption_2023.csv'
GRID_FILE = 'hybit_egrid_cell1.json'
GEN_NEG = False


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

    ## Set up the "world" of the scenario
world = mosaik.World(sim_config)
output_sim = world.start('OutputSim', start_date = START_DATE,output_file=output_file)
pv_sim = world.start('PVSim', sim_id="PVSim", step_size=STEP_SIZE, start_date=f"{START_DATE}Z", gen_neg=GEN_NEG)
flex_sim = world.start("FlexSim", sim_id="FlexSim", step_size=STEP_SIZE, sim_params=dict(gen_neg=False))
#plant_sim = world.start("FlexSim", sim_id="PlantSim", step_size=STEP_SIZE, sim_params=dict(gen_neg=not GEN_NEG))
grid_sim = world.start('GridSim', step_size=STEP_SIZE) # step_size=None is important to have the grid model triggered by any input
weater_input = world.start("InputSim", 
                            sim_start=START_DATE, 
                            date_format=DATE_FORMAT,
                            datafile=os.path.join(data_dir, WEATHER_DATA))
plant_input = world.start("InputSim", 
                            sim_start=START_DATE, 
                            date_format=DATE_FORMAT,
                            datafile=os.path.join(data_dir, STEEL_PLANT_DATA))

outputs = output_sim.CSVWriter(buff_size=STEP_SIZE)
weather = weater_input.WeatherData.create(1)[0]

#plant_input = plant_input.SteelPlant.create(1)[0]
#steel_plant = plant_sim.FLSim.create(1)[0]
steel_plant = plant_input.SteelPlant.create(1)[0]

grid_model = grid_sim.Grid(json=grid_file)
extra_info = grid_sim.get_extra_info()
power_units = {v['name'] : (e, v) for k, v in extra_info.items()
                                for e in grid_model.children
                                    if e.eid == k and\
                                        ('ExternalGrid' in v['name'] or\
                                         'StaticGen' in v['name'] or\
                                         'Load' in v['name'] or\
                                         'Bus' in v['name'])}
renewables = flex_sim.FLSim.create(1)[0] # summator for renewable power
conventional = flex_sim.FLSim.create(1)[0] # summator for conventional power

def get_power_unit(key, type='Bus', first=True):
    units = []
    for k, v in power_units.items():
         if (f'-{key}-' in k) and (f'-{type}-' in k):
              units.append(v[0])
    if first:
        return units[0]
    return units

wt_sims = {}
switch_off = []
units = {}
#gens = 0
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
            model_type = setup["module_type"]
            wtsim = wt_sims.get(model_type)
            if not wtsim:
                wtsim = world.start("WTSim", sim_id=f"WTSim-{model_type}",
                                power_curve_csv=os.path.join(data_dir, WT_MODULES[model_type]),
                                step_size=STEP_SIZE, 
                                gen_neg=GEN_NEG)
                wt_sims[model_type] = wtsim
            units[id] = wtsim.WT(max_power=setup['max_power'])
            world.connect(weather, units[id], 'wind_speed')
            world.connect(units[id], get_power_unit(id), ('P_gen', 'P_gen[MW]'))

            #switch_off.append(get_power_unit(id, 'StaticGen').eid)
            #world.connect(get_power_unit(id, 'StaticGen'), outputs, 'P[MW]')

            world.connect(units[id], renewables, ('P_gen', 'P[MW]'))
            #world.connect(units[id], outputs, ('P_gen', 'P[MW]'))
            #gens += 1
#print(gens)
#i = 1

#print(get_power_unit('SteelPlant', first=False))

for i, v in enumerate(get_power_unit('SteelPlant', first=False)):
    world.connect(steel_plant, v, (f'L{i+1}-P[MW]', 'P_load[MW]'))

#for i, v in enumerate([v for k, v in power_units.items()
#                            if 'SteelPlant' in k and '-Bus-' in k]):
#    world.connect(steel_plant, v[0], (f'L{i+1}-P[MW]', 'P_load[MW]'))
    #if ('SteelPlant' in n) and ('-Load-' in n):
        #switch_off.append(v[0].eid)
        #world.connect(v[0], outputs, 'P[MW]')
    #if ('SteelPlant' in n) and ('-Bus-' in n):
        #world.connect(steel_plant, v[0], (f'L{i+1}-P[MW]', 'P_load[MW]'))
        #world.connect(v[0], outputs, 'P[MW]')
        #print(v[0], (f'L{i}-P[MW]', 'P_load[MW]'))
        #i += 1
        
        #world.connect(plant_input, steel_plant, 'P[MW]')
        #world.connect(steel_plant, get_power_unit('SteelPlant'), ('P[MW]', 'P_load[MW]'))
        #world.connect(steel_plant, outputs, 'P[MW]')
        #world.connect(get_power_unit('SteelPlant'), outputs, 'P[MW]')


#for e in grid_model.children:
#    if e.model == 'Line':
#           world.connect(e, outputs, 'loading[%]')

#sys.exit()
world.connect(power_units['ExternalGrid'][0], outputs, 'P[MW]')
world.connect(steel_plant, outputs, 'P[MW]')
world.connect(renewables, outputs, 'P[MW]')
world.connect(conventional, outputs, 'P[MW]')

#grid_sim.disable_elements(switch_off)

print(f'Renewable power units created: {len(units)}')
print(f'Power grid elements created: {len(power_units)}')

mosaik.util.plot_dataflow_graph(world, hdf5path=os.path.join(results_dir, '.hdf5'), show_plot=False)
world.run(until=END, print_progress='individual')

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
