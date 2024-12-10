'''
Test scenario for the Simulators used.
'''

import os
import sys
import mosaik
from mosaik.util import connect_many_to_one
from data.params import model_setup, setup

sim_config = {
    'WTSim': {
        'python': 'simulators.wind.simulator:Simulator'
    },
    'PVSim': {
        'python': 'pysimmods.mosaik.pysim_mosaik:PysimmodsSimulator'
    },
    'OutputSim': {
                'python': 'mosaik_csv_writer:CSVWriter',
    },
    'InputSim': {
                'python': 'mosaik_csv:CSV'
    },  
}

## Preperation
END = 24 * 60 * 60 # one day in seconds
START_DATE = '2023-11-01 00:00:00'
DATE_FORMAT = 'mixed' # 'YYYY-MM-DD hh:mm:ss'
STEP_SIZE = 15 * 60 # 15 minutes in seconds
WEATHER_DATA = 'DWD_weather_data_Bremen_2020_2023.csv' # data source: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/

base_dir = './'
data_dir = os.path.join(base_dir, 'data')
results_dir = os.path.join(base_dir, 'results')

## Set up the "world" of the scenario
world = mosaik.World(sim_config)

input_sim = world.start("InputSim", 
                        sim_start=START_DATE, 
                        date_format=DATE_FORMAT,
                        datafile=os.path.join(data_dir, WEATHER_DATA))
inputs = input_sim.WeatherData.create(1)[0]
pvsim = world.start('PVSim', step_size=STEP_SIZE, start_date=f"{START_DATE}Z")

wt_sims = {}
units = {}
for id in model_setup.keys():
    cfg = setup(id)
    if 'PV' in id:
        units[id] = pvsim.Photovoltaic(**cfg)
    elif 'WT' in id:       
        wtsim = world.start("WTSim", 
                            power_curve_csv=os.path.join(data_dir, cfg['power_curve_csv']),
                            step_size=STEP_SIZE, 
                            gen_neg=False)
        units[id] = wtsim.WT(max_power=cfg['max_power'])

print(units)

sys.exit()

# LOAD
SteelPlant_CSVload = world.start('CSV', sim_start=STEEL_START, datafile=STEELPLANT_LOAD_DATA)

## Instantiate model entities
powergrid = gridsim.Grid(gridfile=GRID_FILE).children
monitor = collector.Monitor()
controller = controllerSim.Controller(step_size=STEP_SIZE)

# GENERATION
#KW_Mittelsbueren = KW_CSVgeneration.Kraftwerk.create(1)
GUD_Mittelsbueren = GUD_CSVgeneration.Kraftwerk.create(1)
GT3_Mittelsbueren = GT3_CSVgeneration.Kraftwerk.create(1)
windData = WT_CSVspeedData.WindSpeed.create(1)
solarData = PV_CSVsolarData.SolarData.create(1)
    # Forschungs WEA Bremen GmbH
WT1_sim_model = wind_simulator_RE34_104_3400kw.WT(**{'max_power': 3.4})
    # WP Powerwind Anlage 1
WT2_sim_model = wind_simulator_PW90_2500kw.WT(**{'max_power': 2.5})  # Replacement power curve
    # WP Industriehäfen
WT3_sim_model = wind_simulator_E82_E2_2300kw.WT(**{'max_power': 2.3})
WT4_sim_model = wind_simulator_E82_E2_2300kw.WT(**{'max_power': 2.3})
    # WP swb Weserwind
WT5_sim_model = wind_simulator_ANBONUS_2000kw.WT(**{'max_power': 2})  # type-data from: https://www.wpd.de/projekte/referenzliste/#
WT6_sim_model = wind_simulator_ANBONUS_2000kw.WT(**{'max_power': 2})  # wasn't stated in Marktstammdatenregister
WT7_sim_model = wind_simulator_ANBONUS_2000kw.WT(**{'max_power': 2})
WT8_sim_model = wind_simulator_ANBONUS_2000kw.WT(**{'max_power': 2})
WT9_sim_model = wind_simulator_ANBONUS_2000kw.WT(**{'max_power': 2})
WT10_sim_model = wind_simulator_ANBONUS_2000kw.WT(**{'max_power': 2})
    # WP Stahlwerk Bremen
WT11_sim_model = wind_simulator_E82_2000kw.WT(**{'max_power': 2})
WT12_sim_model = wind_simulator_E82_2000kw.WT(**{'max_power': 2})
WT13_sim_model = wind_simulator_ANBONUS_2300kw.WT(**{'max_power': 2.3})
WT14_sim_model = wind_simulator_ANBONUS_2300kw.WT(**{'max_power': 2.3})
WT15_sim_model = wind_simulator_ANBONUS_2300kw.WT(**{'max_power': 2.3})
WT16_sim_model = wind_simulator_ANBONUS_2300kw.WT(**{'max_power': 2.3})
    # WP Mittelsbüren
WT17_sim_model = wind_simulator_E82_2000kw.WT(**{'max_power': 2})
WT18_sim_model = wind_simulator_E82_2000kw.WT(**{'max_power': 2})
    # Ölhafen
WT19_sim_model = wind_simulator_E82_E2_2300kw.WT(**{'max_power': 2.3})
    # WP Weserufer WEA 1
WT20_sim_model = wind_simulator_Senvion34_3400kw.WT(**{'max_power': 3.4})
    # WP Hüttenstraße
WT21_sim_model = wind_simulator_V90_2000kw.WT(**{'max_power': 2})
    #PV-panels
PV01_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_385Wp',257))
PV02_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_375Wp',266))
PV03_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_245Wp',120))
PV04_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_325Wp',34))
PV05_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_345Wp',64))
PV06_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_345Wp',288))
PV07_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_240Wp',1421))
PV08_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_205Wp',195))
PV09_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_330Wp',228))
PV10_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_235Wp',1757))
PV11_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_285Wp',34))
PV12_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_285Wp',34))
PV13_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_275Wp',36))
PV14_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_260Wp',30))
PV15_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_95Wp',132))
PV16_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_115Wp',299))
PV17_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_270Wp',108))
PV18_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_275Wp',36))
PV19_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_255Wp',117))
PV20_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_77_5Wp',756))
PV21_sim_model = pvSim.Photovoltaic(**pvModelParams('PV_310Wp',164))

# LOAD
Steel_Plant = SteelPlant_CSVload.SteelPlant.create(1)

## connect model entities
# get grid nodes and print list of them, to specify the connections
nodes_load = [element for element in powergrid if 'ext_load' in element.eid]
nodes_gen = [element for element in powergrid if 'ext_gen' in element.eid]
print("grid entities")
for x in range(0, len(nodes_gen)):
    print(x, nodes_gen[x])

    # GENERATION
#world.connect(KW_Mittelsbueren[0], nodes_gen[2], ('P_gen', 'p_mw'))
#world.connect(KW_Mittelsbueren[0], controller, ('P_gen','p_in_KW'))
#world.connect(KW_Mittelsbueren[0], monitor, 'P_gen')

world.connect(GUD_Mittelsbueren[0], nodes_gen[2], ('P_gen', 'p_mw'))
#world.connect(GUD_Mittelsbueren[0], monitor, 'P_gen')
world.connect(GUD_Mittelsbueren[0], controller, ('P_gen','p_in_KW'))
world.connect(GT3_Mittelsbueren[0], nodes_gen[2], ('P_gen', 'p_mw'))
world.connect(GT3_Mittelsbueren[0], controller, ('P_gen', 'p_in_KW'))
#world.connect(nodes_gen[2], monitor, 'p_mw')
    # wind turbines
    # high voltage
WT_sim_model_hv_list = [WT5_sim_model,
                        WT6_sim_model,
                        WT7_sim_model,
                        WT8_sim_model,
                        WT9_sim_model,
                        WT10_sim_model,
                        WT11_sim_model,
                        WT12_sim_model,
                        WT13_sim_model,
                        WT14_sim_model,
                        WT15_sim_model,
                        WT16_sim_model]
for WT_sim_model, x in zip(WT_sim_model_hv_list,range(4,15+1)):
    # wind_speed-data to sim-model to calculate P_gen
    world.connect(windData[0], WT_sim_model, 'wind_speed')
    # generated power to grid and controller
    world.connect(WT_sim_model, nodes_gen[x], ('P_gen', 'p_mw'))
    world.connect(WT_sim_model, controller, ('P_gen', 'p_in_WT'))
    # connections to monitor for visualisation
    #world.connect(nodes_gen[x], monitor, 'p_mw')
    # medium voltage
WT_sim_model_mv_list = [WT1_sim_model,
                        WT2_sim_model,
                        WT3_sim_model,
                        WT4_sim_model,
                        WT17_sim_model,
                        WT18_sim_model,
                        WT19_sim_model,
                        WT20_sim_model,
                        WT21_sim_model]
for WT_sim_model, x in zip(WT_sim_model_mv_list, range(148, 156 + 1)):
    #print(x)
    world.connect(windData[0], WT_sim_model, 'wind_speed')
    world.connect(WT_sim_model, nodes_gen[x], ('P_gen', 'p_mw'))
    world.connect(WT_sim_model, nodes_gen[x], ('P_gen', 'p_mw'))
    world.connect(WT_sim_model, controller, ('P_gen', 'p_in_WT'))
    #world.connect(nodes_gen[x], monitor, 'p_mw')

PV_sim_model_mv_list = [PV07_sim_model,
                        PV10_sim_model,
                        ]

for PV_sim_model, x in zip(PV_sim_model_mv_list, range(162, 163 + 1)):
    #print(x)
    world.connect(solarData[0], PV_sim_model, 't_air_deg_celsius', 'bh_w_per_m2', 'dh_w_per_m2')
    world.connect(PV_sim_model, nodes_gen[x], ('p_mw', 'p_mw'))
    world.connect(PV_sim_model, controller, ('p_mw', 'p_in_PV'))
    #world.connect(nodes_gen[x], monitor, 'p_mw')

PV_sim_model_lv_list = [PV01_sim_model,
                        PV02_sim_model,
                        PV03_sim_model,
                        PV04_sim_model,
                        PV05_sim_model,
                        PV06_sim_model,
                        PV08_sim_model,
                        PV09_sim_model,
                        PV11_sim_model,
                        PV12_sim_model,
                        PV13_sim_model,
                        PV14_sim_model,
                        PV15_sim_model,
                        PV16_sim_model,
                        PV17_sim_model,
                        PV18_sim_model,
                        PV19_sim_model,
                        PV20_sim_model,
                        PV21_sim_model
                        ]

for PV_sim_model, x in zip(PV_sim_model_lv_list, range(35,53+1)):
    #print(x)
    world.connect(solarData[0], PV_sim_model, 't_air_deg_celsius', 'bh_w_per_m2', 'dh_w_per_m2')
    world.connect(PV_sim_model, nodes_gen[x], ('p_mw', 'p_mw'))
    world.connect(PV_sim_model, controller, ('p_mw', 'p_in_PV'))
    #world.connect(nodes_gen[x], monitor, 'p_mw')

    # LOAD
world.connect(Steel_Plant[0], nodes_load[157], ('P_load', 'p_mw'))
#world.connect(Steel_Plant[1], nodes_load[158], ('P_load', 'p_mw'))
#world.connect(Steel_Plant[2], nodes_load[159], ('P_load', 'p_mw'))
#world.connect(Steel_Plant[3], nodes_load[160], ('P_load', 'p_mw'))
world.connect(Steel_Plant[0], controller, ('P_load', 'p_steelplant_demand_mw'))
#world.connect(Steel_Plant[1], controller, ('P_load', 'p_steelplant_demand'))
#world.connect(Steel_Plant[2], controller, ('P_load', 'p_steelplant_demand'))
#world.connect(Steel_Plant[3], controller, ('P_load', 'p_steelplant_demand'))

   # CONTROLLER
world.connect(controller, monitor, 'input_power_mwh', 'input_power_mwh_KW', 'input_power_mwh_WT', 'input_power_mwh_PV', 'p_steelplant_demand_mwh', 'p_steelplant_demand_per15min', 'used_gridPower', 'total_used_gridPower', 'total_steelplant_demand', 'total_input_power', 'total_input_power_KW')

## Save data in hdf5 file
# see "view_HDF5-results-file.py" to inspect resulting data
db = world.start('DB', step_size=STEP_SIZE, duration=END)
hdf5 = db.Database(filename='elecGrid-Scenario_results.hdf5')
connect_many_to_one(world, GT3_Mittelsbueren, hdf5, 'P_gen')
connect_many_to_one(world, GUD_Mittelsbueren, hdf5, 'P_gen')
connect_many_to_one(world, Steel_Plant, hdf5, 'P_load')
nodes = [e for e in powergrid if e.type in 'Bus']
print('nodes: ', nodes)
connect_many_to_one(world, nodes, hdf5, 'p_mw', 'q_mvar', 'vm_pu', 'va_degree')

#run
world.run(until=END)
