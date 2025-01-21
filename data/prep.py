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
datafile_weather = os.path.join(base_dir, 'weather_data_bremen_2020_2023.csv.zip')
with zipfile.ZipFile(datafile_weather, "r") as zip_ref:
    zip_ref.extractall(base_dir)
datafile_weather = os.path.join(base_dir, datafile_weather[:-4])
print(datafile_weather)


## STEEL PLANT DATA PREPARATION
datafile_plant = os.path.join(base_dir, 'steel_plant_consumption_a_1.15TW.csv.zip')
with zipfile.ZipFile(datafile_plant, "r") as zip_ref:
    zip_ref.extractall(base_dir)
datafile_plant = os.path.join(base_dir, datafile_plant[:-4])

## TODAY
correct_year = 2023
split_lines = 4
scale_to = 1.15 # TWh/a
steel_plant_file = os.path.join(base_dir, f'steel_plant_consumption_{correct_year}.csv')
plant_data = pd.read_csv(datafile_plant, parse_dates=True, low_memory=False, skiprows=1)
plant_data['Time'] = pd.to_datetime(plant_data['Time'], utc=False)
plant_data.set_index('Time', inplace=True)
ydiff = correct_year - plant_data.index[0].year
plant_data.index += pd.offsets.DateOffset(years=ydiff) 
plant_data.reset_index(inplace=True)

target_capacity = scale_to * 10 ** 6 # TW -> MW
total_capacity = plant_data['P[MW]'].sum()
plant_data['P[MW]'] = plant_data['P[MW]'] * target_capacity / total_capacity
total_capacity = plant_data['P[MW]'].sum() / 10 ** 6

for i in range(1, split_lines + 1):
    plant_data[f'L{i}-P[MW]'] = plant_data['P[MW]'] / split_lines
plant_data.to_csv(steel_plant_file, index=False)
plant_file = Path(steel_plant_file)
plant_file.write_text(f"SteelPlant\n{plant_file.read_text()}")
print(steel_plant_file, "total_demand:", total_capacity, "TWh/a")

## FUTURE
correct_year = 2030
split_lines = 4
scale_to = 3.12 # TWh/a
steel_plant_file = os.path.join(base_dir, f'steel_plant_consumption_{correct_year}.csv')
plant_data = pd.read_csv(datafile_plant, parse_dates=True, low_memory=False, skiprows=1)
plant_data['Time'] = pd.to_datetime(plant_data['Time'], utc=False)
plant_data.set_index('Time', inplace=True)
ydiff = correct_year - plant_data.index[0].year
plant_data.index += pd.offsets.DateOffset(years=ydiff) 
plant_data.reset_index(inplace=True)

target_capacity = scale_to * 10 ** 6 # TW -> MW
total_capacity = plant_data['P[MW]'].sum()
plant_data['P[MW]'] = plant_data['P[MW]'] * target_capacity / total_capacity
total_capacity = plant_data['P[MW]'].sum() / 10 ** 6

for i in range(1, split_lines + 1):
    plant_data[f'L{i}-P[MW]'] = plant_data['P[MW]'] / split_lines
plant_data.to_csv(steel_plant_file, index=False)
plant_file = Path(steel_plant_file)
plant_file.write_text(f"SteelPlant\n{plant_file.read_text()}")
print(steel_plant_file, "total_demand:", total_capacity, "TWh/a")


## POWER PLANT DATA PREPARATION
datafile_plant = os.path.join(base_dir, 'steel_plant_consumption_a_1.15TW.csv.zip')
with zipfile.ZipFile(datafile_plant, "r") as zip_ref:
    zip_ref.extractall(base_dir)
datafile_plant = os.path.join(base_dir, datafile_plant[:-4])

## TODAY
correct_year = 2023
split_lines = 2
scale_to = 1.15 # TWh/a
limit_to = 0.95 # %
steel_plant_file = os.path.join(base_dir, f'power_plant_generation_{correct_year}.csv')
plant_data = pd.read_csv(datafile_plant, parse_dates=True, low_memory=False, skiprows=1)
plant_data['Time'] = pd.to_datetime(plant_data['Time'], utc=False)
plant_data.set_index('Time', inplace=True)
ydiff = correct_year - plant_data.index[0].year
plant_data.index += pd.offsets.DateOffset(years=ydiff) 
plant_data.reset_index(inplace=True)

target_capacity = scale_to * 10 ** 6 # TW -> MW
total_capacity = plant_data['P[MW]'].sum()
plant_data['P[MW]'] = plant_data['P[MW]'] * target_capacity / total_capacity
plant_data['P[MW]'] = plant_data['P[MW]'] * limit_to
total_capacity = plant_data['P[MW]'].sum() / 10 ** 6

for i in range(1, split_lines + 1):
    plant_data[f'G{i}-P[MW]'] = plant_data['P[MW]'] / split_lines
plant_data.to_csv(steel_plant_file, index=False)
plant_file = Path(steel_plant_file)
plant_file.write_text(f"PowerPlant\n{plant_file.read_text()}")
print(steel_plant_file, "total_capacity:", total_capacity, "TWh/a")

## FUTURE
correct_year = 2030
split_lines = 2
scale_to = 3.12 # TWh/a
limit_to = 0.9 # %
steel_plant_file = os.path.join(base_dir, f'power_plant_generation_{correct_year}.csv')
plant_data = pd.read_csv(datafile_plant, parse_dates=True, low_memory=False, skiprows=1)
plant_data['Time'] = pd.to_datetime(plant_data['Time'], utc=False)
plant_data.set_index('Time', inplace=True)
ydiff = correct_year - plant_data.index[0].year
plant_data.index += pd.offsets.DateOffset(years=ydiff) 
plant_data.reset_index(inplace=True)

target_capacity = scale_to * 10 ** 6 # TW -> MW
total_capacity = plant_data['P[MW]'].sum()
plant_data['P[MW]'] = plant_data['P[MW]'] * target_capacity / total_capacity
plant_data['P[MW]'] = plant_data['P[MW]'] * limit_to
total_capacity = plant_data['P[MW]'].sum() / 10 ** 6

for i in range(1, split_lines + 1):
    plant_data[f'G{i}-P[MW]'] = plant_data['P[MW]'] / split_lines
plant_data.to_csv(steel_plant_file, index=False)
plant_file = Path(steel_plant_file)
plant_file.write_text(f"PowerPlant\n{plant_file.read_text()}")
print(steel_plant_file, "total_capacity:", total_capacity, "TWh/a")


## HYDROGEN DEMAND DATA PREPARATION
datafile_plant = os.path.join(base_dir, 'steel_plant_consumption_a_1.15TW.csv.zip')
with zipfile.ZipFile(datafile_plant, "r") as zip_ref:
    zip_ref.extractall(base_dir)
datafile_plant = os.path.join(base_dir, datafile_plant[:-4])

## FUTURE
correct_year = 2030
scale_to = 0.08 # MtH2/a
steel_plant_file = os.path.join(base_dir, f'hydrogen_demand_{correct_year}.csv')
plant_data = pd.read_csv(datafile_plant, parse_dates=True, low_memory=False, skiprows=1)
plant_data['Time'] = pd.to_datetime(plant_data['Time'], utc=False)
plant_data.set_index('Time', inplace=True)
ydiff = correct_year - plant_data.index[0].year
plant_data.index += pd.offsets.DateOffset(years=ydiff) 
plant_data.reset_index(inplace=True)

target_capacity = scale_to * 10 ** 6 # Mt -> t
total_capacity = plant_data['P[MW]'].sum()
plant_data['HD[tH2]'] = plant_data['P[MW]'] * target_capacity / total_capacity
total_capacity = plant_data['HD[tH2]'].sum() / 10 ** 6
plant_data[['Time', 'HD[tH2]']].to_csv(steel_plant_file, index=False)
plant_file = Path(steel_plant_file)
plant_file.write_text(f"Hydrogen\n{plant_file.read_text()}")
print(steel_plant_file, "total_demand:", total_capacity, "MtH2/a")


## ELECTROLYZER DATA PREPARATION
datafile_plant = os.path.join(base_dir, 'steel_plant_consumption_a_1.15TW.csv.zip')
with zipfile.ZipFile(datafile_plant, "r") as zip_ref:
    zip_ref.extractall(base_dir)
datafile_plant = os.path.join(base_dir, datafile_plant[:-4])

## FUTURE
correct_year = 2030
scale_to = 2.38 # TWh/a
steel_plant_file = os.path.join(base_dir, f'electrolyzer_consumption_{correct_year}.csv')
plant_data = pd.read_csv(datafile_plant, parse_dates=True, low_memory=False, skiprows=1)
plant_data['Time'] = pd.to_datetime(plant_data['Time'], utc=False)
plant_data.set_index('Time', inplace=True)
ydiff = correct_year - plant_data.index[0].year
plant_data.index += pd.offsets.DateOffset(years=ydiff) 
plant_data.reset_index(inplace=True)

target_capacity = scale_to * 10 ** 6 # TW -> MW
total_capacity = plant_data['P[MW]'].sum()
plant_data['P[MW]'] = plant_data['P[MW]'] * target_capacity / total_capacity
total_capacity = plant_data['P[MW]'].sum() / 10 ** 6
plant_data.to_csv(steel_plant_file, index=False)
plant_file = Path(steel_plant_file)
plant_file.write_text(f"Electrolyzer\n{plant_file.read_text()}")
print(steel_plant_file, "total_demand:", total_capacity, "TWh/a")
