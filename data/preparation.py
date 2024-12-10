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


delimiter = ';'
datafile_path_temp = '10minutenwerte_TU_00691_20200101_20231231_hist.zip'
datafile_path_solar = '10minutenwerte_SOLAR_00691_20200101_20231231_hist.zip'
datafile_path_wind = '10minutenwerte_wind_00691_20200101_20231231_hist.zip'
weather_file = 'DWD_weather_data_Bremen_2020_2023.csv'

# open the files for reading
datafile_temp = zopen(datafile_path_temp)
datafile_temp = pd.read_csv(datafile_temp, delimiter=delimiter, dtype=str)
datafile_solar = zopen(datafile_path_solar)
datafile_solar = pd.read_csv(datafile_solar, delimiter=delimiter, dtype=str)
datafile_wind = zopen(datafile_path_wind)
datafile_wind = pd.read_csv(datafile_wind, delimiter=delimiter, dtype=str)

df = pd.merge(datafile_temp, datafile_solar, on='MESS_DATUM', how='left')
df = pd.merge(df, datafile_wind, on='MESS_DATUM', how='left')
df['Date'] = df['MESS_DATUM'].apply(lambda x: f"{x[0:4]}-{x[4:6]}-{x[6:8]} {x[8:10]}:{x[10:12]}:00")
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
df[['Date', 't_air_deg_celsius', 'bh_w_per_m2', 'dh_w_per_m2', 'wind_speed']].to_csv(weather_file, index=False)
weather_file = Path(weather_file)
weather_file.write_text(f"WeatherData\n{weather_file.read_text()}")
