import os

data_path = os.getcwd()

# download load profiles and weather data
download_smartnord(data_path, data_path,True, False)
download_weather(data_path, data_path,True, False)
