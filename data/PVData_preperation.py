"""
The Temperetaure-&Solar-Data Files dowloaded from DWD are beeing prepared for usage as input for the pv simulator.
"""
import csv

delimiter = ';'

# specify the path to the datafile to be read and determine row count
datafile_path_temp = '../../data/DWD_AirTemperature_BremenAirport_zehn_min_tu_20200101_20231231_00691.txt'
datafile_path_solar = '../../data/DWD_SolarData_BremenAirport_zehn_min_sd_20200101_20231231_00691.txt'
in_file_temp = open(datafile_path_temp)
row_count = sum(1 for eor in in_file_temp)
print(row_count)

# open the files for reading
datafile_temp = open(datafile_path_temp)
header_temp = next(datafile_temp).strip().split(delimiter)
print(header_temp)
datafile_solar = open(datafile_path_solar)
header_solar = next(datafile_solar).strip().split(delimiter)
print(header_solar)


# specify and open the datafile to be written
newfile_path = '../../data/DWD_solar_data_Bremen_2020_2023.csv'
title = ['SolarData']
header = ['Date','t_air_deg_celsius','bh_w_per_m2','dh_w_per_m2']

with open(newfile_path, 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(title)
    filewriter.writerow(header)

    # loop through rows of existing datafile to add date and temp+solardata to new file
    days = 365*4  # how many days should be extracted?
    row_count = 1 + 144 * days
    for xi in range(1, row_count):
        nextRow_Temp = next(datafile_temp).strip().split(delimiter)
        nextRow_Solar = next(datafile_solar).strip().split(delimiter)
        oldDate = str(nextRow_Temp[1])
        year = oldDate[0:4]
        month = oldDate[4:6]
        day = oldDate[6:8]
        hour = oldDate[8:10]
        minute = oldDate[10:12]
        date = year+'-'+month+'-'+day+' '+hour+':'+minute+':00'

        TT_10 = float(nextRow_Temp[4]) # air temperature in two meters height of the previous 10 minutes
        DS_10 = float(nextRow_Solar[3]) # sum of diffuse solar radiation of the previous 10 minutes
        GS_10 = float(nextRow_Solar[4]) # sum of global solar radiation of the previous 10 minutes

        t_air = TT_10 # air temperature
        bh_w = GS_10 - DS_10
        dh_w = DS_10



        newRow = [date, t_air, bh_w, dh_w]  # combine date, air temperature and solar data to a new row
        filewriter.writerow(newRow)  # & add thew new row

# make a new variable - c - for Python's CSV reader object -
#c = csv.reader(csvfile)

# read whatever you want from the reader object
# print it or use it any way you like
#for row in c:
#    print( row[1] + ", " + row[5])

# save and close the file
datafile_temp.close()
datafile_solar.close()
