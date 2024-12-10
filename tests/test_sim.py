'''
Test scenario for the Simulators used.
'''

import os
import sys
import mosaik
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


def test_sim():
    """
    Run test.
    """

    dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    sys.path.append(dir)
    print('dir:', dir)

    from data.params import MODEL_SETUPS, WT_MODULES, pv_model_params
    
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

    base_dir = dir
    output_file = 'results.csv'
    data_dir = os.path.join(base_dir, 'data')
    results_dir = os.path.join(base_dir, 'results')
    output_file = os.path.join(results_dir, f'test_{output_file}')

    ## Set up the "world" of the scenario
    world = mosaik.World(sim_config)
    osim = world.start('OutputSim', start_date = START_DATE,output_file=output_file)
    isim = world.start("InputSim", 
                            sim_start=START_DATE, 
                            date_format=DATE_FORMAT,
                            datafile=os.path.join(data_dir, WEATHER_DATA))
    pvsim = world.start('PVSim', sim_id="PVSim", step_size=STEP_SIZE, start_date=f"{START_DATE}Z")
    outputs = osim.CSVWriter(buff_size=STEP_SIZE)
    inputs = isim.WeatherData.create(1)[0]
    wtsims = {}
    units = {}
    for id, setup in MODEL_SETUPS.items():
        if 'PV' in id:
            units[id] = pvsim.Photovoltaic(**pv_model_params(**setup))
            world.connect(inputs, units[id], 't_air_deg_celsius', 'bh_w_per_m2', 'dh_w_per_m2')
            world.connect(units[id], outputs, ('p_mw', 'P[MW]'))
        elif 'WT' in id:
            model_type = setup["module_type"]
            wtsim = wtsims.get(model_type)
            if not wtsim:
                wtsim = world.start("WTSim", sim_id=f"WTSim-{model_type}",
                                power_curve_csv=os.path.join(data_dir, WT_MODULES[model_type]),
                                step_size=STEP_SIZE, 
                                gen_neg=False)
                wtsims[model_type] = wtsim
            units[id] = wtsim.WT(max_power=setup['max_power'])
            world.connect(inputs, units[id], 'wind_speed')
            world.connect(units[id], outputs, ('P_gen', 'P[MW]'))

    print(f'Power units created: {len(units)}')

    world.run(until=END, print_progress='individual')

    ## testing part
    print(f'Results were saved: {output_file}')
    r = pd.read_csv(output_file)
    test_sum = 0
    cols = ['WTSim-E82_2000kw.WT_2-P[MW]',
            'WTSim-ANBONUS_2300kw.WT_3-P[MW]', 
            'PVSim.Photovoltaic-15-P[MW]', 
            'PVSim.Photovoltaic-6-P[MW]']

    for c in cols:
        test_sum += r[c].sum()

    assert f'{test_sum:.2f}' == '25.49'


if __name__ == '__main__':
        
        test_sim()