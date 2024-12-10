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


def test_sims():
    """
    Run test.
    """

    dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    sys.path.append(dir)
    print('dir:', dir)

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
    flsim = world.start("FlexSim", sim_id="FlexSim", step_size=STEP_SIZE, sim_params=dict(gen_neg=False))
        
    outputs = osim.CSVWriter(buff_size=STEP_SIZE)
    inputs = isim.WeatherData.create(1)[0]
    wtsims = {}
    units = {}
    for id, setup in MODEL_SETUPS.items():
        if 'PV' in id:
            units[id] = pvsim.Photovoltaic(**pv_model_params(**setup))
            fl = flsim.FLSim.create(1)[0]
            world.connect(inputs, units[id], 't_air_deg_celsius', 'bh_w_per_m2', 'dh_w_per_m2')
            world.connect(units[id], fl, ('p_mw', 'P[MW]'))
            world.connect(units[id], outputs, ('p_mw', 'P[MW]'))
            world.connect(fl, outputs, 'P[MW]')
            #print(id, fl, units[id])
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
            fl = flsim.FLSim.create(1)[0]
            world.connect(inputs, units[id], 'wind_speed')
            world.connect(units[id], fl, ('P_gen', 'P[MW]'))
            world.connect(units[id], outputs, ('P_gen', 'P[MW]'))
            world.connect(fl, outputs, 'P[MW]')
            #print(id, fl, units[id])

    print(f'Power units created: {len(units)}')

    world.run(until=END, print_progress='individual')

    ## testing part
    print(f'Results were saved: {output_file}')
    r = pd.read_csv(output_file)
    s_test_sum = 0
    f_test_sum = 0
    s_cols = ['WTSim-E82_2000kw.WT_2-P[MW]',
            'WTSim-ANBONUS_2300kw.WT_3-P[MW]', 
            'PVSim.Photovoltaic-15-P[MW]', 
            'PVSim.Photovoltaic-6-P[MW]']
    f_cols = ['FlexSim.FLSim-16-P[MW]',
            'FlexSim.FLSim-15-P[MW]', 
            'FlexSim.FLSim-36-P[MW]', 
            'FlexSim.FLSim-27-P[MW]']

    for c in s_cols:
        s_test_sum += r[c].sum()

    for c in f_cols:
        f_test_sum += r[c].sum()

    assert f'{s_test_sum:.2f}' == '25.49'
    assert f'{f_test_sum:.2f}' == '25.49'


if __name__ == '__main__':
        
        test_sims()
