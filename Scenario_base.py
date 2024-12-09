'''
This file contains the Base-Scenario of the hydrogen and electricity based Steel-plant.

An Electrolyser is connected to several wind-turbines and PV-Systems (all located in the area around the steel-plant),
and the power grid. The Electrolyser produces H2 for the Steel-plant, the target product.
A Controller ensures, that the electrolyser always gets enough power to meet the H2-demand. The
Controller gets the information about the current H2-demand and thereof calculates the corresponding
power-demand of the electrolyser. In the next step a decision tree is used, to decide from where the
electrolyser gets the needed power. If the wind-turbines and PV-systems generate enough electricity, this is used,
otherwise the state of charge of the battery is checked and the remaining part is taken from the grid.
If the wind turbines produce a surplus, the battery is charged with it.

mosaik-version: 3.2.0
'''


## Import packages needed for the scenario.
import mosaik
from mosaik.util import connect_many_to_one

## Specify simulator configurations
sim_config = {
    'Grid': {
        'python': 'mosaik_pandapower.simulator:Pandapower'
    },
    'CSV': {
        #'python': 'mosaik_csv:CSV' # getting type error with the original script
        'python': 'mosaik_components.mosaik_csv_test:CSV' # part of the get_data method was changed to fix type error
    },
    'DB': {
        'cmd': 'mosaik-hdf5 %(addr)s'
    },
    'Collector': {
        'cmd': '%(python)s ../mosaik_components/collector.py %(addr)s'
    },
    'Wind': {
        'python': 'mosaik_components.wind.Simulator:Simulator' # function get_power_curve (in WindTurbine script) adjusted
    },
    'PVSim': {
        'python': 'pysimmods.mosaik.pysim_mosaik:PysimmodsSimulator'
    },
    'Controller': {
        'python': 'mosaik_components.controller_base:Controller'
    },
}

## Preperation
END = 30 * 24 * 60 * 60 # one day in seconds
START = '2023-11-01 00:00:00'
BAT_START = '2023-11-01 00:00:00+00:00'
STEEL_START = '2019-11-01 00:00:00'
STEP_SIZE=15*60 # 15 minutes in seconds
# Set file paths
GRID_FILE = '../data/electricGrid_cell1.json'
    # GENERATION DATA
#KW_GENERATION_DATA = '../data/KW_generation_data.csv' # Kraftwerk Mittelsbüren -> made up data for 1 day
GUD_GENERATION_DATA = '../data/GUD_generation_data.csv' # Gas und Dampf Kombikraftwerk (GUD) Mittelsbüren -> made up data for one day
GT3_GENERATION_DATA = '../data/GT3_generation_data.csv'
    # LOAD DATA
STEELPLANT_LOAD_DATA = '../data/profileA_1.15TW_MW.csv' # example load profile from hyBit-project
    # WIND TURBINES
E82E2_POWER_CURVE = '../data/powerCurve_E-82E2_2300kW.txt' # data source: https://www.wind-turbine-models.com/turbines/550-enercon-e-82-e2-2.300#powercurve [last access: 29.08.2024]
E82_Power_CURVE = '../data/powerCurve_E-82_2000kW.txt' # data source: https://www.reuthwind.de/enercon/enercon_e82.pdf [last access: 29.08.2024]
REpower104_POWER_CURVE = '../data/powerCurve_REpower_3400kW-104.txt' # data source: https://www.thewindpower.net/turbine_de_553_senvion_3.4m104.php [last access: 29.08.2024]
VestasV90_POWER_CURVE = '../data/powerCurve_Vestas-V90.txt' # data source: https://www.wind-turbine-models.com/turbines/16-vestas-v90#powercurve [last access: 29.08.2024]
ANBONUS23_POWER_CURVE = '../data/powerCurve_AN-BONUS_2300kW-82.txt' # data source: https://www.wind-turbine-models.com/turbines/699-bonus-b82-2300#powercurve [last access: 29.08.2024]
ANBONUS2_76_POWER_CURVE = '../data/powerCurve_AN-BONUS_2000kW-76.txt' # data source: https://www.thewindpower.net/turbine_de_229_bonus_b76-2000.php [last access: 29.08.2024]
Senvion34_POWER_CURVE = '../data/powerCurve_Senvion-3400kW.txt' # data source: https://en.wind-turbine-models.com/turbines/1003-senvion-3.4m114 [last access: 29.08.2024]
PW90_POWER_CURVE = '../data/powerCurve_FL2500kw-90.txt' # no power curve for PW90 available, therefore used data of a similar turbine: https://www.thewindpower.net/turbine_de_153_fuhrlander_fl-2500-90.php [last access: 29.08.2024]
WIND_SPEED_DATA = '../data/DWD_wind_speed_data_Bremen_2020_2023.csv' # data source: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/wind/historical/10minutenwerte_wind_00691_20000101_20091231_hist.zip [last access: 29.08.2024]
   # PV
# solar data for PV
SOLAR_DATA = '../data/DWD_solar_data_Bremen_2020_2023.csv' # solar data for PV
def pvModelParams(moduleType, no_modules):
    no_modules = no_modules
    PV_modules = {
        'PV_77_5Wp': {'module_length': 1200, 'module_width': 600, 'module_p_peak_kw': 0.0775, 'eta': 0.108}, # eta self-calculated; source: https://www.pvxchange.com/mediafiles/pvxchange/attachments/FS%20Series%202%20Datasheet%20-%20German.pdf
        'PV_95Wp': {'module_length': 1070, 'module_width': 536, 'module_p_peak_kw': 0.095, 'eta': 0.166}, # eta self-calculated: source: https://www.amumot-shop.de/dateien/solarswiss/solarmodul-rahmen-kvm5-95-140-datenblatt.pdf
        'PV_115Wp': {'module_length': 1200, 'module_width': 505, 'module_p_peak_kw': 0.115, 'eta': 0.19}, # source: https://www.esomatic.de/media/pdf/57/54/11/Datenblatt-FDS115-12M10-115Wp.pdf
        #'PV_175Wp': {'module_length': 1482, 'module_width': 676, 'module_p_peak_kw': 0.175, 'eta': 0.175}, # source: https://cdn.enfsolar.com/z/pp/xay60e3c78bd9c1c/5d1e9c90385fe.pdf [last access: 17.09.2024]
        #'PV_185Wp': {'module_length': 1482, 'module_width': 676, 'module_p_peak_kw': 0.185, 'eta': 0.185}, # source: https://cdn.enfsolar.com/z/pp/jddl58oj31/5efbfcf578167.pdf [last access: 17.09.2024]
        'PV_205Wp': {'module_length': 1586, 'module_width': 806, 'module_p_peak_kw': 0.205, 'eta': 0.1614}, # source: https://www.solarswiss.de/unsere-produkte/pv-solarmodule/solarmodul-kvm-205w-24v/ [last access: 17.09.2024]
        'PV_210Wp': {'module_length': 1586, 'module_width': 806, 'module_p_peak_kw': 0.21, 'eta': 0.1643}, # source: https://www.solarswiss.de/unsere-produkte/pv-solarmodule/solarmodul-210-watt-kvm-210-w-24v/ [last access: 17.09.2024]
        #'PV_225Wp': {'module_length': 1650, 'module_width': 992, 'module_p_peak_kw': 0.225, 'eta': 0.137},  # source: https://solarstrom.turbo.at/file.axd?file=/Photovoltaikmodule/TrinaSolar%20TSM-PC05.pdf [last access: 17.ß9.2024]
        'PV_235Wp': {'module_length': 1650, 'module_width': 992, 'module_p_peak_kw': 0.235, 'eta': 0.144},  # source: https://solarstrom.turbo.at/file.axd?file=/Photovoltaikmodule/TrinaSolar%20TSM-PC05.pdf [last access: 17.ß9.2024]
        'PV_240Wp': {'module_length': 1640, 'module_width': 990, 'module_p_peak_kw': 0.240, 'eta': 0.148}, # source: https://www.photovoltaik4all.de/media/e9/15/a1/1694533548/yin03214_ds_yge60cell-29b_series_2_eu_de_201410_v03-hr-1.pdf [last access: 17.09.2024]
        'PV_245Wp': {'module_length': 1640, 'module_width': 990, 'module_p_peak_kw': 0.245, 'eta': 0.151}, # source: https://www.photovoltaik4all.de/media/e9/15/a1/1694533548/yin03214_ds_yge60cell-29b_series_2_eu_de_201410_v03-hr-1.pdf [last access: 17.09.2024]
        'PV_255Wp': {'module_length': 1640, 'module_width': 990, 'module_p_peak_kw': 0.255, 'eta': 0.157}, # source: https://www.photovoltaik4all.de/media/e9/15/a1/1694533548/yin03214_ds_yge60cell-29b_series_2_eu_de_201410_v03-hr-1.pdf [last access: 17.09.2024]
        'PV_260Wp': {'module_length': 1640, 'module_width': 992, 'module_p_peak_kw': 0.260, 'eta': 0.160}, # source: https://www.photovoltaik4all.de/media/e9/15/a1/1694533548/yin03214_ds_yge60cell-29b_series_2_eu_de_201410_v03-hr-1.pdf [last access: 17.09.2024]
        'PV_270Wp': {'module_length': 1678, 'module_width': 991, 'module_p_peak_kw': 0.270, 'eta': 0.162}, # source: https://echtsolar.de/wp-content/uploads/2021/07/JA-Solar-JAP60S03-270-290-SC_Datenblatt.pdf [last access: 17.09.2024]
        'PV_275Wp': {'module_length': 1678, 'module_width': 991, 'module_p_peak_kw': 0.275, 'eta': 0.165}, # source: https://echtsolar.de/wp-content/uploads/2021/07/JA-Solar-JAP60S03-270-290-SC_Datenblatt.pdf [last access: 17.09.2024]
        #'PV_280Wp': {'module_length': 1678, 'module_width': 991, 'module_p_peak_kw': 0.280, 'eta': 0.168}, # source: https://echtsolar.de/wp-content/uploads/2021/07/JA-Solar-JAP60S03-270-290-SC_Datenblatt.pdf [last access: 17.09.2024]
        'PV_285Wp': {'module_length': 1678, 'module_width': 991, 'module_p_peak_kw': 0.285, 'eta': 0.171}, # source: https://echtsolar.de/wp-content/uploads/2021/07/JA-Solar-JAP60S03-270-290-SC_Datenblatt.pdf [last access: 17.09.2024]
        #'PV_290Wp': {'module_length': 1678, 'module_width': 991, 'module_p_peak_kw': 0.290, 'eta': 0.174}, # source: https://echtsolar.de/wp-content/uploads/2021/07/JA-Solar-JAP60S03-270-290-SC_Datenblatt.pdf [last access: 17.09.2024]
        'PV_310Wp': {'module_length': 1680, 'module_width': 990, 'module_p_peak_kw': 0.310, 'eta': 0.188}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Solarwatt-Vision-60M-Datenblatt-DE.pdf[last access: 17.09.2024]
        #'PV_320Wp': {'module_length': 1680, 'module_width': 990, 'module_p_peak_kw': 0.320, 'eta': 0.194}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Solarwatt-Vision-60M-Datenblatt-DE.pdf[last access: 17.09.2024]
        'PV_325Wp': {'module_length': 1670, 'module_width': 1006, 'module_p_peak_kw': 0.325, 'eta': 0.194}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Heckert-Solar-Nemo-2.0-60-M-Black-Datenblatt-DE.pdf [last access: 17.09.2024]
        'PV_330Wp': {'module_length': 1700, 'module_width': 1000, 'module_p_peak_kw': 0.330, 'eta': 0.194}, # source: https://echtsolar.de/wp-content/uploads/2021/07/Sonnenstromfabrik-EXCELLENT_320-325-330_M60-Datenblatt.pdf [last access: 17.09.2024]
        'PV_335Wp': {'module_length': 1670, 'module_width': 1006, 'module_p_peak_kw': 0.335, 'eta': 0.199}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Heckert-Solar-Nemo-2.0-60-M-Datenblatt-DE-2022.pdf [last access: 17.09.2024]
        'PV_345Wp': {'module_length': 1716, 'module_width': 1023, 'module_p_peak_kw': 0.345, 'eta': 0.197}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Aleo-Solar-X63-Premium-2022-Datenblatt-DE.pdf [last access: 17.09.2024]
        'PV_375Wp': {'module_length': 1780, 'module_width': 1052, 'module_p_peak_kw': 0.375, 'eta': 0.202}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Solarwatt-vision-H-3.0-pure-Datenblatt-DE.pdf
        'PV_385Wp': {'module_length': 1767, 'module_width': 1041, 'module_p_peak_kw': 0.385, 'eta': 0.209}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Meyer-Burger-Black-Datenblatt-DE.pdf
    }
    moduleData = PV_modules[moduleType]

    module_Length = moduleData['module_length']
    module_width = moduleData['module_width']
    a_m2 = no_modules * module_Length * module_width * 0.0001 # overall area of PV modules / Gesamtfläche der PV-Anlage (in m^2)
    p_peak_kw = no_modules * moduleData['module_p_peak_kw']  # peak power of PV plant / Nennleistung der PV-Anlage (in kw): x Wp pro Modul bei insgesamt y Modulen
    eta = moduleData['eta']  # efficiency of pv plant / Effizienz der PV-Anlage

    cos_phi = 0.95  # Leistungsfaktor (Phasenwinkel)
    t_module_deg_celsius = 15  # initial temperature of PV module / Anfangstemperatur der Module (in °C)

    pv_model_params = {
        # https://midas-mosaik.gitlab.io/pysimmods/base-models/pv.html
        "params" : {
            "pv": {
                "a_m2": a_m2,
                "eta_percent": eta * 100.0,
            },
            "inverter": {
                "sn_kva": p_peak_kw / cos_phi,
                "q_control": "prioritize_p",
                "cos_phi": cos_phi,
                "inverter_mode": "capacitive",
            },
            "sign_convention": "active",
        },
        "inits" : {
            "pv": {
                "t_module_deg_celsius": t_module_deg_celsius,
            },
            "inverter": None,
        },
    }

    return pv_model_params


## Set up the "world" of the scenario
world = mosaik.World(sim_config)

## Initialize the simulators
gridsim = world.start('Grid', step_size=STEP_SIZE, mode='pf')
collector = world.start('Collector')
controllerSim = world.start('Controller')

# GENERATION
    # gas power plants
#KW_CSVgeneration = world.start('CSV', sim_start=START, datafile=KW_GENERATION_DATA) # KW Mittelsbueren (https://www.marktstammdatenregister.de/MaStR/Einheit/Detail/IndexOeffentlich/4443193)
GUD_CSVgeneration = world.start('CSV', sim_start=START, datafile=GUD_GENERATION_DATA) # GUD Mittelsbueren (https://www.marktstammdatenregister.de/MaStR/Einheit/Detail/IndexOeffentlich/3271556)
GT3_CSVgeneration = world.start('CSV', sim_start=START, datafile=GT3_GENERATION_DATA)
    # wind turbines
WT_CSVspeedData = world.start('CSV', sim_start=START, datafile=WIND_SPEED_DATA)
wind_simulator_E82_2000kw = world.start('Wind', power_curve_csv=E82_Power_CURVE, step_size=STEP_SIZE, gen_neg=False)
wind_simulator_RE34_104_3400kw = world.start('Wind', power_curve_csv=REpower104_POWER_CURVE, step_size=STEP_SIZE, gen_neg=False)
wind_simulator_E82_E2_2300kw = world.start('Wind', power_curve_csv=E82E2_POWER_CURVE, step_size=STEP_SIZE, gen_neg=False)
wind_simulator_ANBONUS_2300kw = world.start('Wind', power_curve_csv=ANBONUS23_POWER_CURVE, step_size=STEP_SIZE, gen_neg=False)
wind_simulator_ANBONUS_2000kw = world.start('Wind', power_curve_csv=ANBONUS2_76_POWER_CURVE, step_size=STEP_SIZE, gen_neg=False)
wind_simulator_V90_2000kw = world.start('Wind', power_curve_csv=VestasV90_POWER_CURVE, step_size=STEP_SIZE, gen_neg=False)
wind_simulator_Senvion34_3400kw = world.start('Wind', power_curve_csv=Senvion34_POWER_CURVE, step_size=STEP_SIZE, gen_neg=False)
wind_simulator_PW90_2500kw = world.start('Wind', power_curve_csv=PW90_POWER_CURVE, step_size=STEP_SIZE, gen_neg=False)
    # pv panels
PV_CSVsolarData = world.start('CSV', sim_start=START, datafile=SOLAR_DATA)
pvSim = world.start('PVSim', step_size=STEP_SIZE, start_date=BAT_START)

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
