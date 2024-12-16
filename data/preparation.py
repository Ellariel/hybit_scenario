"""
Data files dowloaded from DWD are beeing prepared for usage as input for simulators.
data source [last access: 10.12.2024]: 
https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/
https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/air_temperature/historical/10minutenwerte_TU_00691_20200101_20231231_hist.zip
https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/solar/historical/10minutenwerte_SOLAR_00691_20200101_20231231_hist.zip
https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/wind/historical/10minutenwerte_wind_00691_20200101_20231231_hist.zip

"""
import os
import sys
import zipfile
import pandas as pd
from pathlib import Path

def zopen(archive):
    try:
        with zipfile.ZipFile(archive) as z:    
            for filename in z.namelist():
                if not os.path.isdir(filename):
                    #print(f'\nFile "{filename}":')
                    return z.open(filename)
                else:
                    print(f'\nDirectory "{filename}"')
                    break
    except zipfile.BadZipFile:
        print(f'Bad zip file: "{archive}"')
    except IsADirectoryError:
        print(f'Directory, not file: "{archive}"')
    except FileNotFoundError:
        print(f'File not found: "{archive}"')


## BASE CONFIG
base_dir = os.path.dirname(__file__)


## WEATHER DATA PREPARATION

delimiter = ';'
datafile_path_temp = os.path.join(base_dir, '10minutenwerte_TU_00691_20200101_20231231_hist.zip')
datafile_path_solar = os.path.join(base_dir, '10minutenwerte_SOLAR_00691_20200101_20231231_hist.zip')
datafile_path_wind = os.path.join(base_dir, '10minutenwerte_wind_00691_20200101_20231231_hist.zip')
weather_file = os.path.join(base_dir, 'weather_data_2023.csv')

# open the files for reading
datafile_temp = zopen(datafile_path_temp)
datafile_temp = pd.read_csv(datafile_temp, delimiter=delimiter, dtype=str)
datafile_solar = zopen(datafile_path_solar)
datafile_solar = pd.read_csv(datafile_solar, delimiter=delimiter, dtype=str)
datafile_wind = zopen(datafile_path_wind)
datafile_wind = pd.read_csv(datafile_wind, delimiter=delimiter, dtype=str)

df = pd.merge(datafile_temp, datafile_solar, on='MESS_DATUM', how='left')
df = pd.merge(df, datafile_wind, on='MESS_DATUM', how='left')
df['Time'] = df['MESS_DATUM'].apply(lambda x: f"{x[0:4]}-{x[4:6]}-{x[6:8]} {x[8:10]}:{x[10:12]}:00")
df['t_air_deg_celsius'] = pd.to_numeric(df['TT_10'])
df['bh_w_per_m2'] = pd.to_numeric(df['GS_10']) - pd.to_numeric(df['DS_10'])
df['dh_w_per_m2'] = pd.to_numeric(df['DS_10'])
df['wind_speed'] = pd.to_numeric(df['FF_10'])
        # TT_10 # air temperature in two meters height of the previous 10 minutes
        # DS_10 # sum of diffuse solar radiation of the previous 10 minutes
        # GS_10 # sum of global solar radiation of the previous 10 minutes
        #'t_air_deg_celsius' = TT_10 # air temperature
        # bh_w_per_m2 = GS_10 - DS_10
        # dh_w_per_m2 = DS_10
        # FF_10 - wind speed
df[['Time', 't_air_deg_celsius', 'bh_w_per_m2', 'dh_w_per_m2', 'wind_speed']].to_csv(weather_file, index=False)
weather_file = Path(weather_file)
weather_file.write_text(f"WeatherData\n{weather_file.read_text()}")


## STEEL PLANT DATA PREPARATION


delimiter = ','
correct_year = 2023
datafile_plant = os.path.join(base_dir, 'profileA_1.15TW.csv')
plant_file = os.path.join(base_dir, 'steel_plant_consumption_2023.csv')

datafile_plant = pd.read_csv(datafile_plant, delimiter=delimiter, parse_dates=True, low_memory=False)
datafile_plant['Time'] = pd.to_datetime(datafile_plant['Time'], utc=False)
datafile_plant['P[MW]'] = datafile_plant['P[kW]'] / 1000 # kW -> MW
datafile_plant.set_index('Time', inplace=True)
ydiff = correct_year - datafile_plant.index[0].year
datafile_plant.index += pd.offsets.DateOffset(years=ydiff) 
datafile_plant.reset_index(inplace=True)

datafile_plant['L1-P[MW]'] = datafile_plant['P[MW]'] / 4
datafile_plant['L2-P[MW]'] = datafile_plant['P[MW]'] / 4
datafile_plant['L3-P[MW]'] = datafile_plant['P[MW]'] / 4
datafile_plant['L4-P[MW]'] = datafile_plant['P[MW]'] / 4

datafile_plant[['Time', 'P[MW]',
                'L1-P[MW]', 'L2-P[MW]',
                'L3-P[MW]', 'L4-P[MW]']].to_csv(plant_file, index=False)
plant_file = Path(plant_file)
plant_file.write_text(f"SteelPlant\n{plant_file.read_text()}")

